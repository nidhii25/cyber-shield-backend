import pandas as pd

df = pd.read_json('data/merged_cyberattacks.json')

# Drop useless columns
df.drop(columns=['unnamed:_15'], inplace=True, errors='ignore')

# Handle NaN separately for numeric & text columns
for col in df.select_dtypes(include='number').columns:
    df[col].fillna(0, inplace=True)

for col in df.select_dtypes(include='object').columns:
    df[col].fillna("Unknown", inplace=True)

# Normalize text
df['attack_type'] = df['attack_type'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True).str.strip()
df['category'] = df['category'].str.encode('ascii', 'ignore').str.decode('ascii')

# Safely split category into parts
split_cols = df['category'].str.split('->', n=2, expand=True)
split_cols = split_cols.reindex(columns=range(3))
split_cols.columns = ['main_category', 'sub_category', 'topic']
df = pd.concat([df, split_cols], axis=1)

# Fix data types
df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')
df['financial_loss_(in_million_$)'] = pd.to_numeric(df['financial_loss_(in_million_$)'], errors='coerce')
df['number_of_affected_users'] = pd.to_numeric(df['number_of_affected_users'], errors='coerce')

# Save cleaned version
df.to_json('data/cleaned_cyberattacks.json', orient='records', indent=4)
print("✅ Cleaned dataset saved successfully!")
