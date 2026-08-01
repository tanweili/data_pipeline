from pathlib import Path
import pandas as pd
from pandas import DataFrame

# Run this script while within this project at the root folder
ROOT_PATH = Path.cwd().resolve()
DATA_FOLDER = 'data'
PROCESSED_FOLDER = 'processed'
RAW_FOLDER = 'raw'

def process_yearly_data(year: int):
    processed_folder_path = ROOT_PATH / DATA_FOLDER / PROCESSED_FOLDER / str(year)
    if processed_folder_path.exists():
        answer = input(f"Delete all files under {processed_folder_path}? (y/n)").strip().lower()
        if answer == 'y':
            for file in processed_folder_path.iterdir():
                file.unlink()
            print(f"All files under {processed_folder_path} are deleted. Proceeding with data processing.")
        else:
            print("Cancelled. Data processing stopped. Please ensure tot run this file at the root folder.")
            return
    else:
        processed_folder_path.mkdir(parents=True, exist_ok=True)
    raw_folder_path = ROOT_PATH / DATA_FOLDER / RAW_FOLDER / str(year)
    if not raw_folder_path.exists():
        print(f"Raw data folder not detected.")
        return
    for file in sorted(raw_folder_path.iterdir(), key = lambda x: x.name):
        print(f"Begin processing {file}")
        _data = pd.read_parquet(file)
        _data = _data[(_data["trip_distance"] > 0.0) & (_data["fare_amount"] > 0.0)
            & (_data["passenger_count"] > 0.0) & (_data["trip_distance"].notna())
            & (_data["fare_amount"].notna()) & (_data["passenger_count"].notna())
            & (_data["tpep_dropoff_datetime"] > _data["tpep_pickup_datetime"])
        ]
        _data["computed_total_amount"] = (
            _data["fare_amount"] + _data["extra"] + _data["mta_tax"]
            + _data["tip_amount"] + _data["tolls_amount"] + _data["improvement_surcharge"]
            + _data["congestion_surcharge"] + _data["Airport_fee"] +  _data["cbd_congestion_fee"]
        )
        _data["pickup_date"] = _data["tpep_pickup_datetime"].dt.date
        _data["pickup_hour"] = _data["tpep_pickup_datetime"].dt.hour
        _data["dropoff_date"] = _data["tpep_dropoff_datetime"].dt.date
        _data["dropoff_hour"] = _data["tpep_dropoff_datetime"].dt.hour
        _data = _data.drop(columns = (['tpep_pickup_datetime','tpep_pickup_datetime','tpep_dropoff_datetime','tpep_dropoff_datetime',
            'fare_amount','extra','mta_tax','tip_amount','tolls_amount','improvement_surcharge','total_amount','congestion_surcharge','Airport_fee','cbd_congestion_fee']))

        path = Path(ROOT_PATH / DATA_FOLDER / PROCESSED_FOLDER / str(year) / 'processed_events.parquet')
        if path.exists():
            existing = pd.read_parquet(path)
            combined = pd.concat([existing, _data], ignore_index=True)
        else:
            combined = _data
        combined.to_parquet(path, index=False)
        print(f"End processing {file}")
process_yearly_data(2025)