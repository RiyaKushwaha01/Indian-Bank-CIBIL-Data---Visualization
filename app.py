
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
    Credit_Score = st.number_input("Credit Score",start = 400 ,step= 20)
    Total_TL = st.number_input("Total TL", step=0.1)
    Age_Oldest_TL = st.number_input("Age of Oldest TL", step=0.1)
    num_std_6mts = st.number_input("Number of Standard Accounts in 6M", step=0.1)
    num_std_12mts = st.number_input("Number of Standard Accounts in 12M", step=0.1)
    max_recent_level_of_deliq =st.number_input("Maximum level of delinquency in recent times", step=0.1)
    Tot_Closed_TL = st.number_input("Total Closed TL", step=0.1)
    num_std = st.number_input("Number of standard accounts", step=0.1)
    enq_L12m = st.number_input("Total enquires in Last 12 months", step=0.1)
    tot_enq = st.number_input("Total Enquiry", step=0.1) 
    PL_enq = st.number_input("Personal Loan Enquiry", step=0.1)
    PROSPECTID = st.number_input("Applicant ID", step=0.1)
    PL_enq_L12m = st.number_input("Personal Loan enquiry in Last 12 months", step=0.1)
    enq_L6m = st.number_input("Enquiry in last 6 months", step=0.1)
    Secured_TL = st.number_input("Secured TL", step=0.1)
    time_since_recent_enq = st.number_input("Days since the most recent enquiry", step=0.1)
  

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
