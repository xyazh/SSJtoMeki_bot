import requests
import json

class LLMAPI(object):
    def __init__(self, api_key: str, base_url: str, system_prompt: str, max_tokens: int, temperature: float, model: str, max_memory_in_turns: int):
        self.api_key = api_key
        self.base_url = base_url
        self.system_prompt = system_prompt
        self.messages = []
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.model = model
        self.max_memory_in_turns = max_memory_in_turns
        
    def get_response(self, messages):
        raise NotImplementedError

    def extract_response(self, response, debug_mode=False) -> str:
        raise NotImplementedError
    
    def chat(self, user_message, one_turn = False, debug_mode=False) -> str:
        raise NotImplementedError


class DeepseekAPI(LLMAPI):
    def __init__(self, api_key: str,
                 base_url: str = "https://api.deepseek.com/chat/completions",
                 system_prompt: str="You are a helpful assistant.",
                 max_tokens: int = 4096,
                 temperature: float = 1,
                 model: str = "deepseek-chat",
                 max_memory_in_turns: int = 5):
        super().__init__(api_key, base_url, system_prompt, max_tokens, temperature, model, max_memory_in_turns)
        self.system_prompt = {"role": "system", "content": system_prompt}

        self.model_list = ["deepseek-chat", "deepseek-coder"]

        self.headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + self.api_key
        }

        self.error_codes = {
            400: "格式错误",
            401: "认证失败",
            402: "余额不足",
            422: "参数错误",
            429: "请求速率达到上限",
            500: "服务器故障",
            503: "服务器繁忙",
        }

    def get_response(self, messages):
        payload = json.dumps({
        "messages": messages,
        "model": self.model,
        "frequency_penalty": 0,
        "max_tokens": self.max_tokens,
        "presence_penalty": 0,
        "stop": None,
        "stream": False,
        "temperature": self.temperature,
        "top_p": 1,
        "logprobs": False,
        "top_logprobs": None
        })

        response = requests.post(self.base_url, headers=self.headers, data=payload, timeout=100)

        return response
    
    def extract_response(self, response, debug_mode=False) -> str:
        if debug_mode:
            extract_str = "debug mode: \n"
            extract_str += "response content: " + response["choices"][0]["message"]["content"] + "\n"
            extract_str += "token count: " + f'completion_tokens={response["usage"]["completion_tokens"]}, prompt_tokens={response["usage"]["prompt_tokens"]}, total_tokens={response["usage"]["total_tokens"]}\n'
            extract_str += "finish reason: " + response["choices"][0]["finish_reason"] + "\n"
        else:
            extract_str = response["choices"][0]["message"]["content"]

        return extract_str

    def chat(self, user_message, one_turn = False, debug_mode=False) -> str:
        user_message_prompt = {"role": "user", "content": user_message}

        if one_turn:
            messages = [self.system_prompt, user_message_prompt]
        else:
            messages = [self.system_prompt] + self.messages + [user_message_prompt]
        
        response = self.get_response(messages)

        if response.status_code == 200: # success
            response_json = response.json()
            if not one_turn:    # multi-turn chat
                self.messages += [user_message_prompt, response_json["choices"][0]["message"]] # update messages

                if len(self.messages) > self.max_memory_in_turns * 2:
                    self.messages = self.messages[-self.max_memory_in_turns * 2:]   # keep the latest max_memory_in_turns turns
            
            output_str = self.extract_response(response_json, debug_mode)
        else: # error
            output_str = f"错误代码: {response.status_code}, {self.error_codes[response.status_code]}"

        return output_str

