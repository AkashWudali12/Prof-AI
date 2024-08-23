from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv(".env")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPEN_AI_KEY"),
)

class OPEN_AI_AGENT:
    def __init__(self, system_message):
        self.system_message = system_message
    
    def run_completion(self, prompt, temp):

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content":self.system_message},
                {"role":"user", "content":prompt}
            ],
            model="gpt-3.5-turbo",
            temperature=temp
        )

        return chat_completion.choices[0].message.content
