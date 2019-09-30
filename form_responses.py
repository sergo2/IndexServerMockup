import json
import time

def form_status_response(index_server_state):
    data_dict = {}
    data_dict['data'] = {}
    data_dict['data']['service_state'] = index_server_state
    data_dict['data']['service_time'] = int(time.time()) 
    data_json = json.dumps(data_dict)
    return(data_json)

def form_version_response(save_index_error, error_code, msg):
    data_dict = {}
    data_dict['data'] = {}
    if save_index_error:
        err_dict = {'category': -1, 'code': error_code, 'message': msg}
        data_dict['error_list'] = [err_dict]
    data_json = json.dumps(data_dict)
    return(data_json)
