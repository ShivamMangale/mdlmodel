import json
import requests
import numpy as np
import random
import os

filename = open("./secondrecords.txt", 'a')

######### DO NOT CHANGE ANYTHING IN THIS FILE ##################
API_ENDPOINT = 'http://10.4.21.147'
PORT = 3000
MAX_DEG = 11

#### functions that you can call
def get_errors(id, vector):
    """
    returns python array of length 2 
    (train error and validation error)
    """
    for i in vector: assert -10<=abs(i)<=10
    assert len(vector) == MAX_DEG

    return json.loads(send_request(id, vector, 'geterrors'))

def submit(id, vector):
    """
    used to make official submission of your weight vector
    returns string "successfully submitted" if properly submitted.
    """
    for i in vector: assert -10<=abs(i)<=10
    assert len(vector) == MAX_DEG
    return send_request(id, vector, 'submit')

#### utility functions
def urljoin(root, port, path=''):
    root = root + ':' + str(port)
    if path: root = '/'.join([root.rstrip('/'), path.rstrip('/')])
    return root

def send_request(id, vector, path):
    api = urljoin(API_ENDPOINT, PORT, path)
    vector = json.dumps(vector)
    response = requests.post(api, data={'id':id, 'vector':vector}).text
    if "reported" in response:
        print(response)
        exit()

    return response

def get_fitness(inp, sub):
    res = []
    co = 0
    for i in inp:
        err = get_errors('GsR9ZBabR9AARthD4PSJIurrbm3N60os6gkv9bK2Hu0of2pPaC', list(i))
        res.append(err)
        if err[0] + err[1] < 1e7:
            submit_status = submit('GsR9ZBabR9AARthD4PSJIurrbm3N60os6gkv9bK2Hu0of2pPaC', list(i))
            print("submitted")
        co += 1
    # print(err)
    # assert len(err) == 2
    return list(res)

def sum_errors(fitness, round):
    newfitness = []
    # oscillate between the weights given to each to ensure no overfit to either
    # if round%2==1:
    
    for i in range(len(fitness)):
        # newfitness.append((0.4)*fitness[i][0] + (0.6)*fitness[i][1])
        newfitness.append(fitness[i][0] + fitness[i][1] + 0.25*abs(fitness[i][0] - fitness[i][1]))
    # else:
    #     for i in range(len(fitness)):
    #         newfitness.append((0.6)*fitness[i][0] + (0.4)*fitness[i][1])

    return newfitness

def make_probdist(fitness):
    maxfit = np.max(fitness)
    totlen = len(fitness)
    workfitness = fitness.copy()
    weight = []
    sum = 0
    for i in range(totlen):
        weight.append(0)

    for co in range(len(workfitness)):
        i = np.where(workfitness == np.amin(workfitness))
        i = i[0][0]
        if co < 5:
            val = pow(5,5-co)
        else:
            val = 0
        weight[i] = (totlen - co)*(totlen - co)*(totlen - co) + val
        sum += (totlen - co)*(totlen - co)*(totlen - co) + val
        # print(fitness[i], " ", weight[i])
        workfitness[i] = 99999999e+99
    for i in range(len(fitness)):
        weight[i] = weight[i]/sum

    return weight
    
def do_cull(population, fitness, req, weight):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    culled = []
    for i in range(len(population)):
        culled.append(0)
    parents = np.empty((req, population.shape[1]))
    new_fitness = []
    brute = 0
    elit = 1
    maxval = np.max(fitness) + 1e6
    for i in range(elit):
        min_fitness_idx = np.where(fitness == np.amin(fitness))
        min_fitness_idx = min_fitness_idx[0][0]
        new_fitness.append(fitness[min_fitness_idx])
        # print(fitness[min_fitness_idx], "++++921-039")
        culled[min_fitness_idx] = 1
        parents[i, :] = population[min_fitness_idx, :]
        fitness[min_fitness_idx] = maxval
    for parent_num in range(elit,req):
        flag = 0
        itr = 0
        while flag == 0:
            itr += 1
            if itr >= 130 or brute == 1:
                min_fitness_idx = np.where(fitness == np.amin(fitness))
                min_fitness_idx = min_fitness_idx[0][0]
                new_fitness.append(fitness[min_fitness_idx])
                parents[parent_num, :] = population[min_fitness_idx, :]
                culled[min_fitness_idx] = 1
                fitness[min_fitness_idx] = maxval
                flag = 1
                brute = 1
            else:
                min_fitness_idx = int(np.random.choice(len(population),1,p = weight))
                if culled[min_fitness_idx] == 0:
                    # min_fitness_idx = min_fitness_idx[0][0]
                    print("chose ", min_fitness_idx, " with prob= ", weight[min_fitness_idx])
                    parents[parent_num, :] = population[min_fitness_idx, :]
                    new_fitness.append(fitness[min_fitness_idx])
                    fitness[min_fitness_idx] = maxval
                    flag = 1
                    culled[min_fitness_idx] = 1
    # print(len(parents), " ", len(new_fitness))
    return parents, new_fitness

