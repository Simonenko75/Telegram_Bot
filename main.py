import speech_recognition


sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

commands_dict = {
    'commands': {
        'greeting': ['привіт', 'вітаю', 'при'],
        'create_task': ['задача', 'додати завдання', 'запис']
    }
}

#bot1 = telebot.TeleBot('5400393089:AAHL2w3uRKSYN5jQvQpCuTSJiVALkfDbsYI')

# def telegram_bot(token):
#     bot = telebot.TeleBot(token)
#
#     @bot.message_handler(commands=['start'])
#     def start_massage(message):
#         bot.send_message(message.chat.id, "Привіт тобі")
#
#
#     bot.polling()


def listen_command():
    """Func will return the recognized command"""

    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='uk-UA').lower()

        return query
    except speech_recognition.UnknownValueError:
        return 'Я не зрозумів, що ти кажешь?'

def greeting():
    """"Greeting func"""

    return 'Привіт друже!'

def create_task():
    """Create a doing task"""

    print('Що потрібно додати до списку завдань?')

    query = listen_command()

    with open('doing-list.txt', 'a') as file:
        file.write(f'{query}\n')

    return f'Завдання "{query}" успішно додано до файлу doing-list!'

def main():
    query = listen_command()

    for k, v in commands_dict['commands'].items():
        if query in v:
            print(globals()[k]())

if __name__ == '__main__':
    main()
    #telegram_bot(token)
