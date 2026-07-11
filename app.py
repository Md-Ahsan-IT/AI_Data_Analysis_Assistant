import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from analysis import DataAnalyzer

# Page Configuration (Better UI & Dark/Light Theme Support)
st.set_page_config(page_title="AI Data Assistant", page_icon="📊", layout="wide")

st.title("📊 AI-Powered Data Analysis Assistant")
st.markdown("### Track A - Explorer | Bonus Feature Dashboard")

# Step 1: CSV Upload Button (Bonus Feature)
uploaded_file = st.sidebar.file_uploader("Upload your Dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    # Save uploaded file temporarily to work with your DataAnalyzer class
    with open("temp_dataset.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # Initialize your existing analyzer
    analyzer = DataAnalyzer("temp_dataset.csv")
    analyzer.load_data()
    
    # Calculate statistics using your existing logic
    stats = analyzer.compute_statistics()
    
    # ---- UI LAYOUT ----
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📋 Dataset Summary")
        st.write(f"**Total Rows:** {stats['total_records']}")
        st.write(f"**Columns:** {len(analyzer.df.columns)}")
        st.write(f"**Average Sales:** ${stats['average_sales']:,.2f}")
        st.write(f"**Total Profit:** ${stats['total_profit']:,.2f}")
        
        st.subheader("❓ Judge Questions & Answers")
        q1 = "Which product/sub-category generated the highest sales?"
        st.info(f"**Q: {q1}**\n\n*A: {analyzer.answer_question(q1)}*")
        
        q2 = "Which city has the maximum orders?"
        st.info(f"**Q: {q2}**\n\n*A: {analyzer.answer_question(q2)}*")
        
        q3 = "Which category appears most frequently?"
        st.info(f"**Q: {q3}**\n\n*A: {analyzer.answer_question(q3)}*")

    # YAHAN FIXED: Yeh block ab bilkul sahi tarike se if condition ke andar aligned hai
    with col2:
        st.subheader("📈 Visualizations")
        
        # Teen chart options select box (Bonus Feature)
        chart_type = st.selectbox("Select Chart Layout", ["Category Distribution", "Sales Analytics", "Region Distribution"])
        
        fig, ax = plt.subplots(figsize=(8, 4))
        
        if chart_type == "Category Distribution":
            cat_data = analyzer.df['Category'].value_counts()
            sns.barplot(x=cat_data.index, y=cat_data.values, ax=ax, palette="viridis")
            ax.set_title("Orders by Category")
            ax.set_xlabel("Category")
            ax.set_ylabel("Number of Orders")
            
        elif chart_type == "Sales Analytics":
            subcat_sales = analyzer.df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(5)
            sns.barplot(x=subcat_sales.values, y=subcat_sales.index, ax=ax, palette="magma")
            ax.set_title("Top 5 Sub-Categories by Sales")
            ax.set_xlabel("Total Sales ($)")
            ax.set_ylabel("Sub-Category")
            
        elif chart_type == "Region Distribution":
            region_data = analyzer.df['Region'].value_counts()
            sns.barplot(x=region_data.index, y=region_data.values, ax=ax, palette="coolwarm")
            ax.set_title("Orders by Region")
            ax.set_xlabel("Region")
            ax.set_ylabel("Number of Orders")
            
        st.pyplot(fig)
        
        # Rule-based / AI explanation portion
        st.subheader("🤖 AI Explanation (Fallback Active)")
        explanation = (
            f"The dataset shows that office supplies or leading segments are making up a significant portion. "
            f"Specifically, average sales stand at ${stats['average_sales']:,.2f} per order line, with a total net profit "
            f"of ${stats['total_profit']:,.2f} mapped across all records."
        )
        st.success(explanation)

else:
    # Agar user ne file upload nahi ki toh yeh message dikhega
    st.info("👈 Please upload a CSV file from the sidebar to start the analysis dashboard!")