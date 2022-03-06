from SimpleQIWI import *
token_qiwi = 'f9b7820b16fd40389cf229a65cca4a46' 
phone = '+380632347217'

api = QApi(token=token_qiwi, phone=phone)
dic_ = api.balance
print(dic_)

def Qiwi_check():
    date = ''
    while True:
        api = QApi(token=token_qiwi, phone=phone)
        dic_ = api.payments
        #print(api)
        for i in dic_.get('data'):
            comment_qiwi = (i.get('comment'))
            account_qiwi = (i.get('account'))
            amount_qiwi = int(i.get('sum').get('amount'))
            date_qiwi = (i.get('date'))

            print(i, '\n\n')
            # try:
            #     if date_qiwi != date:
            #         user_ = Users.get(Users.USERID == comment_qiwi)
            #         user_.Balance += amount_qiwi
            #         user_.save()
            #         bot.send_message(comment_qiwi, 'Поступил платеж! '+str(amount_qiwi)+' RUB')
            #     date = date_qiwi
            # except:
            #     pass

        time.sleep(30)


#Qiwi_check()