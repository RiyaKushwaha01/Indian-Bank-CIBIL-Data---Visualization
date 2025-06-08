import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    st.set_page_config(page_title="Visaulizations", layout="wide")
    st.title("Indian Bank & CIBIL Data - EDA")

    @st.cache_data
    def load_data():
        return pd.read_csv("Natural_Resources_Revenue.csv")

    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filter Data")

    EDUACTION = sorted(df["Education Level"].dropna().unique())
    GENDER = sorted(df["Gender"].dropna().unique())
    MARITALSTATUS = sorted(df["MaritalStatus"].dropna().unique())
    first_prod_enq2 = sorted(df["Loan Type"].dropna().unique())
    Risk_Category = sorted(df["Risk Category"].dropna().unique())
    Credit_Score_Category = sorted(df["Credit Score Category"].dropna().unique())

    with st.sidebar.expander("📅 Education Level", expanded=True):
        selected_education = st.multiselect("Select Education Level", options=EDUACTION, default=EDUACTION)

    with st.sidebar.expander("🌍 Gender", expanded=True):
        selected_gender = st.multiselect("Select Gender", options=GENDER, default=GENDER)

    with st.sidebar.expander("🏷️MaritalStatus", expanded=True):
        selected_MaritalStatus = st.multiselect("Select MaritalStatus", options=MARITALSTATUS, default=MARITALSTATUS)

    with st.sidebar.expander("🗺️ Loan Type", expanded=True):
        selected_first_prod_enq2 = st.multiselect("Select Loan Type", options=first_prod_enq2, default=first_prod_enq2)

    with st.sidebar.expander("🏘️ Risk Category", expanded=True):
        selected_Risk_Category = st.multiselect("Select Risk Category", options=Risk_Category, default=Risk_Category)

    with st.sidebar.expander("💰 Credit Score Category", expanded=True):
        selected_Credit_Score_Category = st.multiselect("Select Credit Score Category", options=Credit_Score_Category, default=Credit_Score_Category)


    # ✅ Apply filters
    filtered_df = df[
        df["Education Level"].isin(selected_education) &
        df["Gender"].isin(selected_gender) &
        df["MaritalStatus"].isin(selected_MaritalStatus) &
        df["Loan Type"].isin(selected_first_prod_enq2) &
        df["Risk Category"].isin(selected_Risk_Category) &
        df["Credit Score Category"].isin(selected_Credit_Score_Category)
    ]

    st.subheader("Dataset Preview")
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
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    sns.lineplot(data=revenue_trends, x="Calendar Year", y="Revenue", ax=ax1, marker='o')
    ax1.set_title("Distribution of Education Level", fontsize=8)
    ax1.set_xlabel("Education Level", fontsize=6)
    ax1.set_ylabel("Applicants Count", fontsize=6)
    ax1.tick_params(axis='y', labelsize=6)
    ax1.tick_params(axis='x', labelsize=6)

    # Add smart label positioning
    previous_y = None
    for i in range(len(revenue_trends)):
        x = revenue_trends["Calendar Year"].iloc[i]
        y = revenue_trends["Revenue"].iloc[i]
        offset = 0.05 * y  # 5% offset

        if previous_y is not None and abs(y - previous_y) < 0.15 * y:
            # If points are close, adjust label position up or down
            va = 'top' if i % 2 == 0 else 'bottom'
        else:
            va = 'bottom'

        ax1.text(x, y + (offset if va == 'bottom' else -offset), format_revenue(y),
                 fontsize=6, ha='center', va=va, weight='bold')

        previous_y = y

    st.pyplot(fig1)

    # State by Revenue
    st.subheader("Top 10 States by Revenue")
    state_revenue = filtered_df.groupby("State")["Revenue"].sum().sort_values(ascending=False).head(10)
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    state_revenue.plot(kind="bar", width=0.7, ax=ax2)
    ax2.set_title("State by Revenue", fontsize=8)
    ax2.tick_params(axis='y', labelsize=6)
    ax2.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax2.patches:
        ax2.annotate(format_revenue(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    st.pyplot(fig2)

    # County by Revenue
    st.subheader("County by Revenue")
    if "County" in filtered_df.columns and not filtered_df["County"].dropna().empty:
        county_revenue = filtered_df.groupby("County")["Revenue"].sum().sort_values(ascending=False).head(10)
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        county_revenue.plot(kind="bar", ax=ax3)
        ax3.set_title("County by Revenue", fontsize=8)
        ax3.set_xlabel("Revenue")
        ax3.tick_params(axis='x', labelsize=6)

        # Add data labels
        for p in ax3.patches:
            ax3.annotate(format_revenue(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

        st.pyplot(fig3)
    else:
        st.warning("County column missing or contains only NaN.")

    # Correlation Analysis
    st.subheader("Correlation Analysis")
    fig4, ax4 = plt.subplots(figsize=(4, 3))
    sns.heatmap(filtered_df.select_dtypes(include=['float64', 'int64']).corr(), annot=True, ax=ax4)
    ax4.set_title("Correlation Analysis", fontsize=8)
    st.pyplot(fig4)

    # Revenue by Commodity and Lease Type
    st.subheader("Total Revenue for Commodity and Mineral Lease Type")
    revenue_by_combo = filtered_df.groupby(["Commodity", "Mineral Lease Type"])["Revenue"].sum().sort_values(ascending=False).head(10)
    fig5, ax5 = plt.subplots(figsize=(8, 4))
    revenue_by_combo.plot(kind="bar", ax=ax5)
    ax5.set_title("Total Revenue for Commodity and Lease Type", fontsize=8)
    ax5.set_ylabel("Revenue")
    ax5.set_xlabel("Commodity and Lease Type")
    ax5.tick_params(axis='y', labelsize=6)
    ax5.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax5.patches:
        ax5.annotate(format_revenue(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    st.pyplot(fig5)

    # Revenue by Land Class (use df instead of filtered_df)
    st.subheader("Revenue by Land Class")
    revenue_land_class = df.groupby("Land Class")["Revenue"].sum()  # Changed to df
    fig6, ax6 = plt.subplots(figsize=(2, 2))
    ax6.pie(revenue_land_class, labels=revenue_land_class.index, autopct="%.2f%%", startangle=90, wedgeprops={'edgecolor': 'white'})
    ax6.axis("equal")
    ax6.set_title("Revenue Distribution by Land Class", fontsize=8)
    st.pyplot(fig6)

    # Revenue by Land Category (use df instead of filtered_df)
    st.subheader("Revenue by Land Category")
    revenue_land_category = df.groupby("Land Category")["Revenue"].sum()  # Changed to df
    fig7, ax7 = plt.subplots(figsize=(7, 4))
    revenue_land_category.plot(kind="bar", ax=ax7)
    ax7.set_title("Revenue by Land Category", fontsize=8)
    ax7.tick_params(axis='y', labelsize=6)
    ax7.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax7.patches:
        ax7.annotate(format_revenue(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    st.pyplot(fig7)

    # Revenue by Revenue Type (use df instead of filtered_df)
    st.subheader("Top Revenue Types by Total Revenue")
    revenue_rev_type = df.groupby("Revenue Type")["Revenue"].sum().sort_values(ascending=False)  # Changed to df
    fig8, ax8 = plt.subplots(figsize=(3, 2))
    revenue_rev_type.plot(kind="barh", ax=ax8)
    ax8.set_xlabel("Total Revenue", fontsize=6)
    ax8.set_ylabel("Revenue Type", fontsize=6)
    ax8.set_title("Top Revenue Types by Total Revenue", fontsize=8)
    ax8.tick_params(axis='y', labelsize=6)
    ax8.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax8.patches:
        ax8.annotate(format_revenue(p.get_width()), (p.get_x() + p.get_width(), p.get_y() + p.get_height() / 2.),
                     ha='left', va='center', fontsize=6, xytext=(5, 0), textcoords='offset points')

    st.pyplot(fig8)

    # Offshore Region Revenue (use df instead of filtered_df)
    st.subheader("Top 10 Offshore Regions by Revenue")
    df = df.dropna(subset=["Offshore Region"])  # Changed to df
    offshore_revenue = df.groupby("Offshore Region")["Revenue"].sum().sort_values(ascending=False).head(10)  # Changed to df
    fig9, ax9 = plt.subplots(figsize=(7, 4))
    offshore_revenue.plot(kind="bar", ax=ax9)
    ax9.set_xlabel("Offshore Region", fontsize=6)
    ax9.set_ylabel("Total Revenue", fontsize=6)
    ax9.set_title("Top 10 Offshore Regions by Revenue", fontsize=8)
    ax9.tick_params(axis='y', labelsize=6)
    ax9.tick_params(axis='x', labelsize=6)

    # Add data labels
    for p in ax9.patches:
        ax9.annotate(format_revenue(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=6, xytext=(0, 5), textcoords='offset points')

    st.pyplot(fig9)
