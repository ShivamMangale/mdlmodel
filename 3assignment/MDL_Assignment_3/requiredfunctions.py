import json
import requests
import numpy as np
import random
import os

filename = open("./records.txt", 'a')

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

def get_fitness(inp):
    res = []
    co = 0
    for i in inp:
        err = get_errors('GsR9ZBabR9AARthD4PSJIurrbm3N60os6gkv9bK2Hu0of2pPaC', list(i))
        res.append(err)
        if err[0] + err[1] < 3e+7:
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
        newfitness.append((0.45)*fitness[i][0] + (0.5)*fitness[i][1] + (0.05)*(fitness[i][0] - fitness[i][1]))
    # else:
    #     for i in range(len(fitness)):
    #         newfitness.append((0.6)*fitness[i][0] + (0.4)*fitness[i][1])

    return newfitness

def do_cull(population, fitness, req):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = np.empty((req, population.shape[1]))
    for parent_num in range(req):
        min_fitness_idx = np.where(fitness == np.amin(fitness))
        min_fitness_idx = min_fitness_idx[0][0]
        parents[parent_num, :] = population[min_fitness_idx, :]
        fitness[min_fitness_idx] = 9999999999999e+99
    return parents

def do_cross(population, req):
    co = 0
    ltime = 0
    for i in range(int(len(population)/2) + 1):
        for j in range(i+1,min(int(len(population)/2) - 8 + i,int(len(population)/2))):
            if i != j:
                new = np.random.uniform(low=-10.0, high=10.0, size=(1,11))
                for k in range(11):
                    new[0][k] = population[i][k] + population[j][k]
                    new[0][k] = new[0][k]/2
                    # if k < 3:
                    #     new[0][k] += random.random()*random.randrange(-10,10)/100
                    # elif k < 7:
                    #     new[0][k] += random.random()*random.randrange(-10,10)/100000
                    # else:
                    #     new[0][k] += random.random()*random.randrange(-10,10)/1000000000
                    if new[0][k] == population[i][k] or random.randrange(0,2,1) == 1:
                        new[0][k] += random.random()*(random.randrange(-10,10) + random.randrange(-10,10))/pow(8,13)
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
                if equalflag == 0 or ltime > 10:
                    print("doing cross no: ",  co+1 ,"for:", file=filename)
                    print(population[i], file=filename)
                    print(population[j], file=filename)
                    population = np.append(population, new, axis=0)
                    co += 1
                    print("new child after crossing: ", file=filename)
                    print(new[0], file=filename)
                    ltime = 0
                    if co >= req:
                        return population
                else:
                    ltime += 1
        
    return population

def do_mutate(population, req):
    for co in range(req):
        new = np.random.uniform(low=-10.0, high=10.0, size=(1,11))
        for l in range(11):
            # new[0][l] = population[0][l]
            new[0][l] = population[co][l]
        k = random.randrange(0,10,1)
        # new[0][k] += random.random()*random.randrange(-10,10)/pow(10,random.randrange(0,4,1))
        # new[0][k + 1] += random.random()*random.randrange(-10,10)/pow(10,random.randrange(0,4,1))
        new[0][k] = (random.random()*(random.randrange(-10,10)))/pow(10,random.randrange(0,8,1))
        new[0][k] = max(new[0][k],-10)
        new[0][k] = min(new[0][k],10)
        k = random.randrange(0,10,1)
        #did assignment for early runs. afterwards changed to updation..... updation fucks up
        new[0][k] = (random.random()*(random.randrange(-10,10)))/pow(10,random.randrange(8,15,1))
        new[0][k] = max(new[0][k],-10)
        new[0][k] = min(new[0][k],10)
        print("new vector due to mutation ", co+1, " : ", file=filename)
        print(new[0], file=filename)
        population = np.append(population, new, axis=0)
    
    return population

def do_specialaddition(population, req, mag):
    for co in range(req):
        new = np.random.uniform(low=-10.0, high=10.0, size=(1,11))
        for l in range(11):
            new[0][l] = population[co][l]
            chpow = 0
            while abs(new[0][l]/pow(10,-chpow)) < 1:
                chpow += 1
            # for m in range(mag,3 + mag):
            lo = random.randrange(-10,10) + random.randrange(-10,10)
            new[0][l] += lo/pow(10,chpow)
            new[0][l] = max(new[0][l],-10)
            new[0][l] = min(new[0][l],10)
        population = np.append(population, new, axis=0)

    return population

def check(population):
    new1 = population[0]
    new2 = population[20]
    if np.array_equal(new1,new2):
        print("useless now")
        return 1
    else:
        return 0