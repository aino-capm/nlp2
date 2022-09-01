# main.py
import streamlit as st
import pandas as pd
import os
from PIL import Image

st.markdown("## 有価証券報告書 分析アプリ")
st.markdown("&nbsp;")

img = Image.open("utils/img_ir_01.jpeg")
st.image(img)
st.markdown("&nbsp;")

markdown = """

##### 有価証券報告書に記載されているテキストデータを分析します。
&nbsp;
##### 🎤【経営方針、経営環境および対処すべき課題等】と【事業等のリスク】を分析します。
&nbsp;
##### 対象は2022年3月期決算の有価証券報告書（約2,500社）になります。
&nbsp;
##### 右のサイドバーをクリックしてください。

"""

st.markdown(markdown)