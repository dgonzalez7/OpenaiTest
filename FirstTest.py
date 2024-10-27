import os
from openai import OpenAI

print ("Hello World!!!")

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Name five flavors of ice cream."
        }
    ]
)

print(completion.choices[0].message)