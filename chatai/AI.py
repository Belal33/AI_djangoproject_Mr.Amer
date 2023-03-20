import openai

openai.api_key = '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'

# the prompt is the text the user is sending to the model
def gpt_chat(prompt,
            number_of_generated_completions=1):
    
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[{"role": "user", "content": prompt}],
                                              n=number_of_generated_completions,
    )
    
    completions = [choice["message"]["content"] for choice in completion["choices"]]
    res =  completions[0]
    return str(res)

if __name__ == "__main__":
    print(gpt_chat('stellar matter'))   

