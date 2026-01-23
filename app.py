import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# 1. PAGE SETUP (Must be first)
st.set_page_config(page_title="Compass SoCal Trends", layout="wide")

# 2. HIDE GITHUB/HEADER
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

# 3. YOUR DATA 
# (Make sure this is defined BEFORE the sidebar)
data = {
    'Location': ['Beverly Hills', 'Santa Monica', 'Venice', 'Malibu', 'Silver Lake', 'Sherman Oaks'],
    'Attendance': [45, 32, 28, 15, 50, 22]
}
df = pd.DataFrame(data)

# 4. BRANDING
col1, _ = st.columns([1, 4])
with col1:
    logo_url = "https://raw.githubusercontent.com/onemilligram-ctrl/socal-real-estate-dashboard/main/Compass_Logo_H_W.png"
    st.image(logo_url, width=200)

st.markdown("---")

# 5. SIDEBAR & DROPDOWN (This defines 'selected_location')
with st.sidebar:
    st.header("Dashboard Filters")
    locations = sorted(df["Location"].unique().tolist())
    location_list = ["All Locations"] + locations
    
    # This line creates the variable that was causing your error
    selected_location = st.selectbox("Select a Neighborhood:", options=location_list)

# 6. FILTERING LOGIC (Must come AFTER the selectbox)
if selected_location == "All Locations":
    display_df = df
else:
    display_df = df[df["Location"] == selected_location]

# 7. MAIN CONTENT (Charts)
st.subheader(f"Attendance Trends: {selected_location}")
fig = px.bar(display_df, x='Location', y='Attendance', color_discrete_sequence=['#000000'])
st.plotly_chart(fig, use_container_width=True)

# 8. PACIFIC TIMESTAMP (At the very bottom)
st.markdown("---")
tz = pytz.timezone('US/Pacific')
now = datetime.now(tz).strftime("%B %d, %Y at %I:%M %p")
st.caption(f"App Last Refreshed: {now} PT")
