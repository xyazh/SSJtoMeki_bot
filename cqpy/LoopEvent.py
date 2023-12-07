from urllib import request
from html.parser import HTMLParser
import threading
import time
import logging
import json


class AnimeHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.__parsedata = ''  # 设置一个空的标志位
        self.info = []

    def handle_starttag(self, tag, attrs):
        if ("class", "ptxt") in attrs:
            self.__parsedata = "n"

    def handle_endtag(self, tag):
        self.__parsedata = ''  # 在HTML 标签结束时，把标志位清空

    def handle_data(self, data):
        if self.__parsedata == "n":
            data = data.replace("\r", "")
            data = data.replace("\n", "")
            flag = False
            for i in data:
                if i != " ":
                    flag = True
                    break
            if flag:
                self.info.append(data)


class LoopEvent:
    today_anime_news = []
    today_galgame_news = []

    def start():
        LoopEvent.getAnimeNews()
        LoopEvent.getGalNews()

    def getAnimeNews():
        def __get():
            while True:
                try:
                    with request.urlopen('https://acg.gamersky.com/news/') as f:
                        data = f.read()
                        parser = AnimeHTMLParser()
                        parser.feed(str(data, encoding="utf8"))
                        LoopEvent.today_anime_news = parser.info
                        # print(LoopEvent.today_anime_news)
                except BaseException as e:
                    logging.exception(e)
                time.sleep(3600)
        threading.Thread(target=__get).start()

    def getGalNews():
        def __get():
            while True:
                try:
                    with request.urlopen('https://www.ymgal.games/co/topic/list?type=NEWS&page=1') as f:
                        data = str(f.read(), encoding="utf8")
                        data_dict = json.loads(data)
                        if "data" in data_dict:
                            if type(data_dict["data"]) == list:
                                for i in data_dict["data"]:
                                    if "title" in i:
                                        LoopEvent.today_galgame_news.append(
                                            i["title"])
                                # print(LoopEvent.today_galgame_news)
                except BaseException as e:
                    logging.exception(e)
                time.sleep(3600)
        threading.Thread(target=__get).start()


if __name__ == "__main__":
    LoopEvent.start()
