import numpy
from requiredfunctions import get_fitness, do_cull, sum_errors, do_cross, do_mutate
import os

filename = open("./records.txt", 'w')
data = open("./data.txt", 'w')

# print("",file=filename)
# Number of the weights we are looking to optimize.
num_weights = 11

sol_per_pop = 20
num_parents_mating = 5

# Defining the population size.
pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
# inp = input("Enter choice:")

#initializing
option = 1
if option == 1:
    new_population = numpy.random.uniform(low=-1e-1, high=1e-1, size=pop_size)
    print(new_population)
else:
    new_population = [[5.00000000e+00,8.00000000e+00,6.21194106e+00,-7.33461650e-04,-8.41762133e-04,8.13236610e-05,-6.01876916e-05,-1.251557e-07,3.48409638e-08,4.16149250e-11,-6.7324e-12],[7.00000000e+00,7.00000000e+00,6.21194106e+00,-5.45919679e-04,-5.65563615e-03,8.13236610e-05,-6.01876916e-05,-1.25158557e-06,3.48409638e-08,4.16150e-11,-6.72018e-12],[7.00000000e+00,7.00000000e+00,6.21194106e+00,4.89238473e-03,-6.61614151e-03,8.13236610e-05,-6.01876916e-05,-1.25158557e-07,3e-08,-4.16149250e-11,-6.73242018e-12],[7.00000000e+00,7.00005432000e+00,4.4106e+00,-9.47763490e-04,-7.15679024e-03,8.13236610e-05,-6.01876916e-05,-1.25158557e-06,3.48409638e-08,4.16149250e-11,3.73242018e-12],[7.00000000e+00,7.00000000e+00,1.63578907e-03,5.50781091e-03,-7.15679024e-03,8.13236610e-05,-6.01876916e-05,-3.258557e-07,3.48409638e-08,5.16149250e-11,-8.73242018e-12]]
    new_population = do_mutate(new_population, 5)
    # new_population = do_mutate(new_population, 9)
    print(new_population)

fitness = get_fitness(new_population)
print(fitness)
fitness = sum_errors(fitness)
new_population = do_cull(new_population, fitness, 5)
print(new_population)

generations = 40
for i in range(generations):
    new_population = do_cross(new_population, 5)
    new_population = do_mutate(new_population, 5)
    print(new_population)
    fitness = get_fitness(new_population)
    print(fitness)
    fitness = sum_errors(fitness)
    if i != generations - 1:
        new_population = do_cull(new_population, fitness, 10)
        print(new_population)
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