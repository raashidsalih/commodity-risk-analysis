# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to plot the number of articles over time
def plot_articles_over_time(df):
    df['published_date'] = pd.to_datetime(df['published_date'])
    articles_over_time = df.groupby(df['published_date'].dt.date).size()
    plt.figure(figsize=(14, 7))
    articles_over_time.plot(title='Number of Articles Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    st.pyplot(plt)

# Function to plot the sentiment over time
def plot_sentiment_over_time(df):
    df['published_date'] = pd.to_datetime(df['published_date'])
    sentiment_over_time = df.groupby([df['published_date'].dt.date, 'sentiment']).size().unstack().fillna(0)
    plt.figure(figsize=(14, 7))
    sentiment_over_time.plot(title='Number of Positive, Negative, and Neutral Articles Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.legend(title='Sentiment')
    plt.gcf().set_size_inches(14,7)
    st.pyplot(plt)

# Streamlit interface design
# st.markdown("<h1 style='text-align: center; color: grey;'>FreightFox</h1>", unsafe_allow_html=True)

# Load the list of commodities from the header row of 'keywords.csv'
keywords_df = pd.read_csv('keywords.csv')
commodities = keywords_df.columns.tolist()

st.sidebar.markdown("<h1 style='text-align: center; color: grey;'>FreightFox</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: center; color: white;'>Commodity Risk Analysis</h1>", unsafe_allow_html=True)
# Dropdown to choose a commodity
selected_commodity = st.sidebar.selectbox(label = "Choose a Commodity: ", options = commodities, index=None)


# Load the data for the selected commodity
if selected_commodity:
    file_path = f'data/{selected_commodity}_Final.xlsx'
    try:
        commodity_df = pd.read_excel(file_path)
        st.success(f'Data loaded for {selected_commodity}')

        # Display the plots
        st.subheader('Number of Articles Over Time')
        plot_articles_over_time(commodity_df)

        st.subheader('Sentiment Over Time')
        plot_sentiment_over_time(commodity_df)

        st.subheader('Explore Data')
        st.dataframe(commodity_df)

    except FileNotFoundError:
        st.error(f'Data not found: {selected_commodity}')
    except Exception as e:
        st.error(f'An error occurred: {e}')

if __name__ == "__main__":
    run()
