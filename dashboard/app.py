import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from controller import GeoSentinalController

# Page Configuration
st.set_page_config(page_title="GeoSentinal AI", layout="wide")

st.title("🛡️ GeoSentinal: Global Geopolitical Tension Index")
st.markdown("""
**Hybrid AI Framework** for real-time quantification of geopolitical tension. 
Using **Military (MCT)** and **Narrative (INT)** pillars with **PCA Dynamic Weighting**.
""")

# Sidebar for User Inputs
st.sidebar.header("Control Panel")
country_a = st.sidebar.text_input("Country A", "India")
country_b = st.sidebar.text_input("Country B", "Pakistan")
analyze_btn = st.sidebar.button("Run Real-Time Analysis")

if analyze_btn:
    with st.spinner(f"Analyzing {country_a}-{country_b} relationship..."):
        # Controller ko call karna logic execute karne ke liye
        ctrl = GeoSentinalController()
        results = ctrl.run_daily_pipeline(country_a, country_b)

    # --- TOP ROW: KPI Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Current GPTI Index", f"{results['gpti']:.2f}")
    col2.metric("Pillar 1: Kinetic (MCT)", f"{results['mct']:.2f}")
    col3.metric("Pillar 2: Narrative (INT)", f"{results['int']:.2f}")

    # --- MIDDLE ROW: Main GPTI Trend Chart ---
    st.subheader(f"Geopolitical Tension Trend: {country_a} vs {country_b}")
    # Simulating a trend for visualization as per PDF validation steps
    chart_data = pd.DataFrame({
        'Date': pd.date_range(start='2026-03-01', periods=10),
        'GPTI': [results['gpti'] * (1 + (i*0.05)) for i in range(10)]
    })
    fig_gpti = px.line(chart_data, x='Date', y='GPTI', title="Aggregated GPTI Score")
    st.plotly_chart(fig_gpti, use_container_width=True)

    # --- BOTTOM ROW: Pillar Analysis & PCA Weights ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Pillar Breakdown")
        # Synchronization chart logic for MCT vs INT
        fig_pillars = go.Figure()
        fig_pillars.add_trace(go.Scatter(y=[results['mct']], name="MCT (Kinetic)", mode='lines+markers'))
        fig_pillars.add_trace(go.Scatter(y=[results['int']], name="INT (Narrative)", mode='lines+markers'))
        st.plotly_chart(fig_pillars, use_container_width=True)

    with c2:
        st.subheader("PCA Weight Distribution")
        # Stacked area chart showing evolution of weights
        weight_df = pd.DataFrame({
            'Component': ['Kinetic (w_mct)', 'Narrative (w_int)'],
            'Weight': [results['weights']['w_mct'], results['weights']['w_int']]
        })
        fig_weights = px.pie(weight_df, values='Weight', names='Component', hole=0.4)
        st.plotly_chart(fig_weights, use_container_width=True)

    # --- FOOTER: AI Reasoning ---
    st.info(f"**AI Sentinel Reasoning:** This index reflects current events processed via Hybrid AI labor division.")

else:
    st.info("Select countries and click 'Run Analysis' to see the Live Geopolitical Index.")