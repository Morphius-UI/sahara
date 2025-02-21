import requests
import telebot
from telebot import types
import time
import random
import requests
from ktylib.Account import Account
from eth_utils import from_wei

Token = '7734870298:AAHcEohsz-0fdZRKndROLTLUcnWIS1vwuA0'
root = telebot.TeleBot(Token)

k = 0

'''@root.inline_handler(func=lambda query: len(query.query) > 0 )
def query_text(query):
    timer = time.time()
    a = []
    try:
        address = query.query
        send = types.InlineQueryResultArticle(id=1, title="0.1 More", description=f"Address: {address}", input_message_content=types.InputTextMessageContent(message_text=f"0.1 More was send on {address}"))
        root.answer_inline_query(query.id, [send])
        a.append(address)
        timer1 = time.time() - timer



    except Exception as e:
        print(e)

    while True:
        timer1 = time.time() - timer
        if timer1 > 30:
            print(a[-1:])
            break
'''
class MoonveilFaucet:
    def __init__(
        self,
        rpc: str = "https://faucet.testnet.moonveil.gg/api/claim",
        address: str="",
        proxy=None,
        agent=None
    ):
        self.rpc = rpc
        self.address = address
        self.proxy=proxy
        self.agent=agent
    def classic(self):
        url = f'{self.rpc}'
        json_data = {
            'address': self.address
        }
        headers = {
        'User-Agent': self.agent,
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://faucet.testnet.moonveil.gg/',
        'Content-Type': 'application/json',
        'Origin': 'https://faucet.testnet.moonveil.gg',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'DNT': '1',
        'Priority': 'u=0',
        'TE': 'trailers'}

        request = requests.post(url, json=json_data,headers=headers, proxies={'http': self.proxy, 'https': self.proxy}).json()
        return request["msg"]



file = open('proxys')
prox = file.readline()

@root.message_handler(content_types='text')
def address(message):
    try:
        file = open('useragent')
        agent = file.readline()
        message_id = message.message_id
        address = message.text
        result = MoonveilFaucet(proxy=prox, address=str(address), agent=str(agent))
        more = result.classic()
        if more != 'invalid address':
            root.reply_to(message, f"{more}")
        else:
            pass

    except Exception as e:
        print(e)




root.infinity_polling(none_stop=True)
