import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Compass SoCal Trends", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- MANUAL DATA UPDATE DATE ---
# Update this string whenever you add new weekend data to the 'data' dictionary below
LAST_DATA_UPDATE = "January 22, 2025" 

# 2. Sidebar UI & Toggle Logic
with st.sidebar:
    st.header("Dashboard Settings")
    dark_mode = st.toggle("Dark Mode", value=False)
    st.markdown("---")
    st.header("Filters")
    
    data = {
        "Location": [
            "Beverly Hills & Surrounding", "Westside", "Pasadena & SGV",
            "Hollywood & Eastside", "San Fernando Valley", "Orange County",
            "South Bay", "South Los Angeles", "Palm Springs",
            "Santa Clarita Valley", "Topanga & Malibu", "Central Coast", "Conejo Valley"
        ],
        "Sept 13-14": [6.10, 6.66, 9.96, 8.96, 6.29, 6.38, 8.22, 3.25, 4.07, 3.60, 2.50, 0, 0],
        "Sept 20-21": [7.07, 12.96, 9.22, 10.13, 4.64, 7.6, 8.39, 6.5, 0, 8.0, 6.2, 8.57, 10.67],
        "Oct 4-5": [6.38, 10.70, 11.95, 6.35, 5.06, 5.64, 7.40, 6.71, 8.00, 4.63, 4.40, 3.00, 5.00],
        "Oct 11-12": [5.07, 9.17, 8.71, 6.48, 4.38, 7.21, 9.31, 5.67, 6.54, 5.75, 3.67, 5.11, 18.40],
        "Oct 18-19": [5.33, 8.34, 16.00, 8.62, 7.13, 6.48, 9.16, 6.88, 6.34, 4.20, 9.00, 4.00, 7.25],
        "Oct 25-26": [4.62, 15.04, 15.59, 8.44, 5.78, 10.11, 10.09, 6.29, 7.19, 6.36, 7.63, 4, 7.57],
        "Nov 8-9": [5.5, 9.82, 10.44, 6.14, 5.52, 9.48, 6.94, 6.33, 7.31, 4.2, 3.25, 3.86, 5.83],
        "Nov 15-16": [6.63, 3.57, 22.65, 5.79, 3.65, 4.97, 7.71, 8.00, 8.47, 11.00, 1.54, 9.33, 2.00],
        "Nov 22-23": [3.44, 8.86, 7.95, 7.15, 5.20, 7.00, 6.03, 4.43, 5.53, 4.14, 4.00, 8.77, 7.25],
        "Nov 29-30": [4.25, 7.00, 5.71, 6.08, 6.15, 5.39, 4.25, 8.00, 6.40, 1.67, 4.00, 13.75, 0.00],
        "Dec 6-7": [4.42, 16.02, 9.79, 7.28, 8.09, 7.78, 8.04, 14.60, 4.17, 3.17, 3.00, 9.27, 4.00],
        "Dec 13-14": [4.88, 12.83, 6.80, 7.31, 6.00, 4.93, 4.12, 6.00, 4.45, 3.50, 3.80, 5.33, 4.00],
        "Jan 3-4": [8.25, 23.00, 8.29, 9.63, 3.25, 5.00, 7.00, 0.00, 6.83, 26.00, 0.00, 3.50, 0.00],
        "Jan 10-11": [8.69, 12.09, 12.45, 6.95, 6.13, 7.78, 11.39, 8.20, 9.21, 11.67, 3.67, 0.00, 15.00],
        "Jan 17-18": [5.60, 9.59, 9.47, 12.23, 8.42, 7.07, 12.92, 1.00, 8.19, 4.85, 5.67, 0.00, 22.33],
        "Jan 24-25": [5.63, 9.02, 14.28, 6.41, 10.36, 10.09, 13.65, 15.29, 8.33, 7.57, 5.20, 0.00, 22.50],
        "Jan 31-Feb 1": [8.29, 11.16, 16.35, 13.21, 8.43, 9.56, 17.92, 7.8, 7.31, 7.0, 5.82, 12.33]
    }
    df = pd.DataFrame(data)
    towns = sorted(df["Location"].unique())
    selected_town = st.selectbox("Select a Location:", ["All Towns"] + towns)

# 3. Theme-Based Variables
if dark_mode:
    bg_color = "#0E1117"
    text_color = "#FFFFFF"
    chart_template = "plotly_dark"
    logo_url = "https://raw.githubusercontent.com/onemilligram-ctrl/socal-real-estate-dashboard/main/Compass_Logo_H_W.png"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"
    chart_template = "plotly_white"
    logo_url = "https://github.com/onemilligram-ctrl/socal-real-estate-dashboard/blob/main/Compass_Logo_Black_Horizontal%20Only.png?raw=true"

# CSS Injection
theme_css = f"""
    <style>
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label {{
        background-color: {bg_color};
        color: {text_color} !important;
    }}
    header[data-testid="stHeader"] {{ background-color: {bg_color} !important; }}
    [data-testid="stSidebar"] {{ background-color: {bg_color}; border-right: 1px solid #444; }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{ color: {text_color} !important; }}
    #MainMenu {{visibility: hidden;}} 
    footer {{visibility: hidden;}}    
    .stAppDeployButton {{display:none;}} 
    .stAppViewMain {{padding-top: 0rem;}}
    </style>
    """
st.markdown(theme_css, unsafe_allow_html=True)

# 4. Branding
col1, _ = st.columns([1, 4])
with col1:
    st.image(logo_url, width=200)

st.markdown("---")
st.title("🏡 SoCal Open House Attendance Dashboard")

# 5. Data Processing & Filter
df_melted = df.melt(id_vars=["Location"], var_name="Weekend", value_name="Average Attendance")
filtered_df = df_melted if selected_town == "All Towns" else df_melted[df_melted["Location"] == selected_town]

# 6. Chart Logic
fig = px.line(
    filtered_df, 
    x="Weekend", 
    y="Average Attendance", 
    color="Location", 
    markers=True,
    title=f"Attendance Trends: {selected_town}", 
    template=chart_template
)

# 7. Chart Refinement
fig.update_layout(
    paper_bgcolor=bg_color, 
    plot_bgcolor=bg_color, 
    font=dict(color=text_color),
    title=dict(font=dict(color=text_color)), 
    legend=dict(font=dict(color=text_color)),
    xaxis=dict(gridcolor='#444' if dark_mode else '#eee', tickfont=dict(color=text_color), title_font=dict(color=text_color)),
    yaxis=dict(gridcolor='#444' if dark_mode else '#eee', tickfont=dict(color=text_color), title_font=dict(color=text_color))
)

st.plotly_chart(fig, use_container_width=True)

# 8. Static Timestamp
st.markdown("---")
st.caption(f"Data Last Updated: {LAST_DATA_UPDATE}")
