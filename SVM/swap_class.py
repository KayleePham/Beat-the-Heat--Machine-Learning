#This is a test script to change 'CLASS' columns to integers 1 or 0
import pandas as pd
Location = r'C:\Users\strai\Desktop\CA_Wildfires.csv'
df = pd.read_csv(Location)
def swap(x):
    if x == 'Fire':
        x = 1
    else:
        x = 0
    return x
df['CLASS'] = df['CLASS'].apply(swap)
print(df['CLASS'])
df.to_csv(Location)
