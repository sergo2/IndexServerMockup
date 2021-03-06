# -*- coding: utf-8 -*-
import json
import time
import os
import codecs
import random
from config import * 

def form_daily_values(get_param_dict):
    if get_index_error:
        return form_composition_response(True, get_index_error_code, get_index_error_msg)
    else:
        index_id = get_param_dict['indexid'][0]
        trade_date = int(get_param_dict['tradedate'][0])
        # find an index json file with the largest version
        file_list = []
        for file in os.listdir(json_dir):
            if file.startswith(index_id + ".") and file.endswith(".json"):
                file_list.append(file)
        if len(file_list) > 0:
            file_list.sort(reverse=True)
            index_json_file = os.path.join(json_dir,file_list[0])
            logging.info("Found json file for daily values: " + index_json_file)
            f = codecs.open(index_json_file, "r", "utf-8")    
            json_decoded = json.load(f)
            f.close
            # Fill in the result
            data_dict = {}
            data_dict['data'] = {}            
            data_dict['data'] = {} 
            data_dict['data']['index_daily_values'] = {}
            data_dict['data']['index_daily_values']['tradedate'] = trade_date            
            data_dict['data']['index_daily_values']['open_val'] = round(random.uniform(100,300),2)         
            data_dict['data']['index_daily_values']['close_val'] = round(random.uniform(100,300),2)
            data_dict['data']['index_daily_values']['min_val'] = round(random.uniform(80,100),2)
            data_dict['data']['index_daily_values']['max_val'] = round(random.uniform(300,400),2)
            data_dict['data']['index_daily_values']['volume_money_source'] = round(random.uniform(10000000,90000000),2)
            data_dict['data']['index_daily_values']['volume_money'] = round(random.uniform(10000000,90000000),2)
            data_dict['data']['index_daily_values']['volume_amount'] = int(random.uniform(10000000000,9000000000))
            data_dict['data']['index_daily_values']['trade_count'] = int(random.uniform(100000,900000))
            data_dict['data']['index_daily_values']['return_open'] = round(random.uniform(-2,5),2)
            data_dict['data']['index_daily_values']['min52_val'] = round(random.uniform(50,80),2)
            data_dict['data']['index_daily_values']['max52_val'] = round(random.uniform(400,500),2)
            data_dict['data']['index_daily_values']['rate'] = round(random.uniform(70,80),2)            
            data_dict['data']['index_daily_values']['min52_date'] = trade_date - int(random.uniform(1,300))*60*60*24 
            data_dict['data']['index_daily_values']['max52_date'] = trade_date - int(random.uniform(1,300))*60*60*24         
            data_dict['data']['index_daily_values']['volatility'] = round(random.uniform(0,1),2) 
            data_dict['data']['index_daily_values']['yield_index'] = round(random.uniform(3,10),2) 
            data_dict['data']['index_daily_values']['duration_daily'] = int(random.uniform(50,1500)) 
            # Extract instrument codes from the composition dict
            calc_base_list = json_decoded['data']['composition']['calc_base']
            for item in calc_base_list:
                instrument = item['mnemo']
                item.clear()
                item['mnemo'] = instrument
                item['tradedate'] = trade_date
                item['close_price'] = round(random.uniform(100,300),2)
                item['volume_money'] = round(random.uniform(100000,300000),2)
                item['volume_money_source'] = round(random.uniform(100000,300000),2)
                item['volume_amount'] = int(random.uniform(100000,300000))
                item['trade_count'] = int(random.uniform(1000,30000))
                item['cap_val'] = round(random.uniform(1000000,3000000),2)
                item['cap_source'] = round(random.uniform(10000000,300000000),2)
                item['volatility'] = round(random.uniform(0.1,0.9),2)
                item['factor_a'] = round(random.uniform(-1,1),2)
                item['factor_b'] = round(random.uniform(-1,1),2)
                item['sec_influence'] = round(random.uniform(-1,1),2)
                item['determinat'] = round(random.uniform(0,1),2)
                item['ytm'] = round(random.uniform(3,10),2)
                item['duration_daily'] = int(random.uniform(50,1500))
            data_dict['data']['index_daily_values']['calc_base_daily_values_list'] = calc_base_list
            
            data_dict['error_list'] = []
            
            json_str = json.dumps(data_dict)
            return(json_str)
        else:
            msg = "No json files with indexid=" + index_id
            return form_composition_response(True, -102, msg)

