import re

def request_formatter(last_messages):
    if len(last_messages) == 3:
        request = f'@@ПЕРВЫЙ@@ {last_messages[0]} @@ВТОРОЙ@@ {last_messages[1]} @@ПЕРВЫЙ@@ {last_messages[2]} @@ВТОРОЙ@@'
    if len(last_messages) == 1:
        request = f'@@ПЕРВЫЙ@@  @@ВТОРОЙ@@  @@ПЕРВЫЙ@@ {last_messages[0]} @@ВТОРОЙ@@'
    return request

def cut_chat_history(chat_history):
    if len(chat_history)>3:
        return chat_history[-3:]
    else:
        return chat_history

def response_formatter(last_message, response):
    response = re.split('@@ПЕРВЫЙ@@|@@ВТОРОЙ@@', response)
    i = 0
    try:
        while last_message not in response[i]:
            i+=1
        i+=1
        while response[i].replace(' ', '') == '':
            i += 1
        return response[i]
    except:
        return 'К сожалению, что-то пошло не так. Перезапустите бота.'