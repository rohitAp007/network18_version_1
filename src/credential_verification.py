# src/credential_verification.py

import pandas as pd

def load_creators(csv_path='data/creators.csv'):
    """
    Load creators' credentials from a CSV file.
    """
    df = pd.read_csv(csv_path)
    return df

def verify_creator(creator_id, creators_df):
    """
    Verify if a creator is verified.
    """
    creator = creators_df[creators_df['creator_id'] == creator_id]
    if creator.empty:
        return False
    return creator.iloc[0]['verified']

def add_creator(creator_id, creator_name, verified, csv_path='data/creators.csv'):
    """
    Add a new creator to the CSV file.
    """
    new_creator = pd.DataFrame({
        'creator_id': [creator_id],
        'creator_name': [creator_name],
        'verified': [verified]
    })
    df = pd.read_csv(csv_path)
    df = pd.concat([df, new_creator], ignore_index=True)
    df.to_csv(csv_path, index=False)
