import requests
import telebot
telegram_bot_token = ""
with open("bot_token.txt","r") as f:
        telegram_bot_token = f.read()#Чтение telegram bot токена из файла
if telegram_bot_token != "":
        def extract_arg(arg):
            return arg.split()[1:]

        bot = telebot.TeleBot(telegram_bot_token, parse_mode=None)
        @bot.message_handler(commands=["помощь"])
        def send_welcome(message):
                bot.reply_to(message, """📌Список доступных команд:
/просмотреть_страницу n - просмотреть страницу с номером n >= 0(ps: последняя страница на текущий момент имеет номер = 42)
/помощь - получение списка доступных команд
                """)
                        
        @bot.message_handler(commands=["просмотреть_страницу"])
        def lol_answer(message):
                try:
                        page_number = int(extract_arg(message.text)[0])
                        request_url = "https://rickandmortyapi.com/api/character/?page=" + str(page_number)
                        response = requests.get(request_url)
                        JSON_response = response.json()
                        length = len(JSON_response["results"])
                        answer = ""
                        for i in range(0, length):
                                part_of_answer = "📌\n"
                                part_of_answer += "📋 *Идентификатор*: `" + str(JSON_response["results"][i]["id"]) + "`\n"
                                part_of_answer += "💭 *Имя*: `" + str(JSON_response["results"][i]["name"]) + "`\n"
                                part_of_answer += "🔮 *Статус*: `" + str(JSON_response["results"][i]["status"]) + "`\n"
                                part_of_answer += "🔍 *Пол*: `" + str(JSON_response["results"][i]["gender"]) + "`\n"
                                part_of_answer += "🧬 *Происхождение*: `" + str(JSON_response["results"][i]["origin"]["name"]) + "`\n"
                                if (i != length-1):
                                        part_of_answer += "\n"
                                answer += part_of_answer
                        bot.reply_to(message, answer, parse_mode="Markdown")
                except:
                        bot.reply_to(message, "Ошибка ввода номера страницы", parse_mode="Markdown")
                        
        @bot.message_handler(func=lambda message: True)
        def echo_all(message):
                #bot.reply_to(message, message.text)
                bot.reply_to(message, "📌Команда не найдена, проверьте список команд, используя команду:\n`/помощь`", parse_mode="Markdown")
        bot.infinity_polling()
