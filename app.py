import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# 1. Page Configuration (Set to expanded by default)
st.set_page_config(
    page_title="Compass SoCal Trends", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# 2. Updated Interface Cleanup (Hides GitHub, but KEEPS Sidebar visible)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;} 
            footer {visibility: hidden;}    
            .stAppDeployButton {display:none;} 
            
            /* This forces the sidebar to stay open and visible */
            [data-testid="stSidebar"] {
                display: block !important;
                visibility: visible !important;
                min-width: 250px !important;
            }
            
            /* Removes the extra gap at the top */
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
st.title("🏡 SoCal Open House Attendance Dashboard")

# 4. Full Dataset
data = {
    "Location": [
        "Beverly Hills & Surrounding", "Westside", "Pasadena & SGV",
        "Hollywood & Eastside", "San Fernando Valley", "Orange County",
        "South Bay", "South Los Angeles", "Palm Springs",
        "Santa Clarita Valley", "Topanga & Malibu", "Central Coast", "Conejo Valley"
    ],
    "Nov 15-16": [6.63, 3.57, 22.65, 5.79, 3.65, 4.97, 7.71, 8.00, 8.47, 11.00, 1.54, 9.33, 2.00],
    "Nov 22-23": [3.44, 8.86, 7.95, 7.15, 5.20, 7.00, 6.03, 4.43, 5.53, 4.14, 4.00, 8.77, 7.25],
    "Nov 29-30": [4.25, 7.00, 5.71, 6.08, 6.15, 5.39, 4.25, 8.00, 6.40, 1.67, 4.00, 13.75, 0.00],
    "Dec 6-7": [4.42, 16.02, 9.79, 7.28, 8.09, 7.78, 8.04, 14.60, 4.17, 3.17, 3.00, 9.27, 4.00],
    "Dec 13-14": [4.88, 12.83, 6.80, 7.31, 6.00, 4.93, 4.12, 6.00, 4.45, 3.50, 3.80, 5.33, 4.00],
    "Jan 3-4": [8.25, 23.00, 8.29, 9.63, 3.25, 5.00, 7.00, 0.00, 6.83, 26.00, 0.00, 3.50, 0.00],
    "Jan 10-11": [8.69, 12.09, 12.45, 6.95, 6.13, 7.78, 11.39, 8.20, 9.21, 11.67, 3.67, 0.00, 15.00],
    "Jan 17-18": [5.60, 9.59, 9.47, 12.23, 8.42, 7.07, 12.92, 1.00, 8.19, 4.85, 5.67, 0.00, 22.33]
}

# 5. Transform Data
df = pd.DataFrame(data)
df_melted = df.melt(id_vars=["Location"], var_name="Weekend", value_name="Attendance")

# 6. Sidebar UI
# Content here guarantees the sidebar has elements to show
with st.sidebar:
    st.header("Dashboard Filters")
    towns = sorted(df["Location"].unique())
    selected_town = st.selectbox("Select a Location:", ["All Towns"] + towns)
    st.info("The chart will update automatically based on your selection.")

# 7. Filtering Logic
if selected_town == "All Towns":
    filtered_df = df_melted
else:
    filtered_df = df_melted[df_melted["Location"] == selected_town]

# 8. Chart
fig = px.line(filtered_df, x="Weekend", y="Attendance", color="Location", markers=True,
              title=f"Attendance Trends: {selected_town}")
st.plotly_chart(fig, use_container_width=True)

# 9. Automatic Timestamp in Pacific Time
st.markdown("---")
tz = pytz.timezone('US/Pacific') 
now = datetime.now(tz).strftime("%B %d, %Y at %I:%M %p")
st.caption(f"App Last Refreshed: {now} PT")
