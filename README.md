# Task_04_Descriptive_Stats

## Overview

This repository implements descriptive statistics and basic visualizations on social-media datasets related to the 2024 U.S. presidential election. You will find three parallel implementations:

- **Pure Python**: `scripts/pure_python_stats.py`  
- **Pandas**: `scripts/pandas_stats.py`  
- **Polars**: `scripts/polars_stats.py`  

All scripts load a CSV, detect numeric vs. categorical columns, compute count, mean, min/max, quartiles (for numeric) or frequency tables (for categorical), and dump JSON summaries into `results/`. A helper script `scripts/visualize_data.py` generates histograms, bar charts, and boxplots.

---

## Repository Structure

```text
Task_04_Descriptive_Stats/
├── LICENSE
├── README.md
├── .gitignore
├── scripts/
│   ├── pure_python_stats.py
│   ├── pandas_stats.py
│   ├── polars_stats.py
│   └── visualize_data.py
├── Datasets/
│   └── 2024_fb_ads_president_scored_anon.csv
│   └── 2024_fb_posts_president_scored_anon.csv
│   └── 2024_tw_posts_president_scored_anon.csv
└── results/
    ├── fb_ads_pure_python_summary.json
    ├── fb_ads_pandas_summary.json
    ├── fb_ads_polars_summary.json
    ├── … (other JSON summaries)
    ├── hist_sentiment.png
    ├── bar_ads_per_page.png
    └── boxplot_impressions.png
```

---

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/<your-username>/Task_04_Descriptive_Stats.git
   cd Task_04_Descriptive_Stats
   ```

2. **Create a virtual environment** (recommended)  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install pandas polars matplotlib seaborn
   ```

---

## Usage

Replace `<DATA_PATH>` with `Datasets/your_filename.csv`.

### 1. Run Descriptive Statistics

```bash
python scripts/pure_python_stats.py --data <DATA_PATH>     # pure Python
python scripts/pandas_stats.py    --data <DATA_PATH>     # Pandas
python scripts/polars_stats.py    --data <DATA_PATH>     # Polars
```

Each script writes a JSON summary to `results/`.

### 2. Generate Visualizations

```bash
python scripts/visualize_data.py --data <DATA_PATH>
```

This creates PNG files in `results/`, including histograms, bar charts, and boxplots for key metrics.

---

## Notes

- **Do not** commit raw data files or large outputs. See `.gitignore`.
- All JSON summaries can be regenerated via the above scripts.
- If you add new analyses or outputs, please update this README accordingly.

---

## License

This project is [MIT-licensed](LICENSE).  

