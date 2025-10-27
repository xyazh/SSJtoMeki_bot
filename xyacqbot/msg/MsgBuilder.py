class MsgBuilder:
    def __init__(self):
        self.msg: list[dict] = []

    def update(self, data: dict):
        self.msg.append(data)

    def updateText(self, text: str):
        data = {
            "type": "text",
            "data":
                {
                    "text": text
                }
        }
        self.update(data)

    def updateImage(self, file: str):
        """
        file = file://X:/x.jpg 
        file = http://xxx.com/xxx.png 
        file = base64://xxxxxxxx 
        """
        data = {
            "type": "image",
            "data": {
                "file": file
            }
        }
        self.update(data)

    def updateAt(self, qq: int | str):
        """all 表示@全体"""
        data = {
            "type": "at",
            "data": {
                "qq": str(qq)
            }
        }
        self.update(data)

    def updateReply(self, reply_id: int):
        data = {
            "type": "reply",
            "data": {
                "id": reply_id
            }
        }
        self.update(data)

    def updateRecord(self, file: str):
        """
        file = file://X:/x.mp3
        file = http://xxx.com/xxx.wav
        file = base64://xxxxxxxx 
        """
        data = {
            "type": "record",
            "data": {
                "file": file
            }
        }
        self.update(data)

    def updateVideo(self, file: str):
        """
        file = file://X:/x.mp4
        file = http://xxx.com/xxx.mp4
        file = base64://xxxxxxxx 
        """
        data = {
            "type": "video",
            "data": {
                "file": file
            }
        }
        self.update(data)
