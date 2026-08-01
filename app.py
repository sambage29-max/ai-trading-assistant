 with col2:
    st.metric("📈 Trend", trend)
    st.metric("🧠 AI Signal", signal)

st.metric("🎯 Confidence", "75%")
st.caption(f"✅ Last Updated: {datetime.now().strftime('%H:%M:%S')}")