from typing import List
import os
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import FewShotPromptTemplate, PromptTemplate

from langchain_experimental.tabular_synthetic_data.openai import (
    OPENAI_TEMPLATE,
    create_openai_data_generator,
)
from langchain_experimental.tabular_synthetic_data.prompts import (
    SYNTHETIC_FEW_SHOT_PREFIX,
    SYNTHETIC_FEW_SHOT_SUFFIX,
)

from model.accounts import Account
from model.accountContacts import AccountContact
from model.callTranscript import CallTranscript
from model.Contacts import Contact
from model.accountNotes import AccountNote

OPENAI_TEMPLATE = PromptTemplate(input_variables=["example"], template="{example}")

SAMPLE_DIR = "./data/client/"
SAMPLE_ITEMS = 1


def create_template(modal):
    return FewShotPromptTemplate(
        prefix=SYNTHETIC_FEW_SHOT_PREFIX,
        examples=modal().examples,
        suffix=SYNTHETIC_FEW_SHOT_SUFFIX,
        input_variables=["subject", "extra"],
        example_prompt=OPENAI_TEMPLATE,
    )


def generate_results(chat_open_ai, schema, subject, instructions) -> List[str]:
    return create_openai_data_generator(
        output_schema=schema,
        llm=chat_open_ai,
        prompt=create_template(schema),
    ).generate(
        subject=subject,
        extra=instructions,
        runs=SAMPLE_ITEMS,
    )


def create_sample_accounts(llm):
    results = generate_results(llm, Account, "accounts",
                               """the name must be chosen from existing company name.
                                         the address should be some valid address in US.
                                         the note should be a meeting note with max 500 characters.""")
    f = open(SAMPLE_DIR + "accounts.csv", "w")
    f.write("accountId,name,address,notes\n")

    for result in results:
        f.write(f"{result.accountId},{result.name},{result.address},{result.notes}\n")


def create_sample_account_contacts(llm):
    results = generate_results(llm, AccountContact, "accountContacts",
                               """contact id should be chosen at random within range 1000 to 1200""")
    f = open(SAMPLE_DIR + "accountContact.csv", "w")
    f.write("id,accountId,contactId\n")

    for result in results:
        f.write(f"{result.id},{result.accountId},{result.contactId}\n")


def create_account_notes(llm):
    results = generate_results(llm, AccountNote, "accountNote",
                               """id should be chosen at random within range 1000 to 1200""")
    f = open(SAMPLE_DIR + "accountNotes.csv", "w")
    f.write("id,accountContactId,notes\n")

    for result in results:
        f.write(f"{result.id},{result.accountContactId},{result.notes}\n")


def create_call_transcripts(llm):
    results = generate_results(llm, CallTranscript, "callTranscripts",
                               """transcript should be generated as phone call conversation. Avoid newline in 
                               conversation instead Seperate each conversation with | charecter. id should be 
                               sequential""")
    f = open(SAMPLE_DIR + "callTranscript.csv", "w")
    f.write("id,accountContactId,transcript\n")

    for result in results:
        f.write(f"{result.id},{result.accountContactId},{result.transcript}\n")


def create_contacts(llm):
    results = generate_results(llm, Contact, "contacts",
                               """contactId should be chosen at random within range 1000 to 1200.
                               name should be a random name. address should be a valid US address
                               """)
    f = open(SAMPLE_DIR + "contact.csv", "w")
    f.write("contactId,name,address\n")

    for result in results:
        f.write(f"{result.contactId},{result.name},{result.address}\n")


def generate_sample_data():
    chat_open_ai = ChatOpenAI(
        temperature=1,
        openai_api_key=os.environ.get("OPENAI_API_KEY")
    )
    create_sample_accounts(chat_open_ai)
    create_sample_account_contacts(chat_open_ai)
    create_call_transcripts(chat_open_ai)
    create_contacts(chat_open_ai)
    create_account_notes(chat_open_ai)
