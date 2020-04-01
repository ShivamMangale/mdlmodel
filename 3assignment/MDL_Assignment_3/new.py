import numpy
from secondrequiredfunctions import get_fitness, do_cull, sum_errors, do_cross, do_mutate, do_specialaddition, check, make_probdist
import os

filename = open("./secondrecords.txt", 'a')
data = open("./data.txt", 'a')

# print("",file=filename)
# Number of the weights we are looking to optimize.
num_weights = 11

sol_per_pop = 30
num_parents_mating = 5

# Defining the population size.
pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
# inp = input("Enter choice:")
do_size = (sol_per_pop-27,num_weights)
#initializing
option = 1
if option == 1:
    new_population = numpy.random.uniform(low=-1e-3, high=1e-3, size=do_size)
    for d in range(3):
        another9 = numpy.random.uniform(low=-1e-6, high=1e-6, size=(1,11))
        another1 = numpy.random.uniform(low=-1e-8, high=1e-8, size=(1,11))
        another2 = numpy.random.uniform(low=-1e-9, high=1e-9, size=(1,11))
        another3 = numpy.random.uniform(low=-1e-10, high=1e-10, size=(1,11))
        another4 = numpy.random.uniform(low=-1e-11, high=1e-11, size=(1,11))
        another5 = numpy.random.uniform(low=-1e-12, high=1e-12, size=(1,11))
        another6 = numpy.random.uniform(low=-1e-13, high=1e-13, size=(1,11))
        another7 = numpy.random.uniform(low=-1e-14, high=1e-14, size=(1,11))
        another8 = numpy.random.uniform(low=-1e-15, high=1e-15, size=(1,11))
        new_population = numpy.append(new_population, another1, axis=0)
        new_population = numpy.append(new_population, another2, axis=0)
        new_population = numpy.append(new_population, another3, axis=0)
        new_population = numpy.append(new_population, another4, axis=0)
        new_population = numpy.append(new_population, another5, axis=0)
        new_population = numpy.append(new_population, another6, axis=0)
        new_population = numpy.append(new_population, another7, axis=0)
        new_population = numpy.append(new_population, another8, axis=0)
        new_population = numpy.append(new_population, another9, axis=0)
    # another8 = [[1.27178083e-007,-5.79570589e-014,-2.71823500e-004,1.34836792e-006,-2.80069303e-007,-7.08940158e-014,-3.76906638e-013,5.48366984e-013,4.94065646e-323,5.56197895e-012,1.44773457e-015]]
    # new_population = numpy.append(new_population, another8, axis=0)
    # another9 = [[0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]]
    # new_population = numpy.append(new_population, another9, axis=0)
    # another10 = [[3.82715721e-02,8.16635283e-02,-1.02476487e-02,-7.43376720e-06,2.51469486e-04,3.09792192e-06,-1.96704912e-09,2.12002003e-10,-5.51790284e-13,4.56070873e-12,-2.15517574e-14]]
    # new_population = numpy.append(new_population, another10, axis=0)
    # another11 = [[8.16617466e-15,4.31953160e-15,-2.47616056e-16,5.83942304e-02,-5.05318356e-10,3.97767799e-14,-9.20517174e-15,7.23898252e-11,-1.77199749e-11,-0.20947273e-12,0.00013298e-14]]
    # new_population = numpy.append(new_population, another11, axis=0)
    print("Initial population", file = filename)
    print(new_population, file = filename)
else:
    new_population = [[8.16617466e-15,4.31953160e-15,-2.47616056e-16,5.83942304e-02,-5.05318356e-10,3.97767799e-14,-9.20517174e-15,7.23898252e-11,-1.77199749e-11,-0.20947273e-12,0.00013298e-14]]
    # [[5.00000000e+00,8.00000000e+00,6.21194106e+00,-7.33461650e-04,-8.41762133e-04,8.13236610e-05,-6.01876916e-05,-1.251557e-07,3.48409638e-08,4.16149250e-11,-6.7324e-12],[7.00000000e+00,7.00000000e+00,6.21194106e+00,-5.45919679e-04,-5.65563615e-03,8.13236610e-05,-6.01876916e-05,-1.25158557e-06,3.48409638e-08,4.16150e-11,-6.72018e-12],[7.00000000e+00,7.00000000e+00,6.21194106e+00,4.89238473e-03,-6.61614151e-03,8.13236610e-05,-6.01876916e-05,-1.25158557e-07,3e-08,-4.16149250e-11,-6.73242018e-12],[7.00000000e+00,7.00005432000e+00,4.4106e+00,-9.47763490e-04,-7.15679024e-03,8.13236610e-05,-6.01876916e-05,-1.25158557e-06,3.48409638e-08,4.16149250e-11,3.73242018e-12],[7.00000000e+00,7.00000000e+00,1.63578907e-03,5.50781091e-03,-7.15679024e-03,8.13236610e-05,-6.01876916e-05,-3.258557e-07,3.48409638e-08,5.16149250e-11,-8.73242018e-12]]
    new_population = do_mutate(new_population, 24)
    # new_population = do_mutate(new_population, 9)
    print(new_population)

fitness = get_fitness(new_population, 0)
print(fitness, file = filename)
fitness = sum_errors(fitness, 0)
probdist = make_probdist(fitness)
new_population, fitness = do_cull(new_population, fitness, 20, probdist)
print("Initial Population 0:", file = filename)
print(new_population, file = filename)
print("new fitness", file = filename)
print(fitness, file = filename)
probdist = make_probdist(fitness)
print("new probdist outside", file=filename)
print(probdist, file=filename)

# do one run in which you include the good vectors too and tweak them through special addition
# make some coeffs 0
generations = 30
for i in range(generations):
    print(i)
    if i<15:
        new_population = do_cross(new_population, 6, probdist)
        new_population = do_mutate(new_population, 4)
    elif i<23:
        new_population = do_cross(new_population, 6, probdist)
        new_population = do_mutate(new_population, 2)
        new_population = do_specialaddition(new_population, 2, 0)
    else:
        new_population = do_cross(new_population, 3, probdist)
        new_population = do_mutate(new_population, 2)
        new_population = do_specialaddition(new_population, 30-20-3-2, 0)
        # new_population = do_specialaddition(new_population, 50-35-4-3-2, 1)
    # do 6 each and do better "mutation" on top 3 i.e. tweak in their order only(try repeated division till you find a integer on division with 10)
    # if check(new_population) == 1:
    #     break
    print("Final population for ", i+1, ": ", file=filename)
    print(new_population, file=filename)
    fitness = get_fitness(new_population, 1)
    if i != generations - 1:
        fitness = sum_errors(fitness, i)
        probdist = make_probdist(fitness)
        print(i," -0-813")
        print(probdist)
        new_population, fitness = do_cull(new_population, fitness, 20, probdist)
        probdist = make_probdist(fitness)
        # print(probdist)
        print("Initial Population ", i+1," :", file=filename)
        print(new_population, file=filename)
        print("fitness: ", file=filename)
        print(fitness, file=filename)
    else:
        for i in range(len(new_population)):
            print(new_population[i])
            print(fitness[i])

print("final")
print(new_population, file=filename)
print(new_population, file=data)
print(fitness, file=filename)


# not much effect of 0th value as such atleast current cases. and in this case error least at value = 10
# same noticed about 1st value