from faker import Faker

fake = Faker(locale='uk-UA')

#print(*dir(fake), sep='\n')

word_list_sport = [
    'бадмінтон', 'баскетбол', 'бейсбол',
    'бокс', 'боротьба вільна', 'міні футбол',
    'важка атлетика', 'волейбол', 'гімнастика спортивна',
    'теніс', 'легка атлетика', 'теніс настільний', 'футбол']

word_list_movie = [
    'комедія', 'фантастика', 'жахи',
    'бойовик', 'мелодрами', 'містика',
    'драма', 'трилез']

word_list_gender = ['чоловіча', 'жіноча']

fake.first_name()
fake.last_name()
fake.random_int()
fake.boolean()
fake.sentence(1, ext_word_list=word_list_sport)
fake.sentence(1, ext_word_list=word_list_movie)
fake.sentence(1, ext_word_list=word_list_gender)
fake.random_int()