import openai
import datetime
import tiktoken
import time

def tokens_calc(string, encoding = tiktoken.get_encoding("cl100k_base")):
    encoded_string = encoding.encode(string)
    tokens = [encoding.decode([token]) for token in encoded_string]
    embeddings = [0] * len(tokens)
    for i in range(len(tokens)):
        response = openai.Embedding.create(input=tokens[i], model="text-embedding-ada-002")
        embeddings[i] = response["data"][0]["embedding"]
    return len(embeddings)

class GPT():
    def __init__(self, chat=True):
        self.__initialization_time = datetime.datetime.now()
        self.chat = chat
        # model's parameters
        self.__max_tokens_returned_to_model = 500
        self.__model = "gpt-3.5-turbo"
        self.__temperature = 1
        self.__max_generated_tokens = 1000
        self.__presence_penalty = 0
        #self.user_id = "0000"
        
        self.messages_data = {
            "initialization_time": self.__initialization_time,
            "system_messages": {"messages": [], "n_tokens": []},
            "chat_messages": {"messages": [], "role": [], "n_tokens": [], "message_time": []},
            "n_returned_messages": [],
            "prompt_tokens": [],
            "completion_tokens": [],
            "total_tokens": [],
            "finish_reason": []
        }
        

    def __send_chat_req(self, msgs):
        return openai.ChatCompletion.create(model= self.__model,
                                                messages= msgs,
                                                temperature= self.__temperature,
                                                max_tokens= self.__max_generated_tokens,
                                                presence_penalty= self.__presence_penalty,
                                                #user= self.user_id
                                                )
    
    def system_msgs(self, new_sstm_msgs):
        if type(new_sstm_msgs) != type([]):
            if type(new_sstm_msgs) != type(""):
                raise Exception("Please provide a string or a list of strings")
            new_sstm_msgs = [new_sstm_msgs]
        [self.messages_data["system_messages"]["messages"].append(message) 
         for message in new_sstm_msgs]
        [self.messages_data["system_messages"]["n_tokens"].append(tokens_calc(message)) 
         for message in new_sstm_msgs]

    
    def new_user_message(self, new_message):
        messages = [{"role": "system", "content": msg} for msg in self.messages_data["system_messages"]["messages"]]
        messages.append({"role": "user", "content":new_message})
        
        if self.chat:
            additive_n_tokens = 0
            n_returned_messages = 0
            for i in range(len(self.messages_data["chat_messages"]["messages"])):
                if i == 0:
                    continue
                if additive_n_tokens > self.__max_tokens_returned_to_model:
                    break
                additive_n_tokens += self.messages_data["chat_messages"]["n_tokens"][i]
                n_returned_messages += 1

            partial_messages = []
            for i in range(n_returned_messages):
                partial_messages.insert(0, {"role": self.messages_data["chat_messages"]["role"][i],
                                            "content": self.messages_data["chat_messages"]["messages"][i]})
            [messages.append(msg) for msg in partial_messages]
        
        
        req_time = datetime.datetime.now()
        response = self.__send_chat_req(messages)
        res_time = datetime.datetime.now()
        
        res_message = response["choices"][0]["message"]["content"]
        completion_tokens = response["usage"]["completion_tokens"]
        prompt_tokens = response["usage"]["prompt_tokens"]
        total_tokens = completion_tokens + prompt_tokens
        
        if self.chat:
            self.messages_data["n_returned_messages"].insert(0, n_returned_messages)
        else:
            self.messages_data["n_returned_messages"].insert(0, None)
        self.messages_data["chat_messages"]["messages"].insert(0, new_message)
        self.messages_data["chat_messages"]["role"].insert(0, "user")
        self.messages_data["chat_messages"]["message_time"].insert(0, req_time)
        self.messages_data["chat_messages"]["n_tokens"].insert(0, tokens_calc(new_message))
        self.messages_data["prompt_tokens"].insert(0, prompt_tokens)
        
        self.messages_data["chat_messages"]["messages"].insert(0, res_message)
        self.messages_data["chat_messages"]["role"].insert(0, response["choices"][0]["message"]["role"])
        self.messages_data["chat_messages"]["message_time"].insert(0, res_time)
        self.messages_data["chat_messages"]["n_tokens"].insert(0, completion_tokens)
        self.messages_data["completion_tokens"].insert(0, completion_tokens)
        self.messages_data["total_tokens"].insert(0, total_tokens)
        self.messages_data["finish_reason"].insert(0, response["choices"][0]["finish_reason"])
        
        return self.messages_data
        
