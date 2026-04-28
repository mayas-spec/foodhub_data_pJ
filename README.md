# FoodHub Order Analysis

End-to-end data analysis project on FoodHub's food delivery order data. Covers data ingestion, SQL business analysis, exploratory data analysis, visualisation, and predictive modelling.

## Stack

- **Python** — pandas, scikit-learn, matplotlib, seaborn
- **MySQL** — via SQLAlchemy and PyMySQL
- **Jupyter** — EDA and ML notebook
- **Power BI** — cleaned dataset exported for dashboard use

## Project Structure

```
foodhub_data_project1/
├── load_data.py              # Loads Excel data into MySQL
├── sql/
│   └── business_questions.sql  # 12 business intelligence queries
├── notebooks/
│   └── eda_and_ml.ipynb      # EDA, visualisation, and ML models
├── charts/                   # Exported chart PNGs
├── data/
│   ├── foodhub_order_v2.xlsx # Raw source data
│   └── foodhub_powerbi.csv   # Cleaned export for Power BI
├── requirements.txt
└── .env.example
```

## Setup

**1. Clone and install dependencies**
```bash
git clone <repo-url>
cd foodhub_data_project1
pip install -r requirements.txt
```

**2. Configure credentials**
```bash
cp .env.example .env
# Edit .env and set your MySQL credentials
```

**3. Load data into MySQL**
```bash
python load_data.py
```

**4. Run the notebook**
```bash
jupyter notebook notebooks/eda_and_ml.ipynb
```

## SQL Analysis

Twelve business questions answered in [`sql/business_questions.sql`](sql/business_questions.sql), including:

- Order volume and revenue by cuisine type and day of week
- Top restaurants by order count and average rating
- Average prep, delivery, and total wait times by cuisine
- Customer rating distribution (including unrated orders)
- Identification of "problem orders" exceeding 60 minutes total time

## Exploratory Data Analysis

Eight charts covering order distribution, cost patterns, timing breakdowns, and customer ratings. All saved to [`charts/`](charts/).

| Chart | Description |
|-------|-------------|
| chart1 | Orders by cuisine type |
| chart2 | Weekday vs weekend order split |
| chart3 | Order cost distribution with mean/median |
| chart4 | Prep time vs delivery time by cuisine (scatter) |
| chart5 | Average total wait time by cuisine (stacked bar) |
| chart6 | Customer rating distribution |
| chart7 | Actual vs predicted delivery time (both models) |
| chart8 | Random Forest feature importance |

## Machine Learning

Predicts delivery time using four features: cuisine type, day of week, order cost, and food preparation time.

| Model | MAE (minutes) | R² |
|-------|--------------|-----|
| Linear Regression | 3.56 | 0.29 |
| Random Forest (100 trees) | 3.82 | 0.12 |

Linear Regression outperformed Random Forest on both metrics for this dataset. The low R² across both models indicates that delivery time is largely driven by factors not present in the data (e.g. traffic, driver availability), which is itself a meaningful analytical finding.

**Key finding:** Food preparation time is the strongest predictor of delivery time, as shown by the Random Forest feature importance chart.

## Data Cleaning

- Removed stray whitespace from `cost_of_the_order` and coerced to numeric
- Converted `rating` to numeric; "Not given" entries treated as `NaN`
- Engineered `total_time` (prep + delivery) and `is_rated` boolean columns
