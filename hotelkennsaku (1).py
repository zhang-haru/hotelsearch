#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import streamlit as st
import plotly.express as px


# In[30]:


hotels_df = pd.read_csv("cleaned_hotels.csv")


# In[27]:


hotels_df['price'] = pd.to_numeric(hotels_df['price'], errors='coerce')
hotels_df['star'] = pd.to_numeric(hotels_df['star'], errors='coerce')
hotels_df['review'] = pd.to_numeric(hotels_df['review'], errors='coerce')


# In[28]:


st.header("検索条件")
col1, col2 = st.columns(2)
with col1:
    price_limit = st.slider("料金の上限", min_value=3000, max_value=100000, step=1000, value=30000)
with col2:
    score_limit = st.slider("評価の下限", min_value=0.0,  max_value=5.0, step=0.1, value=3.0)


# In[15]:


filtered_df = hotels_df[
    (hotels_df['price'] <= price_limit) &
    (hotels_df['star'] >= score_limit)
]


# In[ ]:


st.subheader(f"条件に合うホテル: {len(filtered_df)}件")


# In[16]:


if not filtered_df.empty:
    fig = px.scatter(
        filtered_df,
        x='star',
        y='price',
        hover_data=['title', 'details', 'review'],
        title='評価と料金の関係',
        labels={'star': '星評価', 'price': '宿泊料金'}
    )
    st.plotly_chart(fig)


# In[17]:


if not filtered_df.empty:
    selected_hotel = st.selectbox('気になるホテルを選んで詳細を確認', filtered_df['title'])
    if selected_hotel:
        try:
            hotel_data = filtered_df[filtered_df['title'] == selected_hotel].iloc[0]
            url = hotel_data['title_url']
            
            image_url = hotel_data.get('画像url', '')
            if image_url and image_url.startswith('http'):
                st.image(image_url, caption=selected_hotel, width=300)
            
            st.markdown(f"[{selected_hotel}のページへ移動]({url})", unsafe_allow_html=True)
        except IndexError:
            st.error("ホテルのURLを取得できませんでした。")


# In[18]:


if not filtered_df.empty:
    sort_key = st.selectbox(
        "ランキング基準を選んでください",
        ("star", "review", "price")
    )
    ascending = True if sort_key == "price" else False


# In[19]:


st.subheader(f"{sort_key} によるホテルランキング(上位10件)")
ranking_df = filtered_df.sort_values(by=sort_key, ascending=ascending).head(10)


# In[ ]:


ranking_df['price'] = ranking_df['price'].apply(lambda x: f"¥{x:,}")

st.dataframe(ranking_df[['title', "price", "star", "review", "details"]])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




