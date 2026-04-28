# FoodHub Delivery Analysis

Exploratory analysis and machine learning project on food delivery order data.
I used this dataset to practice end-to-end data science — from loading raw data into MySQL,
cleaning it, visualising trends, and building a classifier to predict whether an order
will receive a good rating.

## Tech Stack
Python · MySQL · mysql-connector-python · pandas · scikit-learn · seaborn · Jupyter

## Project Structure
```
data/          # raw CSV (not committed — see .env.example for setup)
database/      # schema and SQL business queries
notebooks/     # EDA notebook with charts
src/           # Python modules (ingestion, cleaning, ML model)
outputs/       # saved charts and trained model
```

## How to Run

```bash
# 1. create and activate virtual environment
python -m venv venv && source venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt

# 3. copy env file and fill in your MySQL credentials
cp .env.example .env

# 4. load the CSV into MySQL
python src/db_connection.py

# 5. run EDA notebook
jupyter notebook notebooks/eda.ipynb

# 6. train the model
python src/ml_model.py
```

## Key Findings

- **American cuisine dominates revenue** — $9,530 in total orders, nearly 25% more than Japanese ($7,647) in second place
- **Weekend orders are 2.5x more frequent** than weekday orders (1,349 vs 547), but average spend is almost identical (~$16.50), meaning it's volume not budget that drives weekend revenue
- **Korean food is delivered fastest** (avg 20.9 min) while Vietnamese is slowest (26.1 min) — a 5-minute gap worth investigating further
- **38.7% of orders have no rating** (735 out of 1,896), which made imputation a key cleaning step — I filled missing values with the median rating per cuisine type
- **30% of orders had delivery time longer than food prep time**, suggesting delivery logistics is a bigger bottleneck than kitchen speed
- **Shake Shack is the top restaurant by revenue** ($3,579), more than 1.6x the second-place restaurant

## Model Performance

I trained a Random Forest classifier to predict whether an order gets a good rating (≥ 4 stars).

| Metric | Score |
|--------|-------|
| Accuracy | 82% |
| Weighted F1 | 0.78 |

**Note on class imbalance:** The dataset is heavily skewed toward good ratings (86% of rated orders score ≥ 4). The model reflects this — it's good at identifying high-rated orders but struggles with low-rated ones. A next step would be applying SMOTE or adjusting class weights to improve recall on the minority class.

Features used: order cost, food prep time, delivery time, total time, weekend flag, cuisine type, cost bucket.
