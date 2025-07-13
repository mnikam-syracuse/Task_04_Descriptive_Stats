import csv
import math
import statistics
import json
import os
from collections import defaultdict, Counter

# === Load Data ===
def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

# === Type Detection ===
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_column_types(data):
    column_types = {}
    sample = data[0]
    for col in sample:
        values = [row[col] for row in data if row[col] != '']
        if not values:
            column_types[col] = 'unknown'
            continue
        numeric_count = sum(is_float(v) for v in values)
        column_types[col] = 'numeric' if numeric_count / len(values) > 0.9 else 'categorical'
    return column_types

# === Summary Calculations ===
def summarize_numeric(values):
    if not values:
        return {
            "count": 0,
            "mean": None,
            "min": None,
            "max": None,
            "std_dev": None
        }

    float_values = list(map(float, values))
    return {
        "count": len(float_values),
        "mean": sum(float_values) / len(float_values),
        "min": min(float_values),
        "max": max(float_values),
        "std_dev": statistics.stdev(float_values) if len(float_values) > 1 else 0.0
    }

def summarize_categorical(values):
    counter = Counter(values)
    if len(counter) == 0:
        return {
            "count": 0,
            "unique": 0,
            "most_common": None
        }
    return {
        "count": len(values),
        "unique": len(counter),
        "most_common": counter.most_common(1)[0]
    }

def summarize_columns(data, column_types):
    summaries = {}
    for col in data[0].keys():
        values = [row[col] for row in data if row[col] != '']
        if column_types[col] == 'numeric':
            summaries[col] = summarize_numeric(values)
        else:
            summaries[col] = summarize_categorical(values)
    return summaries

# === Grouping ===
def group_by(data, group_keys):
    groups = defaultdict(list)
    for row in data:
        key = tuple(row[k] for k in group_keys)
        groups[key].append(row)
    return groups

def summarize_grouped_data(data, group_keys, column_types):
    grouped = group_by(data, group_keys)
    result = {}
    for group, rows in grouped.items():
        result[str(group)] = summarize_columns(rows, column_types)
    return result

# === Analyze Individual Dataset ===
def analyze_dataset(filepath, output_name):
    print(f"🔍 Analyzing: {filepath}")
    data = load_data(filepath)
    column_types = get_column_types(data)

    overall_summary = summarize_columns(data, column_types)

    group_by_page = summarize_grouped_data(data, ['page_id'], column_types) if 'page_id' in data[0] else {}
    group_by_page_ad = summarize_grouped_data(data, ['page_id', 'ad_id'], column_types) if 'ad_id' in data[0] else {}

    output = {
        "summary_type": "pure_python",
        "source_file": filepath,
        "overall_summary": overall_summary,
        "grouped_by_page_id": group_by_page,
        "grouped_by_page_id_and_ad_id": group_by_page_ad
    }

    os.makedirs("results", exist_ok=True)
    output_path = f"results/{output_name}.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Summary saved to {output_path}\n")

# === Main ===
def main():
    base_path = "/Users/mrunalnikam/Desktop/RA/Task_04_Descriptive_Stats/Datasets"

    datasets = {
        "fb_ads": f"{base_path}/2024_fb_ads_president_scored_anon.csv",
        "fb_posts": f"{base_path}/2024_fb_posts_president_scored_anon.csv",
        "tw_posts": f"{base_path}/2024_tw_posts_president_scored_anon.csv"
    }

    for name, path in datasets.items():
        analyze_dataset(path, f"{name}_summary")

if __name__ == "__main__":
    main()
