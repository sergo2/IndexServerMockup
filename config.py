# -*- coding: utf-8 -*-
import logging

comp_receiver_state = 'O'
comp_state_url = '/composition/v1/'

publisher_state = 'O'
receiver_url = '/realtime/v1/'

server_port = 65156

plan_error = False
plan_error_category = 1
plan_error_code = -900
plan_error_msg = 'Error from Index Server mockup'

activate_error = True
activate_error_category = 2
activate_error_code = -804
activate_error_msg = 'Для фин. инструмента NL0009348242 не сформированы служебные данные в таблице SecHist на дату 2020-05-25'

get_index_error = False
get_index_error_category = 1
get_index_error_code = -300
get_index_error_msg = 'Reconciliation error'

daily_values_error = False
daily_values_error_category = 1
daily_values_error_code = -400
daily_values_error_msg = 'Cant form daily values'

json_dir = 'json'