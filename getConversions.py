# import the OpenAI Python library for calling the OpenAI API
# importing the pandas library
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI()

strongTone = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "Generate 5 lines conversation between financial advisor and fund house representative using strong tone",
        },
    ],
    temperature=0,
)
print(strongTone.choices[0].message.content)

humorTone = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "Generate 5 lines conversation between financial advisor and fund house representative using humor tone",
        },
    ],
    temperature=0,
)
print(humorTone.choices[0].message.content)

formalTone = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "Generate 5 lines conversation between financial advisor and fund house representative using formal tone",
        },
    ],
    temperature=0,
)
print(formalTone.choices[0].message.content)

callTranscriptFilePath = "./data/client/callTranscript.csv"

# reading the csv file
df = pd.read_csv(callTranscriptFilePath)

# updating the column value/data
df.loc[0, "transcript"] = (strongTone.choices[0].message.content).replace(",", " ")
df.loc[1, "transcript"] = (formalTone.choices[0].message.content).replace(",", " ")
df.loc[2, "transcript"] = (humorTone.choices[0].message.content).replace(",", " ")

# writing into the file
df.to_csv(callTranscriptFilePath, index=False)
