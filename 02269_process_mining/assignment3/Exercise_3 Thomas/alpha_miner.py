from datetime import datetime
from xml.dom import minidom
from itertools import product


#######################  PETRI NET  ##########################
class Place():
    def __init__(self, name):
        self.name = name
        self.in_edges = set()
        self.out_edges = set()
        self.tokens = 0
        
    def add_mark(self):
        self.tokens += 1
        
    def remove_mark(self):
        self.tokens -= 1
        
        
class Transition():
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.in_edges = set()
        self.out_edges = set()
        self.is_enabled = False
        

class Edge():
    def __init__(self, source, target):
        self.source = source
        self.target = target
        


class PetriNet():
    def __init__(self):
        self.places = {}
        self.transitions = {}
        self.edges = []
        self.name_to_id = {}
        
    def add_place(self, name):
        self.places[name] = Place(name)

    def add_transition(self, name, id):
        self.transitions[id] = Transition(name, id)
        self.name_to_id[name]= id

    def add_edge(self, source, target):
        self.edges.append(Edge(source, target))
        return self
      
    def get_tokens(self, place):
        return self.places[place].tokens

    def is_enabled(self, transition):
        list_sources = []
        
        for edge in self.edges:
            if transition == edge.target: list_sources.append(edge.source)
            
        
        for source in list_sources:
            if self.places[source].tokens <= 0:
                self.transitions[transition].is_enabled = False
                return False
                
        self.transitions[transition].is_enabled = True
        return True
            
        
    def add_marking(self, place):
        self.places[place].add_mark()

    def fire_transition(self, transition):
        if self.transitions[transition].is_enabled == False: return False
        
        # Remove token from source of transition
        for edge in self.edges:    
            if transition == edge.target: 
                self.places[edge.source].remove_mark()
                
        # Add token to target of transition
        for edge in self.edges:    
            if transition == edge.source: 
                self.places[edge.target].add_mark()
                
    def transition_name_to_id(self, transition_name):
        return self.name_to_id[transition_name]


#######################  ALPHA ALGORITHM  ##########################

def read_from_file(filename):
    # read the xml file with the given filename from current directory and return trace as a list

    log_file = minidom.parse(filename)
    cases = {}

    for trace in log_file.getElementsByTagName("trace"):
        case = trace.getElementsByTagName("string")[0].attributes["value"].value
        if case not in cases:
            cases[case] = []

        for event in trace.getElementsByTagName("event"):
            event_data = {
                "org:resource": None,
                "concept:name": None,
                "cost": None,
                "time:timestamp": None,
            }
            # strings:
            for ev in event.getElementsByTagName("string"):
                if ev.attributes["key"].value in event_data:
                    event_data[ev.attributes["key"].value] = ev.attributes[
                        "value"
                    ].value
            # ints
            for ev in event.getElementsByTagName("int"):
                if ev.attributes["key"].value in event_data:
                    event_data[ev.attributes["key"].value] = int(
                        ev.attributes["value"].value
                    )

            date = datetime.strptime(
                event.getElementsByTagName("date")[0].attributes["value"].value,
                "%Y-%m-%dT%H:%M:%S%z",
            )
            date = date.replace(tzinfo=None)
            event_data[
                event.getElementsByTagName("date")[0].attributes["key"].value
            ] = date
            cases[case].append(event_data)
    return cases

# Direct Succession Relation
def dependency_graph(log_dictionary):
    for key, value in log_dictionary.items():
        log_dictionary[key] = [v["concept:name"] for v in value]
    """Creates a dependency graph from a log dictionary"""
    dependency_graph = {}

    for tasks in log_dictionary.values():
        for i in range(len(tasks) - 1):
            if tasks[i] not in dependency_graph:
                dependency_graph[tasks[i]] = {tasks[i + 1]: 1}
            elif tasks[i + 1] not in dependency_graph[tasks[i]]:
                dependency_graph[tasks[i]][tasks[i + 1]] = 1
            else:
                dependency_graph[tasks[i]][tasks[i + 1]] += 1
    return dependency_graph


def get_unique_tasks(log_dictionary):
    """Returns a list of unique tasks"""
    return list(set([x for y in log_dictionary.values() for x in y]))

