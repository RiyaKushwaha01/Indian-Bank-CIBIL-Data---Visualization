
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
    Credit_Score = st.selectbox("Credit Score", ["Federal", "Native American"])
    Total_TL = st.selectbox("Total TL", ["Onshore", "Offshore", "Not Tied to a Lease"])
    Age_Oldest_TL = st.selectbox("Age of Oldest TL", ["Texas","Missouri", "Alaska", "California", "Georgia", "New York", "New Mexico", "Indiana", "Florida", "Washington"])
    enq_L3m = st.selectbox(step = +1 (42))
    num_std_6mts = st.selectbox("Mineral Lease Type", [ "Hardrock","Limestone", "Gold", "Coal", "Silver", "Oil & Gas", "Sulfur", "Gilsonite", "Gypsum", "Sodium", "Phosphate", "Gemstones"])
    num_std_12mts = st.selectbox("Commodity", ["Oil", "Gas", "Coal", "Copper", "Hardrock", "Natural gas liquids", "Gilsonite", "Phosphate", "Oil & gas (pre-production)", "Geothermal"])
    max_recent_level_of_deliq = st.selectbox(step = +1(900))
    Tot_Closed_TL = st.selectbox("Product", ["Nitrogen", "Copper Concentrate","Oil", "Coal Bed Methane", "Coal", "Gas Plant Products", "Calcium Oxide", "Carbon Dioxide Gas (CO2)", "Fuel Gas", "Fuel Oil", "Helium"])
    num_std = 
    enq_L12m = st.selectbox(step = +1 (42))
    tot_enq = 
    PL_enq = 
    PROSPECTID = 
    PL_enq_L12m = 
    enq_L6m = 
    Secured_TL = 
    time_since_recent_enq = 

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
