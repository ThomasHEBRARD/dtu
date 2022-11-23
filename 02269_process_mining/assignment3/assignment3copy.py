import pprint
import datetime

from xml.dom import minidom
from itertools import combinations

###############################################################
#########                   PETRI NET                  ########
###############################################################


class Transition:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Place:
    def __init__(self, id, mark):
        self.id = id
        self.mark = mark

    def do_mark(self):
        self.mark += 1

    def unmark(self):
        self.mark -= 1


class PetriNet:
    def __init__(self):
        self.places = {}
        self.transitions = {}
        self.edges = {}
        self.m, self.c, self.p = 0, 0, 0

    def reset_petri_net(self):
        self.m, self.c, self.p = 0, 0, 0
        for place in self.places.values():
            place.mark = 0

        self.places[1].mark = len(self.edges[-1]["before"])

    def add_place(self, id):
        self.places[id] = Place(id, 0)

    def add_transition(self, name, id):
        self.transitions[id] = Transition(id, name)

    def add_edge(self, source, target):
        if source not in self.edges:
            self.edges[source] = {"before": [], "after": []}
        if target not in self.edges:
            self.edges[target] = {"before": [], "after": []}

        if source < 0:
            self.edges[source]["after"].append(self.places[target])
            self.edges[source]["after"] = list(set(self.edges[source]["after"]))

            self.edges[target]["before"].append(self.transitions[source])
            self.edges[target]["before"] = list(set(self.edges[target]["before"]))
        else:
            self.edges[source]["after"].append(self.transitions[target])
            self.edges[source]["after"] = list(set(self.edges[source]["after"]))

            self.edges[target]["before"].append(self.places[source])
            self.edges[target]["before"] = list(set(self.edges[target]["before"]))

        return self

    def is_enabled(self, transition):
        for place in self.edges[transition]["before"]:
            if place.mark <= 0:
                return False
        return True

    def fire_transition(self, transition):
        if self.is_enabled(transition):
            for place in self.edges[transition]["before"]:
                place.unmark()

            for place in self.edges[transition]["after"]:
                place.do_mark()

    def transition_name_to_id(self, name):
        for transition_obj in self.transitions.values():
            if transition_obj.name == name:
                return transition_obj.id

def dependency_graph(log):
    for key, value in log.items():
        log[key] = [v["concept:name"] for v in value]

    TEMP = {}
    for tasks in log.values():
        for i in range(len(tasks) - 1):
            if tasks[i] not in TEMP:
                TEMP[tasks[i]] = {tasks[i + 1]: 1}
            elif tasks[i + 1] not in TEMP[tasks[i]]:
                TEMP[tasks[i]][tasks[i + 1]] = 1
            else:
                TEMP[tasks[i]][tasks[i + 1]] += 1
    return TEMP


###############################################################
#########                 READ_FROM_FILE               ########
###############################################################


def read_from_file(filename):
    CASES = {}
    file = minidom.parse(f"{filename}")

    for model in file.getElementsByTagName("trace"):
        case = model.getElementsByTagName("string")[0].attributes["value"].value
        if case not in CASES:
            CASES[case] = []

        for event in model.getElementsByTagName("event"):
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

            date = datetime.datetime.strptime(
                event.getElementsByTagName("date")[0].attributes["value"].value,
                "%Y-%m-%dT%H:%M:%S%z",
            )
            date = date.replace(tzinfo=None)
            event_data[
                event.getElementsByTagName("date")[0].attributes["key"].value
            ] = date
            CASES[case].append(event_data)
    return CASES


###############################################################
#########                     ALPHA                    ########
###############################################################


