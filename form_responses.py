import json
import time

def form_status_response(index_server_state):
    data_dict = {}
    data_dict['data'] = {}
    data_dict['data']['service_state'] = index_server_state
    data_dict['data']['service_time'] = int(time.time()) 
    data_json = json.dumps(data_dict)
    return(data_json)