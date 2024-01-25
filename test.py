# import subprocess

# subprocess.run(["data\\commands\\ahk\\Compiler\\Ahk2exe.exe", 
#                 "/in", 
#                 "data\\commands\\ahk\\mute_volume.ahk",
#                 "/out",
#                 "data\\commands\\ahk\\mute_volume.exe"], shell=True)

# subprocess.run(["data\\commands\\ahk\\mute_volume.exe", '0'], shell=True)


# import schedule
# import time
# import os

# # Функция для выполнения задачи
# def execute_task(task=''):
#     print(f'Задача выполнена {task}')

# # Планирование задачи
    
# def schedule_task(qury):
#     schedule.every(5).seconds.do(execute_task, task=query)

# # Запуск задачи на определенную дату

# # Бесконечный цикл для проверки и выполнения запланированных задач
# while True:
#     query = input("напишите задачу: ")
#     if query != "":
#         schedule_task(query)
#     all_jobs = schedule.get_jobs()
#     print(all_jobs)
#     schedule.run_pending()
#     time.sleep(1)


# import func as f
# import tracemalloc
# tracemalloc.start()

# query = ["установи громкость на", "приветики дружбан", "что делаешь", "сколько времени в данный момент на часах", "почему дельфины синие", "вруби классную музыку", "сколько времени в данный момент на часах"]

# for i in query:
#     print(f.determ_query(i.split()))

# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage is {current / (1024*1024)}MB; Peak was {peak / (1024*1024)}MB")

# tracemalloc.stop()
