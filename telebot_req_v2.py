import parser
import requests
import json
from yobit import get_btc
from time import sleep
import telebot
import myosdisk
import os

MY_TOKEN = ""
MY_URL = "https://api.telegram.org/bot{}/".format(MY_TOKEN)

global bot 
bot = telebot.TeleBot(MY_TOKEN)


global last_update_id
last_update_id = 0


 
def get_updates():
	
	method = 'getUpdates'
	url = MY_URL + method
	r = requests.get(url) #ответ от сервера (ссылка)
	return r.json() # возврат ответа в формате json()

def get_msg():
	#Отвечать на новые сообщения 
	# Получаем update_id каждого обновления записываем в переменную а затем сравниваем -
	# изменился ли он или нет (Update_id последнего элемента в списке result

	data = get_updates()
	
     
	current_update_id = data['result'][-1]['update_id']
	
	global last_update_id
	if last_update_id != current_update_id:
		last_update_id = current_update_id
		
		chat_id = data['result'][-1]['message']['chat']['id'] #Составной словарь -> можно посмотреть файл json. это выборка по ключам
		text_msg = data['result'][-1]['message']['text']
		
		message = {'chat_id' : chat_id, 
					'text' : text_msg} #Пример другого вида комментария + словарь возвращяющий чат ай-ди и сообщение  '''
		return message
	return None

def send_msg(chat_id, text = 'W8 plz...'):
	method = 'sendMessage?chat_id={}&text={}'.format(chat_id,text)
	url = MY_URL + method  
	requests.get(url)

	
def send_photo(chat_id,url_file):
	bot.send_photo(chat_id,url_file)
	
def send_video(chat_id,url_file):
	bot.send_video(chat_id,url_file)


	
def main():
	#d = get_updates() 
	
	#with open('updates.json', 'w', encoding ="utf-8" ) as file: #добовляем encoding = "utf-8", что бы мы могли записывать в файл дамб с русскмими буквами)
	#	json.dump(d, file, indent = 2, ensure_ascii = False)
	
	
	
	
	while True:
		answer = get_msg()
		if answer != None:
			text = answer['text']
			if text == '/btc':
				send_msg(answer['chat_id'], get_btc())
			elif text[:2] == '/d':
				inst_id = text[3:] 
				#забираем вторую часть после /d <name> для индентификации пользователя
				#TODO если коней файла кончается на mpg - > sendVideo , если jpg -> sendPhoto
				tmp_a = myosdisk.start_the_script(inst_id)
				for i in tmp_a:
					if i.split('.')[1] == 'mp4':
						send_video(answer['chat_id'],open((os.getcwd()+"\\stories\\"+ inst_id +"\\" + i), 'rb'))
					elif i.split('.')[1] == 'jpg':
						send_photo(answer['chat_id'],open((os.getcwd()+"\\stories\\"+ inst_id +"\\" + i), 'rb'))
				
				
				send_msg(answer['chat_id'], text[3:] + "<- Grab Done, now delete temp file...")
				myosdisk.remove_files()
			elif text == '/start':
				send_msg(answer['chat_id'], 'I can send you instagram stories. \n Just type /d <name> \n Where <name> = Insagram name \n' +
				'For example: /d iamcardib \n It can take like 10 seconds before i can send you some files ')
		else:
			continue
		sleep(3)


		
if __name__ == '__main__':
	main()
	
