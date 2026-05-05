import pandas as pd
import numpy as np

def clean_data():
    # Load raw data
    print("Loading data...")
    df = pd.read_csv('Hotel_bookings_final.csv')
    
    # 1. Standardize Column Names (SQL friendly)
    df.columns = [col.strip().replace(' ', '_').replace('?', '').lower() for col in df.columns]
    
    # 2. Convert Dates
    date_cols = ['booking_date', 'check_in_date', 'check_out_date', 'travel_date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        
    # 3. Feature Engineering for SQL/PBI
    df['stay_duration'] = (df['check_out_date'] - df['check_in_date']).dt.days
    df['lead_time'] = (df['check_in_date'] - df['booking_date']).dt.days
    df['total_margin'] = df['selling_price'] - df['costprice']
    
    # Handle missing stay_duration/lead_time (set to -1 or null)
    # We keep them for now, SQL/PBI can handle nulls
    
    # 4. Data Quality Flags
    df['is_valid_date'] = df['check_in_date'].notna() & (df['stay_duration'] > 0)
    
    # 5. Clean Categorical Data
    df['booking_status'] = df['booking_status'].fillna('Unknown')
    df['room_type'] = df['room_type'].fillna('Unknown')
    
    # 6. Save Cleaned Version
    output_file = 'Hotel_Bookings_Cleaned.csv'
    df.to_csv(output_file, index=False)
    print(f"Data cleaning complete. Exported to {output_file}")

if __name__ == "__main__":
    clean_data()
