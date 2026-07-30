from pathlib import Path
import pyarrow.parquet as pq

root_file_path = Path(__file__).resolve().parent.parent
print(root_file_path)
trips = pq.read_table(root_file_path / 'data' / 'raw' / 'yellow_tripdata_2025-01.parquet')
trips = trips.to_pandas()
print(trips.head(100))
print(trips.info(verbose = True))