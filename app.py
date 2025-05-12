import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Product Recommender", layout="centered")

# ------------------------------
# Load product data
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("popular_products.csv")
    return df

popular_products = load_data()
product_options = popular_products["Description"].tolist()

# ------------------------------
# Title and instructions
# ------------------------------
st.title("🛍️ Product Recommendation System")

st.markdown("""
Select up to 5 products and rate them from 1 to 5.
You'll receive personalized product recommendations and an AI-style explanation.
""")

# ------------------------------
# Show the list of top products
# ------------------------------
st.subheader("📃 List of Popular Products")
st.dataframe(
    popular_products[["Description"]]
    .rename(columns={"Description": "Product Name"})
    .reset_index(drop=True),
    use_container_width=True
)

# ------------------------------
# User Ratings Section
# ------------------------------
st.subheader("⭐ Rate Products")

user_ratings = {}
for i in range(5):
    col1, col2 = st.columns(2)
    with col1:
        product = st.selectbox(f"Product {i+1}", ["None"] + product_options, key=f"product_{i}")
    if product != "None":
        with col2:
            rating = st.slider("Rating (1–5)", 1, 5, key=f"rating_{i}")
            product_code = popular_products[popular_products["Description"] == product]["StockCode"].values[0]
            user_ratings[product_code] = rating

# ------------------------------
# Mock recommendation function
# ------------------------------
def recommend_products(user_ratings, n=5):
    all_products = set(popular_products["StockCode"])
    rated_products = set(user_ratings.keys())
    candidates = list(all_products - rated_products)

    # Assign fake predicted ratings
    top_recs = random.sample(candidates, min(n, len(candidates)))
    return [(pid, round(random.uniform(3.5, 5.0), 2)) for pid in top_recs]

# ------------------------------
# One button, two outcomes
# ------------------------------
button_clicked = st.button("🎯 Get Recommendations")

if button_clicked:
    if user_ratings:
        st.subheader("Your Recommendations")

        top_recs = recommend_products(user_ratings)

        for pid, score in top_recs:
            desc = popular_products[popular_products["StockCode"] == pid]["Description"].values[0]
            st.write(f"**{desc}** — Predicted Rating: {score}")

        st.subheader("🤖 AI Explanation")
        st.write(f"""
        Based on your interest in products like {', '.join([popular_products[popular_products['StockCode'] == k]['Description'].values[0] for k in user_ratings])},
        we identified items that customers with similar preferences also enjoyed. These recommendations are tailored to match your style.
        """)
    else:
        st.warning("Please rate at least one product before requesting recommendations.")