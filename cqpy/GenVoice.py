import socket,json,re

class GenVoice:
    @staticmethod
    def gen(text:str,l:str)->str:
        d = {"fn_index":0,"data":[text,"Character_manami_1",l,1],"session_hash":"hpdznkf8iui"}
        body_data = json.dumps(d,ensure_ascii=False).encode("utf8")
        body_len = len(body_data)
        head_data = b'POST /run/predict/ HTTP/1.1\r\nHost: 127.0.0.1:7860\r\nContent-Length: %d\r\nsec-ch-ua: "Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"\r\nsec-ch-ua-platform: "Windows"\r\nsec-ch-ua-mobile: ?0\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58\r\nContent-Type: application/json\r\nAccept: */*\r\nOrigin: http://127.0.0.1:7860\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: cors\r\nSec-Fetch-Dest: empty\r\nReferer: http://127.0.0.1:7860/\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\r\n\r\n'%(body_len)
        sockets = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sockets.connect(("127.0.0.1",7860))
        sockets.sendall(head_data)
        sockets.sendall(body_data)
        r_head = sockets.recv(10240)
        r_data = json.loads(sockets.recv(10240))
        sockets.close()
        file_name = ""
        if r_data["data"][0] == "Success":
            file_name = r_data["data"][1]["name"]
        return file_name

    @staticmethod
    def genVioce(text:str)->str:
        l = "English"
        if re.search(r"[ぁ-ゔ]+|[ァ-ヴー]+|[々〆〤]",text):
            l="日本語"
        elif re.search(r"[一-龠]+",text):
            l="简体中文"
        return GenVoice.gen(text,l)
    