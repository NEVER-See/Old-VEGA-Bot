import os
import time

os.system('bot-systems.py')
print("[ ЗАПУСК ]  Файл bot-systems.py успешно запущен, ожидается запуск файла bot-commands.py.\n")
time.sleep(10)
print("[ ЗАПУСК ]  Время ожидания прошло...\n")
os.system('bot-commands.py')
print("[ ЗАПУСК ]  Файл bot-commands.py успешно запущен.\n")
