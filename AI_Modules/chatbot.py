import openai
import tiktoken


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

def prepare_msgs(msgs):
    max_prompt_tokens = 500
    prompt_tokens = 0
    chat_msg_returned = False
    messages = []
    for msg, role in msgs:
        match role:
            case "system":
                messages.insert(0, {"role": role, "content": msg})
            case "assistant":
                if not chat_msg_returned:
                    messages.insert(1, {"role": role, "content": msg})
                    chat_msg_returned = True
            case "user":
                messages.insert(1, {"role": role, "content": msg})
        prompt_tokens = gpt3_tokens_calc(messages, chat= True)
        if prompt_tokens >= max_prompt_tokens:
            break
            
    n_prompt_messages = len(messages)
    
    data = {
        "messages": msgs,
        "prompt_tokens": prompt_tokens,
        "n_prompt_messages": n_prompt_messages,
        "n_sent_messages": len(msgs)
    }
    
def get_gpt_chat_response(msgs,
                        user_id = "0000",
                        model = "gpt-3.5-turbo",
                        temperature = 1,
                        max_tokens = 500
                        ):
    def chat_req():
        return openai.ChatCompletion.create(model = model,
                                            messages = msgs,
                                            temperature = temperature,
                                            max_tokens = max_tokens,
                                            stream = True,
                                            user = user_id
                                            )
    for i in range(5):
        try:
            res = chat_req()
            return res
        except (openai.error.TryAgain,
                openai.error.ServiceUnavailableError,
                openai.error.APIError,
                openai.error.APIConnectionError,
                openai.error.Timeout
                ) as err:
            if i == 4:
                raise Exception(err)
            continue

def transcripe(path):
    audio_file = open(path, "rb")
    res = openai.Audio.transcribe("whisper-1", audio_file)
    return res.text
