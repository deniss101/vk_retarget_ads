import requests
import time
from os import environ
from progress.bar import IncrementalBar

print('Let`s work' '\n')
vk_token = environ.get('VK_API')
HOST = "https://api.vk.com/method/"


def work():
    target = (input("Введите ID или название сообщества: "))
    start_time = time.perf_counter()
    offset = 0
    people_in_target = requests.get(HOST + 'groups.getMembers', params={'group_id': target, 'access_token': vk_token, 'v': 5.131})
    people_1000 = people_in_target.json()['response']['count']
    print("Количество подписчиков:", people_1000)

    result_file = open("ids.txt", "w")
    bar = IncrementalBar('Выгружаю:', max=people_1000 // 1000 + 1, suffix='%(percent)d%%')
    for i in range(people_1000 // 1000 + 1):
        time.sleep(0.3)
        answer = requests.get(HOST + 'groups.getMembers', params={'group_id': target, 'offset': offset, 'access_token': vk_token, 'v': 5.131})
        to_write = [*answer.json()['response']['items']]
        offset += 1000
        for item in to_write:
            print(item, file=result_file, sep='\n')
        bar.next()
    bar.finish()
    result_file.close()
    finish_time = time.perf_counter()
    print("Успех, ID выгружены.", "Выполнено за", round(finish_time-start_time, 3), "сек." + "\n")

    next = str(input("Получить список из другой группы? + / - " + "\n"))
    if next == "+":
        work()
    else:
        exit()


def test():
    print('tested')


work()
