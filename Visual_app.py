import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
from io import BytesIO

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

# Check session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    st.set_page_config(page_title="Visualizations", layout="wide")
    st.title("Indian Bank & CIBIL Data - EDA")

    @st.cache_data
    def load_data_from_zip(zip_file):
        with zipfile.ZipFile(zip_file) as z:
            file_names = z.namelist()
            df1 = pd.read_excel(z.open([f for f in file_names if "Internal_Bank_Dataset" in f][0]))
            df2 = pd.read_excel(z.open([f for f in file_names if "External_Cibil_Dataset" in f][0]))
        return df1, df2

    # File uploader
    uploaded_zip = st.file_uploader("Upload ZIP file with Excel datasets", type="zip")

    if uploaded_zip:
        df1, df2 = load_data_from_zip(uploaded_zip)
        st.success("Files loaded successfully!")

        # Show the original dataframes
        st.subheader("Internal Bank Dataset")
        st.write(df1.head())

        st.subheader("External CIBIL Dataset")
        st.write(df2.head())

        # You can apply filters on df1 or df2 as needed
        df = df1  # Example: using df1 for filtering

        # Sidebar filters
        st.sidebar.header("Filter Data")

        EDUCATION = sorted(df["Education Level"].dropna().unique())
        GENDER = sorted(df["Gender"].dropna().unique())
        MARITALSTATUS = sorted(df["MaritalStatus"].dropna().unique())
        LOAN_TYPE = sorted(df["Loan Type"].dropna().unique())
        RISK_CATEGORY = sorted(df["Risk Category"].dropna().unique())
        CREDIT_SCORE_CATEGORY = sorted(df["Credit Score Category"].dropna().unique())

        with st.sidebar.expander("📚 Education Level", expanded=True):
            selected_education = st.multiselect("Select Education Level", options=EDUCATION, default=EDUCATION)

        with st.sidebar.expander("🌍 Gender", expanded=True):
            selected_gender = st.multiselect("Select Gender", options=GENDER, default=GENDER)

        with st.sidebar.expander("💍 Marital Status", expanded=True):
            selected_marital_status = st.multiselect("Select Marital Status", options=MARITALSTATUS, default=MARITALSTATUS)

        with st.sidebar.expander("🏦 Loan Type", expanded=True):
            selected_loan_type = st.multiselect("Select Loan Type", options=LOAN_TYPE, default=LOAN_TYPE)

        with st.sidebar.expander("⚠️ Risk Category", expanded=True):
            selected_risk_category = st.multiselect("Select Risk Category", options=RISK_CATEGORY, default=RISK_CATEGORY)

        with st.sidebar.expander("💳 Credit Score Category", expanded=True):
            selected_credit_score_category = st.multiselect("Select Credit Score Category", options=CREDIT_SCORE_CATEGORY, default=CREDIT_SCORE_CATEGORY)

        # ✅ Apply filters
        filtered_df = df[
            df["Education Level"].isin(selected_education) &
            df["Gender"].isin(selected_gender) &
            df["MaritalStatus"].isin(selected_marital_status) &
            df["Loan Type"].isin(selected_loan_type) &
            df["Risk Category"].isin(selected_risk_category) &
            df["Credit Score Category"].isin(selected_credit_score_category)
        ]

        st.subheader("Filtered Dataset")
        st.dataframe(filtered_df)


    # Function to format numbers in millions or billions
    def format_revenue(value):
        if value >= 1e9:
            return f"${value/1e9:.2f}B"
        elif value >= 1e6:
            return f"${value/1e6:.2f}M"
        else:
            return f"${value:.2f}"
            
    # 1. Distribution of Education Level
    st.subheader("Distribution of Education Level")
    Education_Level = filtered_df.groupby("EDUCATION")["PROSPECTID"].sum().sort_values(ascending = False).reset_index()
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    Education_Level.plot(kind="bar", width=0.7, ax=ax1)
    ax1.set_title("Distribution of Education Level", fontsize=8)
    ax1.tick_params(axis='y', labelsize=6)
    ax1.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax1.patches:
        ax1.annotate(format_education(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    st.pyplot(fig1)


    # 2. Distribution of Gender
    st.subheader("Distribution of Gender")
    Gender_Distribution = df.groupby("GENDER")["PROSPECTID"].sum()  # Changed to df
    fig2, ax2 = plt.subplots(figsize=(2, 2))
    ax2.pie(Gender_Distribution, labels=Gender_Distribution.index, autopct="%.2f%%", startangle=90, wedgeprops={'edgecolor': 'white'})
    ax2.axis("equal")
    ax2.set_title("Distribution of Gender", fontsize=8)
    st.pyplot(fig2)

    # 3. Distribution of Maritalstatus
    st.subheader("Distribution of Maritalstatus")
    MaritalStatus = filtered_df.groupby("MARITALSTATUS")["PROSPECTID"].sum().sort_values(ascending = False).reset_index()
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    MaritalStatus.plot(kind="barh", width=0.7, ax=ax3)
    ax3.set_title("Distribution of Maritalstatus", fontsize=8)
    ax3.tick_params(axis='y', labelsize=6)
    ax3.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax3.patches:
        ax3.annotate(format_MaritalStatus(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    st.pyplot(fig3)

    # 4. Distribution of Loan Type
    st.subheader("Distribution of Loan Type")
    Loan_Type = filtered_df.groupby("first_prod_enq2")["PROSPECTID"].sum().sort_values(ascending = False).reset_index()
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    Loan_Type.plot(kind="barh", width=0.7, ax=ax4)
    ax4.set_title("Distribution of Loan Type", fontsize=8)
    ax4.tick_params(axis='y', labelsize=6)
    ax4.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax4.patches:
        ax4.annotate(format_Loan_Type(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    # 5.  Top 5 Income of Applicants
    st.subheader("Top 5 Income of Applicants")
    Applicants_Income = filtered_df.groupby("NETMONTHLYINCOME")["PROSPECTID"].sum().sort_values(ascending = False).reset_index()
    fig5, ax5 = plt.subplots(figsize=(7, 4))
    Applicants_Income.plot(kind="bar", width=0.7, ax=ax5)
    ax5.set_title("Top 5 Income of Applicants", fontsize=8)
    ax5.tick_params(axis='y', labelsize=6)
    ax5.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax5.patches:
        ax5.annotate(format_Income(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    # 6. Top 10 Credit Score
    st.subheader("Top 10 Credit Scores")
    Credit_Score = filtered_df.groupby("Credit_Score")["PROSPECTID"].sum().sort_values(ascending = False).reset_index()
    fig6, ax6 = plt.subplots(figsize=(7, 4))
    Credit_Score.plot(kind="bar", width=0.7, ax=ax6)
    ax6.set_title("Top 5 Income of Applicants", fontsize=8)
    ax6.tick_params(axis='y', labelsize=6)
    ax6.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax6.patches:
        ax6.annotate(format_Credit_Score(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    # 7. Distribution of Risk Category
    st.subheader("Distribution of Risk Category")
    Risk_Category = df.groupby("Risk_Category")["PROSPECTID"].sum()  # Changed to df
    fig7, ax7 = plt.subplots(figsize=(2, 2))
    ax7.pie(Risk_Category, labels=Risk_Category.index, autopct="%.2f%%", startangle=90, wedgeprops={'edgecolor': 'white'})
    ax7.axis("equal")
    ax7.set_title("Distribution of Risk Category", fontsize=8)
    st.pyplot(fig7)

   # 8. Distribution of Credit Score by Segmentation
    st.subheader("Distribution of Credit Score by Segmentation")
    Credit_Score_Category = filtered_df.groupby("Credit_Score_Category")["PROSPECTID"].sum().sort_values(ascending = False).reset_index()
    fig8, ax8 = plt.subplots(figsize=(7, 4))
    Credit_Score_Category.plot(kind="barh", width=0.7, ax=ax8)
    ax8.set_title("Distribution of Credit Score by Segmentation", fontsize=8)
    ax8.tick_params(axis='y', labelsize=6)
    ax8.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax8.patches:
        ax8.annotate(format_Credit_Score(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')
        
    # 9. Distribution of y column(Approved Flag)
    st.subheader("Distribution of y column(Approved Flag)")
    Approved_Flag = filtered_df.groupby("Approved_Flag")["PROSPECTID"].sum().sort_values(ascending = False).reset_index()
    fig9, ax9 = plt.subplots(figsize=(7, 4))
    Approved_Flag.plot(kind="barh", width=0.7, ax=ax9)
    ax9.set_title("Distribution of y column(Approved Flag)", fontsize=8)
    ax9.tick_params(axis='y', labelsize=6)
    ax9.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax9.patches:
        ax9.annotate(format_Flag(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    # 10. Applicants with a high percentage of missed payments
    st.subheader("Applicants with a high percentage of missed payments)")
    Missed_Payments = ( df1[df1['Tot_Missed_Pmnt'] != 0] .groupby('Tot_Missed_Pmnt')['PROSPECTID'] .count() .sort_values(ascending=False) .to_frame()).head(5)
    fig10, ax10 = plt.subplots(figsize=(7, 4))
    Missed_Payments.plot(kind="barh", width=0.7, ax=ax10)
    ax10.set_title("Applicants with a high percentage of missed payments", fontsize=8)
    ax10.tick_params(axis='y', labelsize=6)
    ax10.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax10.patches:
        ax10.annotate(format_Flag(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    # 11.  Applicants who opened multiple new accounts in the last 6 months
    st.subheader("Applicants who opened multiple new accounts in the last 6 months")
    new_Multiple_Accounts = filtered_df.groupby("Total_TL_opened_L6M")["PROSPECTID"].sum().sort_values(ascending = False).reset_index()
    fig11, ax11 = plt.subplots(figsize=(7, 4))
    new_Multiple_Accounts.plot(kind="barh", width=0.7, ax=ax11)
    ax11.set_title(" Applicants who opened multiple new accounts in the last 6 months", fontsize=8)
    ax11.tick_params(axis='y', labelsize=6)
    ax11.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax11.patches:
        ax11.annotate(format_Flag(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

     # 12. Applicants who Closed multiple accounts in last 6 months
    st.subheader("Applicants who Closed multiple accounts in last 6 months")
    Closed_Multiple_Accounts = filtered_df.groupby("Tot_TL_closed_L6M")["PROSPECTID"].sum().sort_values(ascending = False).reset_index()
    fig12, ax12 = plt.subplots(figsize=(7, 4))
    Closed_Multiple_Accounts.plot(kind="barh", width=0.7, ax=ax12)
    ax12.set_title("Applicants who Closed multiple accounts in last 6 months", fontsize=8)
    ax12.tick_params(axis='y', labelsize=6)
    ax12.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax12.patches:
        ax12.annotate(format_Flag(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