def choice_relation(direct_succession, unique_tasks):
    """Creates a choice relation dictionary"""
    choice_relation = {}
    
    
    TEMP = []

    # Iterate through all tasks in unique tasks
    for task in unique_tasks:
        if task in direct_succession.keys():
            TEMP = list(direct_succession[task].keys())
            TEMP.append(task)
            for key, value in direct_succession.items():
                if key not in TEMP and task not in value.keys():
                    if task not in choice_relation:
                        choice_relation[task] = [key]
                    else:
                        choice_relation[task].append(key)
        else:
            for key, value in direct_succession.items():
                if task not in value.keys():
                    if task not in choice_relation:
                        choice_relation[task] = [key]
                    else:
                        choice_relation[task].append(key)
    
    return choice_relation

def get_relation(dependency_graph):
    causal = {}
    parallel = {}
    for ai in sorted(dependency_graph.keys()):
        causal[ai] = set()
        for aj in sorted(dependency_graph[ai].keys()):
            try:
                if ai in dependency_graph[aj].keys():
                    parallel[(ai, aj)] = ""
                else: 
                    causal[ai].add(aj)
            except:
                causal[ai].add(aj)
          
        if len(causal[ai]) == 0: del causal[ai]
            
    return causal, parallel


def check_related(a, elem_1, elem_2):
    S = set(product(elem_1, elem_2)).union(set(product(elem_1, elem_2)))
    for pair in S:
        if pair in a.parallel or pair in a.causal: 
            return True
    return False

def identifiy_places(pairs, p):
    for elem in pairs:
        if p != elem and p[0].issubset(elem[0]) and p[1].issubset(elem[1]): return False
    return True


def calculate_pairs(causality_relation, a):
    """Calculates the pairs of the alpha miner"""

    pairs = []

    for key, value in causality_relation.items():
        for item in value:
            pairs.append(({key}, {item}))

    for i in range(0, len(pairs)):
            p1 = pairs[i]
            for j in range(i, len(pairs)):
                p2 = pairs[j]

                if p1 == p2: continue

                is_subset = (p1[0].issubset(p2[0]) or p1[1].issubset(p2[1]))
                if not is_subset: continue
                
                is_related = (check_related(a, p1[0], p2[0]) or check_related(a, p1[1], p2[1]))
                
                if is_related: continue
                
                new_pair = (p1[0] | p2[0], p1[1] | p2[1])
                if new_pair not in pairs: pairs.append(new_pair)
    
    return pairs

class AlphaAlgorithm:
    def __init__(self, dg, cr, pr, ch):
        self.dependency_graph = dg
        self.causal = cr
        self.parallel = pr
        self.choice = ch

def alpha(log_dictionary):
    #print(log_dictionary)

    # Create Dependency Graph
    dependency_graph_v = dependency_graph(log_dictionary)
    #print('Dependency Graph: ', dependency_graph_v)
    
    unique_tasks = get_unique_tasks(log_dictionary)

    causality_relation_v, parallel_relation_v = get_relation(dependency_graph_v)
    #print('Causality Relation: ', causality_relation_v)
    #print('Parallel Relation: ', parallel_relation_v)



    choice_relation_v = choice_relation(dependency_graph_v, unique_tasks)
    #print('Choice Relation: ', choice_relation_v)

    a = AlphaAlgorithm(dependency_graph_v, causality_relation_v, parallel_relation_v, choice_relation_v)

    p = PetriNet()

    pairs = calculate_pairs(causality_relation_v, a)

    final_places = filter(lambda p: identifiy_places(pairs, p), pairs)

    for i in range(len(unique_tasks)): p.add_transition(unique_tasks[i], -i)

    # Get all possible successor events/transitions from dependency graph
    successor_events = [x for y in dependency_graph_v.values() for x in list(y.keys())]

    # Get all possible start/initial events/transitions from dependency graph
    start_events = []

    for key in dependency_graph_v.keys():
        if key not in successor_events:
            start_events.append(key)

    # Get all possible end/final events/transitions from dependency graph
    end_events = []

    for x in list(set(successor_events)):
        if x not in dependency_graph_v.keys():
            end_events.append(x)

    # Add source
    p.add_place('start')
    p.add_marking('start')
    for start_event in start_events:
        p.add_edge('start', p.transition_name_to_id(start_event))

    # Add sink
    p.add_place('end')
    for end_event in end_events:
        p.add_edge(p.transition_name_to_id(end_event), 'end')
    
    for pair in final_places:
        new_id = len(p.places)
        p.add_place(new_id)

        for in_edge in pair[0]: p.add_edge(p.transition_name_to_id(in_edge), new_id)
        for out_edge in pair[1]: p.add_edge(new_id, p.transition_name_to_id(out_edge))
    
    return p


