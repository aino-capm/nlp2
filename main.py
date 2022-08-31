# main.py
import streamlit as st
import pandas as pd
import os
from PIL import Image

st.markdown("## 有価証券報告書 分析アプリ")

img = Image.open("utils/img_ir_01.jpeg")
st.image(img)

markdown = """
- 有価証券報告書に記載されているテキストデータを分析します。
- 分析ができるテキストデータは次の2種類です。
 1. 経営方針:1【経営方針、経営環境および対処すべき課題等】
 2. 事業等のリスク:2【事業等のリスク】

- 対象は2022年3月期決算の有価証券報告書（約2,500社）になります。

- 以下の分析が可能です。右のサイドバーをクリックしてください。
##### テキスト・キーワード検索
※2021年3月期決算の有価証券報告書も検索可能です。
##### TF-IDF重要語抽出
##### 類似文書検索
##### t-SNE可視化
##### LDAクラスタリング
"""