#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


DTYPES = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "str",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

PARSE_DATES = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--url-prefix', default='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/', help='URL prefix for downloading data')
@click.option('--db-name', default='yellow_tripdata_2021-01.csv.gz', help='Database file name to download')
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--pg-table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunk-size', default=100000, type=int, help='Number of rows per chunk')
def run(url_prefix, db_name, pg_user, pg_pass, pg_host, pg_port, pg_db, pg_table, chunk_size):
    """Download and ingest NYC taxi data into PostgreSQL."""
    try:
        full_url = url_prefix + db_name
        click.echo(f"Downloading from: {full_url}")
        
        # Build connection string
        db_url = f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
        click.echo(f"Connecting to: {pg_host}:{pg_port}/{pg_db}")
        
        engine = create_engine(db_url)

        click.echo(f"Reading CSV and creating chunks of {chunk_size} rows...")
        df_iter = pd.read_csv(
            filepath_or_buffer=full_url,
            dtype=DTYPES,
            parse_dates=PARSE_DATES,
            iterator=True,
            chunksize=chunk_size,
        )
        

        click.echo(f"Ingesting data...")
        chunk_count = 0
        for df_chunk in tqdm(df_iter, desc="Ingesting chunks"):
            if chunk_count == 0:
                df_chunk.head(0).to_sql(
                    name=pg_table,
                    con=engine,
                    if_exists='replace'
                )
                click.echo(f"Table '{pg_table} created'")
            
            df_chunk.to_sql(
                name=pg_table,
                con=engine,
                if_exists='append',
            )
            chunk_count += 1
        
        click.echo(f"Ingestion complete! ({chunk_count} chunks processed)")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    run()




