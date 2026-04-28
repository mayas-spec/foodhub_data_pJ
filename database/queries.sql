-- 1. Top 10 restaurants by revenue
SELECT restaurant_name, SUM(cost_of_the_order) AS total_revenue
FROM orders GROUP BY restaurant_name
ORDER BY total_revenue DESC LIMIT 10;

-- 2. Average delivery time by cuisine
SELECT cuisine_type, ROUND(AVG(delivery_time), 2) AS avg_delivery
FROM orders GROUP BY cuisine_type ORDER BY avg_delivery;

-- 3. Rating distribution
SELECT rating, COUNT(*) AS count
FROM orders WHERE rating IS NOT NULL
GROUP BY rating ORDER BY rating;

-- 4. Weekend vs Weekday order volume & avg spend
SELECT day_of_the_week,
       COUNT(*) AS orders,
       ROUND(AVG(cost_of_the_order), 2) AS avg_spend
FROM orders GROUP BY day_of_the_week;

-- 5. Orders where delivery took longer than prep
SELECT COUNT(*) AS slow_deliveries
FROM orders WHERE delivery_time > food_preparation_time;