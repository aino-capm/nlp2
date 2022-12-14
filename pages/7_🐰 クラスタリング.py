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


st.markdown("## ð° ã¯ã©ã¹ã¿ãªã³ã°")
st.caption("ãããã¯ã¢ãã«ï¼LDAï¼ã§å¨ææ¸ãã¯ã©ã¹ã¿ãªã³ã°ããã¯ã©ã¹ã¿ãã¨ã«ã¯ã¼ãã¯ã©ã¦ãã§å¯è¦åãã¾ã")
st.markdown("***")



state = st.radio("ææ¸ã®ç¨®é¡ãé¸æãã¦ãã ãã",("çµå¶æ¹é","äºæ¥­ç­ã®ãªã¹ã¯"))
if state == "çµå¶æ¹é":
  file_path = "models/docs_keiei_2203_lda.bin"
else:
  file_path = "models/docs_risk_2203_lda.bin"

with open(file_path,"rb") as p:
    sentences = pickle.load(p)
dictionary = Dictionary(sentences)


st.markdown("#### ãã©ã¡ã¼ã¿ã®è¨­å®")
with st.form("form"):

  st.caption("åºç¾ãxææ¸ã«æºããªãåèªã¨ãy%ä»¥ä¸ã®ææ¸ã«åºç¾ããåèªãæ¥µç«¯ã¨è¦åãåé¤ãã")
  x = st.slider("ä½é »åº¦åèªã®åé¤ï¼æä½åºç¾ææ¸æ°",min_value=100,max_value=500)
  y = st.slider("é«é »åº¦åèªã®åé¤ï¼æå¤§åºç¾ææ¸ç",min_value=0.5,max_value=1.0)
  z = st.number_input("ã¯ã©ã¹ã¿æ°ã®è¨­å®",min_value=4,max_value=20,value=6,step=2)
  submittted = st.form_submit_button("å®è¡")
  if submittted:
# ãããã¯æ°ãæå®ãã¦ã¢ãã«ãå­¦ç¿
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
