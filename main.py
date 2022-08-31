# main.py
import streamlit as st
import pandas as pd
import os
from PIL import Image

st.markdown("## 📖 有価証券報告書 分析アプリ")

img = Image.open("utils/img_ir_01.jpeg")
st.image(img)