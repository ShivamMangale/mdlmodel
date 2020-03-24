import numpy
from requiredfunctions import get_fitness, do_cull, sum_errors, do_cross, do_mutate, do_specialaddition
import os

filename = open("./records.txt", 'w')
data = open("./data.txt", 'w')

# print("",file=filename)
# Number of the weights we are looking to optimize.
num_weights = 11

sol_per_pop = 15
num_parents_mating = 5

# Defining the population size.
pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
# inp = input("Enter choice:")
do_size = (sol_per_pop-5,num_weights)
#initializing
option = 1
if option == 1:
    new_population = numpy.random.uniform(low=-1e-2, high=1e-2, size=do_size)
    another1 = numpy.random.uniform(low=-1e-9, high=1e-9, size=(1,11))
    another2 = numpy.random.uniform(low=-1e-10, high=1e-10, size=(1,11))
    another3 = numpy.random.uniform(low=-1e-11, high=1e-11, size=(1,11))
    another4 = numpy.random.uniform(low=-1e-10, high=1e-10, size=(1,11))
    another5 = numpy.random.uniform(low=-1e-8, high=1e-8, size=(1,11))
    new_population = numpy.append(new_population, another1, axis=0)
    new_population = numpy.append(new_population, another2, axis=0)
    new_population = numpy.append(new_population, another3, axis=0)
    new_population = numpy.append(new_population, another4, axis=0)
    new_population = numpy.append(new_population, another5, axis=0)

    print(new_population)
else:
    new_population = [[-5.15189358e-11,6.91448407e-01,-4.84146910e-12,2.53311111e-11,-4.67684865e-13,1.71844629e-05,1.03248181e-13,3.35866851e-10,-1.22743085e-11,6.42702811e-13,7.88403271e-15],[-5.15189358e-11,-1.61312681e-01,7.01864510e-11,2.53311111e-11,-4.67684865e-13,1.71844629e-05,1.03248181e-13,5.62251179e-10,-5.44372889e-13,6.42702811e-13,7.88403271e-15],[-5.15189358e-11,6.91448407e-01,-1.32219427e-04,5.84455729e-04,-4.67684865e-13,1.71844629e-05,-5.13609404e-14,4.79808701e-14,-1.22743085e-11,6.42702811e-13,7.88403271e-15],[-5.15189358e-11,-1.96905265e-02,-3.10088218e-01,2.53311111e-11,-4.67684865e-13,1.71844629e-05,1.03248181e-13,-7.91418577e-16,2.87372360e-14,6.42702811e-13,7.88403271e-15],[-5.15139463e-11,6.05017356e-01,-3.13041139e-08,-2.52139649e-03,-1.80234575e-07,1.71844627e-05,2.99645063e-13,3.02195844e-10,-1.26647327e-11,6.39317259e-13,1.35931943e-14]]
    # [[5.00000000e+00,8.00000000e+00,6.21194106e+00,-7.33461650e-04,-8.41762133e-04,8.13236610e-05,-6.01876916e-05,-1.251557e-07,3.48409638e-08,4.16149250e-11,-6.7324e-12],[7.00000000e+00,7.00000000e+00,6.21194106e+00,-5.45919679e-04,-5.65563615e-03,8.13236610e-05,-6.01876916e-05,-1.25158557e-06,3.48409638e-08,4.16150e-11,-6.72018e-12],[7.00000000e+00,7.00000000e+00,6.21194106e+00,4.89238473e-03,-6.61614151e-03,8.13236610e-05,-6.01876916e-05,-1.25158557e-07,3e-08,-4.16149250e-11,-6.73242018e-12],[7.00000000e+00,7.00005432000e+00,4.4106e+00,-9.47763490e-04,-7.15679024e-03,8.13236610e-05,-6.01876916e-05,-1.25158557e-06,3.48409638e-08,4.16149250e-11,3.73242018e-12],[7.00000000e+00,7.00000000e+00,1.63578907e-03,5.50781091e-03,-7.15679024e-03,8.13236610e-05,-6.01876916e-05,-3.258557e-07,3.48409638e-08,5.16149250e-11,-8.73242018e-12]]
    new_population = do_mutate(new_population, 10)
    # new_population = do_mutate(new_population, 9)
    print(new_population)

fitness = get_fitness(new_population)
print(fitness)
fitness = sum_errors(fitness)
new_population = do_cull(new_population, fitness, 10)
print(new_population)

generations = 2
for i in range(generations):
    if i<-1:
        new_population = do_cross(new_population, 7)
        new_population = do_mutate(new_population, 8)
    else:
        new_population = do_cross(new_population, 1)
        new_population = do_mutate(new_population, 1)
        new_population = do_specialaddition(new_population, 3)
    # do 6 each and do better "mutation" on top 3 i.e. tweak in their order only(try repeated division till you find a integer on division with 10)
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