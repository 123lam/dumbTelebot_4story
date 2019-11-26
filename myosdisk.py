import os

PROG_NAME = 'pyinstastories.py -d'
URL_STORIES = '.\\stories\\'

def change_names_and_get_list(name):
	starting_dir = os.getcwd()
	os.chdir(URL_STORIES+name)
	my_list = os.listdir('.')
	print(os.getcwd())
	print()
	iterator = 0
	for i in my_list:
		postfix = (i.split('.')[1])
		iterator += 1
		os.rename(i,(str(iterator)+'.'+postfix))
	my_list = os.listdir('.')	
	os.chdir(starting_dir)
	
	return(my_list)
	
def remove_files():
	starting_dir = os.getcwd()
	os.chdir(URL_STORIES)
	my_list = os.listdir('.')
	for i in my_list:
		os.system("rd /s /q "+i)
	os.chdir(starting_dir)

def start_the_script(name):
	method = 'python '+ PROG_NAME+ ' '  + name
	print(method)
	print()
	print(URL_STORIES + name)
	 
	if os.path.exists(URL_STORIES + name):
		pass
	else:	
		os.mkdir(URL_STORIES + name)
	os.system(method)
	return change_names_and_get_list(name)

	
if __name__ == '__main__':
	#print(start_the_script('yenishark'))
	remove_files()

	