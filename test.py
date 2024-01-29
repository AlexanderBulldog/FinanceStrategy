import pandas as pd
from datetime import datetime, timedelta

file_path = "TRADEDATABTC.gz"
data = pd.read_csv(file_path)

data['timestamp'] = pd.to_datetime(data['timestamp'], unit='us') + timedelta(hours=3)

data['price_x_amount'] = data['price'] * data['amount']

vwap_data = data.groupby('timestamp').agg(
    total_price_x_amount=('price_x_amount', 'sum'),
    total_amount=('amount', 'sum')
).reset_index()

vwap_data['vwap'] = vwap_data['total_price_x_amount'] / vwap_data['total_amount']

data = data.merge(vwap_data[['timestamp', 'vwap']], on='timestamp')

data['side'] = data['side'].apply(lambda x: 1 if x == 'buy' else -1)

data['midprice'] = data['price'].shift(-1)

data['order MO'] = (data['price'] != data['midprice']).astype(int)

new_table = data[['timestamp', 'side', 'vwap', 'order MO', 'amount']]

print(new_table.head(10))
