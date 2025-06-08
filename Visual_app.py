import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

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

# Helper function for annotations
def format_value(value):
    return f"{int(value):,}"

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    st.set_page_config(page_title="Visualizations", layout="wide")
    st.title("Indian Bank & CIBIL Data - EDA")

    # Load data from local ZIP file
    @st.cache_data
    def load_data_from_zip(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as z:
            file_names = z.namelist()
            df1 = pd.read_excel(z.open([f for f in file_names if "Internal_Bank_Dataset" in f][0]))
            df2 = pd.read_excel(z.open([f for f in file_names if "External_Cibil_Dataset" in f][0]))
        return df1, df2

    zip_file_path = os.path.join(os.getcwd(), "Dataset 1.zip")
    df1, df2 = load_data_from_zip(zip_file_path)

    # Debug: Uncomment to check actual columns in df2
    # st.write(df2.columns.tolist())

    # Sidebar filters
    st.sidebar.header("Filter Data")

    # Correct column names (case sensitive)
    EDUCATION = sorted(df2["EDUCATION"].dropna().unique())
    GENDER = sorted(df2["GENDER"].dropna().unique())  # Fixed from "Gender" to "GENDER"
    MARITALSTATUS = sorted(df2["MARITALSTATUS"].dropna().unique())
    LOAN_TYPE = sorted(df2["first_prod_enq2"].dropna().unique())

    selected_education = st.sidebar.multiselect("📚 Education", EDUCATION, default=EDUCATION)
    selected_gender = st.sidebar.multiselect("🌍 Gender", GENDER, default=GENDER)
    selected_marital_status = st.sidebar.multiselect("💍 Marital Status", MARITALSTATUS, default=MARITALSTATUS)
    selected_loan_type = st.sidebar.multiselect("🏦 Loan Type", LOAN_TYPE, default=LOAN_TYPE)

    filtered_df2 = df2[
        df2["EDUCATION"].isin(selected_education) &
        df2["GENDER"].isin(selected_gender) &   # fixed here too
        df2["MARITALSTATUS"].isin(selected_marital_status) &
        df2["first_prod_enq2"].isin(selected_loan_type)
    ]

    st.subheader("Filtered Data Preview")
    st.dataframe(filtered_df2)

    # Education Distribution
    st.subheader("Distribution of Education")
    edu_data = filtered_df2.groupby("EDUCATION")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    ax1.bar(edu_data["EDUCATION"], edu_data["PROSPECTID"])
    ax1.set_title("Education Distribution", fontsize=10)
    ax1.tick_params(axis='x', labelrotation=45)
    for p in ax1.patches:
        ax1.annotate(format_value(p.get_height()), (p.get_x() + p.get_width() / 2, p.get_height()),
                     ha='center', va='bottom', fontsize=6)
    st.pyplot(fig1)

    # Gender Pie
    st.subheader("Gender Distribution")
    gender_data = filtered_df2["GENDER"].value_counts()  # fixed here too
    fig2, ax2 = plt.subplots(figsize=(3, 3))
    ax2.pie(gender_data, labels=gender_data.index, autopct="%.2f%%", startangle=90)
    ax2.axis("equal")
    st.pyplot(fig2)

    # Marital Status
    st.subheader("Marital Status Distribution")
    marital_data = filtered_df2["MARITALSTATUS"].value_counts().reset_index()
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    ax3.barh(marital_data["index"], marital_data["MARITALSTATUS"])
    ax3.set_title("Marital Status Distribution", fontsize=10)
    for p in ax3.patches:
        ax3.annotate(format_value(p.get_width()), (p.get_width(), p.get_y() + p.get_height() / 2),
                     ha='left', va='center', fontsize=6)
    st.pyplot(fig3)

    # Loan Type
    st.subheader("Loan Type Distribution")
    loan_data = filtered_df2.groupby("first_prod_enq2")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    ax4.barh(loan_data["first_prod_enq2"], loan_data["PROSPECTID"])
    ax4.set_title("Loan Type Distribution", fontsize=10)
    for p in ax4.patches:
        ax4.annotate(format_value(p.get_width()), (p.get_width(), p.get_y() + p.get_height() / 2),
                     ha='left', va='center', fontsize=6)
    st.pyplot(fig4)

    # Income
    st.subheader("Top 5 Applicants by Income")
    income_data = df2.groupby("NETMONTHLYINCOME")["PROSPECTID"].count().sort_values(ascending=False).head(5).reset_index()
    fig5, ax5 = plt.subplots(figsize=(7, 4))
    ax5.bar(income_data["NETMONTHLYINCOME"], income_data["PROSPECTID"])
    ax5.set_title("Top 5 Income Applicants", fontsize=10)
    st.pyplot(fig5)

    # Credit Score
    st.subheader("Top 10 Credit Scores")
    score_data = df2.groupby("Credit_Score")["PROSPECTID"].count().sort_values(ascending=False).head(10).reset_index()
    fig6, ax6 = plt.subplots(figsize=(7, 4))
    ax6.bar(score_data["Credit_Score"], score_data["PROSPECTID"])
    ax6.set_title("Credit Score Distribution", fontsize=10)
    st.pyplot(fig6)

    # Risk Category
    st.subheader("Risk Category Pie")
    risk_data = df1.groupby("Risk_Category")["PROSPECTID"].count()
    fig7, ax7 = plt.subplots(figsize=(3, 3))
    ax7.pie(risk_data, labels=risk_data.index, autopct="%.2f%%", startangle=90)
    ax7.axis("equal")
    st.pyplot(fig7)

    # Credit Score Category
    st.subheader("Credit Score Segmentation")
    seg_data = df1.groupby("Credit_Score_Category")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
    fig8, ax8 = plt.subplots(figsize=(7, 4))
    ax8.barh(seg_data["Credit_Score_Category"], seg_data["PROSPECTID"])
    ax8.set_title("Credit Score Segmentation", fontsize=10)
    st.pyplot(fig8)

    # Approved Flag
    st.subheader("Approved Flag Distribution")
    flag_data = df2.groupby("Approved_Flag")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
    fig9, ax9 = plt.subplots(figsize=(7, 4))
    ax9.barh(flag_data["Approved_Flag"], flag_data["PROSPECTID"])
    ax9.set_title("Approved Flag", fontsize=10)
    st.pyplot(fig9)

    # Missed Payments
    st.subheader("Top Missed Payments")
    missed_data = df1[df1["Tot_Missed_Pmnt"] > 0].groupby("Tot_Missed_Pmnt")["PROSPECTID"].count().sort_values(ascending=False).head(5).reset_index()
    fig10, ax10 = plt.subplots(figsize=(7, 4))
    ax10.barh(missed_data["Tot_Missed_Pmnt"], missed_data["PROSPECTID"])
    ax10.set_title("Top Missed Payments", fontsize=10)
    st.pyplot(fig10)

    # New Accounts
    st.subheader("New Accounts Opened in Last 6 Months")
    new_data = df1.groupby("Total_TL_opened_L6M")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
    fig11, ax11 = plt.subplots(figsize=(7, 4))
    ax11.barh(new_data["Total_TL_opened_L6M"], new_data["PROSPECTID"])
    ax11.set_title("New Accounts in Last 6M", fontsize=10)
    st.pyplot(fig11)

    # Closed Accounts
    st.subheader("Accounts Closed in Last 6 Months")
    closed_data = df1.groupby("Tot_TL_closed_L6M")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
    fig12, ax12 = plt.subplots(figsize=(7, 4))
    ax12.barh(closed_data["Tot_TL_closed_L6M"], closed_data["PROSPECTID"])
    ax12.set_title("Closed Accounts in Last 6M", fontsize=10)
    st.pyplot(fig12)
