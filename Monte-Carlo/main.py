import random

n = int(input("Enter the number of generation:"))
count = {
    "0": 0,
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
}

    
P0 = 0.4825
P1 = 0.2126*pow(0.5893, 0)
P2 = 0.2126*pow(0.5893, 1)
P3 = 0.2126*pow(0.5893, 2)

# print(P0, P1, P2, P3)
sum = P0 + P1 + P2 + P3
extra = max(0, 1-sum)
P0 += extra

# print(P0, P1, P2, P3)
P1 = P0 + P1
P2 = P1 + P2
P3 = P2 + P3

# print(P0, P1, P2, P3)
def calculate_neutron():
    prob = random.uniform(0, 1)
    global total_neutron
    if prob <= P0:
        total_neutron += 0
    elif prob <= P1:
        total_neutron += 1
    elif prob <= P2:
        total_neutron += 2
    elif prob <= P3:
        total_neutron += 3
    return


def tree(i):
    if i == n-1:
        calculate_neutron()
        return
    
    prob = random.uniform(0, 1)
    if prob <= P0:
        pass 
    elif prob <= P1:
        tree(i + 1)
    elif prob <= P2:
        tree(i + 1)
        tree(i + 1)
    elif prob <= P3:
        tree(i + 1)
        tree(i + 1)
        tree(i + 1)
    return



iterations = 10000
for i in range(iterations):
    global total_neutron
    total_neutron = 0
    tree(0)
    if total_neutron == 0:
        count["0"] += 1
    elif total_neutron == 1:
        count["1"] += 1
    elif total_neutron == 2:
        count["2"] += 1
    elif total_neutron == 3:
        count["3"] += 1
    elif total_neutron == 4:
        count["4"] += 1
    


print("Probability of 0 neutron: ", count["0"]/iterations)
print("Probability of 1 neutron: ", count["1"]/iterations)
print("Probability of 2 neutron: ", count["2"]/iterations)
print("Probability of 3 neutron: ", count["3"]/iterations)
print("Probability of 4 neutron: ", count["4"]/iterations)