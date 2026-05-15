import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set Page Configuration
st.set_page_config(page_title="Netflix Strategy Dashboard", page_icon="📈", layout="wide")

# Custom CSS for Premium Aesthetics (Netflix Dark Theme)
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .main {
        background-color: #000000;
    }
    h1, h2, h3 {
        color: #E50914 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
    }
    .stSelectbox label, .stSlider label {
        color: #b3b3b3 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 2.5rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #b3b3b3;
    }
    .css-1r6slb0.e1tzin5v2 {
        background-color: #141414;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 20px;
    }
    .insight-box {
        background-color: rgba(229, 9, 20, 0.1);
        border-left: 4px solid #E50914;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 20px;
        border-radius: 0 5px 5px 0;
        font-size: 0.95rem;
        color: #e5e5e5;
    }
    </style>
    """, unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), format='%B %d, %Y', errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['country'] = df['country'].fillna('Unknown')
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('Unknown')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'netflix_titles.csv' not found. Please ensure the file is in the same directory.")
    st.stop()

# Header
col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=100)
with col_title:
    st.title("Executive Content Strategy Dashboard")
st.markdown("<p style='color: #b3b3b3; font-size: 1.1rem;'>Transforming raw catalogue data into actionable business intelligence to drive future content acquisition and production decisions.</p>", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.markdown("### 🎛️ Strategic Filters")
content_type = st.sidebar.multiselect(
    "Content Format:",
    options=df["type"].unique(),
    default=df["type"].unique()
)

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())
year_range = st.sidebar.slider(
    "Release Year Range:",
    min_value=min_year, max_value=max_year,
    value=(2010, max_year)
)

country_list = ['Global Overview'] + sorted(df['country'].str.split(', ').explode().dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Market Region:", options=country_list, index=0)

# Apply Filters
filtered_df = df[(df["type"].isin(content_type)) & 
                 (df["release_year"] >= year_range[0]) & 
                 (df["release_year"] <= year_range[1])]

if selected_country != 'Global Overview':
    filtered_df = filtered_df[filtered_df['country'].str.contains(selected_country, na=False)]

# Key Metrics
st.markdown("### 📊 Portfolio At A Glance")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Catalog Assets", value=f"{len(filtered_df):,}")
with col2:
    movies_pct = len(filtered_df[filtered_df['type'] == 'Movie']) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    st.metric(label="Movie Dominance", value=f"{movies_pct:.1f}%")
with col3:
    st.metric(label="Active Markets", value=filtered_df['country'].nunique())
with col4:
    recent_additions = len(filtered_df[filtered_df['year_added'] >= 2020])
    st.metric(label="Recent Additions (Post 2020)", value=f"{recent_additions:,}")

st.divider()

# Section 1: Growth & Timing Strategy
st.markdown("### 📈 1. Growth & Timing Strategy")

col_g1, col_g2 = st.columns(2)

with col_g1:
    year_counts = filtered_df['year_added'].value_counts().reset_index().sort_values('year_added')
    year_counts.columns = ['Year', 'Assets Added']
    fig_line = px.area(year_counts, x='Year', y='Assets Added', 
                       color_discrete_sequence=['#E50914'],
                       title="Content Acquisition Velocity")
    fig_line.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("""
    <div class='insight-box'>
    <strong>Decision Point:</strong> Observe the massive acceleration post-2015. Did the pivot to original content yield better retention? If acquisition is slowing down, we must shift budget from volume licensing to high-impact originals.
    </div>
    """, unsafe_allow_html=True)

with col_g2:
    if len(filtered_df) > 0:
        heatmap_data = filtered_df.groupby(['year_added', 'month_added']).size().reset_index(name='count')
        heatmap_data = heatmap_data.pivot(index='month_added', columns='year_added', values='count').fillna(0)
        fig_heat = px.imshow(heatmap_data, 
                             labels=dict(x="Year", y="Month", color="Releases"),
                             color_continuous_scale="Reds",
                             title="Release Timing Heatmap")
        fig_heat.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_heat, use_container_width=True)
        st.markdown("""
        <div class='insight-box'>
        <strong>Decision Point:</strong> Historically, are we clustering releases in Q4? Optimizing the release calendar to distribute tentpole content evenly throughout the year can reduce churn rates.
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Section 2: Global Expansion Strategy
st.markdown("### 🌍 2. Market Penetration & Expansion")

# Choropleth Map
country_counts = filtered_df['country'].str.split(', ').explode().value_counts().reset_index()
country_counts.columns = ['Country', 'Count']
# Basic mapping for plotly
country_counts['Country'] = country_counts['Country'].replace({
    'United States': 'USA', 'United Kingdom': 'UK', 'South Korea': 'South Korea'
})

fig_map = px.choropleth(country_counts, locations="Country", locationmode='country names',
                        color="Count", hover_name="Country",
                        color_continuous_scale="Reds",
                        title="Global Content Production Footprint")
fig_map.update_layout(template="plotly_dark", geo=dict(bgcolor='rgba(0,0,0,0)', showcoastlines=True, coastlinecolor="#333"),
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=40, b=0))
st.plotly_chart(fig_map, use_container_width=True)
st.markdown("""
<div class='insight-box'>
<strong>Decision Point:</strong> While the US and India dominate, look at the blank spaces on the map. To capture the next billion subscribers, where should we establish local production hubs? Africa and Southeast Asia represent untapped markets.
</div>
""", unsafe_allow_html=True)

st.divider()

# Section 3: Genre & Target Audience Strategy
st.markdown("### 🎭 3. Genre & Audience Strategy")

col_a1, col_a2 = st.columns(2)

with col_a1:
    genres = filtered_df['listed_in'].str.split(', ').explode().value_counts().reset_index().head(15)
    genres.columns = ['Genre', 'Count']
    fig_tree = px.treemap(genres, path=['Genre'], values='Count',
                          color='Count', color_continuous_scale='Reds',
                          title="Top 15 Genre Distribution")
    fig_tree.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_tree, use_container_width=True)
    st.markdown("""
    <div class='insight-box'>
    <strong>Decision Point:</strong> International Movies and Dramas take up massive real estate. Are we over-saturating this genre? We should cross-reference this with viewership metrics to see if niche genres yield higher ROI.
    </div>
    """, unsafe_allow_html=True)

with col_a2:
    rating_counts = filtered_df['rating'].value_counts().reset_index()
    rating_counts.columns = ['Rating', 'Count']
    fig_rating = px.bar(rating_counts, x='Rating', y='Count', 
                        color='Count', color_continuous_scale=['#b3b3b3', '#E50914'],
                        title="Audience Maturity Rating Profile")
    fig_rating.update_layout(template="plotly_dark", xaxis={'categoryorder':'total descending'}, 
                             plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_rating, use_container_width=True)
    st.markdown("""
    <div class='insight-box'>
    <strong>Decision Point:</strong> TV-MA dominates our catalog. If we want to reduce churn among family households, we need to significantly increase investment in TV-Y and TV-PG content to compete with Disney+.
    </div>
    """, unsafe_allow_html=True)

