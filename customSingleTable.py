from sdv.lite import SingleTablePreset
from sdv.metadata import SingleTableMetadata
from sdv.datasets.local import load_csvs
from sdv.single_table import GaussianCopulaSynthesizer

metadata = SingleTableMetadata()
metadata.detect_from_csv(filepath='data/person.csv')
metadata.update_column(column_name='id', sdtype='id')


# assume that data contains a CSV file named 'personData.csv'
datasets = load_csvs(
    folder_name='data/',
    read_csv_parameters={
        'skipinitialspace': True,
        # 'encoding': 'utf_32'
    }
)

# the data is available under the file name
realData = datasets['personData']

# synthesizer = SingleTablePreset(metadata, name='FAST_ML')
# synthesizer.fit(realData)

# synthetic_data = synthesizer.sample(num_rows=10)

# print(synthetic_data)

synthesizer = GaussianCopulaSynthesizer(metadata)
synthesizer.fit(realData)

synthetic_data = synthesizer.sample(num_rows=10)

print(synthetic_data)