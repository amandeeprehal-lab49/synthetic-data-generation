from sdv.metadata import MultiTableMetadata
from sdv.datasets.local import load_csvs
from sdv.multi_table import HMASynthesizer
from rdt.transformers.pii import AnonymizedFaker

def setupContactMetadata(metadata):
    metadata.update_column(table_name='contact', column_name='contactId', sdtype='id')
    metadata.set_primary_key(table_name='contact', column_name='contactId');
    metadata.update_column(table_name='contact', column_name='name', sdtype='name')
    metadata.update_column(table_name='contact', column_name='address', sdtype='address')

def setupAccountNotesMetadata(metadata):
    metadata.update_column(table_name='accountNotes', column_name='id', sdtype='id')
    metadata.set_primary_key(table_name='accountNotes', column_name='id');
    metadata.update_column(table_name='accountNotes', column_name='accountContactId', sdtype='id')
    metadata.update_column(table_name='accountNotes', column_name='notes', sdtype='text')

def setupCallTranscriptMetadata(metadata):
    metadata.update_column(table_name='callTranscript', column_name='id', sdtype='id')
    metadata.set_primary_key(table_name='callTranscript', column_name='id');
    metadata.update_column(table_name='callTranscript', column_name='accountContactId', sdtype='id')
    # metadata.update_column(table_name='callTranscript', column_name='transcript', sdtype='text')

def setupAccountContactMetadata(metadata):
    metadata.update_column(table_name='accountContact', column_name='id', sdtype='id')
    metadata.set_primary_key(table_name='accountContact', column_name='id');
    metadata.update_column(table_name='accountContact', column_name='accountId', sdtype='id')
    metadata.update_column(table_name='accountContact', column_name='contactId', sdtype='id')

def setupAccountMetadata(metadata):
    metadata.update_column(table_name='account', column_name='accountId', sdtype='id')
    metadata.set_primary_key(table_name='account', column_name='accountId');
    metadata.update_column(table_name='account', column_name='notes', sdtype='text')
    metadata.update_column(table_name='account', column_name='address', sdtype='address')
    metadata.update_column(table_name='account', column_name='name', sdtype='company')

def setupEntityRelationships(metadata):
    metadata.relationships = list()
    metadata.add_relationship(parent_table_name='accountContact', parent_primary_key='id', child_table_name='accountNotes', child_foreign_key='accountContactId')

    metadata.add_relationship(parent_table_name='accountContact', parent_primary_key='id', child_table_name='callTranscript', child_foreign_key='accountContactId')

    metadata.add_relationship(parent_table_name='account', parent_primary_key='accountId', child_table_name='accountContact', child_foreign_key='accountId')
    metadata.add_relationship(parent_table_name='contact', parent_primary_key='contactId', child_table_name='accountContact', child_foreign_key='contactId')

def loadCsvData():
    return load_csvs(
    folder_name='data/client',
    read_csv_parameters={
        'skipinitialspace': True,
        # 'encoding': 'utf_32'
    }
)

def updateTransformers(synthesizer):
    transformers = synthesizer.get_transformers(table_name='accountNotes')
    transformers['notes'].enforce_uniqueness=True
    transformers['notes'].function_kwargs={'max_nb_chars': 2000}
    transformers = synthesizer.get_transformers(table_name='callTranscript')
    transformers['transcript'].enforce_uniqueness=False
    # transformers['transcript'].function_kwargs={'max_nb_chars': 2000}
    transformers = synthesizer.get_transformers(table_name='account')
    transformers['notes'].enforce_uniqueness=True
    transformers['notes'].function_kwargs={'max_nb_chars': 2000}

    addressTransformer = AnonymizedFaker(provider_name='address', function_name='address', enforce_uniqueness=True)
    synthesizer.update_transformers(table_name='account', column_name_to_transformer={'address': addressTransformer})
    companyTransformer = AnonymizedFaker(provider_name='company', function_name='company', enforce_uniqueness=True)
    synthesizer.update_transformers(table_name='account', column_name_to_transformer={'name': companyTransformer})

def writeResultToFile(RESULT_FILE_PATH, synthetic_data):
    synthetic_data['account'].to_json(RESULT_FILE_PATH + '/account.json', orient='records', lines=True)
    synthetic_data['contact'].to_json(RESULT_FILE_PATH + '/contact.json', orient='records', lines=True)
    synthetic_data['accountContact'].to_json(RESULT_FILE_PATH + '/accountContact.json', orient='records', lines=True)
    synthetic_data['accountNotes'].to_json(RESULT_FILE_PATH + '/accountNotes.json', orient='records', lines=True)
    synthetic_data['callTranscript'].to_json(RESULT_FILE_PATH + '/callTranscript.json', orient='records', lines=True)

def main():
    RESULT_FILE_PATH = './data/result'
    INITIAL_DATA_FILE = './data/client'
    metadata = MultiTableMetadata()
    metadata.detect_from_csvs(
        folder_name=INITIAL_DATA_FILE
    )
    setupContactMetadata(metadata)
    setupAccountNotesMetadata(metadata)
    setupCallTranscriptMetadata(metadata)
    setupAccountContactMetadata(metadata)
    setupAccountMetadata(metadata)
    setupEntityRelationships(metadata)

    datasets = loadCsvData()

    synthesizer = HMASynthesizer(metadata)
    synthesizer.fit(datasets)
    updateTransformers(synthesizer)
    synthesizer.fit(datasets)
    synthetic_data = synthesizer.sample(scale=0.5)
    writeResultToFile(RESULT_FILE_PATH, synthetic_data)
    print('*************** Check result in ./data/result *********************')

if __name__ == '__main__':
         main()