def alpha(cases):
    FIRST_TRANSITION = list(cases.values())[0][0]
    FINAL_TRANSITION = list(cases.values())[-1][-1]

    d_g = dependency_graph(cases)

    ############################ Look for causal and parallels ############################

    causal, parallel = {}, {}

    for k in sorted(d_g.keys()):
        causal[k] = set()
        for vk in sorted(d_g[k].keys()):
            try:
                if k in d_g[vk].keys():
                    parallel[(k, vk)] = ""
                else: 
                    causal[k].add(vk)
            except:
                causal[k].add(vk)
          
        if len(causal[k]) == 0: del causal[k]

    ############################ Look for causal and parallels ############################
    p = PetriNet()

    def get_activity_details(dg):
        starting_tasks = []
        ending_tasks = []
        
        for ai in dg.keys():
            if ai not in starting_tasks: starting_tasks.append(ai)
            
            [ending_tasks.append(x) for x in dg[ai].keys() if x not in ending_tasks] 
                    
        # Set starting activity
        starting = [x for x in starting_tasks if x not in ending_tasks]
        
        # Set ending activity
        ending = [x for x in ending_tasks if x not in starting_tasks]
        
        all_tasks = list(set().union(starting_tasks, ending_tasks))
        
        return starting, ending, all_tasks

    activities, end_activities, start_activities = get_activity_details(d_g)

    def check_related(causal, parallel, elem_1, elem_2):
        from itertools import product
        S = set(product(elem_1, elem_2)).union(set(product(elem_1, elem_2)))
        for pair in S:
            if pair in parallel or pair in causal: 
                return True
        return False


    def identifiy_places(pairs, p):
        for elem in pairs:
            if p != elem and p[0].issubset(elem[0]) and p[1].issubset(elem[1]): return False
        return True

    pairs = []
    for key, element in causal.items():
        for item in element: 
            pairs.append(({key}, {item}))

    for i in range(0, len(pairs)):
            p1 = pairs[i]
            for j in range(i, len(pairs)):
                p2 = pairs[j]
                
                if p1 == p2: continue
                    
                # Check whether items in p1 are present in p2
                is_subset = (p1[0].issubset(p2[0]) or p1[1].issubset(p2[1]))
                if not is_subset: continue
                
                is_related = (check_related(causal, parallel, p1[0], p2[0]) or check_related(causal, parallel, p1[1], p2[1]))
                
                if is_related: continue
                
                new_pair = (p1[0] | p2[0], p1[1] | p2[1])
                if new_pair not in pairs: pairs.append(new_pair)

    FINAL_SETS = [[list(g) for g in f] for f in pairs]
    import pprint
    pprint.pprint(FINAL_SETS)
    # print("new_pair")
    # pprint.pprint(pairs)

    # places_to_add = filter(lambda p: identifiy_places(pairs, p), pairs)

    # # Each activity corresponds to a transition
    # for i in range(len(activities)): p.add_transition(activities[i], -i)
        
    # # Add source
    # p.add_place('start')
    # p.places["start"].do_mark()

    # for s in start_activities: p.add_edge('start', p.transition_name_to_id(s))

    # # Add sink
    # p.add_place('end')
    # for e in end_activities: p.add_edge(p.transition_name_to_id(e), 'end')
    
    # for pair in places_to_add:
    #     new_id = len(p.places)
    #     p.add_place(new_id)
        
    #     for in_edge in pair[0]: p.add_edge(p.transition_name_to_id(in_edge), new_id)
    #     for out_edge in pair[1]: p.add_edge(new_id, p.transition_name_to_id(out_edge))
    
    # return p

    # possible_sets = [[k, list(v.keys())] for k, v in d_g.items()]
    # possible_sets = []

    all_tasks = list(set(d_g.keys()))

    # for i in range(len(possible_sets)):
    #     s = possible_sets[i]
    #     kk, vv = s
    #     kk, vv = [kk] if isinstance(kk, str) else kk, [vv] if isinstance(
    #         vv, str
    #     ) else vv
    #     sets = [
    #         list(com)
    #         for sub in range(1, len(all_tasks))
    #         for com in combinations(kk + vv, sub + 1)
    #     ]

    #     for s in sets:
    #         if s in possible_sets[:i] + possible_sets[i + 1 :]:
    #             to_remove.append(s)

    # FINAL_SETS = []
    # for pos in possible_sets:
    #     if pos not in to_remove:
    #         FINAL_SETS.append(pos)

    # pprint.pprint(FINAL_SETS)

    pn = PetriNet()
    for idx in range(len(all_tasks)):
        pn.add_transition(all_tasks[idx], -idx)

    places_to_add = filter(lambda p: identifiy_places(pairs, p), pairs)
    for pair in places_to_add:
        new_id = len(pn.places)
        pn.add_place(new_id)
        print(pair)
        for in_edge in pair[0]: 
            pn.add_edge(pn.transition_name_to_id(in_edge), new_id)
        for out_edge in pair[1]: 
            pn.add_edge(new_id, pn.transition_name_to_id(out_edge))
    

    # transition_idx = 1
    # place_idx = None
    # already_created_places = {}

    # for idx, s in enumerate(FINAL_SETS, 2):
    #     kk, vv = s
    #     kk, vv = [kk] if isinstance(kk, str) else kk, [vv] if isinstance(
    #         vv, str
    #     ) else vv

    #     vv.sort()

    #     if str(vv) not in already_created_places.keys():
    #         pn.add_place(idx)
    #         already_created_places[str(vv)] = idx

    #     place_idx = already_created_places[str(vv)]
    #     place = pn.places[place_idx].id

    #     transition_before = []
    #     transition_after = []

    #     for k in kk:
    #         if k not in [t.name for t in pn.transitions.values()]:
    #             pn.add_transition(name=k, id=-transition_idx)
    #             transition_before.append(-transition_idx)
    #             transition_idx += 1

    #     for v in vv:
    #         if v not in [t.name for t in pn.transitions.values()]:
    #             pn.add_transition(name=v, id=-transition_idx)
    #             transition_after.append(-transition_idx)
    #             transition_idx += 1

    #     for k in kk:
    #         pn.add_edge(source=pn.transition_name_to_id(k), target=place)

    #     for v in vv:
    #         pn.add_edge(source=place, target=pn.transition_name_to_id(v))

    # Adding first place and giving it a token
    pn.add_place(1)
    pn.add_edge(
        pn.places[1].id, pn.transition_name_to_id(FIRST_TRANSITION["concept:name"])
    )

    pn.places[1].do_mark()

    # Adding end place
    pn.add_place(place_idx + 1)
    pn.add_edge(
        pn.transition_name_to_id(FINAL_TRANSITION["concept:name"]),
        pn.places[place_idx + 1].id,
    )

    return pn


###############################################################
#########                    TESTING                   ########
###############################################################

# mined_model = alpha(read_from_file("extension-log.xes"))
mined_model = alpha(read_from_file("loan-process.xes"))

def check_enabled(pn, a):
    # ts = [
    #     "record issue",
    #     "inspection",
    #     "intervention authorization",
    #     "action not required",
    #     "work mandate",
    #     "no concession",
    #     "work completion",
    #     "issue completion",
    # ]
    ts = [
        "register application",
        "check credit",
        "calculate capacity",
        "check system",
        "accept",
        "reject",
        "send decision e-mail",
    ]
    for t in ts:
        print(pn.is_enabled(pn.transition_name_to_id(t)))
        pass
    print("")


# trace = [
#     "record issue",
#     "inspection",
#     "intervention authorization",
#     "work mandate",
#     "work completion",
#     "issue completion",
# ]
trace = [
    "register application",
    "check credit",
    "check system",
    "calculate capacity",
    "accept",
    "send decision e-mail",
]
for a in trace:
    check_enabled(mined_model, a)
    mined_model.fire_transition(mined_model.transition_name_to_id(a))


