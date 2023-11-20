from sdv.metadata import MultiTableMetadata
from sdv.datasets.local import load_csvs
from sdv.multi_table import HMASynthesizer

metadata = MultiTableMetadata()
metadata.detect_from_csvs(
    folder_name='data/client'
)
metadata.update_column(table_name='contact', column_name='contactId', sdtype='id')
metadata.set_primary_key(table_name='contact', column_name='contactId');

metadata.update_column(table_name='accountNotes', column_name='id', sdtype='id')
metadata.set_primary_key(table_name='accountNotes', column_name='id');
metadata.update_column(table_name='accountNotes', column_name='accountContactId', sdtype='id')

metadata.update_column(table_name='callTranscript', column_name='id', sdtype='id')
metadata.set_primary_key(table_name='callTranscript', column_name='id');
metadata.update_column(table_name='callTranscript', column_name='accountContactId', sdtype='id')

metadata.update_column(table_name='accountContact', column_name='id', sdtype='id')
metadata.set_primary_key(table_name='accountContact', column_name='id');
metadata.update_column(table_name='accountContact', column_name='accountId', sdtype='id')
metadata.update_column(table_name='accountContact', column_name='contactId', sdtype='id')

metadata.update_column(table_name='account', column_name='accountId', sdtype='id')
metadata.set_primary_key(table_name='account', column_name='accountId');

metadata.relationships = list()

metadata.add_relationship(parent_table_name='accountContact', parent_primary_key='id', child_table_name='accountNotes', child_foreign_key='accountContactId')

metadata.add_relationship(parent_table_name='accountContact', parent_primary_key='id', child_table_name='callTranscript', child_foreign_key='accountContactId')

metadata.add_relationship(parent_table_name='account', parent_primary_key='accountId', child_table_name='accountContact', child_foreign_key='accountId')
metadata.add_relationship(parent_table_name='contact', parent_primary_key='contactId', child_table_name='accountContact', child_foreign_key='contactId')


print(metadata.to_dict)

datasets = load_csvs(
    folder_name='data/client',
    read_csv_parameters={
        'skipinitialspace': True,
        # 'encoding': 'utf_32'
    }
)

synthesizer = HMASynthesizer(metadata)
synthesizer.fit(datasets)

synthetic_data = synthesizer.sample(scale=2)

print(synthetic_data['callTranscript'])
print(synthetic_data['account'])
print(synthetic_data['contact'])