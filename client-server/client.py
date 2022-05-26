'''
Клиент
'''

import sys
import json
import socket
import time
#модуль с готовыми заголовками протокола
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
