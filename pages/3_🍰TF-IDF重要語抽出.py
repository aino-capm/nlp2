import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import streamlit as st
import japanize_matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud

st.markdown("## TF-IDFによる重要語の抽出")
st.markdown("***")
st.caption("テキスト文書の中で重要な単語をTF-IDFを使って抽出します")
st.caption("表形式のデータフレームとワードクラウドで表示します")


#ファイルアップロード
df = pd.read_csv("files/2203有報セット.csv",index_col=0)
corp = df["会社名"]


#ラジオボタンで、テキスト文書を選択する
state = st.radio("選択してください",("経営方針","事業等のリスク"))
if state == "経営方針":
  file_path = "models/docs_keiei_2203.bin"
else:
  file_path = "models/docs_risk_2203.bin"
#選択したテキスト文書を呼び出す
with open(file_path,"rb") as p:
  docs = pickle.load(p)


@st.cache
def tf_idf(docs):
  # モデルを生成
  vectorizer = TfidfVectorizer(smooth_idf=False)
  X = vectorizer.fit_transform(docs)
  # データフレームに表現
  values = X.toarray()
  feature_names = vectorizer.get_feature_names()
  tfidf_df = pd.DataFrame(values, columns = feature_names)  
  
  return values,feature_names,tfidf_df


def vecs_dic(feature_names,values,z):
  words = feature_names
  vecs = values.tolist()
  temp_dic = {}
  vecs_dic = []
  for vec in vecs:
    for i in range(len(vec)):
      temp_dic[words[i]] = vec[i] 
    vecs_dic.append(temp_dic)
    temp_dic = {}
    
  fig = plt.figure(figsize=(12,12))

  mask = np.array(Image.open("utils/phpYSbfIJ.png"))
  im = WordCloud(
        font_path='fonts/Noto_Serif_JP/NotoSerifJP-Regular.otf',
        background_color='white',
        colormap = "viridis",
        mask=mask,
        random_state=0,
        max_words=z).generate_from_frequencies(vecs_dic[index])
  plt.imshow(im)
  plt.axis('off')
  plt.tight_layout()
  st.pyplot(fig)


with st.form("form1"):
  x = st.selectbox("企業を選択してください",corp)
  index = df.loc[df["会社名"]==x].index[0]
  y = st.number_input("データフレームの単語抽出数",min_value=5,max_value=30,value=10,step=5)
  z = st.number_input("ワードクラウドの単語抽出数",min_value=20,max_value=50,value=50,step=5)
  submittted = st.form_submit_button("データフレーム&ワードクラウド")
  if submittted:
    values,feature_names,tfidf_df = tf_idf(docs)
    df = pd.DataFrame(tfidf_df.T[index].sort_values(ascending=False)[:y])  
    st.dataframe(df)  
    
    vecs_dic(feature_names,values,z)
    
    
    
  

   