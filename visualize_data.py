import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv("Datasets/2024_fb_ads_president_scored_anon.csv")

print("Columns:", df.columns.tolist())

os.makedirs("results", exist_ok=True)

# 1. Histogram of sentiment or sentiment_score
sent_col = next((col for col in df.columns if 'sentiment' in col.lower()), None)
if sent_col:
    plt.figure(figsize=(8, 5))
    sns.histplot(df[sent_col], bins=30, kde=True)
    plt.title(f"Distribution of {sent_col}")
    plt.xlabel(sent_col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("results/hist_sentiment.png")
    plt.close()

# 2. Bar chart: Number of Ads per Page
page_col = next((col for col in df.columns if 'page' in col.lower()), None)
if page_col:
    plt.figure(figsize=(10, 6))
    top_pages = df[page_col].value_counts().head(10)
    sns.barplot(x=top_pages.index.astype(str), y=top_pages.values)
    plt.title("Top 10 Pages by Number of Ads")
    plt.xticks(rotation=45)
    plt.xlabel(page_col)
    plt.ylabel("Ad Count")
    plt.tight_layout()
    plt.savefig("results/bar_ads_per_page.png")
    plt.close()

# 3. Boxplot of impressions by page
impress_col = next((col for col in df.columns if 'impression' in col.lower()), None)
if impress_col and page_col:
    plt.figure(figsize=(12, 6))
    top5 = df[page_col].value_counts().nlargest(5).index
    sns.boxplot(x=page_col, y=impress_col, data=df[df[page_col].isin(top5)])
    plt.title("Impressions by Page")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("results/boxplot_impressions.png")
    plt.close()

print("✅ Visualizations saved to results/")
