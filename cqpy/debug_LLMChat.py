#from .LLMChat import DeepseekAPI
from LLMChat import DeepseekAPI, ERNIEAPI, QwenAPI

if __name__ == "__main__":
    import pickle

    with open('key.pkl', 'rb') as f:
        key_dict = pickle.load(f)

    qwen_api = QwenAPI(key_dict['Qwen'], model="qwen1.5-0.5b-chat")
    
    while True:
        user_input = input("You: ")
        if user_input == "":
            break
        print(qwen_api.chat(user_input, debug_mode=True))
