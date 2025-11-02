import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style("whitegrid")

# ----- 0. Load data -----
df = pd.read_json("../data/cleaned_cyberattacks.json")  # adjust path

print("✅ Data loaded successfully.")
print("Columns:", df.columns.tolist())
print("Rows:", len(df))

# ----- 1. Basic fill for NaN safety -----
df["attack_type"] = df["attack_type"].fillna("Unknown").astype(str)
df["country"] = df["country"].fillna("Unknown").astype(str)
df["target_industry"] = df["target_industry"].fillna("Unknown").astype(str)
df["impact"] = df["impact"].fillna("Unknown").astype(str)

# ----- 2. Top 20 Attack Types → Line Chart -----
top_attacks = df["attack_type"].replace("", "Unknown").value_counts().head(20)
top_attacks_perc = (top_attacks / top_attacks.sum()) * 100

plt.figure(figsize=(12, 6))
plt.plot(
    top_attacks_perc.index,
    top_attacks_perc.to_numpy(),
    marker="o",
    linestyle="-",
    color="steelblue"
)
plt.title("Top 20 Cyberattack Types (%)")
plt.xlabel("Attack Type")
plt.ylabel("Percentage")
plt.xticks(rotation=75, ha="right")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# ----- 3. Top 15 Countries → Column Chart -----
if "country" in df.columns:
    top_countries = df.loc[df["country"].str.lower() != "unknown", "country"].value_counts().head(15)
    if len(top_countries) == 0:
        print("No real countries found (all Unknown).")
    else:
        top_countries_perc = (top_countries / top_countries.sum()) * 100
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x=top_countries_perc.index,
            y=top_countries_perc.values,
            color="lightgreen"
        )
        plt.title("Top 15 Countries (%)")
        plt.xlabel("Country")
        plt.ylabel("Percentage")
        plt.xticks(rotation=60, ha="right")
        plt.tight_layout()
        plt.show()

# ----- 4. Top 10 Target Industries -----
if "target_industry" in df.columns:
    top_ind = df.loc[df["target_industry"].str.lower() != "unknown", "target_industry"].value_counts().head(10)
    if len(top_ind) == 0:
        print("No target industries available (all Unknown).")
    else:
        labels = top_ind.index.astype(str).tolist()
        sizes = sizes = top_ind.to_numpy()
        plt.figure(figsize=(8, 8))
        plt.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=140,
            colors=sns.color_palette("pastel", len(labels))
        )
        plt.title("Top 10 Target Industries")
        plt.tight_layout()
        plt.show()

# ----- 5. Scatter Plot: Financial Loss vs. Affected Users -----
if (
    "financial_loss_(in_million_$)" in df.columns
    and "number_of_affected_users" in df.columns
):
    # clean numeric
    df["financial_loss_(in_million_$)"] = pd.to_numeric(df["financial_loss_(in_million_$)"], errors="coerce")
    df["number_of_affected_users"] = pd.to_numeric(df["number_of_affected_users"], errors="coerce")

    # remove zero or missing entries
    scatter_df = df.dropna(subset=["financial_loss_(in_million_$)", "number_of_affected_users"])
    scatter_df = scatter_df[(scatter_df["financial_loss_(in_million_$)"] > 0) & (scatter_df["number_of_affected_users"] > 0)]

    if len(scatter_df) > 0:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=scatter_df,
            x="financial_loss_(in_million_$)",
            y="number_of_affected_users",
            hue="attack_type",
            alpha=0.7
        )
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Financial Loss (Million $) [log scale]")
        plt.ylabel("Number of Affected Users [log scale]")
        plt.title("Financial Loss vs Affected Users by Attack Type")
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Attack Type")
        plt.tight_layout()
        plt.show()
    else:
        print("Not enough valid data for scatter plot.")
# 4️⃣ Attack vs Impact (fallback to text impact)
if "impact" in df.columns:
    impact_counts = df["impact"].value_counts().head(15)
    if len(impact_counts) > 0:
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x=impact_counts.to_numpy(),
            y=impact_counts.index.to_numpy(),
            color="salmon"
        )
        plt.title("Top 15 Impact Descriptions (Counts)")
        plt.xlabel("Count")
        plt.ylabel("Impact Description")
        plt.tight_layout()
        plt.show()

# ----- 6. Correlation Heatmap -----
num_cols = df.select_dtypes(include=[np.number]).columns
if len(num_cols) > 0:
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Correlation Heatmap of Numerical Features")
    plt.tight_layout()
    plt.show()
else:
    print("No numeric columns available for correlation heatmap.")