def do_cross(population, req, weight):
    co = 0
    init = len(population)
    track = np.random.uniform(low = 0, high = 0, size=(len(population), len(population)))
    while co < req:
        # print(init, " ", len(weight))
        # print(weight)
        i = int(np.random.choice(init,1,p = weight))
        j = int(np.random.choice(init,1,p = weight))
        while i == j or track[i][j] == 1:
            i = int(np.random.choice(init,1,p = weight))
            j = int(np.random.choice(init,1,p = weight))
        track[i][j] = 1
        track[j][i] = 1
        new = np.random.uniform(low=-10.0, high=10.0, size=(1,11))
        for k in range(11):
            new[0][k] = population[i][k] + population[j][k]
            new[0][k] = new[0][k]/2
            # if new[0][k] == population[i][k] or random.randrange(0,2,1) == 1:
                # add this as a attempt too
                # new[0][k] += random.random()*random.randrange(-10,10)/pow(8,13)
            new[0][k] += (random.random()*random.randrange(-10,10))/pow(10,random.randrange(3,15))
            new[0][k] = max(new[0][k],-10)
            new[0][k] = min(new[0][k],10)
        equalflag = 0
        for d in range(len(population)):
            currflag = 1
            for e in range(11):
                if population[d][e] != new[0][e]:
                    currflag = 0
            if currflag == 1:
                equalflag = 1
                break
        # k = random.randint(0,9)
        # for h in range(k):
        #     new[0][h] = population[i][h]
        # for h in range(k,11):
        #     new[0][h] = population[j][h]
        if equalflag == 0:
            print("doing cross for ", co+1, " : ", file=filename)
            print(population[i], file=filename)
            print(population[j], file=filename)
            print("new child due to cross: ", file=filename)
            print(new[0], file=filename)
            population = np.append(population, new, axis=0)
            co += 1
        else:
            print("ignored because may be duplicate do_cross")    
    return population

def do_mutate(population, req):
    for co in range(req):
        new = np.random.uniform(low=-10.0, high=10.0, size=(1,11))
        par = random.randint(0+co,1+co)
        for l in range(11):
            new[0][l] = population[par][l]
        k = random.randrange(0,10,1)
        new[0][k] = (random.random()*random.randrange(-10,10))/pow(10,random.randrange(0,15,1))
        new[0][k] = max(new[0][k],-10)
        new[0][k] = min(new[0][k],10)
        # k = random.randrange(0,10,1)
        # new[0][k] = (random.random()*random.randrange(-10,10))/pow(10,random.randrange(0,15,1))
        # new[0][k] = max(new[0][k],-10)
        # new[0][k] = min(new[0][k],10)
        print("mutation number :", co," ::", file=filename)
        print(new[0], file=filename)
        population = np.append(population, new, axis=0)
    
    return population

def do_specialaddition(population, req, mag):
    for co in range(req):
        new = np.random.uniform(low=-10.0, high=10.0, size=(1,11))
        par = random.randrange(0+co,10+co)
        for l in range(11):
            new[0][l] = population[par][l]
            chpow = 0
            while abs(new[0][l]/pow(10,-chpow)) < 1:
                chpow += 1
            for m in range(mag,3 + mag):
                lo = random.randrange(-10,10) + random.randrange(-10,10)
                new[0][l] += lo/pow(10,chpow+m)
                new[0][l] = max(new[0][l],-10)
                new[0][l] = min(new[0][l],10)
        population = np.append(population, new, axis=0)

    return population

def check(population):
    new1 = population[0]
    new2 = population[25]
    if np.array_equal(new1,new2):
        print("useless now")
        return 1
    else:
        return 0


# for i in range(2):
    #     for j in range(i+1,3):
    #         print("doing cross for",i, " ",j)
    #         new = np.random.uniform(low=-10.0, high=10.0, size=(1,11))
    #         # k = random.randint(0,9)
    #         # for h in range(k):
    #         #     new[0][h] = population[i][h]
    #         # for h in range(k,11):
    #         #     new[0][h] = population[j][h]
    #         for k in range(11):
    #             new[0][k] = population[i][k] + population[j][k]
    #             new[0][k] = new[0][k]/2
    #             # if new[0][k] == population[i][k] or random.randrange(0,2,1) == 1:
    #                 # add this as a attempt too
    #                 # new[0][k] += random.random()*random.randrange(-10,10)/pow(8,13)
    #             new[0][k] += (random.random()*random.randrange(-10,10))/pow(10,random.randrange(6,15))
    #             new[0][k] = max(new[0][k],-10)
    #             new[0][k] = min(new[0][k],10)
    #         equalflag = 0
    #         for d in range(len(population)):
    #             currflag = 1
    #             for e in range(11):
    #                 if population[d][e] != new[0][e]:
    #                     currflag = 0
    #             if currflag == 0:
    #                 equalflag = 1
    #                 break
    #         if equalflag == 0:
    #             population = np.append(population, new, axis=0)
    #             co += 1
    #             track[i][j] = 1
    #             track[j][i] = 1
    #             if co >= req:
    #                 return population
    #         else:
    #             print("ignored because may be duplicate")
    