from config import config
from threading import Thread
import datetime
from datetime import datetime
from telegram import Update
from telegram.ext import Filters
from telegram.ext import Updater
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler


########################################################################################################################
                                                #ПЕРЕМЕННЫЕ


CODE = 1
start_code = 'start'
now_time =''
id_list = list()
zadanie_1 = 'Задание 1\n<z1 text>/nКод опасности ХУЙ.'
print ('start')
updater = Updater(
        config.TOKEN,
        base_url=config.API_URL,
        use_context=True
    )


########################################################################################################################


########################################################################################################################
                                            #ЧАСЫ РЕАЛЬНОГО ВРЕМЕНИ


def clock():
    global now_time
    while True:
        now_time = datetime.now().time()


########################################################################################################################


########################################################################################################################
                                                #РЕГИСТРАЦИЯ


def main():
    global now_time, id_list, zadanie_1, updater

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
    #updater.idle()


class registration:

    def sg_start(update: Update, context):
        global id_list, updater
        print ('sg_start')
        if now_time.hour < 17:
            print(1)
            id_list.append(update.message.chat_id)
            context.bot.send_message(chat_id=update.message.chat_id, text='Введите код начала игры.')
            return CODE
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='Registraciya zevershena.')
            updater.stop()
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


########################################################################################################################
                                                #ИФНО


def echo(update: Update, context):
    global now_time
    print(update.message.text, now_time)
    context.bot.send_message(chat_id=update.message.chat_id, text=f'Chat_id: {update.effective_message.chat_id}\nMessage_id: {update.effective_message.message_id}\nText: {update.effective_message.text}\nMessage_time: {now_time}')


########################################################################################################################
                                                #ЗАДАНИЕ_1


def z1():
    global now_time, id_list, zadanie_1
    updater_z1 = Updater(
        config.TOKEN,
        base_url=config.API_URL,
        use_context=True
     )

    loop = True
    while loop:
        if now_time.hour == 17 and now_time.minute == 57:
            for id in id_list:
                 z1.zadanie1_send(context=updater_z1, id=id)
            break

    dispatcher_z1 = updater_z1.dispatcher

    code1_handler = MessageHandler(Filters.text, z1.zadanie1_code)

    dispatcher_z1.add_handler(code1_handler)

    updater_z1.start_polling()



class z1:

    def zadanie1_send(context, id):
        context.bot.send_message(chat_id=id, text=zadanie_1)
        return


    def zadanie1_code(update: Update, context):

        return
########################################################################################################################


















if __name__ == '__main__':
    print(1)
    Thread(target=main).start()
    print(2)
    Thread(target=clock).start()
    print(3)
    Thread(target=z1).start()







