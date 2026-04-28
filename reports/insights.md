# Key Insights — FoodHub Delivery Analysis

## Data Overview
- 1,896 orders across 14 cuisine types and multiple restaurants
- 38.7% of orders (735) had no rating submitted — missing values were imputed using the median rating per cuisine type

## Revenue
- American cuisine generated the most revenue ($9,531), accounting for nearly a quarter of total order value
- Shake Shack was the top-earning restaurant ($3,580), over 1.6x more than second-place The Meatball Shop ($2,145)
- Italian and Japanese rounded out the top 3 cuisines by revenue

## Order Patterns
- 71% of orders were placed on weekends (1,349 vs 547 weekday orders)
- Despite the volume gap, average spend was almost identical — $16.58 on weekends vs $16.31 on weekdays, suggesting customers don't spend more just because it's the weekend

## Delivery Performance
- Korean cuisine had the fastest average delivery time (20.9 min), while Vietnamese was slowest (26.1 min) — a nearly 6-minute gap
- 30% of all orders had a delivery time longer than the food preparation time, pointing to last-mile logistics as the main bottleneck rather than kitchen speed

## Ratings
- Average rating across all orders was 4.47 out of 5, with 86% of rated orders scoring 4 or above
- The heavy skew toward positive ratings made predicting low ratings difficult — a known limitation of the classifier

## Model
- A Random Forest classifier was trained to predict whether an order receives a good rating (≥ 4 stars)
- Achieved 82% accuracy on the test set
- Features: order cost, food prep time, delivery time, total time, weekend flag, cuisine type, cost bucket
- Class imbalance (very few low-rated orders) is the main limitation — future work could apply SMOTE or tune class weights to improve recall on poor ratings
