import streamlit as st
import pandas as pd

st.markdown("## テキスト検索・キーワード検索")
st.markdown("***")


state = st.radio("決算期を選択してください",("21年3月期","22年3月期"))
if state == "21年3月期":
  file_path = "files/2103有報セット.csv"
else:
  file_path = "files/2203有報セット.csv"
df = pd.read_csv(file_path,index_col=0)
corp = df["会社名"]

st.markdown("#### ☕️ テキスト検索")
st.caption("特定の企業の経営方針・事業等のリスクを表示します")

with st.form("form1"):
  x = st.selectbox("企業を選択してください",corp)
  index = df.loc[df["会社名"]==x].index[0]
  text = st.radio("文書を選択してください",('経営方針','事業等のリスク'))
  slider = st.slider("表示文字数",min_value=300,max_value=2500)
  submittted = st.form_submit_button("検索")
  if submittted:
    st.write(df.iloc[index][text][:slider])

st.markdown("#### 🎤 キーワード検索")
st.caption("特定のキーワードに言及している企業数と企業名をかえします")

with st.form("form2"):
  text = st.radio("検索する文書を選択してください",("経営方針","事業等のリスク"))
  word1 = st.text_input("キーワードを入力してください",value="人権")
  word2 = st.text_input("キーワードを入力してください",value="地政学")
  word3 = st.text_input("キーワードを入力してください",value="パーパス")
  submittted = st.form_submit_button("検索")
  if submittted:
    words = [word1,word2,word3]
    df_w = pd.DataFrame()
    for word in words:
        count = 0
        corp = []
        for _ ,data in df.iterrows():
            if word in data[text]:
                count += 1
                corp.append(data["会社名"])
        s = pd.DataFrame([count,corp],columns=[word],index=["企業数","企業名"]).T
        df_w = df_w.append(s)
    st.dataframe(df_w)
