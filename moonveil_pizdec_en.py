import requests
import telebot
from eth_abi.grammar import parse
from telebot import types
import time
import random
import requests
import re
from peewee import *
from datetime import date
import calendar
import threading


Token = '7874201562:AAHhaTJUclkYsaPMQshtt5TUaCB_BlBsnPY'
root = telebot.TeleBot(Token)

# chat_member = root.get_chat_member(message_id, message_id).user.username


k = 0
db = SqliteDatabase('fof.sqlite')

def randomfr(username):
    lista = [f'👍 @{username}, your limit has been restored - requesting tokens again.',f'✨ @{username}, limit replenished, you can take tokens again.',f'✅ @{username}, limit refreshed, initiating token request.',f'🚀 @{username}, limit restored – time for new tokens!',f'🎉 @{username}, token limit back, requesting them right now!']
    return lista[random.randrange(0, len(lista)+1)]

class MoonveilFaucet:
    def __init__(
            self,
            rpc: str = "https://faucet.testnet.moonveil.gg/api/claim",
            address: str = "",
            proxy=None
    ):
        self.rpc = rpc
        self.address = address
        self.proxy = proxy

    def classic(self):
        url = f'{self.rpc}'
        json_data = {
            'address': self.address
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0',
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

        request = requests.post(url, json=json_data, headers=headers,
                                proxies={'http': self.proxy, 'https': self.proxy}).json()
        return request["msg"]




class research:
    def reserch_user(userId):
        for user in Person.select().where(Person.userId == userId):
            return user.point

    def nextdata(userId):
        for user in Person.select().where(Person.userId == userId):
            return user.nextsend

    def delandcreat(userId):
        point = research.reserch_user(userId)
        q = Person.delete().where(Person.userId == userId)
        q.execute()
        Person.create(userId=userId, lastsend=calendar.timegm(time.gmtime()),nextsend=calendar.timegm(time.gmtime()) + 86400, point=point+1)


class Person(Model):
    userId = IntegerField()
    lastsend = IntegerField()
    nextsend = IntegerField()
    point = IntegerField()
    class Meta:
        database = db


class Timeframe(Model):
    lastsend = IntegerField()
    nextsend = IntegerField()
    userId = IntegerField()
    class Meta:
        database = db


def leaderboard1(message):
    f = ''
    chat_id = message.chat.id
    k=0
    after = 0
    undo = []
    for person in Person.select(Person).order_by(Person.point.desc()):
        k+=1
        userId = person.userId
        UsrInfo = root.get_chat_member(chat_id, userId).user.username
        undo.append(person.point)
        if k>=11 and undo[k-1] != undo[k-2]:
            break
        if k>=11 and undo[k-1] == undo[k-2]:
            kol = person.point
            after +=1
            continue
        if person.point == 1:
            f= f+ str(k)+ f'. @{UsrInfo} — ' +str(person.point) + ' request.\n'
        else:
            f = f + str(k) + f'. @{UsrInfo} — ' + str(person.point) + ' requests.\n'
    if after != 0:
        f+= f'+{str(after)} users with {kol} requests'
        return f
    else:
        return f

def print_numbers():
    while True:
        print(calendar.timegm(time.gmtime()))
        for user in Timeframe.select():
            userId = user.userId
            print(user.nextsend)
            print(calendar.timegm(time.gmtime()))
            if user.nextsend <= calendar.timegm(time.gmtime()):
                UsrInfo = root.get_chat_member(userId, userId).user.username
                text = randomfr(UsrInfo)
                root.send_message(userId, f"{text}")
                q = Timeframe.delete().where(Timeframe.userId == userId)
                q.execute()
        time.sleep(60)


thread = threading.Thread(target=print_numbers)
thread.start()

file = open('proxys')
prox = file.readline()

db.connect()



@root.message_handler(commands=['leaderboard'])
def leaderboard2(message):
    try:
        h = leaderboard1(message)
        root.reply_to(message, f'🏆<b>Leaderboard:</b>\n{h}', parse_mode='HTML')
    except Exception as e:
        print(e)

@root.message_handler(content_types=['text'])
def address(message):
    try:
        chat_id = message.chat.id
        print(chat_id)
        message_id = message.from_user.id
        print(message_id)
        address = message.text
        result = MoonveilFaucet(proxy=prox, address=str(address))
        more = result.classic()
        Person.create(userId=int(message_id), lastsend=calendar.timegm(time.gmtime()),
                      nextsend=calendar.timegm(time.gmtime()) + 86400, point=1)
        if more != 'invalid address':
            if more.split()[0] == "Txhash:":
                if research.reserch_user(message_id) == None:
                    Person.create(userId=int(message_id), lastsend=calendar.timegm(time.gmtime()),
                                  nextsend=calendar.timegm(time.gmtime()) + 86400, point=1)
                    Timeframe.create(lastsend=calendar.timegm(time.gmtime()),
                                     nextsend=calendar.timegm(time.gmtime()) + 86400, userId=int(message_id))
                    root.reply_to(message, f"<b>✅ Tokens successfully sent to the specified address!</b>\n\n Transaction:<a href='https://blockscout.testnet.moonveil.gg/tx/{more.split()[1]}'>Moonveil Explorer»</a>", parse_mode='HTML')

                else:
                    if research.nextdata(message_id) <= calendar.timegm(time.gmtime()):
                        research.delandcreat(message_id)
                        root.reply_to(message,
                                      f"<b>✅ Tokens successfully sent to the specified address!</b>\n\n Transaction:<a href='https://blockscout.testnet.moonveil.gg/tx/{more.split()[1]}'>Moonveil Explorer»</a>",
                                      parse_mode='HTML')
                    else:
                        root.reply_to(message,
                                      f"<b>✅ Tokens successfully sent to the specified address!</b>\n\n Transaction:<a href='https://blockscout.testnet.moonveil.gg/tx/{more.split()[1]}'>Moonveil Explorer»</a>",
                                      parse_mode='HTML')



            elif more.split()[0] == "You":
                otvet = re.findall(r'\d+', more.split()[8])
                if len(otvet) == 3:
                    root.reply_to(message,
                                  f"🤷‍♂️ You have already requested tokens today, please return via <b>{otvet[0]}</b> hours <b>{otvet[1]}</b> minutes and request them again.", parse_mode='HTML')
                else:
                    root.reply_to(message,
                                  f"🤷‍♂️ You have already requested tokens today, please return via <b>{otvet[0]}</b> minutes and request them again.", parse_mode='HTML')

            elif more.split()[0] == "Request":
                pass

            else:
                root.reply_to(message, f"🙅‍♂️ <b>Faucet error, please repeat later!</b>", parse_mode='HTML')

        else:
            pass

    except Exception as e:
        print(e)






root.infinity_polling(none_stop=True)