import numpy
from requiredfunctions import get_fitness, do_cull, sum_errors, do_cross
import os

filename = open("./records.txt", 'w')
data = open("./data.txt", 'w')

# print("",file=filename)
# Number of the weights we are looking to optimize.
num_weights = 11

sol_per_pop = 10
num_parents_mating = 5

# Defining the population size.
pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
# inp = input("Enter choice:")

#initializing
option = 1
if option == 1:
    new_population = numpy.random.uniform(low=-1e-5, high=1e-5, size=pop_size)
    print(new_population)
else:
    new_population = [[-1.98241962e-06,8.05444214e-06,-7.53731313e-06,6.37716132e-06,-2.88323247e-06,-8.24682833e-06,-7.28147124e-06,-3.77332796e-06,-2.50008625e-07,-3.80158972e-06,1.10818993e-06],[1.83425520e-06,-6.39361785e-06,8.53014610e-06,-5.40137982e-06,-9.93180934e-06,2.22034544e-06,-7.72019279e-06,3.68581194e-06,4.37238984e-06,-4.89519357e-06,-2.39247245e-06],[-5.85361286e-06,6.47706184e-06,5.11329207e-06,4.20528746e-06,-3.92290373e-07,2.41323935e-07,-6.54037487e-07,9.03935816e-06,-8.50058308e-06,-5.29611862e-06,-2.60893519e-06],[3.23561446e-06,-1.93284786e-06,-3.10860158e-06,5.60939708e-06,4.94724201e-06,-6.37818773e-06,-1.72118844e-06,9.85891201e-06,2.43023117e-06,2.32576866e-07,2.69655230e-06],[-5.35498064e-06,-8.52933644e-06,-3.58004675e-06,-2.00374685e-06,-8.91767426e-06,3.84394320e-07,2.90325616e-06,-2.99013285e-06,5.37011977e-06,-9.95005461e-06,2.98508100e-06]]
    new_population = do_cross(new_population, 5)
    print(new_population)

fitness = get_fitness(new_population)
print(fitness)
fitness = sum_errors(fitness)
new_population = do_cull(new_population, fitness, 5)
print(new_population)

generations = 5
for i in range(generations):
    new_population = do_cross(new_population, 5)
    print(new_population)
    fitness = get_fitness(new_population)
    print(fitness)
    fitness = sum_errors(fitness)
    if i != generations - 1:
        new_population = do_cull(new_population, fitness, 5)
        print(new_population)

print("final")
print(new_population, file=filename)
print(new_population, file=data)
print(fitness, file=filename)