#ライブラリの読み込み
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import japanize_matplotlib
import os
import pickle

#タイトル
st.markdown("## 類似文書の検索")
st.caption("Doc2Vecで有価証券報告書のテキスト文書をベクトル化します。選択した企業と類似した文書を作成している企業を検索します")
st.markdown("***")



df = pd.read_csv("files/2203有報セット.csv",index_col=0).reset_index()  
df_group = df.groupby("提出者業種")
gyosyu = sorted(list(df_group.groups.keys()),reverse=True)
corp = df["会社名"]

@st.cache
def doc2vec(sentences,vector_size,epochs):
  documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(sentences)]
  model = Doc2Vec(documents, vector_size=vector_size,  window=7, min_count=1, workers=4, epochs=epochs)
  
  return model

#ラジオボタンで、テキスト文書を選択する
state = st.radio("文書の種類を選択してください",("経営方針","事業等のリスク"))
if state == "経営方針":
  file_path = "models/sentences_keiei_2203.bin"
else:
  file_path = "models/sentences_risk_2203.bin"
#選択したテキスト文書を呼び出す
with open(file_path,"rb") as p:
  sentences = pickle.load(p)

g = st.selectbox("業種を選択してください",gyosyu)
x = st.selectbox("企業を選択してください",df_group.get_group(g)["会社名"])
index = df.loc[df["会社名"]==x].index[0]
#計算実行の前提の実装


with st.form("form"):
 
  st.caption("ベクトルのサイズ・エポック数を入力してください")
  vector_size = st.number_input("ベクトルのサイズ",min_value=100,max_value=300,value=300,step=50)
  epochs = st.number_input("エポック数",min_value=10,max_value=20,value=20,step=5)
  submittted = st.form_submit_button("計算実行")
  if submittted:
    model = doc2vec(sentences,vector_size,epochs)
  
    st.markdown("#### 検索結果")
    result = pd.DataFrame(model.docvecs.most_similar(index),columns=["index","類似度"])
    result["会社名"] = result["index"].apply(lambda x : df.iloc[x,4])
    st.write(result)


