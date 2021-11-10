n, m = list(input().split())
n = int(n)
m = int(m)

list_l = []

for _ in range(0, m):
    l = list(input().split(" "))
    l = list(map(int, l))
    list_l.append(l)

# special cases: only two positions or one position for food trucks:
# we just add extra 0 columns (positions)
while len(list_l[0]) < 4:
    for i in range(len(list_l)):
        list_l[i].append(0)

# print(list_l)
# truck and value class, defined as C
class C:
    def __init__(self, i, j, value):
        self.i = i  # day
        self.j = j  # position
        self.value = value


# trucks configuration for each day
class Configuration:
    def __init__(self, truck1, truck2, truck3):
        self.truck1 = truck1
        self.truck2 = truck2
        self.truck3 = truck3
        self.value = truck1.value + truck2.value + truck3.value


n2 = len(list_l[0])
list_l1 = list(range(n2))

# Find all triplets in list - takes O(m^3)
l_triplets = []
for i in range(0, n2 - 2):
    for j in range(i + 1, n2 - 1):
        for k in range(j + 1, n2):
            l_triplets.append([i, j, k])
            k += 1
        j += 1
    i += 1

# print(list_l)
CONFIG = [[Configuration(C(0, 0, 0), C(0, 0, 0), C(0, 0, 0))] * len(l_triplets)] * len(
    list_l
)  # initialize based only the first 2 days

# print('\nGENERAL CASE: ALL CONFIGURATION STARTPOINT')
# start point:
i1 = 0
i2 = 0
i3 = 0

c = 0
for combin_j in l_triplets:

    # print('Combination: ', combin_j)
    j1 = combin_j[0]  # pos truck 1
    j2 = combin_j[1]  # pos truck 1
    j3 = combin_j[2]  # pos truck 3

    truck1 = C(i1, j1, list_l[i1][j1])
    truck2 = C(i2, j2, list_l[i2][j2])
    truck3 = C(i3, j3, list_l[i3][j3])

    CONFIG[0][c] = Configuration(truck1, truck2, truck3)
    c += 1


def possible_configurations(configurations_row, pos_list_current):
    l_configs = []
    l_configs_values = []
    set_pos_current = set(pos_list_current)
    # print(set_pos_current)
    for configuration_prev in configurations_row:
        pos_list_prev = [
            configuration_prev.truck1.j,
            configuration_prev.truck2.j,
            configuration_prev.truck3.j,
        ]
        set_pos_prev = set(pos_list_prev)
        if len(set_pos_current.copy().intersection(set_pos_prev.copy())) >= 2:
            # print(set_pos_prev)
            # print(set_pos_current.copy().intersection(set_pos_prev.copy()))
            l_configs.append(configuration_prev)
            l_configs_values.append(configuration_prev.value)
            maxval = max(l_configs_values)
            idx = l_configs_values.index(maxval)

    return maxval, l_configs[idx]


m = len(list_l)
cc = len(l_triplets)
for i in range(1, m):
    # print(i)
    possible_configurations_row = [CONFIG[i - 1][c] for c in range(cc)]
    for c in range(cc):
        j1 = CONFIG[i - 1][c].truck1.j
        j2 = CONFIG[i - 1][c].truck2.j
        j3 = CONFIG[i - 1][c].truck3.j
        maxval, config_optim = possible_configurations(
            possible_configurations_row, [j1, j2, j3]
        )
        # print(maxval)

        truck1 = C(i, j1, list_l[i1][j1])
        truck2 = C(i, j2, list_l[i2][j2])
        truck3 = C(i, j3, list_l[i3][j3])
        CONFIG[i][c] = Configuration(truck1, truck2, truck3)
        CONFIG[i][c].value = list_l[i][j1] + list_l[i][j2] + list_l[i][j3] + maxval

conf_list_vals = []
for conf in CONFIG[m - 1]:
    conf_list_vals.append(conf.value)

print(max(conf_list_vals))