class ERNIEAPI(LLMAPI):
    def __init__(self, api_key: str,
                 secret_key: str,
                 base_url: str = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/",
                 system_prompt: str="You are a helpful assistant.",
                 max_tokens: int = 2048,
                 temperature: float = 0.95,
                 model: str = "ERNIE-Speed-8K",
                 max_memory_in_turns: int = 5):
        super().__init__(api_key, base_url, system_prompt, max_tokens, temperature, model, max_memory_in_turns)
        self.secret_key = secret_key
        self.access_token = self.get_access_token()

        self.headers = {
        'Content-Type': 'application/json',
        }

        self.model_list = ["ERNIE-Speed-8K", "ERNIE-Speed-128K", "ERNIE-4.0-8K", "ERNIE-3.5-8K", "ERNIE-Lite-8K", "ERNIE-Tiny-8K"]

        self.model_url = {
            "ERNIE-Speed-8K": "ernie_speed",
            "ERNIE-Speed-128K": "ernie-speed-128k",
            "ERNIE-4.0-8K": "ernie-4.0-8k-preview",
            "ERNIE-3.5-8K": "ernie-3.5-8k-preview",
            "ERNIE-Lite-8K": "ernie-lite-8k",
            "ERNIE-Tiny-8K": "ernie-tiny-8k"
        }


    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.secret_key}
        return str(requests.post(url, params=params).json().get("access_token"))


    def get_response(self, messages):
        url = self.base_url + self.model_url[self.model] + "?access_token=" + self.access_token

        payload = json.dumps({
        "messages": messages,
        "system": self.system_prompt,
        "temperature": self.temperature,
        "max_output_tokens": self.max_tokens,
        })

        response = requests.post(url=url, headers=self.headers, data=payload, timeout=100)

        return response


    def extract_response(self, response, debug_mode=False) -> str:
        if debug_mode:
            extract_str = "debug mode: \n"
            extract_str += "response content: " + response['result'] + "\n"
            extract_str += "token count: " + f'completion_tokens={response["usage"]["completion_tokens"]}, prompt_tokens={response["usage"]["prompt_tokens"]}, total_tokens={response["usage"]["total_tokens"]}\n'
            extract_str += "is truncated: " + str(response["is_truncated"]) + "\n"
        else:
            extract_str = response['result']

        return extract_str


    def chat(self, user_message, one_turn = False, debug_mode=False) -> str:
        user_message_prompt = {"role": "user", "content": user_message}

        if one_turn:
            messages = [user_message_prompt]
        else:
            messages = self.messages + [user_message_prompt]
        
        response = self.get_response(messages)
        response_json = response.json()

        if "error_code" not in response_json: # success
            if not one_turn:    # multi-turn chat
                self.messages += [user_message_prompt, {"role": "assistant", "content": response_json['result']}] # update messages

                if len(self.messages) > self.max_memory_in_turns * 2:
                    self.messages = self.messages[-self.max_memory_in_turns * 2:]   # keep the latest max_memory_in_turns turns
            
            output_str = self.extract_response(response_json, debug_mode)
        else: # error
            error_code = response_json["error_code"]
            error_message = response_json["error_msg"]
            output_str = f"错误代码: {error_code}, {error_message}"

        return output_str


class QwenAPI(LLMAPI):
    def __init__(self, api_key: str,
                 base_url: str = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
                 system_prompt: str="You are a helpful assistant.",
                 max_tokens: int = 1500,
                 temperature: float = 1,
                 model: str = "qwen-long",
                 max_memory_in_turns: int = 5):
        super().__init__(api_key, base_url, system_prompt, max_tokens, temperature, model, max_memory_in_turns)
        self.system_prompt = {"role": "system", "content": system_prompt}

        self.model_list = ["qwen-long", "qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext",
                           "qwen1.5-110b-chat", "qwen1.5-72b-chat", "qwen1.5-32b-chat", "qwen1.5-14b-chat", 
                           "qwen1.5-7b-chat", "qwen1.5-1.8b-chat", "qwen1.5-0.5b-chat", "codeqwen1.5-7b-chat"
                           ]

        self.headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + self.api_key
        }

    def get_response(self, messages):
        payload = json.dumps({
        "input":{"messages": messages},
        "model": self.model,
        "parameters": {
            "result_format": "message",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
            }
        })

        response = requests.post(self.base_url, headers=self.headers, data=payload, timeout=100)

        return response
    
    def extract_response(self, response, debug_mode=False) -> str:
        if debug_mode:
            extract_str = "debug mode: \n"
            extract_str += "response content: " + response['output']["choices"][0]["message"]["content"] + "\n"
            extract_str += "token count: " + f'input_tokens={response["usage"]["input_tokens"]}, output_tokens={response["usage"]["output_tokens"]}, total_tokens={response["usage"]["total_tokens"]}\n'
            extract_str += "finish reason: " + response['output']["choices"][0]["finish_reason"] + "\n"
        else:
            extract_str = response['output']["choices"][0]["message"]["content"]

        return extract_str

    def chat(self, user_message, one_turn = False, debug_mode=False) -> str:
        user_message_prompt = {"role": "user", "content": user_message}

        if one_turn:
            messages = [self.system_prompt, user_message_prompt]
        else:
            messages = [self.system_prompt] + self.messages + [user_message_prompt]
        
        response = self.get_response(messages)
        response_json = response.json()

        if response.status_code == 200: # success
            if not one_turn:    # multi-turn chat
                self.messages += [user_message_prompt, response_json["output"]["choices"][0]["message"]] # update messages

                if len(self.messages) > self.max_memory_in_turns * 2:
                    self.messages = self.messages[-self.max_memory_in_turns * 2:]   # keep the latest max_memory_in_turns turns
            
            output_str = self.extract_response(response_json, debug_mode)
        else: # error
            output_str = f"错误代码: {response_json['code']}, {response_json['message']}"

        return output_str
    
