import os
from openai import OpenAI

print ("Hello World!!!")

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Name five popular flavors of ice cream."}
  ]
)

print("Response:\n" + completion.choices[0].message.content)

print("\n\nDiag:\n")
print(completion.choices[0])

print("\nProgram end...")
