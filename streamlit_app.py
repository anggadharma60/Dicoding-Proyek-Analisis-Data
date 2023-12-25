import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def df_payment_type(df):
    data= df['payment_type'].value_counts()
    return data

def df_review(df):
    data= df['review_score'].value_counts()
    return data


def df_rfm(df, now):
    df['order_purchase_timestamp']=pd.to_datetime(df['order_purchase_timestamp'])
    recency=df.groupby('customer_id', as_index=False)['order_purchase_timestamp'].max()
    recency.columns = ['customer_id', 'last_purchase']
    recency['Recency'] = (now - recency['last_purchase']).dt.days
    recency = recency[['customer_id', 'Recency']]
    
    
    frequency=df.groupby('customer_id', as_index=False)['order_id'].count()
    frequency.columns = ['customer_id', 'Frequency']
    
    
    monetary = df.groupby('customer_id', as_index=False)['payment_value'].sum()
    monetary.columns = ['customer_id', 'Monetary']
    
    
    rfm = pd.merge(left=pd.merge(left=recency, right=frequency, left_on='customer_id', right_on='customer_id'), right= monetary, left_on='customer_id', right_on='customer_id')
    


    
    return rfm

# Load cleaned data
all_df = pd.read_csv("all_data.csv")
all_df['order_purchase_timestamp']=pd.to_datetime(all_df['order_purchase_timestamp'])
now = pd.to_datetime('2018-09-1 00:00:00')
payment_type = df_payment_type(all_df)
review = df_review(all_df)
rfm_df = df_rfm(all_df, now)

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.png")

    
st.header('Dicoding Collection Dashboard :sparkles:')

###Visualisasi 1
st.subheader('Payment Type')
explode = (0.01, 0.0, 0, 0) 
fig, ax = plt.subplots(figsize=(16, 8))
ax.pie(payment_type, labels=payment_type.keys(), autopct='%.0f%%',explode=explode)
st.pyplot(fig)

###Visualisasi 2
st.subheader('Review Score')
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x=review.keys(),
            y=review.values,
            order=review.keys(),
            )
ax.bar_label(ax.containers[0])
ax.set_xlabel(None)
st.pyplot(fig)


# Best Customer Based on RFM Parameters
st.subheader("Best Customer Based on RFM Parameters")
st.metric("Time Assumption", str(now))
col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.Recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.Frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm_df.Monetary.mean(), "R$", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(y="Recency", x="customer_id", data=rfm_df.sort_values(by="Recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35,labelbottom=False)
ax[0].set_xlabel(None)

sns.barplot(y="Frequency", x="customer_id", data=rfm_df.sort_values(by="Frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35,labelbottom=False)
ax[1].set_xlabel(None)

sns.barplot(y="Monetary", x="customer_id", data=rfm_df.sort_values(by="Monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35,labelbottom=False)
ax[2].set_xlabel(None)

st.pyplot(fig)

st.caption('Copyright © anggadharma60 - anggadharma60@gmail.com')