# test if the openai SDK is installed
# if not, install it

try:
    from openai import OpenAI
except ImportError:
    import os
    os.system("pip install openai")
    from openai import OpenAI

def createClient(api_key: str, base_url: str = "https://api.deepseek.com"):
    return OpenAI(api_key=api_key, base_url=base_url)


def get_response(client, message, model, max_tokens=4096, temperature=1, AI_role="system", user_role="user", AI_content="You are a helpful assistant"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": AI_role, "content": AI_content},
            {"role": user_role, "content": message},
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )

    return response


def extract_response(response, debug_mode=False) -> str:
    if debug_mode:
        extract_str = "debug mode: \n"
        extract_str += "response content: " + response.choices[0].message.content + "\n"
        extract_str += "token count: " + f'completion_tokens={response.usage.completion_tokens}, prompt_tokens={response.usage.prompt_tokens}, total_tokens={response.usage.total_tokens}\n'
        extract_str += "finish reason: " + response.choices[0].finish_reason + "\n"
    else:
        extract_str = response.choices[0].message.content

    
    return extract_str
