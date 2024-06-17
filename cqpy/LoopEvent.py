from urllib import request
from html.parser import HTMLParser
if __name__ == "__main__":
    from xyazhServer import ConsoleMessage
else:
    from .xyazhServer import ConsoleMessage
import threading
import time
import logging
import json
DO_LOOP: list[threading.Thread] = []

class AnimeHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.__parsedata = False  # 设置一个空的标志位
        self.info = []

    def handle_starttag(self, tag, attrs):
        if ("class", "ptxt") in attrs:
            self.__parsedata = True

    def handle_endtag(self, tag):
        self.__parsedata = False  # 在HTML 标签结束时，把标志位还原

    def handle_data(self, data):
        if self.__parsedata:
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

    @staticmethod
    def doLoop(t):
        def loop(fuc, *args, **kw):
            def loopFuc():
                while True:
                    fuc(*args, **kw)
                    time.sleep(t)
            DO_LOOP.append(threading.Thread(target=loopFuc))
            return fuc
        return loop

    @staticmethod
    def start():
        for t in DO_LOOP:
            t.start()

    @staticmethod
    @doLoop(60)
    def getAnimeNews():
        try:
            data = None
            with request.urlopen('https://acg.gamersky.com/news/') as f:
                data = f.read()
            if data is None:
                return
            parser = AnimeHTMLParser()
            parser.feed(str(data, encoding="utf8"))
            LoopEvent.today_anime_news = parser.info
            ConsoleMessage.printDebug(LoopEvent.today_anime_news)
        except BaseException as e:
            logging.exception(e)

    @staticmethod
    @doLoop(60)
    def getGalNews():
        try:
            data = None
            with request.urlopen('https://www.ymgal.games/co/topic/list?type=NEWS&page=1') as f:
                data = str(f.read(), encoding="utf8")
            if data is None:
                return
            data_dict = json.loads(data)
            if "data" not in data_dict:
                return
            if isinstance(data_dict["data"], list):
                LoopEvent.today_galgame_news.clear()
                for i in data_dict["data"]:
                    if "title" not in i:
                        continue
                    LoopEvent.today_galgame_news.append(i["title"])
                ConsoleMessage.printDebug(LoopEvent.today_galgame_news)
        except BaseException as e:
            logging.exception(e)


if __name__ == "__main__":
    LoopEvent.start()
