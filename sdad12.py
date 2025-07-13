#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import streamlit as st
import plotly.express as px

# 读取酒店数据
hotels_df = pd.read_csv("cleaned_hotels.csv")

# 确保数值列是数值类型
hotels_df['price'] = pd.to_numeric(hotels_df['price'], errors='coerce')
hotels_df['star'] = pd.to_numeric(hotels_df['star'], errors='coerce')
hotels_df['review'] = pd.to_numeric(hotels_df['review'], errors='coerce')

# Streamlit 应用界面
st.title("ホテルサーチ")

# 侧边栏控制面板
with st.sidebar:
    st.header("検索条件")
    price_limit = st.slider(
        "宿泊料金の上限", 
        min_value=3000, 
        max_value=100000, 
        step=1000, 
        value=30000
    )
    score_limit = st.slider(
        "星評価の下限", 
        min_value=0.0, 
        max_value=5.0, 
        step=0.1, 
        value=3.0
    )

# 数据过滤
filtered_df = hotels_df[
    (hotels_df['price'] <= price_limit) &
    (hotels_df['star'] >= score_limit)
]

# 显示找到的酒店数量
st.subheader(f"条件に合うホテル: {len(filtered_df)}件")

# 绘制散点图
if not filtered_df.empty:
    fig = px.scatter(
        filtered_df,
        x='star',
        y='price',
        hover_data=['title', 'details', 'review'],
        title='星評価と宿泊料金の関係',
        labels={'star': '星評価', 'price': '宿泊料金'}
    )
    st.plotly_chart(fig)
else:
    st.warning("条件に合うホテルが見つかりませんでした。検索条件を変更してください。")

# 酒店选择器
if not filtered_df.empty:
    selected_hotel = st.selectbox('気になるホテルを選んで詳細を確認', filtered_df['title'])
    if selected_hotel:
        try:
            url = filtered_df[filtered_df['title'] == selected_hotel]['title_url'].values[0]
            st.markdown(f"[{selected_hotel}のページへ移動]({url})", unsafe_allow_html=True)
        except IndexError:
            st.error("ホテルのURLを取得できませんでした。")

# 排序选项
if not filtered_df.empty:
    sort_key = st.selectbox(
        "ランキング基準を選んでください",
        ("star", "review", "price")
    )
    ascending = True if sort_key == "price" else False

    # 显示排行榜
    st.subheader(f"{sort_key} によるホテルランキング(上位10件)")
    ranking_df = filtered_df.sort_values(by=sort_key, ascending=ascending).head(10)
    
    # 格式化价格列
    ranking_df['price'] = ranking_df['price'].apply(lambda x: f"¥{x:,}")
    
    st.dataframe(ranking_df[['title', "price", "star", "review", "details"]])
else:
    st.info("ランキングを表示するホテルがありません。")

