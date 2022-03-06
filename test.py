from SimpleQIWI import *

token_qiwi = 'f9b7820b16fd40389cf229a65cca4a46' 
phone = '+380632347217'


api = QApi(token=token_qiwi, phone=phone)

print(api.balance)