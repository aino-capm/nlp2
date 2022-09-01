#ライブラリの読み込み
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.manifold import TSNE
import japanize_matplotlib
import pickle
import plotly.express as px

st.markdown("## 🐮 文章ベクトルの可視化（業種別）")
st.caption("t-SNEを使って有価証券報告書の文章ベクトルを低次元に変換し、業種別に可視化します")
st.markdown("***")
df = pd.read_csv("files/2203有報セット.csv",index_col=0)


state = st.radio("文書の種類を選択してください",("経営方針","事業等のリスク"))
if state == "経営方針":
  file_path = "models/doc2vec_2203keiei_sentences_vectors.bin"
else:
  file_path = "models/doc2vec_2203risk_sentences_vectors.bin"

with open(file_path,"rb") as p:
  sentence_vectors = pickle.load(p)


#可視化のタイプを選択する。
sight_menu = st.radio("次元数を選択してください", ["2次元","3次元"])

if sight_menu == "2次元":
  st.markdown("#### 2次元で可視化します")
  execute = st.button("実行")
  if execute:
    vectors_tsne = TSNE(n_components=2).fit_transform(sentence_vectors)
    df_vec_tsne = pd.DataFrame(vectors_tsne).reset_index()
    df_vec_tsne["corp"] = df.reset_index()["会社名"]
    df_vec_tsne["業種"] = df.reset_index()["提出者業種"]
    fig = px.scatter(
      df_vec_tsne, x=0, y=1,
      color="業種",labels={"color":"業種"},hover_data = ['corp'])
    fig.update_traces(marker_size=5)
    fig.update_layout(plot_bgcolor="white",width=1000,height=1000)
    st.plotly_chart(fig, use_container_width=True)

if sight_menu == "3次元":
  st.markdown("#### 3次元で可視化します")
  execute = st.button("実行")
  if execute:
    vectors_tsne3 = TSNE(n_components=3).fit_transform(sentence_vectors)
    df_vec_tsne3 = pd.DataFrame(vectors_tsne3).reset_index()
    df_vec_tsne3["corp"] = df.reset_index()["会社名"]
    df_vec_tsne3["業種"] = df.reset_index()["提出者業種"]
    fig = px.scatter_3d(
      df_vec_tsne3, x=0, y=1,z=2,
      color="業種",labels={"color":"業種"},hover_data = ['corp'])
    fig.update_traces(marker_size=2)
    fig.update_layout(plot_bgcolor="white",width=1000,height=1000)
    st.plotly_chart(fig, use_container_width=True)

