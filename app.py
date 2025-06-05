
import streamlit as st
import numpy as np
import pandas as pd
import pickle

# --- Login Section ---
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "User" and password == "User@123":
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password")

# Session authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
        
    # --- Revenue Prediction App ---
    st.title("Revenue Prediction App")
    st.header("Enter Feature Values")
        
    # Input fields for each feature
    land_class = st.selectbox("Land Class", ["Federal", "Native American"])
    land_category = st.selectbox("Land Category", ["Onshore", "Offshore", "Not Tied to a Lease"])
    state = st.selectbox("State", ["Texas","Missouri", "Alaska", "California", "Georgia", "New York", "New Mexico", "Indiana", "Florida", "Washington"])
    revenue_type = st.selectbox("Royalties", ["Royalty", "Bonus", "Rent", "Inspection fees", "Civil penalties", "Other revenue"])
    lease_type = st.selectbox("Mineral Lease Type", [ "Hardrock","Limestone", "Gold", "Coal", "Silver", "Oil & Gas", "Sulfur", "Gilsonite", "Gypsum", "Sodium", "Phosphate", "Gemstones"])
    commodity = st.selectbox("Commodity", ["Oil", "Gas", "Coal", "Copper", "Hardrock", "Natural gas liquids", "Gilsonite", "Phosphate", "Oil & gas (pre-production)", "Geothermal"])
    county = st.selectbox("County", ["Carbon","Iron", "Eddy", "Sweet Water", "Bannock", "Goshen", "Cleveland", "Franklin", "Washington", "Chambers"])
    product = st.selectbox("Product", ["Nitrogen", "Copper Concentrate","Oil", "Coal Bed Methane", "Coal", "Gas Plant Products", "Calcium Oxide", "Carbon Dioxide Gas (CO2)", "Fuel Gas", "Fuel Oil", "Helium"])

    # Collect input in a DataFrame
    input_data = pd.DataFrame([{
        "Land Class": land_class,
        "Land Category": land_category,
        "State": state,
        "Revenue Type": revenue_type,
        "Mineral Lease Type": lease_type,
        "Commodity": commodity,
        "County": county,
        "Product": product
    }])

    # Load the CatBoost model  
    with open("Model.pkl", "rb") as f:
         model = pickle.load(f)

    # Predict and display result
    if st.button("Predict Revenue"):
        prediction =  model.predict(input_data)
        st.success(f"Estimated Revenue: ${prediction[0]:,.2f}")

        st.markdown("""
        <hr>
        <small>Developed with ❤️ using Streamlit</small>
        """, unsafe_allow_html=True)
