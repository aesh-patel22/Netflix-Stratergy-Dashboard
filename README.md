# Netflix-Stratergy-Dashboard
🎬 An interactive Executive Content Strategy Dashboard and Data Visualization project analyzing the Netflix dataset to drive business decisions, featuring advanced Plotly visualizations and Streamlit.

# 📈 Netflix Content Strategy & Decision Intelligence Dashboard

Welcome to the Netflix Data Visualization project! Rather than just plotting basic charts, this project acts as an **internal Business Intelligence tool**. It transforms raw Netflix catalogue data into actionable insights to answer critical strategic questions:
* *Where should Netflix establish its next regional production hubs?*
* *Is the catalog oversaturated with mature content (TV-MA) at the expense of family households?*
* *How can we optimize release timing to reduce subscriber churn?*

Built with **Python**, **Streamlit**, and **Plotly**, this project features interactive choropleth maps, treemaps, and heatmaps wrapped in a premium Netflix-dark aesthetic.

# Netflix Data Visualization Project 🎬

This project is a comprehensive Data Visualization and Exploratory Data Analysis (EDA) of the Netflix Movies and TV Shows dataset. It was built as **Task 3** for the internship program.

## Project Objectives

1. **Transform raw data into visual formats** like charts, graphs, and dashboards.
2. **Use tools like Matplotlib, Seaborn, and Plotly** for creating impactful visuals.
3. **Design visuals that enhance understanding** and reveal insights clearly.
4. **Craft compelling data stories** that support decision-making.
5. **Build a strong portfolio** with a GitHub-ready project.

## Project Structure

- `netflix_titles.csv`: The raw dataset used for the analysis.
- `Netflix_Data_Visualization.ipynb`: A Jupyter Notebook containing the static data analysis, data cleaning steps, and a step-by-step data story using Matplotlib and Seaborn.
- `app.py`: An interactive web dashboard built with Streamlit and Plotly, allowing users to filter and explore the data dynamically.
- `requirements.txt`: List of Python dependencies required to run the project.

## Key Insights Discovered

- **Movies vs. TV Shows**: Netflix's catalog is predominantly composed of Movies, though the number of original TV Shows has been increasing.
- **Content Growth**: There was a massive spike in content added between 2016 and 2019, reflecting Netflix's global expansion.
- **Top Producers**: The United States and India are the leading countries producing content for the platform.

## Setup and Installation

### 1. Clone the repository
(If you are downloading this from GitHub, clone the repo. Otherwise, navigate to the project directory).

```bash
cd "Task 3"
```

### 2. Create a Virtual Environment (Optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## How to Run

### Jupyter Notebook (Static EDA)
To view the data story and static visualizations:
```bash
jupyter notebook Netflix_Data_Visualization.ipynb
```

### Streamlit Dashboard (Interactive web app)
To launch the interactive dashboard:
```bash
streamlit run app.py
```
This will open a new tab in your web browser with the fully functional interactive dashboard.

---
or run:
https://netflix-stratergy-dashboard-nhnptqjzuxvwqwnpksjddr.streamlit.app/
