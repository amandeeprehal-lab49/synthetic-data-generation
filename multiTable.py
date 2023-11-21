from sdv.metadata import MultiTableMetadata
from sdv.datasets.local import load_csvs
from sdv.multi_table import HMASynthesizer
from rdt.transformers.pii import AnonymizedFaker

metadata = MultiTableMetadata()
metadata.detect_from_csvs(
    folder_name='data/client'
)
metadata.update_column(table_name='contact', column_name='contactId', sdtype='id')
metadata.set_primary_key(table_name='contact', column_name='contactId');
metadata.update_column(table_name='contact', column_name='name', sdtype='name')
metadata.update_column(table_name='contact', column_name='address', sdtype='address')

metadata.update_column(table_name='accountNotes', column_name='id', sdtype='id')
metadata.set_primary_key(table_name='accountNotes', column_name='id');
metadata.update_column(table_name='accountNotes', column_name='accountContactId', sdtype='id')
metadata.update_column(table_name='accountNotes', column_name='notes', sdtype='text')

metadata.update_column(table_name='callTranscript', column_name='id', sdtype='id')
metadata.set_primary_key(table_name='callTranscript', column_name='id');
metadata.update_column(table_name='callTranscript', column_name='accountContactId', sdtype='id')
metadata.update_column(table_name='callTranscript', column_name='transcript', sdtype='text')

metadata.update_column(table_name='accountContact', column_name='id', sdtype='id')
metadata.set_primary_key(table_name='accountContact', column_name='id');
metadata.update_column(table_name='accountContact', column_name='accountId', sdtype='id')
metadata.update_column(table_name='accountContact', column_name='contactId', sdtype='id')

metadata.update_column(table_name='account', column_name='accountId', sdtype='id')
metadata.set_primary_key(table_name='account', column_name='accountId');
metadata.update_column(table_name='account', column_name='notes', sdtype='text')
metadata.update_column(table_name='account', column_name='address', sdtype='address')
metadata.update_column(table_name='account', column_name='name', sdtype='company')

metadata.relationships = list()

metadata.add_relationship(parent_table_name='accountContact', parent_primary_key='id', child_table_name='accountNotes', child_foreign_key='accountContactId')

metadata.add_relationship(parent_table_name='accountContact', parent_primary_key='id', child_table_name='callTranscript', child_foreign_key='accountContactId')

metadata.add_relationship(parent_table_name='account', parent_primary_key='accountId', child_table_name='accountContact', child_foreign_key='accountId')
metadata.add_relationship(parent_table_name='contact', parent_primary_key='contactId', child_table_name='accountContact', child_foreign_key='contactId')

datasets = load_csvs(
    folder_name='data/client',
    read_csv_parameters={
        'skipinitialspace': True,
        # 'encoding': 'utf_32'
    }
)

synthesizer = HMASynthesizer(metadata)
synthesizer.fit(datasets)

transformers = synthesizer.get_transformers(table_name='accountNotes')
transformers['notes'].enforce_uniqueness=True
transformers = synthesizer.get_transformers(table_name='callTranscript')
transformers['transcript'].enforce_uniqueness=True
transformers = synthesizer.get_transformers(table_name='account')
transformers['notes'].enforce_uniqueness=True

addressTransformer = AnonymizedFaker(provider_name='address', function_name='address', enforce_uniqueness=True)
synthesizer.update_transformers(table_name='account', column_name_to_transformer={'address': addressTransformer})
companyTransformer = AnonymizedFaker(provider_name='company', function_name='company', enforce_uniqueness=True)
synthesizer.update_transformers(table_name='account', column_name_to_transformer={'name': companyTransformer})

synthesizer.fit(datasets)

synthetic_data = synthesizer.sample(scale=1)

synthetic_data['account'].to_json('./data/result/account.json', orient='records', lines=True)
synthetic_data['contact'].to_json('./data/result/contact.json', orient='records', lines=True)
synthetic_data['accountContact'].to_json('./data/result/accountContact.json', orient='records', lines=True)
synthetic_data['accountNotes'].to_json('./data/result/accountNotes.json', orient='records', lines=True)
synthetic_data['callTranscript'].to_json('./data/result/callTranscript.json', orient='records', lines=True)

print('*************** Check result in ./data/result *********************')
