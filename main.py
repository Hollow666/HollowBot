from config import config
from threading import Thread
import datetime
from datetime import datetime
from telegram import Update
from telegram.ext import Filters
from telegram.ext import Updater
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler

CODE, Z1, Z1_CODE = range(3)
start_code = 'start'
now_time =''
id_list = list()
zadanie_1 = 'Задание 1\n<z1 text>/nКод опасности ХУЙ.'
reg_flag = True

def clock():
    global now_time
    while True:
        now_time = datetime.now().time()


def main():
    global now_time, id_list, zadanie_1, reg_flag
    updater = Updater(
        config.TOKEN,
        base_url=config.API_URL,
        use_context=True
    )
    dispatcher = updater.dispatcher
    conversation = ConversationHandler(
        entry_points=[
            CommandHandler('sg',  registration.sg_start),
        ],
        states={
            CODE: [
                MessageHandler(Filters.text,  registration.sg_code)
            ],
        },
        fallbacks=[
            CommandHandler('cancelgame', registration.sg_cancel),
        ],
        allow_reentry=True,
    )


    dispatcher.add_handler(conversation)
    dispatcher.add_handler(MessageHandler(Filters.all, echo), )


    updater.start_polling()
    updater.idle()


##### FUCKING REGISTRATION
class registration:

    def sg_start(update: Update, context):
        global id_list
        print ('sg_start')
        if now_time.hour < 23:
            print(1)
            id_list.append(update.message.chat_id)
            context.bot.send_message(chat_id=update.message.chat_id, text='Введите код начала игры.')
            return CODE
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='Registraciya zevershena.')
            return ConversationHandler.END


    def sg_code(update: Update, context):
        global start_code, id_list
        print('sg_code')
        for id in id_list:
            if update.message.chat_id == id:
                if update.message.text == start_code:
                    context.bot.send_message(chat_id=update.message.chat_id, text='Вы ввели верный код. Игра начнется в 22:00!!!')
                    print('registred')
                    return ConversationHandler.END
                else:
                    context.bot.send_message(chat_id=update.message.chat_id, text='Вы ввели неверный код.')
                    print('didn\'t registred')
                    return ConversationHandler.END


    def sg_cancel(update: Update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text='Игра отклонена.')
        return ConversationHandler.END
##### END OF FUCKING REGISTRATION


def echo(update: Update, context):
    global now_time
    print(update.message.text, now_time)
    context.bot.send_message(chat_id=update.message.chat_id, text=f'Chat_id: {update.effective_message.chat_id}\nMessage_id: {update.effective_message.message_id}\nText: {update.effective_message.text}\nMessage_time: {now_time}')


def game():
    global now_time, id_list, zadanie_1, reg_flag
    updater = Updater(
        config.TOKEN,
        base_url=config.API_URL,
        use_context=True
    )

    loop = True
    while loop:
        if now_time.hour == 22 and now_time.minute == 32:
            for id in id_list:
                zadanie1_msg(context=updater, id=id)
            break


def zadanie1_msg(context, id):
    context.bot.send_message(chat_id=id, text=zadanie_1)
    return

if __name__ == '__main__':
    Thread(target=main).start()
    Thread(target=clock).start()
    Thread(target=game).start()







