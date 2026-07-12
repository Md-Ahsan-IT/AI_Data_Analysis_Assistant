import streamlit as st
import os
import pandas as pd
from analysis import DataAnalyzer
from visualization import (
    generate_category_sales_chart,
    generate_region_orders_chart,
    generate_city_orders_chart,
    generate_sales_trend_chart,
    generate_sales_distribution_chart
)

st.set_page_config(page_title="AI Data Analysis Assistant", layout="wide")

st.title("📊 AI-Powered Data Analysis Assistant")
st.subheader("Track A - Explorer | Bonus Feature Dashboard")

# Sidebar for file upload
st.sidebar.header("Upload your Dataset (CSV)")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Agar koi file upload nahi hui toh default dataset use karein
if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp_dataset.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    csv_path = "temp_dataset.csv"
else:
    csv_path = "dataset.csv"

# Check if dataset exists before proceeding
if os.path.exists(csv_path):
    analyzer = DataAnalyzer(csv_path)
    analyzer.load_data()
    stats = analyzer.compute_statistics()

    # Layout: Summary and Visualizations side by side
    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("### 📋 Dataset Summary")
        st.write(f"**Total Rows:** {stats.get('total_rows', 0)}")
        st.write(f"**Total Columns:** {stats.get('total_columns', 0)}")
        
        # Format sales safely
        avg_sales = stats.get('average_sales', 0)
        st.write(f"**Average Sales/Value:** ${avg_sales:,.2f}")
        
        tot_profit = stats.get('total_profit', 0)
        st.write(f"**Total Profit/Summary:** ${tot_profit:,.2f}")

        # Judge Questions Section
        st.write("### ❓ Judge Questions & Answers")
        
        q1 = "Which product/sub-category generated the highest sales?"
        st.info(f"**Q: {q1}**\n\nA: {analyzer.answer_question(q1)}")
        
        q2 = "Which city has the maximum orders?"
        st.info(f"**Q: {q2}**\n\nA: {analyzer.answer_question(q2)}")
        
        q3 = "Which category appears most frequently?"
        st.info(f"**Q: {q3}**\n\nA: {analyzer.answer_question(q3)}")

    with col2:
        st.write("### 📈 Visualizations")
        
        # Automatically generate all 5 charts safely in the background
        chart1 = generate_category_sales_chart(analyzer.df)
        chart2 = generate_region_orders_chart(analyzer.df)
        chart3 = generate_city_orders_chart(analyzer.df)
        chart4 = generate_sales_trend_chart(analyzer.df)
        chart5 = generate_sales_distribution_chart(analyzer.df)

        # Dropdown menu for layouts matching your 5 chart files
        chart_option = st.selectbox(
            "Select Chart Layout",
            ["Category Distribution", "Top Sub-Categories", "Top Cities/Groups", "Sales Trend", "Sales Distribution"]
        )

        # Render charts safely by checking if the file was actually generated
        if chart_option == "Category Distribution" and os.path.exists(chart2):
            st.image(chart2, caption="Order Distribution Chart", use_container_width=True)
            
        elif chart_option == "Top Sub-Categories" and os.path.exists(chart1):
            st.image(chart1, caption="Top Sub-Categories Sales Bar Chart", use_container_width=True)
            
        elif chart_option == "Top Cities/Groups" and os.path.exists(chart3):
            st.image(chart3, caption="Top Cities/Groups Order Count Chart", use_container_width=True)
            
        elif chart_option == "Sales Trend" and os.path.exists(chart4):
            st.image(chart4, caption="Sales/Value Trend Over Time", use_container_width=True)
            
        elif chart_option == "Sales Distribution" and os.path.exists(chart5):
            st.image(chart5, caption="Value/Sales Frequency Distribution Histogram", use_container_width=True)
        else:
            st.warning("This specific chart layout is unavailable for the uploaded dataset format.")

else:
    st.warning("Please upload a dataset or ensure 'dataset.csv' is present in the project folder.")
