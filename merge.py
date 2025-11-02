import pandas as pd

df1=pd.read_csv('data/global.csv')
df2=pd.read_csv('data/defense.csv')

df1.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)
df2.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)
print("DF1 Columns:", df1.columns)
print("DF2 Columns:", df2.columns)

merged_df = pd.merge(df1, df2, on='attack_type', how='outer')


merged_df.fillna({'industry': 'Unknown', 'cause': 'Unknown'}, inplace=True)
merged_df.drop_duplicates(inplace=True)

merged_df.to_csv("data/merged_cyberattacks.csv", index=False)
print("Merged dataset saved!")
merged_df.to_json("data/merged_cyberattacks.json", orient="records", indent=4)

print("✅ Merged dataset saved in both CSV and JSON formats!")