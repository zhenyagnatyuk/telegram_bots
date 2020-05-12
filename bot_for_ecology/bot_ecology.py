
# @calc_ecology_bot in telegram


import logging
import os

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, DictPersistence)

PORT = int(os.environ.get('PORT', 5000))
TOKEN = "968557809:AAFf1kTrVggthzjrpXdr3L0AzWVvgv0Haqc"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

Q, Type, S, N1, N2 = range(5)

K, ETA1, D0, W, Z, ETA2 = range(6)

def start_calc_nitrogen_oxides(update, context):
    update.message.reply_text(
        "Hi! Let`s calculate nitrogen oxides. "
        "Send /cancel to stop talking to me.\n\n"
        "Please enter value of K.\n"
        "It is must be a number")

    return K

def get_k(update, context):
    logger.info("K = %s", update.message.text)
    context.user_data['K'] = update.message.text
    reply_keyboard = [['Малотоксичні пальники'], ['Ступенева подача повітря'], ['Подача третинного повітря'], 
                      ['Рециркуляція димових газів'], ['Трьохступенева подача повітря та палива'], 
                      ['Малотоксичні пальники + ступенева подача повітря'], ['Малотоксичні пальники + подача третинного повітря'], 
                      ['Малотоксичні пальники + рециркуляція димових газів'], ['Ступенева подача повітря + подача третинного повітря'], 
                      ['Ступенева подача повітря + рециркуляція димових газів'], 
                      ['Малотоксичні пальники + ступенева подача повітря + рециркуляція димових газів'], 
                      ['Малотоксичні пальники + ступенева подача повітря + подача третинного повітря']]
    
    update.message.reply_text('Тепер оберіть тип первинних заходів зі скорочення викиду оксиду азоту',
                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return ETA1

def get_eta1(update, context):
    key = update.message.text
    values = {
        'Малотоксичні пальники' : 0.2, 
        'Ступенева подача повітря' : 0.3, 
        'Подача третинного повітря' : 0.2, 
        'Рециркуляція димових газів' : 0.1, 
        'Трьохступенева подача повітря та палива' : 0.35, 
        'Малотоксичні пальники + ступенева подача повітря' : 0.45, 
        'Малотоксичні пальники + подача третинного повітря' : 0.4, 
        'Малотоксичні пальники + рециркуляція димових газів' : 0.3, 
        'Ступенева подача повітря + подача третинного повітря' : 0.45, 
        'Ступенева подача повітря + рециркуляція димових газів' : 0.4, 
        'Малотоксичні пальники + ступенева подача повітря + рециркуляція димових газів' : 0.5, 
        'Малотоксичні пальники + ступенева подача повітря + подача третинного повітря' : 0.6
    }
    if key in values.keys():
        n1 = values[key]
    else:
        update.message.reply_text('Не зрозумілий тип первинних заходів зі скорочення викиду оксиду азоту,'
                                   'завершення підрахунку',
                                   reply_markup=ReplyKeyboardRemove())
        
    logger.info("Eta1 = %s", n1)
    context.user_data['eta1'] = n1
    update.message.reply_text('Введіть продуктивність парового котла.\n'
                              'Це повинно бути число',
                               reply_markup=ReplyKeyboardRemove())
    
    return D0


def get_d0(update, context):
    logger.info("D0 = %s", update.message.text)
    context.user_data['D0'] = update.message.text
    reply_keyboard = [['Котел з тиском свіжої пари p0 ( 13,8 МПа (при D0³ 500 т/год) з проміжним перегрівом'], 
                      ['Котел з тиском пари в межах: 9,8 МПа £ p0£ 13,8 МПа (при D0 < 500 т/год) без проміжного перегріву'],
                      ['Котел з тиском пари в межах: 1,4 МПа < p0 < 9,8 МПа (при D0 = 6,5…75 т/год для перегрітої пари) без проміжного перегріву'],
                      ['Котел з тиском пари p0£ 1,4 МПа (при D0£ 20 т/год для насиченої пари) без проміжного перегріву']]
    update.message.reply_text('Тепер оберіть тип котла',
                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return W


def get_w(update, context):
    key = update.message.text
    values = {
        'Котел з тиском свіжої пари p0 ( 13,8 МПа (при D0³ 500 т/год) з проміжним перегрівом' : 1.35, 
        'Котел з тиском пари в межах: 9,8 МПа £ p0£ 13,8 МПа (при D0 < 500 т/год) без проміжного перегріву' : 1.45, 
        'Котел з тиском пари в межах: 1,4 МПа < p0 < 9,8 МПа (при D0 = 6,5…75 т/год для перегрітої пари) без проміжного перегріву' : 1.35, 
        'Котел з тиском пари p0£ 1,4 МПа (при D0£ 20 т/год для насиченої пари) без проміжного перегріву' : 1.5
    }
    if key in values.keys():
        w = values[key]
    else:
        update.message.reply_text('Не зрозумілий тип котлу, завершення підрахунку',
                                   reply_markup=ReplyKeyboardRemove())
        
    logger.info("W = %s", w)
    context.user_data['w'] = w
    reply_keyboard = [['Тверде паливо'], 
                      ['Природне паливо'],
                      ['Мазут']]
    update.message.reply_text('Оберіть тип палива',
                               reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return Z

def get_z(update, context):
    key = update.message.text
    values = {
        'Тверде паливо' : 1.15, 
        'Природне паливо' : 1.25, 
        'Мазут' : 1.25
    }
    if key in values.keys():
        z = values[key]
    else:
        update.message.reply_text('Не зрозумілий тип палива, завершення підрахунку',
                                   reply_markup=ReplyKeyboardRemove())
        
    logger.info("Z = %s", z)
    context.user_data['z'] = z
    reply_keyboard = [['Селективне некаталітичне відновлення'], 
                      ['Селективне каталітичне відновлення'],
                      ['Активоване вугілля'],
                      ['DESONOX – SNOX']]
    update.message.reply_text('Оберіть технологію очищення від димових газів',
                               reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return ETA2

def get_eta2(update, context):
    key = update.message.text
    values = {
        'Селективне некаталітичне відновлення' : (0.5, 0.99),  
        'Селективне каталітичне відновленняпаливо' : (0.8, 0.99), 
        'Активоване вугілля' : (0.7, 0.99),
        'DESONOX – SNOX' : (0.95, 0.99)
    }
    if key in values.keys():
        n2, b = values[key]
    else:
        update.message.reply_text('Не зрозуміла технологія очищення, завершення підрахунку',
                                   reply_markup=ReplyKeyboardRemove())
        
    logger.info("n2 = %s, b = %s", n2, b)
    
    k, n1, d, w, z = float(context.user_data['K']), context.user_data['eta1'], float(context.user_data['D0']), context.user_data['w'], context.user_data['z']
    
    logger.info("k = %s, n1 = %s, d = %s, w = %s, z = %s", k, n1, d, w, z)
    
    del context.user_data['K'] 
    del context.user_data['eta1']
    del context.user_data['D0']
    del context.user_data['w']
    del context.user_data['z']
    
    value = k * ((d/w)**z) * (1 - n1) * (1 - n2*b)
    
    reply_keyboard = [['/start_calc_nitrogen_oxides'], 
                      ['/start_calc_sulfur_dioxide']]
    
    update.message.reply_text('The value is {:.4f}'.format(value),
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return ConversationHandler.END
    
    
def start_calc_sulfur_dioxide(update, context):

    update.message.reply_text(
        "Hi! Let`s calculate sulfure dioxide. "
        "Send /cancel to stop talking to me.\n\n"
        "Please enter value of Q."
        "It is must be a number")

    return Q


def get_q(update, context):
    reply_keyboard = [['Вугілля', 'Мазут']]
    logger.info("Q = %s", update.message.text)
    context.user_data['Q'] = update.message.text
    update.message.reply_text('Now enter тип палива',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return Type

def get_type(update, context):
    user = update.message.from_user
    t = str(update.message.text)
    logger.info("Type is %s", t)
    if t == 'Вугілля':
        reply_keyboard = [['Антрацибовий штиб АШ'], ['Пісне вугілля ТР'], ['Донецьке газове ГР'], 
                          ['Донецьке довгополумневе ДР'], ['Львівсько-волинське(ЛВ) ГР'], ['Олександрійське буре Б1Р']]
    elif t == 'Мазут':
        reply_keyboard = [['Високосірчаний 40'], ['Високосірчаний 100'], ['Високосірчаний 200'], 
                          ['Малосірчаний 40'], ['Малосірчаний 100']]
    else:
        update.message.reply_text('Не зрозумілий тип палива, завершення підрахунку')
        update.message.reply_text(t)
        return ConversationHandler.END
    update.message.reply_text('Введіть марку палива',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return S


def get_s(update, context):
    user = update.message.from_user
    key = update.message.text
    values_of_s = {
        'Антрацибовий штиб АШ' : 2.4,
        'Пісне вугілля ТР' : 3.3,
        'Донецьке газове ГР' : 4.4,
        'Донецьке довгополумневе ДР' : 4.3,
        'Львівсько-волинське(ЛВ) ГР' : 3.7,
        'Олександрійське буре Б1Р' : 5.9,
        'Високосірчаний 40' : 2.5,
        'Високосірчаний 100' : 2.7,
        'Високосірчаний 200' : 3.0,
        'Малосірчаний 40' : 0.4,
        'Малосірчаний 100' : 0.4
    }
    if key in values_of_s.keys():
        s = values_of_s[key]
    else:
        update.message.reply_text('Не зрозуміла марка палива, завершення підрахунку',
                                 reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    
    logger.info("%s enter S is : %s", user.first_name, s)
    context.user_data['S'] = s
    reply_keyboard = [['Факельне спалювання вугілля в котлах с рідким шлаковидаленням'], 
                      ['Факельне спалювання вугілля в котлах с твердим шлаковидаленням'], 
                      ['Факельне спалювання мазуту в котлах'], 
                      ['Спалювання в киплячому шарі']]
    
    update.message.reply_text('Виберіть технологію спалювання',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return N1


def get_n1(update, context):
    user = update.message.from_user
    key = update.message.text
    values_of_n1 = {
        'Факельне спалювання вугілля в котлах с рідким шлаковидаленням' : 0.05, 
        'Факельне спалювання вугілля в котлах с твердим шлаковидаленням' : 0.1, 
        'Факельне спалювання мазуту в котлах' : 0.02, 
        'Спалювання в киплячому шарі': 0.95
    }
    if key in values_of_n1.keys():
        n1 = values_of_n1[key]
    else:
        update.message.reply_text('Не зрозуміла технологія спалювання, завершення підрахунку',
                                 reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    logger.info("%s enter N1 : %s", user.first_name, n1)
    context.user_data['N1'] = n1
    reply_keyboard = [['Мокре очищення - у скрубері з використанням вапняку або доломіту'], 
                      ['Мокре очищення - процес Веллмана-Лорда'], 
                      ['Напівсухе очищення - розпилення крапель суспензії в реакторі'], 
                      ['Сухе очищення - інжекція сухого сорбенту'],
                      ['Напівсухе очищення - процес LIFAC'],
                      ['Напівсухе очищення - процес Lurgi CFB'],
                      ['Сухе очищення - абсорбція сухим вугіллям'],
                      ['Каталітичне очищення від оксидів сірки і азоту']]
    
    
    update.message.reply_text('Виберіть технологію десульфуризації димових газів',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return N2

def get_n2(update, context):
    user = update.message.from_user
    key = update.message.text
    values_of_n2 = {
        'Мокре очищення - у скрубері з використанням вапняку або доломіту' : (0.95, 0.99), 
        'Мокре очищення - процес Веллмана-Лорда' : (0.97, 0.99), 
        'Напівсухе очищення - розпилення крапель суспензії в реакторі' : (0.88, 0.98), 
        'Сухе очищення - інжекція сухого сорбенту' : (0.9, 0.99),
        'Напівсухе очищення - процес LIFAC' : (0.45, 0.98),
        'Напівсухе очищення - процес Lurgi CFB' : (0.8, 0.98),
        'Сухе очищення - абсорбція сухим вугіллям' : (0.9, 0.99),
        'Каталітичне очищення від оксидів сірки і азоту' : (0.95, 0.99)
    }
    if key in values_of_n2.keys():
        n2, b  = values_of_n2[key]
    else:
        update.message.reply_text('Не зрозуміла технологія десульфуризації, завершення підрахунку',
                                 reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    logger.info("%s enter N2 : %s and b : %s", user.first_name, n2, b)
    logger.info("%s enter data : Q = %s, S =  %s, N1 = %s, N2 = %s, b = %s", user.first_name, context.user_data['Q'], 
                context.user_data['S'], context.user_data['N1'], n2, b)
    q, s, n1 = float(context.user_data['Q']), float(context.user_data['S']), float(context.user_data['N1'])
    del context.user_data['Q']
    del context.user_data['S']
    del context.user_data['N1']
    value = (10**6/q)*(2*s/100)*(1-n1)*(1-n2*b)
    reply_keyboard = [['/start_calc_nitrogen_oxides'], 
                      ['/start_calc_sulfur_dioxide']]
    update.message.reply_text('The value is {:.4f}'.format(value),
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
   
    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    reply_keyboard = [['/start_calc_nitrogen_oxides'], 
                      ['/start_calc_sulfur_dioxide']]
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ConversationHandler.END


def start(update, context):
    reply_keyboard = [['/start_calc_nitrogen_oxides'], 
                      ['/start_calc_sulfur_dioxide']]
    update.message.reply_text('Hello, I`m Telegram bot, that will help you to calculate something.\n'
                              'Бот був створений для лабораторної роботи з екології студентами'
                              'групи ТІ-82 Гнатюком Євгенієм та Човган Іванною\n'
                              'use commends on keyboard to start calculating.',
                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True, persistence = DictPersistence())

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler_nitrogen_oxides = ConversationHandler(
        entry_points=[CommandHandler('start_calc_nitrogen_oxides', start_calc_nitrogen_oxides)],

        states={
            K: [MessageHandler(Filters.regex('^[-+]?\d*\.?\d*$'), get_k)],

            ETA1: [MessageHandler(~Filters.command, get_eta1)],
            
            D0: [MessageHandler(Filters.regex('^[-+]?\d*\.?\d*$'), get_d0)],
            
            W: [MessageHandler(~Filters.command, get_w)],
            
            Z: [MessageHandler(~Filters.command, get_z)],
            
            ETA2: [MessageHandler(~Filters.command, get_eta2)]
        },

        fallbacks=[CommandHandler('cancel', cancel)],
        name = "calc_nitrogen_oxides",
        persistent = True
    )
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start_calc_sulfur_dioxide', start_calc_sulfur_dioxide)],

        states={
            Q: [MessageHandler(Filters.regex('^[-+]?\d*\.?\d*$'), get_q)],

            Type: [MessageHandler(~Filters.command, get_type)],
            
            S: [MessageHandler(~Filters.command, get_s)],
            
            N1: [MessageHandler(~Filters.command, get_n1)],
            
            N2: [MessageHandler(~Filters.command, get_n2)]
        },

        fallbacks=[CommandHandler('cancel', cancel)],
        name = "calc_sulfur_dioxide",
        persistent = True
    )

    dp.add_handler(conv_handler)
    dp.add_handler(conv_handler_nitrogen_oxides)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('start_calc_sulfur_dioxide', start_calc_sulfur_dioxide))
    dp.add_handler(CommandHandler('start_calc_nitrogen_oxides', start_calc_nitrogen_oxides))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://telegram-calc-ecology-bot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


# In[ ]:




