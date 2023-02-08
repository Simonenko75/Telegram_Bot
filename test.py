import sqlite3

try:
    conn = sqlite3.connect("mydb.db")
    cursor = conn.cursor()

    #Створив користувача з user_id = 7
    cursor.execute("INSERT OR IGNORE INTO `users` (`user_id`) VALUES (?)", (7,))

    #Зчитування усіх користувачів
    users = cursor.execute("SELECT `favorite_sport`, `favorite_movie_genre`, `gender`, `relationship` FROM `interview`")

    sport = []
    movie = []
    gender = []
    relationship = []

    for s, m, g, r in tuple(users):
        sport.append(s)
        movie.append(m)
        gender.append(g)
        relationship.append(r)

    #print(*sport, sep='\n')
    #print(*movie, sep='\n')
    #print(*gender, sep='\n')
    #print(*relationship, sep='\n')

    male = gender.count('Чоловіча.')
    female = gender.count('Жіноча.')

    print(male, female)

    word_list_sport = [
        'Бадмінтон.', 'Баскетбол.', 'Бейсбол.',
        'Бокс.', 'Боротьба Вільна.', 'Міні Футбол.',
        'Важка Атлетика.', 'Волейбол.', 'Гімнастика Спортивна.',
        'Теніс.', 'Легка Атлетика.', 'Теніс Настільний.', 'Футбол.']

    sport_male = []
    sport_female = []
    sport_1 = []
    sport_2 = []

    for i in range(len(sport)):
        if gender[i] == 'Чоловіча.':
            sport_1.append(sport[i])
        elif gender[i] == 'Жіноча.':
            sport_2.append(sport[i])

    for elem in word_list_sport:
        sport_male.append(sport_1.count(elem))
        sport_female.append(sport_2.count(elem))

    #Підтвердження змін
    conn.commit()

except sqlite3.Error as error:
    print("Error", error)

finally:
    if(conn):
        conn.close()