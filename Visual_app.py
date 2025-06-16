import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

# Set page config at the very top before any Streamlit calls
st.set_page_config(page_title="Visualizations", layout="wide")

# --- Login Section ---
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "Riya" and password == "Riya@123":
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
    st.title("💳 EDA Dashboard: CIBIL Scores & Indian Banking Trends")

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

    # Sidebar filters
    st.sidebar.header("Filter Data")
    EDUCATION = sorted(df2["EDUCATION"].dropna().unique())
    GENDER = sorted(df2["GENDER"].dropna().unique())
    MARITALSTATUS = sorted(df2["MARITALSTATUS"].dropna().unique())
    LOAN_TYPE = sorted(df2["first_prod_enq2"].dropna().unique())

    selected_education = st.sidebar.multiselect("📚 Education", EDUCATION, default=EDUCATION)
    selected_gender = st.sidebar.multiselect("🌍 Gender", GENDER, default=GENDER)
    selected_marital_status = st.sidebar.multiselect("💍 Marital Status", MARITALSTATUS, default=MARITALSTATUS)
    selected_loan_type = st.sidebar.multiselect("🏦 Loan Type", LOAN_TYPE, default=LOAN_TYPE)

    filtered_df2 = df2[
        df2["EDUCATION"].isin(selected_education) &
        df2["GENDER"].isin(selected_gender) &
        df2["MARITALSTATUS"].isin(selected_marital_status) &
        df2["first_prod_enq2"].isin(selected_loan_type)
    ]

    # 1. Education Distribution
    st.subheader("Distribution of Education")
    try:
        edu_data = filtered_df2.groupby("EDUCATION")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        bars = ax1.bar(edu_data["EDUCATION"], edu_data["PROSPECTID"], color='skyblue', edgecolor='black')
        ax1.set_title("Education Distribution", fontsize=10)
        ax1.tick_params(axis='x', labelrotation=45)
        ax1.tick_params(axis='y', labelsize=6)
        ax1.tick_params(axis='x', labelsize=6)
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(format_value(height),
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3), textcoords="offset points",
                         ha='center', va='bottom', fontsize= 7)
        st.pyplot(fig1)
        plt.close(fig1)
    except Exception as e:
        st.error(f"An error occurred while plotting the Education Distribution graph: {e}")

    # 2. Gender Pie
    st.subheader("Gender Distribution")
    gender_data = filtered_df2["GENDER"].value_counts()
    # Use a slightly larger figure for clarity, but render tightly
    fig2, ax2 = plt.subplots(figsize=(1, 1), dpi=400)  # High DPI for sharpness
    ax2.pie(gender_data,labels=gender_data.index,autopct="%.2f%%",startangle=90,textprops={'fontsize': 3})  # Small but readable
    # Equal aspect ratio ensures a circle
    ax2.axis("equal")
    st.pyplot(fig2, bbox_inches="tight")
    plt.close(fig2)


    # 3. Marital Status Distribution
    st.subheader("Marital Status Distribution")
    marital_data = filtered_df2["MARITALSTATUS"].value_counts().reset_index()
    marital_data.columns = ["MARITALSTATUS", "Count"]
    fig3, ax3 = plt.subplots(figsize=(6, 3))
    bars = ax3.barh(marital_data["MARITALSTATUS"], marital_data["Count"], color='lightgreen', edgecolor='black')
    ax3.set_title("Distribution of MartitalStatus", fontsize=10)
    for bar in bars:
        ax3.annotate(format_value(bar.get_width()),
                     xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                     ha='left', va='center', fontsize=6)
    st.pyplot(fig3)
    plt.close(fig3)

    # 4. Loan Type Distribution
    st.subheader("Loan Type Distribution")
    loan_data = filtered_df2.groupby("first_prod_enq2")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
    fig4, ax4 = plt.subplots(figsize=(6, 3))
    bars = ax4.barh(loan_data["first_prod_enq2"], loan_data["PROSPECTID"], color='orange', edgecolor='black')
    ax4.set_title("Loan Type Distribution", fontsize=10)
    for bar in bars:
        ax4.annotate(format_value(bar.get_width()),
                     xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                     ha='left', va='center', fontsize= 7)
    st.pyplot(fig4)
    plt.close(fig4)

    # 5. Top 5 Applicants by Income
    st.subheader("Top 5 Applicants by Income")
    income_data = df2.groupby("NETMONTHLYINCOME")["PROSPECTID"].count().sort_values(ascending=False).head(5).reset_index()
    fig5, ax5 = plt.subplots(figsize=(6, 3))
    bars = ax5.bar(income_data["NETMONTHLYINCOME"].astype(str), income_data["PROSPECTID"], color='magenta', edgecolor='black')
    ax5.set_title("Top 5 Income Applicants", fontsize=10)
    ax5.tick_params(axis='y', labelsize=6)
    ax5.tick_params(axis='x', labelsize=6)

    # Annotate bars (data labels in the middle)
    for bar in bars:
        height = bar.get_height()
        ax5.annotate(f"{height}",
                     xy=(bar.get_x() + bar.get_width() / 2, height / 2),
                     ha='center', va='center', fontsize=8, color='white')

    st.pyplot(fig5)
    plt.close(fig5)


    # 6. Top 10 Credit Scores
    st.subheader("Top 10 Credit Scores")
    score_data = df2.groupby("Credit_Score")["PROSPECTID"].count().sort_values(ascending=False).head(10).reset_index()
    fig6, ax6 = plt.subplots(figsize=(6, 3))

    bars = ax6.bar(score_data["Credit_Score"].astype(str), score_data["PROSPECTID"], color='purple', edgecolor='black')
    ax6.set_title("Credit Score Distribution", fontsize=10)
    ax6.tick_params(axis='y', labelsize=6)
    ax6.tick_params(axis='x', labelsize=6)

    # Annotate bars (data labels in the middle)
    for bar in bars:
        height = bar.get_height()
        ax6.annotate(f"{height}",
                     xy=(bar.get_x() + bar.get_width() / 2, height / 2),
                     ha='center', va='center', fontsize=7, color='white')

    st.pyplot(fig6)
    plt.close(fig6)


    # Create Risk_Category column
    df1['Risk_Category'] = df1['Tot_Missed_Pmnt'].apply(
        lambda x: 'High Risk' if x > 5 else 'Medium Risk' if 2 <= x <= 5 else 'Low Risk'
    )

    # 7. Risk Category Pie
    st.subheader("Risk Category Distribution")
    risk_data = df1.groupby("Risk_Category")["PROSPECTID"].count()
    fig7, ax7 = plt.subplots(figsize=(1, 1), dpi=300)  # Higher DPI for clarity
    ax7.pie(risk_data,labels=risk_data.index,autopct="%.2f%%",startangle=90,textprops={'fontsize': 5},labeldistance=1.1,   # Push category labels out
    pctdistance=0.75     # Adjust position of % labels inside slices
    )
    ax7.axis("equal")  # Equal aspect ratio to maintain circle
    st.pyplot(fig7, bbox_inches="tight")
    plt.close(fig7)


    # Create Credit Score Category column
    def categorize_credit_score(score):
        if score < 580:
            return 'Poor (<580)'
        elif 580 <= score <= 669:
            return 'Fair (580-669)'
        elif 670 <= score <= 739:
            return 'Good (670-739)'
        elif 740 <= score <= 799:
            return 'Very Good (740-799)'
        else:
            return 'Excellent (800+)'

    df2['Credit_Score_Category'] = df2['Credit_Score'].apply(categorize_credit_score)

    # 8. Credit Score Segmentation
    st.subheader("Credit Score Segmentation")
    # Group data
    seg_data = df2.groupby("Credit_Score_Category")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
    # Plot
    fig8, ax8 = plt.subplots(figsize=(6, 3))
    bars = ax8.barh(seg_data["Credit_Score_Category"], seg_data["PROSPECTID"], color='teal', edgecolor='black')
    ax8.set_title("Credit Score Segmentation", fontsize=10)

    # Add data labels to bars
    for bar in bars:
        width = bar.get_width()
        ax8.annotate(f"{int(width)}",  # or use format_value(width) if you have a formatter
                     xy=(width, bar.get_y() + bar.get_height() / 2),
                     xytext=(5, 0),  # slight right offset
                     textcoords="offset points",
                     ha='left', va='center', fontsize=7, color='black')
    # Show in Streamlit
    st.pyplot(fig8)
    plt.close(fig8)


    # 9. Approved Flag Distribution
    st.subheader("Approved Flag Distribution")
    flag_data = df2.groupby("Approved_Flag")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
    fig9, ax9 = plt.subplots(figsize=(6, 3))
    bars = ax9.barh(flag_data["Approved_Flag"], flag_data["PROSPECTID"], color='brown', edgecolor='black')

    ax9.set_title("Approved Flag", fontsize=10)
    max_width = flag_data["PROSPECTID"].max()
    ax9.set_xlim(0, max_width * 1.15)  # Add 15% padding for better label spacing
    ax9.tick_params(axis='y', labelsize=6)
    ax9.tick_params(axis='x', labelsize=6)
    # Annotate each bar (always to the right of the bar for visibility)
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width + (max_width * 0.015)  # Offset to the right of the bar
        ax9.annotate(f"{int(width):,}",
                     xy=(label_x_pos, bar.get_y() + bar.get_height() / 2),
                     ha='left', va='center', fontsize=7, color='black')

    # Improve layout
    fig9.tight_layout()
    st.pyplot(fig9)
    plt.close(fig9)

    # 10. Top Missed Payments
    st.subheader("Top Missed Payments")
    # Prepare data
    missed_data = (df1[df1["Tot_Missed_Pmnt"] > 0].groupby("Tot_Missed_Pmnt")["PROSPECTID"].count().sort_values(ascending=False).head(5).reset_index())

    # Plot setup
    fig10, ax10 = plt.subplots(figsize=(6, 3))
    bars = ax10.barh(missed_data["Tot_Missed_Pmnt"].astype(str), missed_data["PROSPECTID"], color='red', edgecolor='black')

    # Title and ticks
    ax10.set_title("Top Missed Payments", fontsize=10)
    ax10.tick_params(axis='y', labelsize=6)
    ax10.tick_params(axis='x', labelsize=6)

    # Calculate padding
    max_width = missed_data["PROSPECTID"].max()
    ax10.set_xlim(0, max_width * 1.15)

    # Annotate bars
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width + (max_width * 0.015)
        ax10.annotate(f"{int(width):,}",
                      xy=(label_x_pos, bar.get_y() + bar.get_height() / 2),
                      ha='left', va='center', fontsize=6, color='black')

    # Render
    fig10.tight_layout()
    st.pyplot(fig10)
    plt.close(fig10)


    # 11. New Accounts Opened in Last 6 Months
    st.subheader("New Accounts Opened in Last 6 Months")
    new_data = (df1.groupby("Total_TL_opened_L6M")["PROSPECTID"].count().sort_values(ascending=False).reset_index())
    fig11, ax11 = plt.subplots(figsize=(6, 3))
    bars = ax11.barh(new_data["Total_TL_opened_L6M"].astype(str), new_data["PROSPECTID"], color='navy', edgecolor='black')
    ax11.set_title("New Accounts in Last 6M", fontsize=10)
    ax11.tick_params(axis='y', labelsize=6)
    ax11.tick_params(axis='x', labelsize=6)

    # X-axis limit padding
    max_width = new_data["PROSPECTID"].max()
    ax11.set_xlim(0, max_width * 1.15)
    # Annotate bars
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width + (max_width * 0.015)
        ax11.annotate(f"{int(width):,}",
                      xy=(label_x_pos, bar.get_y() + bar.get_height() / 2),
                      ha='left', va='center', fontsize=6, color='black')
    fig11.tight_layout()
    st.pyplot(fig11)
    plt.close(fig11)


    # 12. Accounts Closed in Last 6 Months
    st.subheader("Accounts Closed in Last 6 Months")
    closed_data = df1.groupby("Tot_TL_closed_L6M")["PROSPECTID"].count().sort_values(ascending=False).reset_index()
    fig12, ax12 = plt.subplots(figsize=(6, 3))
    ax12.barh(closed_data["Tot_TL_closed_L6M"].astype(str), closed_data["PROSPECTID"], color='gray', edgecolor='black')
    ax12.set_title("Closed Accounts in Last 6M", fontsize=10)
    ax12.tick_params(axis='y', labelsize=6)
    ax12.tick_params(axis='x', labelsize=6)
    for bar in bars:
        ax12.annotate(format_value(bar.get_width()),
                     xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                     ha='left', va='center', fontsize=6)
    st.pyplot(fig12)
    plt.close(fig12)
