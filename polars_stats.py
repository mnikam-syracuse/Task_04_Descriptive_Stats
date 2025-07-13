import polars as pl
import os
import json

# === Descriptive Summary Function ===
def describe_dataset(df):
    summary = {}

    # Basic describe
    try:
        stats = df.describe()
        summary["basic_stats"] = stats.to_dict(as_series=False)
    except Exception as e:
        summary["basic_stats"] = {"error": str(e)}

    # Additional unique & most frequent values
    for col in df.columns:
        summary[col] = {}
        try:
            summary[col]["n_unique"] = df[col].n_unique()
            value_counts = df[col].value_counts().sort("counts", descending=True)
            if value_counts.shape[0] > 0:
                summary[col]["most_common"] = value_counts[0, col]
                summary[col]["frequency"] = int(value_counts[0, "counts"])
            else:
                summary[col]["most_common"] = None
                summary[col]["frequency"] = 0
        except:
            summary[col]["n_unique"] = None
            summary[col]["most_common"] = None
            summary[col]["frequency"] = None

    return summary

# === Grouped Summary Function ===
def group_describe(df, group_cols):
    try:
        grouped = df.group_by(group_cols).agg([
            pl.all().mean().suffix("_mean"),
            pl.all().min().suffix("_min"),
            pl.all().max().suffix("_max"),
            pl.all().std().suffix("_std"),
            pl.all().count().suffix("_count")
        ])
        return grouped.to_dict(as_series=False)
    except Exception as e:
        return {"error": str(e)}

# === Analyze One Dataset ===
def analyze_dataset(filepath, output_name):
    print(f"🔍 Processing: {filepath}")
    df = pl.read_csv(filepath)

    summary = {
        "summary_type": "polars",
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
        analyze_dataset(path, f"{name}_polars_summary")

if __name__ == "__main__":
    main()
