CREATE DATABASE IF NOT EXISTS foodhub;
USE foodhub;

CREATE TABLE IF NOT EXISTS orders (
    order_id              BIGINT PRIMARY KEY,
    customer_id           BIGINT,
    restaurant_name       VARCHAR(255),
    cuisine_type          VARCHAR(100),
    cost_of_the_order     DECIMAL(10,2),
    day_of_the_week       VARCHAR(20),
    rating                FLOAT,
    food_preparation_time INT,
    delivery_time         INT,
    total_time            INT,
    is_rated              BOOLEAN
);