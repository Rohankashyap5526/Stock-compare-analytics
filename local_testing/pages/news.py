import streamlit as st
import plotly.express as px

# from utils import *
# from configuration import *
import logging
import requests
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger()
logger.setLevel(logging.INFO)

st.title("News Data Analytics")

# Rest API
parameters = {
    "start": "2022-07-01T0:00:00Z",
    "symbols": "AAPL,AMZN,META,NFLX,TSLA",
    "limit": "50",
    "sort": "ASC",
}
headers = {
    "APCA-API-KEY-ID": "PKF2QMR530IM4SKCFZ68",
    "APCA-API-SECRET-KEY": "4BGfZRQbMFZ67U0x5M8bayTUgUcP1qpK6lfdq1Zd",
}
response = requests.get(
    "https://data.alpaca.markets/v1beta1/news?", params=parameters, headers=headers
)

# Create the DataFrame for the News API
df = pd.DataFrame.from_dict(response.json()["news"])

# Most Frequent Words Plot
st.subheader("Most Frequent Words")
text = " ".join(i for i in df["summary"])
STOPWORDS = ["S"] + list(STOPWORDS)
stopwords = set(STOPWORDS)
wordcloud = WordCloud(stopwords=stopwords, background_color="black").generate(text)
# print(text)
plt.figure(figsize=(15, 10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
# plt.show()
# st.set_option("deprecation.showPyplotGlobalUse", False)
st.pyplot(plt)

# Authors Plot
fig = px.bar(df, x="author")
st.subheader("Authors Plot")
st.plotly_chart(fig)

# Most Cited Symbols/Companies Plot
st.subheader("Most Cited Symbols")

# Flatten the list of symbols
join_df = np.concatenate(df["symbols"].values).ravel()

# Filter relevant symbols
symbols = ["AAPL", "META", "NFLX", "AMZN", "TSLA"]
filtered_symbols = [symbol for symbol in join_df if symbol in symbols]

# Count occurrences
symbol_counts = pd.Series(filtered_symbols).value_counts().reset_index()
symbol_counts.columns = ["Symbol", "Count"]

# Create Plotly bar chart
fig = px.bar(symbol_counts, x="Symbol", y="Count", title="Most Cited Symbols")
fig.update_layout(showlegend=False)  # ✅ Apply update before rendering

# Render chart
st.plotly_chart(fig)
