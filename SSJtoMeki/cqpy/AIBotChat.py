import requests
import json
import time

API_KEY = "ffBDb9gnLxzdPWPzGUUxskCN"
SECRET_KEY = "Ov0jLWtTKxvs626ymvKsqH1VbnFIXlLM"


class AIBotChat:
    ACCESS_TOKEN = None
    ACCESS_TOKEN_DATETIME = 0

    aip = 0

    aips = [
        "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=",
        "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=",
        "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/bloomz_7b1?access_token="
    ]

    DIS_CHAT = [
        {
            "role": "user",
            "content": "在接下来的对话中，你需要模仿一个叫MEKI的女孩，当别人问你是谁时你应该告诉他你是MEKI"
        },
        {
            "role": "assistant",
            "content": "好的，我将扮演MEKI跟你对话。在接下来的聊天过程中，我将代入这个角色跟你聊天。"
        }
    ]
    GROUPS_CHAT: dict[int, list] = {}

    def setAip(self,n):
        n = n if 0 <= n <= 2 else 0
        AIBotChat.aip = n

    def getAccessToken(self):
        if time.time() - AIBotChat.ACCESS_TOKEN_DATETIME >= 30 * 24 * 60 * 60:
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {"grant_type": "client_credentials",
                      "client_id": API_KEY, "client_secret": SECRET_KEY}
            AIBotChat.ACCESS_TOKEN = str(requests.post(
                url, params=params).json().get("access_token"))
            AIBotChat.ACCESS_TOKEN_DATETIME = time.time()
        if AIBotChat.ACCESS_TOKEN is None:
            raise ValueError("获取ACCESS_TOKEN失败")
        return AIBotChat.ACCESS_TOKEN

    def getUrl(self):
        return AIBotChat.aips[AIBotChat.aip] + self.getAccessToken()

    def genChat(self, group_id: str):
        url = self.getUrl()
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({"messages":self.getData(group_id)})
        response = requests.request("POST", url, headers=headers, data=payload)
        r: dict = json.loads(response.text)
        msg = r.get("result")
        if msg == None:
            raise ValueError("获取回复失败")
        self.getData(group_id).append(
            {
                "role": "assistant",
                "content": msg
            },
        )
        return msg

    def getData(self, group_id) -> list:
        if group_id not in AIBotChat.GROUPS_CHAT:
            AIBotChat.GROUPS_CHAT[group_id] = AIBotChat.DIS_CHAT.copy()
        if len(AIBotChat.GROUPS_CHAT[group_id]) >= 20:
            AIBotChat.GROUPS_CHAT[group_id] = AIBotChat.DIS_CHAT.copy(
            ) + AIBotChat.GROUPS_CHAT[group_id][-10:]
        return AIBotChat.GROUPS_CHAT[group_id]

    def send(self, group_id, msg)->str:
        self.getData(group_id).append(
            {
                "role": "user",
                "content": msg
            },
        )
        return self.genChat(group_id)

if __name__ == "__main__":
    ai = AIBotChat()
    print(ai.send(123,"好好好"))
    print(ai.send(123,"草"))
