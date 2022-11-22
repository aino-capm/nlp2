import streamlit as st
import pandas as pd

st.markdown("## 🐶 テキスト検索")
st.caption("選択した企業の経営方針・事業等のリスクを表示します")
st.markdown("***")


state = st.radio("決算期を選択してください",("21年3月期","22年3月期"))
if state == "21年3月期":
  file_path = "files/2103有報セット.csv"
else:
  file_path = "files/2203有報セット.csv"
df = pd.read_csv(file_path,index_col=0).reset_index()
df_group = df.groupby("提出者業種")
gyosyu = sorted(list(df_group.groups.keys()),reverse=True)
corp = df["会社名"]



g = st.selectbox("業種を選択してください",gyosyu)
x = st.selectbox("企業を選択してください",df_group.get_group(g)["会社名"])
index = df.loc[df["会社名"]==x].index[0]

with st.form("form1"):  
  text = st.radio("文書の種類を選択してください",('経営方針','事業等のリスク'))
  slider = st.slider("表示文字数",min_value=300,max_value=00)
  submittted = st.form_submit_button("検索")
  if submittted:
    st.write(df.iloc[index][text][:slider])

