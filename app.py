import json
import os

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_resource
def load_model():
    return joblib.load(os.path.join(BASE_DIR, 'outputs', 'model.pkl'))


@st.cache_data
def load_cuisine_map():
    with open(os.path.join(BASE_DIR, 'outputs', 'cuisine_encoding.json')) as f:
        return json.load(f)


@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(BASE_DIR, 'data', 'foodhub_powerbi.csv'))


def encode_cost_bucket(cost):
    if cost <= 15:
        return 0
    elif cost <= 25:
        return 1
    return 2


st.set_page_config(page_title='FoodHub Analysis', layout='wide')
st.title('FoodHub Delivery Analysis')

tab_eda, tab_predict = st.tabs(['EDA Dashboard', 'Rating Predictor'])

with tab_eda:
    df = load_data()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total Orders', f"{len(df):,}")
    col2.metric('Avg Order Value', f"${df['cost_of_the_order'].mean():.2f}")
    col3.metric('Avg Delivery Time', f"{df['delivery_time'].mean():.1f} min")
    rated = df.dropna(subset=['rating'])
    col4.metric('% Good Ratings (≥4)', f"{(rated['rating'] >= 4).mean() * 100:.1f}%")

    st.divider()

    charts = [
        ('chart1_revenue_by_cuisine.png', 'Revenue by Cuisine'),
        ('chart2_delivery_time_distribution.png', 'Delivery Time Distribution'),
        ('chart3_rating_heatmap.png', 'Rating Heatmap'),
        ('chart4_correlation_matrix.png', 'Correlation Matrix'),
    ]
    chart_dir = os.path.join(BASE_DIR, 'outputs')
    c1, c2 = st.columns(2)
    for i, (fname, title) in enumerate(charts):
        (c1 if i % 2 == 0 else c2).image(
            os.path.join(chart_dir, fname), caption=title, width='stretch'
        )

with tab_predict:
    st.subheader('Predict Order Rating')
    st.caption('Estimate whether an order will receive a good rating (≥ 4 stars) based on order details.')

    model = load_model()
    cuisine_map = load_cuisine_map()

    col1, col2 = st.columns(2)
    with col1:
        cuisine = st.selectbox('Cuisine Type', options=sorted(cuisine_map.keys()))
        cost = st.slider('Order Cost ($)', min_value=4.5, max_value=35.5, value=16.5, step=0.5)
        is_weekend = st.radio('Day Type', ['Weekend', 'Weekday'], horizontal=True) == 'Weekend'
    with col2:
        prep_time = st.slider('Food Prep Time (min)', min_value=20, max_value=35, value=27)
        delivery_time = st.slider('Delivery Time (min)', min_value=15, max_value=33, value=24)
        total_time = prep_time + delivery_time
        st.metric('Total Time', f'{total_time} min')

    if st.button('Predict Rating', type='primary'):
        X = [[
            cost,
            prep_time,
            delivery_time,
            total_time,
            int(is_weekend),
            cuisine_map[cuisine],
            encode_cost_bucket(cost),
        ]]
        prediction = model.predict(X)[0]
        prob_good = model.predict_proba(X)[0][1]

        if prediction == 1:
            st.success(f'Good Rating Likely (≥ 4 ★) — {prob_good * 100:.0f}% confidence')
        else:
            st.warning(f'Low Rating Risk (< 4 ★) — {(1 - prob_good) * 100:.0f}% confidence')
