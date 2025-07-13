import pandas as pd
import os
import json

# === Descriptive Summary Function ===
def describe_dataset(df):
    summary = {}

    # Basic describe (numeric + object)
    summary["basic_stats"] = df.describe(include="all").fillna("").to_dict()

    # Unique value counts and most common for all columns
    for col in df.columns:
        summary[col] = {}
        summary[col]["n_unique"] = df[col].nunique()
        if df[col].dtype == 'object' or df[col].dtype.name == 'category':
            value_counts = df[col].value_counts()
            summary[col]["most_common"] = value_counts.index[0] if not value_counts.empty else None
            summary[col]["frequency"] = int(value_counts.iloc[0]) if not value_counts.empty else 0

    return summary

# === Grouped Summary Function ===
def group_describe(df, group_cols):
    try:
        numeric_cols = df.select_dtypes(include=['number']).columns
        agg_dict = {col: ['mean', 'min', 'max', 'std', 'count'] for col in numeric_cols}
        grouped_summary = df.groupby(group_cols).agg(agg_dict)
        # flatten column names
        grouped_summary.columns = ['_'.join(col).strip() for col in grouped_summary.columns.values]
        return grouped_summary.reset_index().to_dict(orient="list")
    except Exception as e:
        return {"error": str(e)}

# === Analyze One Dataset ===
def analyze_dataset(filepath, output_name):
    print(f"🔍 Processing: {filepath}")
    df = pd.read_csv(filepath)

    summary = {
        "summary_type": "pandas",
        "source_file": filepath,
        "overall": describe_dataset(df)
    }

    if 'page_id' in df.columns:
        summary["grouped_by_page_id"] = group_describe(df, ['page_id'])

    if 'page_id' in df.columns and 'ad_id' in df.columns:
        summary["grouped_by_page_and_ad_id"] = group_describe(df, ['page_id', 'ad_id'])

    os.makedirs("results", exist_ok=True)
    with open(f"results/{output_name}.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"✅ Saved to results/{output_name}.json\n")

# === Main Entry ===
def main():
    base_path = "/Users/mrunalnikam/Desktop/RA/Task_04_Descriptive_Stats/Datasets"

    datasets = {
        "fb_ads": f"{base_path}/2024_fb_ads_president_scored_anon.csv",
        "fb_posts": f"{base_path}/2024_fb_posts_president_scored_anon.csv",
        "tw_posts": f"{base_path}/2024_tw_posts_president_scored_anon.csv"
    }

    for name, path in datasets.items():
        analyze_dataset(path, f"{name}_pandas_summary")

if __name__ == "__main__":
    main()
