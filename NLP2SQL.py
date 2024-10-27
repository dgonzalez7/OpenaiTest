# import os
from openai import OpenAI
import pandas as pd

print ("Program start...\n")

df = pd.read_csv("sales_data_sample.csv")
print(df)

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

# Temp DB in RAM

temp_db = create_engine('sqlite:///:memory:',echo=True)

# Push Pandas DF to Temp DB

data = df.to_sql(name='Sales',con=temp_db)

# SQL query on temp DB

with temp_db.connect() as conn:
    # Makes the connection
    # Run code in block

    result = conn.execute(text("SELECT SUM(SALES) from Sales"))

    # Auto close connection

 # Convert result to a pandas DataFrame
result_df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
# Print the DataFrame
print(result_df)

print("\n\nStarting next section...\n")

def create_table_definition(df):
    prompt = """### sqlite SQL tabel, with its properies:
    # 
    # Sales({})
    
    
    
    """.format(",".join(str(col) for col in df.columns))

    return prompt

print(create_table_definition(df))

def prompt_input():
    nlp_text = input("Enter the infor you want: ")
    return nlp_text

# print(prompt_input())

def combine_prompts(df, query_prompt):
    definition = create_table_definition(df)
    query_init_string = f"### A query to answer: {query_prompt}\nSELECT"

    print("\ndefinition:\n")
    print(definition)
    print("\nquery_init_string:\n")
    print(query_init_string)

    return definition+query_init_string

nlp_text = prompt_input()  # NLP
command_for_openai = combine_prompts(df, nlp_text)  # DF + query + NLP

print("\nThe command:\n")
print(command_for_openai)

# client = OpenAI()

# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Name five popular flavors of ice cream."}
#   ]
# )

# print("Response:\n" + completion.choices[0].message.content)

# print("\n\nDiag:\n")
# print(completion.choices[0])

print("\nProgram end...")