def form_index_version(get_param_dict):
    if get_index_error:
        return form_composition_response(True, get_index_error_code, get_index_error_msg)
    else:
        index_id = get_param_dict['indexid'][0]
        index_version = get_param_dict['version'][0]
        # find an index json file with the largest version
        file_list = []
        for file in os.listdir(json_dir):
            if file.startswith(index_id + "." + index_version) and file.endswith(".json"):
                file_list.append(file)
        if len(file_list) > 0:
            file_list.sort(reverse=True)
            index_json_file = os.path.join(json_dir,file_list[0])
            logging.info("Serving json file: {index_json_file}")
            f = codecs.open(index_json_file, "r", "utf-8")    
            json_decoded = json.load(f)
            f.close
            json_decoded['error_list'] = []
            json_str = json.dumps(json_decoded)
            return(json_str)
        else:
            msg = "No json files with indexid=" + index_id + " and version=" + index_version
            return form_composition_response(True, -102, msg)
    
def form_status_response(return_state, req_type):
    data_dict = {}
    data_dict['data'] = {}
    data_dict['data']['service_state'] = return_state
    data_dict['data']['service_time'] = int(time.time()) 
    if req_type == 'realtime':
        data_dict['data']['reload_session_number'] = 0
        data_dict['data']['indices_list'] = {}
    data_json = json.dumps(data_dict)
    return(data_json)

def form_composition_response(req_error=None, error_code=None, error_msg=None, version_status = None):
    data_dict = {}
    data_dict['data'] = {}
    err_list = []
    if version_status == 'P' and plan_error:
        err_list.append({'category': plan_error_category, 'code': plan_error_code, 'message': plan_error_msg})
    if version_status == 'A' and activate_error:
        err_list.append({'category': activate_error_category, 'code': activate_error_code, 'message': activate_error_msg})
    if version_status == 'P' and plan_error:
        err_list.append({'category': plan_error_category, 'code': plan_error_code, 'message': plan_error_msg})
    if version_status == None:
        err_list.append({'category': 1, 'code': error_code, 'message': error_msg})
    data_dict['error_list'] = err_list
    data_json = json.dumps(data_dict)
    return(data_json)

def dump_json(body_dict, index_code):
    comp_version = body_dict['data']['composition']['version']
    json_file_name = index_code + '.' + str(comp_version) + '.' + str(int(time.time())) + '.json'
    json_file_name = os.path.join(json_dir,json_file_name)
    
    with open(json_file_name, 'w', encoding='utf-8') as f:
        json.dump(body_dict, f, ensure_ascii=False, indent=4)
    return

