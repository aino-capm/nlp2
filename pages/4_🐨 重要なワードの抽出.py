import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import streamlit as st
import japanize_matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud

st.markdown("## ð¨ éè¦ãªã¯ã¼ãã®æ½åº")
st.markdown("***")
st.caption("ãã­ã¹ãææ¸ã®ä¸­ã§éè¦ãªã¯ã¼ããTF-IDFãä½¿ã£ã¦æ½åºãã¾ã")
st.caption("è¡¨å½¢å¼ã®ãã¼ã¿ãã¬ã¼ã ã§è¡¨ç¤ºãã¾ã")


#ãã¡ã¤ã«ã¢ããã­ã¼ã
df = pd.read_csv("files/2203æå ±ã»ãã.csv",index_col=0).reset_index()
df_group = df.groupby("æåºèæ¥­ç¨®")
gyosyu = sorted(list(df_group.groups.keys()),reverse=True)
corp = df["ä¼ç¤¾å"]


#ã©ã¸ãªãã¿ã³ã§ããã­ã¹ãææ¸ãé¸æãã
state = st.radio("ææ¸ã®ç¨®é¡ãé¸æãã¦ãã ãã",("çµå¶æ¹é","äºæ¥­ç­ã®ãªã¹ã¯"))
if state == "çµå¶æ¹é":
  file_path = "models/docs_keiei_2203.bin"
else:
  file_path = "models/docs_risk_2203.bin"
#é¸æãããã­ã¹ãææ¸ãå¼ã³åºã
with open(file_path,"rb") as p:
  docs = pickle.load(p)


@st.cache
def tf_idf(docs):
  # ã¢ãã«ãçæ
  vectorizer = TfidfVectorizer(smooth_idf=False)
  X = vectorizer.fit_transform(docs)
  # ãã¼ã¿ãã¬ã¼ã ã«è¡¨ç¾
  values = X.toarray()
  feature_names = vectorizer.get_feature_names()
  tfidf_df = pd.DataFrame(values, columns = feature_names)  
  
  return values,feature_names,tfidf_df

#ã¯ã¼ãã¯ã©ã¦ãç¨ã®è¾æ¸ãå¤§ãããã¦ã¯ã©ãã·ã¥ãã¦ãã¾ã
# def vecs_dic(feature_names,values,z):
#   words = feature_names
#   vecs = values.tolist()
#   temp_dic = {}
#   vecs_dic = []
#   for vec in vecs:
#     for i in range(len(vec)):
#       temp_dic[words[i]] = vec[i] 
#     vecs_dic.append(temp_dic)
#     temp_dic = {}
    
#   fig = plt.figure(figsize=(12,12))

#   mask = np.array(Image.open("utils/phpYSbfIJ.png"))
#   im = WordCloud(
#         font_path='fonts/Noto_Serif_JP/NotoSerifJP-Regular.otf',
#         background_color='white',
#         colormap = "viridis",
#         mask=mask,
#         random_state=0,
#         max_words=z).generate_from_frequencies(vecs_dic[index])
#   plt.imshow(im)
#   plt.axis('off')
#   plt.tight_layout()
#   st.pyplot(fig)

g = st.selectbox("æ¥­ç¨®ãé¸æãã¦ãã ãã",gyosyu)
x = st.selectbox("ä¼æ¥­ãé¸æãã¦ãã ãã",df_group.get_group(g)["ä¼ç¤¾å"])
index = df.loc[df["ä¼ç¤¾å"]==x].index[0]

st.markdown("#### ãã©ã¡ã¼ã¿ã®è¨­å®")
with st.form("form1"):
  y = st.number_input("ãã¼ã¿ãã¬ã¼ã ã®åèªæ½åºæ°",min_value=5,max_value=30,value=10,step=5)
  #z = st.number_input("ã¯ã¼ãã¯ã©ã¦ãã®åèªæ½åºæ°",min_value=20,max_value=50,value=50,step=5)
  submittted = st.form_submit_button("ã¯ã¼ãæ½åº")
  if submittted:
    values,feature_names,tfidf_df = tf_idf(docs)
    df = pd.DataFrame(tfidf_df.T[index].sort_values(ascending=False)[:y])  
    st.dataframe(df)  
    
    # vecs_dic(feature_names,values,z)
    
    
  

   