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
    prompt = """### sqlite SQL table, with its properies:
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

    return definition+query_init_string

nlp_text = prompt_input()  # NLP
prompt = combine_prompts(df, nlp_text)  # DF + query + NLP

print("\nThe prompt:\n")
print(prompt)

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are only writing SQL."},
        {"role": "user", "content": prompt}],
    temperature=0,
    max_tokens=150,
    frequency_penalty=0,
    presence_penalty=0,
    stop=['#',';']
)

print("Response:\n" + completion.choices[0].message.content)

print("\n\nDiag:\n")
print(completion.choices[0])

sql_query = completion.choices[0].message.content
print("\n\n<<<" + sql_query + ">>>\n\n")

trimmed_sql_query = sql_query[6:]
print(trimmed_sql_query)

with temp_db.connect() as conn:
    result = conn.execute(text(trimmed_sql_query))

 # Convert result to a pandas DataFrame
result_df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
# Print the DataFrame
print(result_df)


print("\nProgram end...")
