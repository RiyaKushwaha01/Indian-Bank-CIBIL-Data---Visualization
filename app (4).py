#!/usr/bin/env python
# coding: utf-8

# #### 1. Import the required packages :

# In[6]:


import pyodbc
import numpy as np
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib 
matplotlib.use('TkAgg')


# #### 2. Import the Data

# ##### Connect the SQL Server to get the data

# In[8]:


# Eshtablishing the connection :

conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=DESKTOP-DDTGTVD\SQLEXPRESS02;'
    r'DATABASE=BANK_DB;'
    r'Trusted_Connection=yes;'
)


# In[10]:


# If connection is succesfull, print True
if conn:
    print('True')


# In[12]:


df1 = "SELECT * FROM Internal_Data "
df2 = "SELECT * FROM External_CIBIL_Data"


# In[14]:


df1 = pd.read_sql(df1, conn)
df2 = pd.read_sql(df2, conn)


# In[18]:


df1.head(2)


# In[20]:


df2.head(2)


# #### 3. Analysis and Visualization

# ##### 1. Distribution of Education Level

# In[16]:


Education_Level = pd.DataFrame(df2.groupby('EDUCATION').PROSPECTID.sum().sort_values(ascending = False))
Education_Level


# In[18]:


get_ipython().run_line_magic('matplotlib', 'inline')
Education_Level.plot(kind='bar', figsize=(4, 3))
plt.title('Distribution of Education Level')
plt.xlabel('Education Level')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 2. Distribution of Gender

# In[20]:


Gender_Distribution = pd.DataFrame(df2.groupby('GENDER').PROSPECTID.sum().sort_values(ascending = False))
Gender_Distribution


# In[22]:


Gender_Distribution.plot(kind = 'pie' , subplots=True, autopct = '%.2f')
plt.title('Distribution of Gender')
plt.xlabel('Gender')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 3. Distribution of Maritalstatus

# In[24]:


MaritalStatus = pd.DataFrame(df2.groupby('MARITALSTATUS').PROSPECTID.sum().sort_values(ascending = False))
MaritalStatus


# In[26]:


MaritalStatus.plot(kind='barh', figsize=(4, 3))
plt.title('Distribution of Marital Status')
plt.xlabel('Marital Status')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 4. Distribution of Loan Type

# In[28]:


Loan_Type = pd.DataFrame(df2.groupby('first_prod_enq2').PROSPECTID.sum().sort_values(ascending = False))
Loan_Type


# In[30]:


Loan_Type.plot(kind='barh', figsize=(4, 3))
plt.title('Distribution of Loan Type')
plt.xlabel('Loan type')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 5. Top 5 Income of Applicants

# In[32]:


Applicants_Income = df2.groupby('NETMONTHLYINCOME')['PROSPECTID'].count().sort_values(ascending=False).head(6)
Applicants_Income


# In[34]:


Applicants_Income.plot(kind='bar', figsize=(4, 3))
plt.title('Top 6 Income of Applicants')
plt.xlabel('Income')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 6. Top 10 Credit Score

# In[36]:


Credit_Score = df2.groupby('Credit_Score')['PROSPECTID'].count().sort_values(ascending=False).head(10)
Credit_Score


# In[38]:


Credit_Score.plot(kind='bar', figsize=(4, 3))
plt.title('Top 10 Credit Score')
plt.xlabel('Credit Score')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 7. Distribution of Risk Category

# In[40]:


# Create the Risk_Category column using conditions
df1['Risk_Category'] = df1['Tot_Missed_Pmnt'].apply(
    lambda x: 'High Risk' if x > 5 else 'Medium Risk' if 2 <= x <= 5 else 'Low Risk'
)

# Sort by Risk_Category
Risk_Category = df1.sort_values(by='Risk_Category')

# Display the result
Risk_Category.head()


# In[42]:


Risk_Category = pd.DataFrame(df1.groupby('Risk_Category').PROSPECTID.sum().sort_values(ascending=False))
Risk_Category


# In[44]:


Risk_Category.plot(kind = 'pie' , subplots=True, autopct = '%.2f')
plt.title('Distribution of Risk Category')
plt.xlabel('Risk Category')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 8. Distribution of Credit Score by Segmentation

# In[46]:


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

# Create the Credit_Score_Category column
df2['Credit_Score_Category'] = df2['Credit_Score'].apply(categorize_credit_score)


# In[48]:


Credit_Score_Category = pd.DataFrame(df2.groupby('Credit_Score_Category').PROSPECTID.sum().sort_values(ascending = False))
Credit_Score_Category


# In[50]:


Credit_Score_Category.plot(kind='bar', figsize=(4, 3))
plt.title('Distribution of Credit Score by Segmentation')
plt.xlabel('Credit_Score_Category')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 9. Distribution of y column(Approved Flag)

# In[52]:


Approved_Flag = pd.DataFrame(df2.groupby('Approved_Flag').PROSPECTID.sum().sort_values(ascending = False))
Approved_Flag


# In[54]:


Approved_Flag.plot(kind='barh', figsize=(4, 3))
plt.title('Distribution of y')
plt.xlabel('Approved Flag')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 10. Identify Applicants with a high percentage of missed payments

# In[72]:


Missed_Payments = ( df1[df1['Tot_Missed_Pmnt'] != 0] .groupby('Tot_Missed_Pmnt')['PROSPECTID'] .count() .sort_values(ascending=False) .to_frame())

Missed_Payments.head(10)


# In[74]:


Missed_Payments.plot(kind='barh', figsize=(4, 3))
plt.title('Applicants with a high percentage of missed payments')
plt.xlabel('Missed Payments')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 10. Applicants who opened multiple new accounts in the last 6 months

# In[76]:


new_Multiple_Accounts = pd.DataFrame( df1.groupby('Total_TL_opened_L6M')['PROSPECTID'] .count() .sort_values(ascending=False)).head(6)
new_Multiple_Accounts


# In[78]:


new_Multiple_Accounts.plot(kind='bar', figsize=(4, 3))
plt.title('Applicants who opened multiple accounts in L6M')
plt.xlabel('Multiple Accounts')
plt.ylabel('Applicants Count')
st.pyplot()


# ##### 12. Applicants who Closed multiple accounts in last 6 months

# In[81]:


Closed_Multiple_Accounts = pd.DataFrame( df1.groupby('Tot_TL_closed_L6M')['PROSPECTID'] .count() .sort_values(ascending=False)).head(6)
Closed_Multiple_Accounts


# In[83]:


Closed_Multiple_Accounts.plot(kind='bar', figsize=(4, 3))
plt.title('Applicants who closed multiple accounts in L6M')
plt.xlabel('Multiple Closed Accounts')
plt.ylabel('Applicants Count')
st.pyplot()


# In[ ]:




