import pandas as pd
import os

def load_dataset(data_dir):

    price_data = pd.read_csv(os.path.join(data_dir, 'ercot_hourly_price.csv'))
    price_data['timestamp'] = pd.to_datetime(price_data['timestamp'], dayfirst=True)
    price_data['hour'] = price_data['timestamp'].dt.hour

    load_data = pd.read_csv(os.path.join(data_dir, 'load_hourly_2018.csv')) 
    load_data['time'] = pd.to_datetime(load_data['time'])
    load_data['hour'] = load_data['time'].dt.hour

    return price_data, load_data

def calculate_hourly_profiles(price_data, load_data):
    hourly_prices = price_data.groupby('hour')['Price'].mean().reset_index()

    shiftable_categories = ['air', 'car', 'clotheswasher', 'dishwasher', 'dry']
    load_data['shiftable_load'] = load_data[shiftable_categories].sum(axis=1)

    load_profiles = load_data.groupby(['dataid', 'hour']).agg({'total': 'mean',, 'shiftable_load': 'mean', 'non-shiftable': 'mean'}).reset_index()

    system_load_profile = load_data.groupby('hour').agg({
        'total': 'mean',
        'shiftable_load': 'mean',
        'non-shiftable': 'mean'
        }).reset_index()

    return hourly_prices, load_profiles, system_load_profile

def calculate_price_thresholds(price_data):
    prices = price_data['Price']
    thresholds = {
            'low': np.percentile(prices, 25),
            'medium': np.percentile(prices, 50),
            'high': np.percentile(prices, 75),
            'very_high': np.percentile(prices, 95)
            }
    return threhsolds


    
