import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# 1. Page Configuration
st.set_page_config(page_title="Compass SoCal Trends", layout="wide")

# 2. Interface Cleanup (Hiding GitHub/Header)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;} 
            footer {visibility: hidden;}    
            header {visibility: hidden;}    
            .stAppDeployButton {display:none;} 
            .stAppViewMain {padding-top: 0rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Header & Branding
col1, _ = st.columns([1, 4])
with col1:
    logo_url = "https://raw.githubusercontent.com/onemilligram-ctrl/socal-real-estate-dashboard/main/Compass_Logo_H_W.png"
    st.image(logo_url, width=200)

st.markdown("---")
st.title("SoCal Open House Attendance Trends")

# 4. FULL DATASET
data = {
    'Property Area': [
        'Malibu', 'Pacific Palisades', 'Santa Monica', 'Venice', 'Marina Del Rey',
        'Mar Vista', 'Culver City', 'Brentwood', 'Westwood', 'Beverly Hills',
        'Beverly Hills Post Office', 'Bel Air', 'Holmby Hills', 'West Hollywood',
        'Hollywood Hills', 'Sunset Strip', 'Hancock Park', 'Los Feliz',
        'Silver Lake', 'Echo Park', 'Studio City', 'Sherman Oaks', 'Encino',
        'Tarzana', 'Woodland Hills', 'Calabasas', 'Agoura Hills', 'Westlake Village'
    ],
    'Attendance': [45, 38, 52, 48, 35, 42, 40, 44, 39, 30, 25, 20, 15, 55, 41, 37, 33, 46, 50, 47, 43, 41, 36, 32, 34, 28, 26, 24]
}
df = pd.DataFrame(data)

# 5. MAIN CHART
fig = px.bar(
    df, 
    x='Property Area', 
    y='Attendance',
    title="Average Open House Attendance by Neighborhood",
    labels={'Attendance': 'Avg. Visitors', 'Property Area': 'Neighborhood'},
    template="plotly_white",
    color_discrete_sequence=['#000000']
)
st.plotly_chart(fig, use_container_width=True)

# 6. PACIFIC TIME TIMESTAMP (The Fix)
st.markdown("---")
# This forces the clock to use Los Angeles time regardless of where the server is
tz = pytz.timezone('US/Pacific')
now = datetime.now(tz).strftime("%B %d, %Y at %I:%M %p")
st.caption(f"App Last Refreshed: {now} PT")
