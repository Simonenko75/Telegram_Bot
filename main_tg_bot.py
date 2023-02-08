
import speech_recognition
from auth_data import tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import BotDB
from faker import Faker
import matplotlib.pyplot as plt


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

BotDB = BotDB('mydb.db')

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

fake = Faker(locale='uk-UA')

commands_dict = {
    'commands': {
        'greeting': ['привіт', 'вітаю', 'добрий день', 'мої привітання', 'мої вітання'],
        'analysis': ['аналіз', 'аналіз даних', 'дані', 'проаналізувати дані', 'виконати аналіз даних', 'виконати аналіз'],
        'different_word': ['llllllllll'],
        'interview': ['опитування', 'анкета', 'запитання', 'пройти опитування', 'анкетування'],
        'ending': ['кінець роботи', 'стоп', 'завершити роботу']
    }
}

word_list_sport = [
        'Бадмінтон.', 'Баскетбол.', 'Бейсбол.',
        'Бокс.', 'Боротьба Вільна.', 'Міні Футбол.',
        'Важка Атлетика.', 'Волейбол.', 'Гімнастика Спортивна.',
        'Теніс.', 'Легка Атлетика.', 'Теніс Настільний.', 'Футбол.']

word_list_movie = [
    'Комедія.', 'Фантастика.', 'Жахи.',
    'Бойовик.', 'Мелодрами.', 'Містика.',
    'Драма.', 'Трилез.']

word_list_gender = ['чоловіча', 'жіноча']

word_list_relationship = [0, 1]

def listen_command():
    """Func will return the recognized command"""

    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='uk-UA').lower()
        return query
    except speech_recognition.UnknownValueError:
        return 'Я не зрозумів, що Ви кажете.'

async def greeting(message):
    """"Greeting func"""

    return 'Вітаю Вас. Що потрібно виконати?'

async def analysis(message):
    """"Analysis func"""

    sport = []
    movie = []
    gender = []
    relationship = []

    sport, movie, gender, relationship = BotDB.date_(sport, movie, gender, relationship)
    BotDB.conn.close()

    sport_male, sport_female = date_change(sport, gender, word_list_sport)
    # print(f"sport_male {sport_male}")
    # print(f"sport_female {sport_female}")

    fig1 = plt.figure(figsize=(8, 7))
    ax1 = fig1.add_subplot()
    ax1.set_title("Ранжування частотності улюбленого виду спорту\nза даними чоловіків")
    ax1.grid()
    ax1.pie(sport_male, labels=word_list_sport, autopct='%.2f')

    fig2 = plt.figure(figsize=(8, 7))
    ax2 = fig2.add_subplot()
    ax2.set_title("Ранжування частотності улюбленого виду спорту\nза даними жінок")
    ax2.grid()
    ax2.pie(sport_female, labels=word_list_sport, autopct='%.2f')
    # plt.plot(ax1)

    movie_male, movie_female = date_change(movie, gender, word_list_movie)
    # print(f"movie_male {movie_male}")
    # print(f"movie_female {movie_female}")

    fig3 = plt.figure(figsize=(8, 7))
    ax3 = fig3.add_subplot()
    ax3.set_title("Ранжування частотності улюбленого жанру кіно\nза даними чоловіків")
    ax3.grid()
    ax3.pie(movie_male, labels=word_list_movie, autopct='%.2f')

    fig4 = plt.figure(figsize=(8, 7))
    ax4 = fig4.add_subplot()
    ax4.set_title("Ранжування частотності улюбленого жанру кіно\nза даними жінок")
    ax4.grid()
    ax4.pie(movie_female, labels=word_list_movie, autopct='%.2f')
    #plt.show()

    relationship_male, relationship_female = date_change(relationship, gender, word_list_relationship)
    # print(f"relationship_male {relationship_male}")
    # print(f"relationship_female {relationship_female}")

    fig5 = plt.figure(figsize=(8, 7))
    ax5 = fig5.add_subplot()
    ax5.set_title('Графік розподілення чоловікі та жінок\nза ознакою перебування у відносинах')
    ax5.grid()

    x1 = ['Чоловіки не у відносинах', 'Чоловіки у відносинах']
    x2 = ['Жінки не у відносинах', 'Жінки у відносинах']

    ax5.barh(x1, relationship_male)
    ax5.barh(x2, relationship_female)
    plt.show()

    return "Аналіз завершено."

def date_change(date_chose, date_gender, word_list):
    """"Date change func"""

    chose_1 = []
    chose_2 = []
    chose_male = []
    chose_female = []

    for i in range(len(date_chose)):
        if date_gender[i] == 'Чоловіча.':
            chose_1.append(date_chose[i])
        elif date_gender[i] == 'Жіноча.':
            chose_2.append(date_chose[i])

    for elem in word_list:
        chose_male.append(chose_1.count(elem))
        chose_female.append(chose_2.count(elem))

    return chose_male, chose_female

async def different_word(message):
    """Different word"""

    return "Я не зрозумів, що Ви маєте на увазі."

async def interview(message):
    """interview func"""

    await bot.send_message(message.from_user.id, "Ваше ім'я?")
    first_name = listen_command()
    await bot.send_message(message.from_user.id, f"Ваше ім'я {first_name}")

    await bot.send_message(message.from_user.id, "Ваша фамілія?")
    last_name = listen_command()
    await bot.send_message(message.from_user.id, f"Ваше фамілія {last_name}")

    await bot.send_message(message.from_user.id, "Улюблений вид спорту?")
    favorite_sport = listen_command()
    await bot.send_message(message.from_user.id, f"Улюблений вид спорту: {favorite_sport}")

    await bot.send_message(message.from_user.id, "Улюблений жанр?")
    favorite_movie_genre = listen_command()
    await bot.send_message(message.from_user.id, f"Улюблений жанр: {favorite_movie_genre}")

    await bot.send_message(message.from_user.id, "Ваша стать?")
    gender = listen_command()
    await bot.send_message(message.from_user.id, f"Ваша стать: {gender}")

    await bot.send_message(message.from_user.id, "Чи перебуваєте Ви у відносинах?")
    relationship = listen_command()
    await bot.send_message(message.from_user.id, f"Ваше відповідь {relationship}")

    BotDB.add_date_interview(message.from_user.id, first_name, last_name, favorite_sport, favorite_movie_genre, gender, relationship)

    return "Опитування завершено, дані успішно занесені до бази даних."

async def fakes_interview(message):
    """"Faker func"""

    for i in range(9, 300):
        BotDB.add_user(i)

    for i in range(300):
        BotDB.add_date_interview(
            i,
            fake.first_name(),
            fake.last_name(),
            fake.sentence(1, ext_word_list=word_list_sport),
            fake.sentence(1, ext_word_list=word_list_movie),
            fake.sentence(1, ext_word_list=word_list_gender),
            fake.boolean())
    return "Додавання даних завершено."

async def ending(message):
    """Ending work func"""

    return "На цьому моя робота завершена.\n" \
           "Якщо буду потрібен просто введіть команду /start\n" \
           "Успіхів Вам!!!"

def main(message):
    """Ending work func"""

    query = listen_command()

    for k, v in commands_dict['commands'].items():
        if query in v:
            return globals()[k](message)
    return different_word(message)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Я дуже уважно Вас слухаю. Що потрібно виконати?")

    mess = ''

    while mess != 'На цьому моя робота завершена.\nЯкщо буду потрібен просто введіть команду /start\nУспіхів Вам!!!':
        mess = await main(message)
        await bot.send_message(message.from_user.id, mess)

if __name__ == '__main__':
    executor.start_polling(dp)