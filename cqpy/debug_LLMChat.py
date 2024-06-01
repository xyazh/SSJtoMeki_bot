#from .LLMChat import DeepseekAPI


if __name__ == "__main__":
    import pickle
    from LLMChat import DeepseekAPI, ERNIEAPI, QwenAPI
    from DataManager import DataManager

    data_manager:DataManager = DataManager("\\PiaoXue\\")
    with data_manager.openFile('key.pkl', 'rb') as f:
        key_dict = pickle.load(f)
    qwen_api = QwenAPI(key_dict['Qwen'], model="qwen1.5-0.5b-chat")
    
    while True:
        user_input = input("You: ")
        if user_input == "":
            break
        print(qwen_api.chat(user_input, debug_mode=True))
