import json
import requests
import numpy as np
import random
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

# if __name__ == "__main__":
#     """
#     Replace "test" with your secret ID and just run this file 
#     to verify that the server is working for your ID.
#     """

#     # inp = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
#     inp = [1e-08,1e-08,1e-08,1e-08,1e-08,1e-08,1e-08,1e-08,1e-08,1e-08,1e-08]

#     err = get_errors('GsR9ZBabR9AARthD4PSJIurrbm3N60os6gkv9bK2Hu0of2pPaC', list(inp))
#     print(err)
#     assert len(err) == 2

#     submit_status = submit('GsR9ZBabR9AARthD4PSJIurrbm3N60os6gkv9bK2Hu0of2pPaC', list(inp))
#     assert "submitted" in submit_status

def get_fitness(inp):
    res = []
    for i in inp:
        err = get_errors('GsR9ZBabR9AARthD4PSJIurrbm3N60os6gkv9bK2Hu0of2pPaC', list(i))
        res.append(err)
        if err[0] + err[1] < 1e+15:
            submit_status = submit('GsR9ZBabR9AARthD4PSJIurrbm3N60os6gkv9bK2Hu0of2pPaC', list(i))
    # print(err)
    # assert len(err) == 2
    return list(res)

# def do_cull(population, fitness, req):
#     newpopulation = []
#     for i in range(req):
#         maxfit = max(fitness)
#         for ind in range(len(population)):
#             if fitness[ind] == maxfit:
#                 newpopulation.append(population.delete(ind))
#                 ignore = fitness.pop(ind)
#                 break
    
#     return newpopulation

def sum_errors(fitness):
    newfitness = []
    for i in range(len(fitness)):
        newfitness.append((0.9)*fitness[i][0] + fitness[i][1])
    
    return newfitness

def do_cull(population, fitness, req):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = np.empty((req, population.shape[1]))
    for parent_num in range(req):
        # print(fitness)
        # print(population)
        min_fitness_idx = np.where(fitness == np.amin(fitness))
        min_fitness_idx = min_fitness_idx[0][0]
        parents[parent_num, :] = population[min_fitness_idx, :]
        fitness[min_fitness_idx] = 9999999999999e+99
    return parents

def do_cross(population, req):
    co = 0
    for i in range(int(len(population)/2) + 1):
        for j in range(i+1,int(len(population)/2) + 1):
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
                    new[0][k] += random.random()*random.randrange(-10,10)/pow(10,13)
                    new[0][k] = max(new[0][k],-10)
                    new[0][k] = min(new[0][k],10)
                population = np.append(population, new, axis=0)
                co += 1
                print("did cross for", i, " ", j)
                if co >= req:
                    return population
    
    return population

def do_mutate(population, req):
    for co in range(req):
        new = np.random.uniform(low=-10.0, high=10.0, size=(1,11))
        for l in range(11):
            # new[0][l] = population[0][l]
            new[0][l] = population[co][l]
        k = random.randrange(0,6,1)
        # new[0][k] += random.random()*random.randrange(-10,10)/pow(10,random.randrange(0,4,1))
        # new[0][k + 1] += random.random()*random.randrange(-10,10)/pow(10,random.randrange(0,4,1))
        new[0][k] = random.random()*random.randrange(-10,10)/pow(10,random.randrange(0,15,1))
        new[0][k + 1] = random.random()*random.randrange(-10,10)/pow(10,random.randrange(0,15,1))
        new[0][k] = max(new[0][k],-10)
        new[0][k] = min(new[0][k],10)
        new[0][k+1] = max(new[0][k+1],-10)
        new[0][k+1] = min(new[0][k+1],10)
        k = random.randrange(6,10,1)
        #did assignment for early runs. afterwards changed to updation..... updation fucks up
        new[0][k] = random.random()*random.randrange(-10,10)/pow(10,random.randrange(10,15,1))
        new[0][k + 1] = random.random()*random.randrange(-10,10)/pow(10,random.randrange(10,15,1))
        new[0][k] = max(new[0][k],-10)
        new[0][k] = min(new[0][k],10)
        new[0][k+1] = max(new[0][k+1],-10)
        new[0][k+1] = min(new[0][k+1],10)
        population = np.append(population, new, axis=0)
    
    return population

def do_specialaddition(population, req):
    for co in range(req):
        new = np.random.uniform(low=-10.0, high=10.0, size=(1,11))
        for l in range(11):
            new[0][l] = population[co][l]
            chpow = 0
            while abs(new[0][l]/pow(10,-chpow)) < 1:
                chpow += 1
            # ensure power same of random generated and actual. wrong right now
            new[0][l] += random.random()*random.randrange(-10,10)/pow(10,-(chpow-1))
            new[0][l] = max(new[0][l],-10)
            new[0][l] = min(new[0][l],10)
            population = np.append(population, new, axis=0)

    return population