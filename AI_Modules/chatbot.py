import openai
import datetime
import tiktoken
import time

def gpt3_tokens_calc(argument, chat= False, encoding = tiktoken.get_encoding("cl100k_base")):
    if chat:
        num_tokens = 0
        for message in argument:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens + 1
    elif not chat:
        encoded_string = encoding.encode(argument)
        tokens = [encoding.decode([token]) for token in encoded_string]
        return len(tokens)

def get_gpt_chat_response(msgs,
                        user_id,
                        model = "gpt-3.5-turbo",
                        temperature = 1,  
                        stream = True,
                        max_tokens = 500):
    
    max_prompt_tokens = 500
    prompt_tokens = 0
    chat_msg_returned = False
    msgs = []
    for msg, role in msgs:
        if role == "system":
            msgs.insert(0, {"role": role, "content": msg})
        if role == "assistant":
            if not chat_msg_returned:
                msgs.insert(1, {"role": role, "content": msg})
                chat_msg_returned = True
        if role == "user":
            msgs.insert(1, {"role": role, "content": msg})
        prompt_tokens = gpt3_tokens_calc(msgs, chat= True)
        if prompt_tokens >= max_tokens_returned_to_model:
            break
    n_prompt_messages = len(msgs)
    
    def chat_req():
        n_trys += 1
        return openai.ChatCompletion.create(model = model,
                                            messages = msgs,
                                            temperature = temperature,
                                            max_tokens = max_tokens,
                                            stream = stream,
                                            user = user_id,
                                           )
    
    n_trys = 0
    req_time = datetime.datetime.now()
    try:
        res = chat_req()
    except (openai.error.TryAgain,
            openai.error.ServiceUnavailableError,
            openai.error.APIError,
            openai.error.APIConnectionError,
            openai.error.Timeout
           ) as err:
        if n_trys > 5:
            raise Exception(err)
        else:
            time.sleep(5)
            res = chat_req()
    res_time = datetime.datetime.now()
    
    if stream:
        data = {
            "generator": res,
            "prompt_tokens": prompt_tokens,
            "n_prompt_messages": n_prompt_messages,
            "server_req_time": req_time,
            "server_res_time": res_time,
            "temperature": temperature
        }
        return data