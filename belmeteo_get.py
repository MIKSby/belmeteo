# -*- coding: utf-8 -*-
from datetime import *
from time import sleep
from tqdm import tqdm
import requests
import threading


class Belmeteo:
    def __init__(self):
        self.today = date.today()
        self.old = date(2010, 6, 1)
        self.pre_url = 'http://belmeteo.net/archive/'
        self.delta = [self.old]

        while self.old < self.today + timedelta(days=-1):
            self.old = self.old + timedelta(days=1)
            if self.old.year in [2010, 2011, 2014, 2015, 2016, 2017, 2018]:
                self.delta.append(self.old)

    def file_save(self, url, file):
        while True:
            try:
                p = requests.get(f'{self.pre_url}{url}.txt')
                with open(f'{file}.txt', 'wb') as file:
                    file.write(p.content)
                    return
            except requests.exceptions.ConnectionError:
                print('Connection Error! Wait 5 sec and repeat')
                sleep(5)

    def get(self, d):
        if d.year == 2018:
            self.file_save(url=f'{d.isoformat()}', file=f'{d.isoformat()}')
        else:
            self.file_save(url=f'{d.year}/{d.isoformat()}', file=f'{d.isoformat()}')

    def run(self):
        for d in tqdm(self.delta):
            thread = threading.Thread(target=self.get, args=(d, ))
            thread.start()
            sleep(.01)


if __name__ == '__main__':
    Belmeteo().run()
