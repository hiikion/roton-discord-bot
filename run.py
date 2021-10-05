from multiprocessing import Process
from psutil import cpu_percent, virtual_memory
import src.main
from time import sleep
import os
import src.config as c


def statistics_graph():
    while True:
        os.system('cls')
        print('cpu load: ' + str(cpu_percent()) + '%\nram usage: ' + str(virtual_memory()[2]) + '%')
        sleep(10)

if __name__ == '__main__': 
    if bool(c.config['stats_graph']) == True:
        statistics_process = Process(target=statistics_graph)
        statistics_process.start()
    else:
        pass
    src.main.run()