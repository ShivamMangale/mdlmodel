import json
import requests
import numpy as np

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

if __name__ == "__main__":
    """
    Replace "test" with your secret ID and just run this file 
    to verify that the server is working for your ID.
    """

    # inp = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
    # inp = [1e-08,1e-08,1e-08,1e-08,1e-08,1e-08,1e-08,1e-08,1e-08,1e-08,1e-08]
    # inp = [6.00000000e+00,6.00000000e+00,8.21194106e+00,-5.45919679e-04,-5.65563615e-03,8.13236610e-05,-6.01876916e-05,-1.25158557e-06,3.48409638e-07,4.16150e-10,-6.72018e-12]
    inp = [-8.85798218e-04,4.32600684e-03,-7.34802074e-02,-1.46966750e-05,2.46042087e-04,3.09101360e-06,3.13926184e-12,1.39210766e-12,-7.03562607e-14,4.71849791e-12,-2.09957444e-14]
    err = get_errors('GsR9ZBabR9AARthD4PSJIurrbm3N60os6gkv9bK2Hu0of2pPaC', list(inp))
    print(err)
    print(err[0]+err[1])
    assert len(err) == 2

    submit_status = submit('GsR9ZBabR9AARthD4PSJIurrbm3N60os6gkv9bK2Hu0of2pPaC', list(inp))
    assert "submitted" in submit_status