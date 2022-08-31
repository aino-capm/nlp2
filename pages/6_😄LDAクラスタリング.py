import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import japanize_matplotlib
import pickle
import plotly.express as px
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel
import pickle
from wordcloud import WordCloud
from PIL import Image
import os
import math


st.markdown("## トピックモデルによるクラスタリング")
st.caption("LDAモデルで全文書をクラスタリングし、クラスターごとにワードクラウドで可視化します")
st.markdown("***")



state = st.radio("文書の種類を選択してください",("経営方針","事業等のリスク"))
if state == "経営方針":
  file_path = "models/docs_keiei_2203_lda.bin"
else:
  file_path = "models/docs_risk_2203_lda.bin"

with open(file_path,"rb") as p:
    sentences = pickle.load(p)
dictionary = Dictionary(sentences)


st.markdown("#### パラメータの設定")
with st.form("form"):

  st.caption("出現がx文書に満たない単語と、y%以上の文書に出現する単語を極端と見做し削除する")
  x = st.slider("低頻度単語の削除：最低出現文書数",min_value=100,max_value=500)
  y = st.slider("高頻度単語の削除：最大出現文書率",min_value=0.5,max_value=1.0)
  z = st.number_input("クラスタ数の設定",min_value=4,max_value=20,value=6,step=2)
  submittted = st.form_submit_button("実行")
  if submittted:
# トピック数を指定してモデルを学習
    dictionary.filter_extremes(no_below=x,no_above=y)
    corpus = [dictionary.doc2bow(text) for text in sentences]
    lda = LdaModel(corpus, id2word =dictionary, num_topics=z)

# import pyLDAvis
# import pyLDAvis.gensim_models as gensimvis

# vis = gensimvis.prepare(lda, corpus, dictionary, sort_topics=False)
# pyLDAvis.save_html(vis, './pyldavis_output.html')

    
    fig, axs = plt.subplots(ncols=2, nrows=int(math.ceil(z/2)), figsize=(20,20))
    axs = axs.flatten()


    mask = np.array(Image.open("utils/phpYSbfIJ.png"))

    for i, t in enumerate(range(lda.num_topics)):
      x = dict(lda.show_topic(t, 30))
      im = WordCloud(
        font_path='fonts/Shippori_Mincho/ShipporiMincho-Regular.ttf',
        background_color='white',
        colormap = "viridis",
        mask=mask,
        random_state=0
        ).generate_from_frequencies(x)
      axs[i].imshow(im)
      axs[i].axis('off')
      axs[i].set_title('Topic '+str(t))
    plt.tight_layout()
    st.pyplot(fig)
