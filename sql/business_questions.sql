-- ============================================================
-- business_questions.sql
-- FoodHub Order Analysis — Business Intelligence Queries
-- Database: foodhub | Table: orders
-- ============================================================

USE foodhub;


-- ============================================================
-- Q1. How many total orders does FoodHub have?
-- ============================================================
SELECT
    COUNT(*) AS total_orders
FROM orders;


-- ============================================================
-- Q2. What are the average, minimum, and maximum order values?
-- ============================================================
SELECT
    ROUND(AVG(cost_of_the_order), 2) AS avg_order_value,
    ROUND(MIN(cost_of_the_order), 2) AS min_order_value,
    ROUND(MAX(cost_of_the_order), 2) AS max_order_value
FROM orders
WHERE cost_of_the_order IS NOT NULL;


-- ============================================================
-- Q3. How many unique customers and restaurants are there?
-- ============================================================
SELECT
    COUNT(DISTINCT customer_id)      AS unique_customers,
    COUNT(DISTINCT restaurant_name)  AS unique_restaurants
FROM orders;


-- ============================================================
-- Q4. How many orders does each cuisine type get, with market share %?
-- ============================================================
SELECT
    cuisine_type,
    COUNT(*)                                             AS total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS market_share_pct
FROM orders
GROUP BY cuisine_type
ORDER BY total_orders DESC;


-- ============================================================
-- Q5. What is the total revenue per cuisine?
-- ============================================================
SELECT
    cuisine_type,
    ROUND(SUM(cost_of_the_order), 2)  AS total_revenue,
    COUNT(*)                           AS total_orders,
    ROUND(AVG(cost_of_the_order), 2)  AS avg_order_value
FROM orders
WHERE cost_of_the_order IS NOT NULL
GROUP BY cuisine_type
ORDER BY total_revenue DESC;


-- ============================================================
-- Q6. Which are the top 10 restaurants by number of orders?
-- ============================================================

SELECT
    restaurant_name,
    COUNT(*)                          AS total_orders,
    ROUND(AVG(cost_of_the_order), 2) AS avg_order_value
FROM orders
GROUP BY restaurant_name
ORDER BY total_orders DESC
LIMIT 10;


-- ============================================================
-- Q7. How does performance differ between weekdays and weekends?
-- ============================================================
SELECT
    day_of_the_week,
    COUNT(*)                                              AS total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS pct_of_orders,
    ROUND(AVG(cost_of_the_order), 2)                     AS avg_order_value,
    ROUND(SUM(cost_of_the_order), 2)                     AS total_revenue
FROM orders
WHERE cost_of_the_order IS NOT NULL
GROUP BY day_of_the_week
ORDER BY total_orders DESC;


-- ============================================================
-- Q8. What are the average prep time, delivery time, and total wait time?
-- ============================================================
SELECT
    ROUND(AVG(food_preparation_time), 2) AS avg_prep_time_mins,
    ROUND(AVG(delivery_time), 2)         AS avg_delivery_time_mins,
    ROUND(AVG(food_preparation_time + delivery_time), 2) AS avg_total_wait_mins
FROM orders;


-- ============================================================
-- Q9. Which cuisines are slowest? (highest average total time)
-- ============================================================
SELECT
    cuisine_type,
    ROUND(AVG(food_preparation_time), 2)                  AS avg_prep_mins,
    ROUND(AVG(delivery_time), 2)                          AS avg_delivery_mins,
    ROUND(AVG(food_preparation_time + delivery_time), 2)  AS avg_total_mins
FROM orders
GROUP BY cuisine_type
ORDER BY avg_total_mins DESC;


-- ============================================================
-- Q10. What is the rating breakdown, including "Not given" ratings?
-- ============================================================
SELECT
    rating,
    COUNT(*)                                                   AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY rating
ORDER BY rating;


-- ============================================================
-- Q11. Which restaurants have the highest ratings? (min 10 orders)
-- ============================================================
SELECT
    restaurant_name,
    COUNT(*)                   AS total_orders,
    ROUND(AVG(rating), 2)      AS avg_rating
FROM orders
WHERE rating != 'Not given'
GROUP BY restaurant_name
HAVING total_orders >= 10
ORDER BY avg_rating DESC, total_orders DESC
LIMIT 10;


-- ============================================================
-- Q12. Which orders are "problem orders" (total time over 60 minutes)?
-- ============================================================
SELECT
    order_id,
    restaurant_name,
    cuisine_type,
    food_preparation_time,
    delivery_time,
    (food_preparation_time + delivery_time) AS total_time_mins,
    cost_of_the_order,
    rating
FROM orders
WHERE (food_preparation_time + delivery_time) > 60
ORDER BY total_time_mins DESC;

-- Count of problem orders
SELECT
    COUNT(*) AS problem_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS pct_of_all_orders
FROM orders
WHERE (food_preparation_time + delivery_time) > 60;
