import random
import matplotlib.pyplot as plt


# uniform random value between 0 and 1
def random_value():
    return random.uniform(0, 1)

# generate random population
def generate_population():
    population = []
    for i in range(n):
        population.append(random_value())
    return population


def select_train_test_population(populations, m):
    # randomly select m population
    train_population = []
    test_population = []
    for population in populations:
        test_population.append(population)
    
    train_population = random.sample(populations, m)
    for i in range(m):
        test_population.remove(train_population[i])
    return train_population, test_population

def find_top_s_population(populations, s):
    # sort population
    sorted_population = []
    for population in populations:
        sorted_population.append(population)
    sorted_population.sort(reverse=True)

    # select top s population
    top_s_population = sorted_population[:s]
    return top_s_population

def find_best_train_candidate(train_populations):
    best_score = -1.0
    for train_population in train_populations:
        if train_population > best_score:
            best_score = train_population
    return best_score

def is_present_in_top_s_population(test_population, top_s_population):
    if test_population in top_s_population:
        return True
    else:
        return False

if __name__ == "__main__":
    n = int(input("Enter the number of populations size: "))
    iterations = int(input("Enter the number of iterations: "))

    s = [1, 3, 5, 10]

    populations = generate_population()
    
    for ss in s:
        m_list = []
        success_list = []
        for m in range(0, n):
            
            total_succes = 0
            for it in range(iterations):
                train_populations, test_populations = select_train_test_population(populations, m)
                # print("train population: ", train_populations)
                # print("test population: ", test_populations)
            
                best_score = find_best_train_candidate(train_populations)
                # print("best score: ", best_score)

                
                top_s_population = find_top_s_population(populations, ss)
                # print("top s population: ", top_s_population)
                for test_population in test_populations:
                    if test_population > best_score:
                        if(is_present_in_top_s_population(test_population, top_s_population)):
                            # print("current_val: ", test_population)
                            total_succes += 1
                        break
                    # the last item
                    if test_population == test_populations[-1]:
                        if(is_present_in_top_s_population(test_population, top_s_population)):
                            total_succes += 1
                    
            # print("total success: ", total_succes)
            success_rate = (total_succes / iterations)
            # print("success rate: ", success_rate)
            m_list.append(m)
            success_list.append(success_rate)
        
        # plot the graph
        plt.plot(m_list, success_list, label="s = {}".format(ss))
        plt.xlabel("m")
        plt.ylabel("Success Rate")
        plt.legend()
        plt.show()


            

               