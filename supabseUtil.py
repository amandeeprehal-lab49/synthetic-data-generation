import os

from langchain.schema import Document
from supabase import create_client, Client
from langchain.vectorstores.supabase import SupabaseVectorStore
from langchain.embeddings import openai, OpenAIEmbeddings

DATA_DIR = "./data/result/"

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
client: Client = create_client(supabase_url=url, supabase_key=key)

embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)


def insert_into_database(table_name, data):
    store = SupabaseVectorStore(embedding=embeddings, client=client, table_name=table_name,
                                query_name='match_documents')
    store.add_documents(data)


def read_file(file_name) -> list[Document]:
    file = open(DATA_DIR + file_name, "r")
    data: list = []
    flag = True
    for line in file.readlines():
        if flag:
            flag = False
        else:
            data.append(Document(page_content=line))

    return data


def supabase_insert_account_contacts():
    data = read_file("accountContact.csv")
    insert_into_database('account_contacts', data)


def supabase_insert_account_notes():
    data = read_file("accountNotes.csv")
    insert_into_database('account_notes', data)


def supabase_insert_accounts():
    data = read_file("accounts.csv")
    insert_into_database('accounts', data)


def supabase_insert_call_transcripts():
    data = read_file("callTranscript.csv")
    insert_into_database('call_transcripts', data)


def supabase_insert_contacts():
    data = read_file("contact.csv")
    insert_into_database('contacts', data)


def insert_data_to_supabase():
    supabase_insert_accounts()
    supabase_insert_account_contacts()
    supabase_insert_account_notes()
    supabase_insert_call_transcripts()
    supabase_insert_contacts()