# teststr = "{"data":{"composition":{"indexid":"CF","version":6,"version_status":"A","short_name":"IMOEX","first_calc_val":1000.0,"first_calc_date":1567717200,"code":"IMOEX","short_name_en":"IMOEX","index_type":"A","bulletin":"Y","bulletin_snp":"N","public_to_web":"N","w0_precision":7,"price_kind":"C","kind_calc":1,"calc_interval_sec":1,"decimals_num":2,"currency_trade":"RUB","currency_index":"RUB","calc_method":"SC","activation_date":1569531600,"divisor":3924864189.7938,"period_list":["N"],"main_board":"TQBR","board_list":["TQBR"],"calc_base":[{"free_float":0.16,"weight_factor":1.0,"issue_size":1.117433E10,"ki":0.02,"mnemo":"MAGN","dividend_value":1.562171334E+10,"price":39.51,"sec_type":"1","short_name":"ММК"},{"free_float":0.16,"weight_factor":1.0,"issue_size":1.117433E10,"ki":0.02,"mnemo":"MAGN","dividend_value":1.662740304E+10,"price":39.51,"sec_type":"1","short_name":"ММК"},{"free_float":0.16,"weight_factor":1.0,"issue_size":1.117433E10,"ki":0.02,"mnemo":"MAGN","dividend_value":2.362253362E+10,"price":39.51,"sec_type":"1","short_name":"ММК"},{"free_float":0.16,"weight_factor":1.0,"issue_size":5.99322724E9,"ki":0.02,"mnemo":"NLMK","dividend_value":34760717992,"price":141.68,"sec_type":"1","short_name":"НЛМК ао"},{"free_float":0.16,"weight_factor":1.0,"issue_size":5.99322724E9,"ki":0.02,"mnemo":"NLMK","dividend_value":36199092529,"price":141.68,"sec_type":"1","short_name":"НЛМК ао"},{"free_float":0.16,"weight_factor":1.0,"issue_size":5.99322724E9,"ki":0.02,"mnemo":"NLMK","dividend_value":43990287941.6,"price":141.68,"sec_type":"1","short_name":"НЛМК ао"},{"free_float":0.96,"weight_factor":0.8269221,"issue_size":2.92567655E8,"ki":0.02,"mnemo":"YNDX","price":2319.6,"sec_type":"1","short_name":"Yandex clA"},{"free_float":0.33,"weight_factor":1.0,"issue_size":9.65E9,"ki":0.02,"mnemo":"AFKS","dividend_value":1.0615E+9,"price":12.856,"sec_type":"1","short_name":"Система ао"},{"free_float":0.46,"weight_factor":0.6390014,"issue_size":2.36735129E10,"ki":0.02,"mnemo":"GAZP","dividend_value":393217049269,"price":231.97,"sec_type":"1","short_name":"ГАЗПРОМ ао"},{"free_float":0.38,"weight_factor":0.6964831,"issue_size":1.58245476E8,"ki":0.02,"mnemo":"GMKN","dividend_value":125412704639.52,"price":16388.0,"sec_type":"1","short_name":"ГМКНорНик"},{"free_float":0.71,"weight_factor":1.0,"issue_size":1.01911355E8,"ki":0.02,"mnemo":"MGNT","dividend_value":14000581949.9,"price":3587.0,"sec_type":"1","short_name":"Магнит ао"},{"free_float":0.71,"weight_factor":1.0,"issue_size":1.01911355E8,"ki":0.02,"mnemo":"MGNT","dividend_value":16996775786.9,"price":3587.0,"sec_type":"1","short_name":"Магнит ао"},{"free_float":0.11,"weight_factor":1.0,"issue_size":1.0598177817E10,"ki":0.02,"mnemo":"ROSN","dividend_value":120077354666.61,"price":422.55,"sec_type":"1","short_name":"Роснефть"},{"free_float":0.73,"weight_factor":1.0,"issue_size":7.701998235E9,"ki":0.02,"mnemo":"SNGSP","dividend_value":58689226550.7,"price":37.02,"sec_type":"1","short_name":"Сургнфгз-п"},{"free_float":0.58,"weight_factor":1.0,"issue_size":2.276401458E9,"ki":0.02,"mnemo":"MOEX","dividend_value":17528291226.6,"price":94.94,"sec_type":"1","short_name":"МосБиржа"},{"free_float":0.16,"weight_factor":1.0,"issue_size":1.5193014862E10,"ki":0.02,"mnemo":"RUAL","price":28.59,"sec_type":"1","short_name":"RUSAL plc"},{"free_float":0.19,"weight_factor":1.0,"issue_size":4.26288813551E11,"ki":0.02,"mnemo":"HYDR","dividend_value":15918514454.21,"price":0.5282,"sec_type":"1","short_name":"РусГидро"},{"free_float":0.54,"weight_factor":0.6964831,"issue_size":7.15E8,"ki":0.02,"mnemo":"LKOH","dividend_value":7.125E+10,"price":5387.5,"sec_type":"1","short_name":"ЛУКОЙЛ"},{"free_float":0.54,"weight_factor":0.6964831,"issue_size":7.15E8,"ki":0.02,"mnemo":"LKOH","dividend_value":1.1625E+11,"price":5387.5,"sec_type":"1","short_name":"ЛУКОЙЛ"},{"free_float":0.21,"weight_factor":0.6964831,"issue_size":3.036306E9,"ki":0.02,"mnemo":"NVTK","dividend_value":5.104030386E+10,"price":1367.0,"sec_type":"1","short_name":"Новатэк ао"},{"free_float":1.0,"weight_factor":0.6415593,"issue_size":1.0E9,"ki":0.02,"mnemo":"SBERP","dividend_value":1.6E+10,"price":202.9,"sec_type":"1","short_name":"Сбербанк-п"},{"free_float":0.45,"weight_factor":1.0,"issue_size":4.70183404E8,"ki":0.02,"mnemo":"POLY","dividend_value":9623908094.267,"price":938.0,"sec_type":"1","short_name":"Polymetal"},{"free_float":0.34,"weight_factor":1.0,"issue_size":7.39E8,"ki":0.02,"mnemo":"DSKY","dividend_value":3.24421E+9,"price":90.02,"sec_type":"1","short_name":"ДетскийМир"},{"free_float":0.34,"weight_factor":1.0,"issue_size":7.39E8,"ki":0.02,"mnemo":"DSKY","dividend_value":3.28855E+9,"price":90.02,"sec_type":"1","short_name":"ДетскийМир"},{"free_float":0.32,"weight_factor":0.9350228,"issue_size":2.1786907E9,"ki":0.02,"mnemo":"TATN","dividend_value":48497654982,"price":704.9,"sec_type":"1","short_name":"Татнфт 3ао"},{"free_float":0.32,"weight_factor":0.9350228,"issue_size":2.1786907E9,"ki":0.02,"mnemo":"TATN","dividend_value":70546004866,"price":704.9,"sec_type":"1","short_name":"Татнфт 3ао"},{"free_float":0.27,"weight_factor":1.0,"issue_size":1.2960541337338E13,"ki":0.02,"mnemo":"VTBR","dividend_value":14239456640.85,"price":0.04292,"sec_type":"1","short_name":"ВТБ ао"},{"free_float":0.45,"weight_factor":1.0,"issue_size":1.998381575E9,"ki":0.02,"mnemo":"MTSS","dividend_value":39927310941.78,"price":266.0,"sec_type":"1","short_name":"МТС-ао"},{"free_float":0.33,"weight_factor":1.0,"issue_size":1.044E11,"ki":0.02,"mnemo":"IRAO","dividend_value":1.791875E+10,"price":4.5495,"sec_type":"1","short_name":"ИнтерРАОао"},{"free_float":0.18,"weight_factor":1.0,"issue_size":6.60497344E8,"ki":0.02,"mnemo":"PIKK","dividend_value":14999894682,"price":397.0,"sec_type":"1","short_name":"ПИК ао"},{"free_float":0.32,"weight_factor":1.0,"issue_size":2.574914954E9,"ki":0.02,"mnemo":"RTKM","dividend_value":6437287385,"price":78.98,"sec_type":"1","short_name":"Ростел -ао"},{"free_float":0.18,"weight_factor":1.0,"issue_size":1.274665323063E12,"ki":0.02,"mnemo":"FEES","dividend_value":2.0449361E+10,"price":0.18166,"sec_type":"1","short_name":"ФСК ЕЭС ао"},{"free_float":0.17,"weight_factor":1.0,"issue_size":1.79768227E8,"ki":0.02,"mnemo":"MVID","price":427.5,"sec_type":"1","short_name":"М.видео"},{"free_float":0.41,"weight_factor":1.0,"issue_size":1.110616299E9,"ki":0.02,"mnemo":"AFLT","dividend_value":2.8565E+9,"price":102.98,"sec_type":"1","short_name":"Аэрофлот"},{"free_float":0.2,"weight_factor":1.0,"issue_size":8.3771866E8,"ki":0.02,"mnemo":"CHMF","dividend_value":26874014612.8,"price":950.8,"sec_type":"1","short_name":"СевСт-ао"},{"free_float":0.2,"weight_factor":1.0,"issue_size":8.3771866E8,"ki":0.02,"mnemo":"CHMF","dividend_value":29680372123.8,"price":950.8,"sec_type":"1","short_name":"СевСт-ао"},{"free_float":0.2,"weight_factor":1.0,"issue_size":8.3771866E8,"ki":0.02,"mnemo":"CHMF","dividend_value":37186331317.4,"price":950.8,"sec_type":"1","short_name":"СевСт-ао"},{"free_float":0.16,"weight_factor":1.0,"issue_size":6.3048706145E10,"ki":0.02,"mnemo":"UPRO","dividend_value":7.0E+9,"price":2.628,"sec_type":"1","short_name":"Юнипро ао"},{"free_float":0.48,"weight_factor":0.6415593,"issue_size":2.1586948E10,"ki":0.02,"mnemo":"SBER","dividend_value":3.45391168E+11,"price":229.09,"sec_type":"1","short_name":"Сбербанк"},{"free_float":0.25,"weight_factor":1.0,"issue_size":3.5725994705E10,"ki":0.02,"mnemo":"SNGS","dividend_value":23221896558.25,"price":34.715,"sec_type":"1","short_name":"Сургнфгз"},{"free_float":0.32,"weight_factor":1.0,"issue_size":1554875.0,"ki":0.02,"mnemo":"TRNFP","dividend_value":16646414006.25,"price":151200.0,"sec_type":"1","short_name":"Транснф ап"},{"free_float":0.25,"weight_factor":1.0,"issue_size":1.295E8,"ki":0.02,"mnemo":"PHOR","dividend_value":6.6045E+9,"price":2458.0,"sec_type":"1","short_name":"ФосАгро ао"},{"free_float":0.25,"weight_factor":1.0,"issue_size":1.295E8,"ki":0.02,"mnemo":"PHOR","dividend_value":9.324E+9,"price":2458.0,"sec_type":"1","short_name":"ФосАгро ао"},{"free_float":0.37,"weight_factor":1.0,"issue_size":1.11637791E8,"ki":0.02,"mnemo":"SFIN","dividend_value":1618747969.5,"price":470.0,"sec_type":"1","short_name":"САФМАР ао"},{"free_float":0.16,"weight_factor":1.0,"issue_size":1.33561119E8,"ki":0.02,"mnemo":"PLZL","dividend_value":19129707181.6,"price":7775.0,"sec_type":"1","short_name":"Полюс"},{"free_float":1.0,"weight_factor":0.9350228,"issue_size":1.475085E8,"ki":0.02,"mnemo":"TATNP","dividend_value":3.28353921E+9,"price":631.9,"sec_type":"1","short_name":"Татнфт 3ап"},{"free_float":1.0,"weight_factor":0.9350228,"issue_size":1.475085E8,"ki":0.02,"mnemo":"TATNP","dividend_value":4.77632523E+9,"price":631.9,"sec_type":"1","short_name":"Татнфт 3ап"},{"free_float":0.18,"weight_factor":1.0,"issue_size":2.7079709866E10,"ki":0.02,"mnemo":"CBOM","dividend_value":2978768085.26,"price":5.783,"sec_type":"1","short_name":"МКБ ао"},{"free_float":0.09,"weight_factor":1.0,"issue_size":2.9412E8,"ki":0.02,"mnemo":"RNFT","price":577.8,"sec_type":"1","short_name":"РуссНфт ао"},{"free_float":0.42,"weight_factor":1.0,"issue_size":1.03030215E8,"ki":0.01,"mnemo":"LSRG","dividend_value":8.03635677E+9,"price":730.6,"sec_type":"1","short_name":"ЛСР ао"},{"free_float":0.34,"weight_factor":1.0,"issue_size":7.36496563E9,"ki":0.02,"mnemo":"ALRS","dividend_value":30270008739.3,"price":73.27,"sec_type":"1","short_name":"АЛРОСА ао"},{"free_float":0.21,"weight_factor":1.0,"issue_size":4.8792966E8,"ki":0.02,"mnemo":"LNTA","price":218.5,"sec_type":"1","short_name":"Лента др"},{"free_float":0.41,"weight_factor":1.0,"issue_size":2.71572872E8,"ki":0.02,"mnemo":"FIVE","dividend_value":2.5E+10,"price":2263.5,"sec_type":"1","short_name":"FIVE-гдр"}]}}}"
# dump_json(teststr)
# print(form_status_response("A","compositions"))