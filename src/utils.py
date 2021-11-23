import requests
import json

def flatten_data(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def get_token(host, username, password):
    url = "{}/SASLogon/oauth/token?grant_type=password&username={}&password={}".format(host, username, password)

    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic c2FzLmVjOg=='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    step1_json = json.loads(response.text)

    return step1_json["access_token"]

def delete_session(host, token, session_id):

    url = "{}/casManagement/servers/cas-shared-default/sessions/{}".format(host, session_id)

    payload=""
    headers = {
    'Accept': '*/*',
    'Authorization': 'Bearer {}'.format(token)
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    return(response)
