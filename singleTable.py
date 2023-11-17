from sdv.datasets.demo import download_demo
from sdv.lite import SingleTablePreset


real_data, metadata = download_demo(
    modality='single_table',
    dataset_name='fake_hotel_guests'
)

print(real_data.head())
print(metadata.columns)

synthesizer = SingleTablePreset(
    metadata,
    name='FAST_ML'
)

synthesizer.fit(
    data=real_data
)

synthetic_data = synthesizer.sample(
    num_rows=10
)

print(synthetic_data.head())


