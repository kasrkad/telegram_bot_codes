#!/bin/python3
import requests
from bs4 import BeautifulSoup
from log_pass import DATA
import time

def get_1c_codes(phone_number):
    
    code_dict = {}
    parse_list = ['https://my.devinotele.com/Message/StatisticsDetailed?page=1','https://my.devinotele.com/Message/StatisticsDetailed?page=2']

    session  = requests.Session()
    authorization = session.post('https://my.devinotele.com/Account/LogOn', data = DATA )
    print(session.cookies)
    for site in parse_list:
        time.sleep(3)
        print (f'проверяем списки смс {authorization}')
        dd = session.get(site)
        html_doc = BeautifulSoup(dd.text, features='html.parser')
        list_of_tr = html_doc.find_all('tbody',{'class': ''})

        replace_list = ['<td>','</td>','<tr>','</tr>','<tbody>','</tbody>']
        list_new = str(list_of_tr).replace(u'\xa0', ' ')
        for replacer in replace_list:
            list_new = list_new.replace(replacer,'')
        split_list = list_new.splitlines()
        split_list.pop(0)
        split_list.pop(len(split_list)-1)

        while (len(split_list)//15) > 0:
            if split_list[3] in code_dict:
                del split_list[0:15]
            else:
                if split_list[12].startswith('Код для входа'):
                    code_dict[split_list[3]]=split_list[12]
                del split_list[0:15]        
    return f'Для номера {phone_number} - {code_dict[phone_number]}'

get_1c_codes('79227192634')