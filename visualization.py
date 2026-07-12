"""
visualization.py
-----------------
Generates charts dynamically for the AI Data Analysis Assistant.
Automatically detects alternative columns to prevent crashes on non-Superstore datasets.
"""

import os
import matplotlib
matplotlib.use("Agg")  # allows chart generation without a display
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("whitegrid")


def _get_dynamic_columns(df):
    """Helper function to auto-detect text, numeric, and date columns if standard ones are missing."""
    text_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    # Defaults with smart fallbacks
    x_subcat = 'Sub-Category' if 'Sub-Category' in df.columns else (text_cols[1] if len(text_cols) > 1 else (text_cols[0] if text_cols else None))
    y_sales = 'Sales' if 'Sales' in df.columns else (num_cols[0] if num_cols else None)
    cat_col = 'Category' if 'Category' in df.columns else (text_cols[0] if text_cols else None)
    city_col = 'City' if 'City' in df.columns else (text_cols[2] if len(text_cols) > 2 else (text_cols[0] if text_cols else None))
    date_col = 'Order Date' if 'Order Date' in df.columns else None
    
    # If no explicit Date column, check if any column can be parsed as datetime
    if not date_col:
        for col in df.columns:
            if "date" in col.lower() or "time" in col.lower():
                date_col = col
                break
                
    return x_subcat, y_sales, cat_col, city_col, date_col


def generate_category_sales_chart(df, output_path="charts/category_sales_chart.png"):
    """Generates a bar chart showing Top Categories/Sub-Categories by Value."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    x_col, y_col, _, _, _ = _get_dynamic_columns(df)
    
    if not x_col or not y_col:
        return output_path  # Skip if data types don't match

    # Group and get top 5
    subcat_sales = df.groupby(x_col)[y_col].sum().sort_values(ascending=False).head(5)

    plt.figure(figsize=(9, 5))
    colors = sns.color_palette("viridis", len(subcat_sales))
    bars = plt.bar(subcat_sales.index, subcat_sales.values, color=colors, edgecolor="grey", alpha=0.85)

    plt.title(f"Top {x_col} by Total {y_col}", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel(x_col, fontsize=11)
    plt.ylabel(y_col, fontsize=11)
    plt.xticks(rotation=15 if df[x_col].astype(str).str.len().max() > 10 else 0)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + (height * 0.01),
                  f"${height:,.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def generate_region_orders_chart(df, output_path="charts/region_orders_chart.png"):
    """Generates a pie chart showing Category Distribution (Order Counts)."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    _, _, cat_col, _, _ = _get_dynamic_columns(df)
    
    if not cat_col:
        return output_path

    category_counts = df[cat_col].value_counts().head(5) # limit to top 5 for neat pie chart

    plt.figure(figsize=(7, 7))
    colors = sns.color_palette("pastel", len(category_counts))
    
    plt.pie(
        category_counts.values, 
        labels=category_counts.index, 
        autopct=lambda p: f'{p:.1f}%\n({p * sum(category_counts.values) / 100:.0f} items)',
        colors=colors, 
        startangle=140,
        textprops={'fontsize': 11}
    )
    
    plt.title(f"Distribution by {cat_col} (Total Count)", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def generate_city_orders_chart(df, output_path="charts/city_orders_chart.png"):
    """Generates a horizontal bar chart for Top Groups/Cities by Orders."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    _, _, _, city_col, _ = _get_dynamic_columns(df)
    
    if not city_col:
        return output_path

    city_counts = df[city_col].value_counts().head(5)

    plt.figure(figsize=(9, 5))
    colors = sns.color_palette("coolwarm", len(city_counts))
    bars = plt.barh(city_counts.index, city_counts.values, color=colors, edgecolor="grey", alpha=0.85)

    plt.title(f"Top {city_col} by Total Records/Orders", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Count", fontsize=11)
    plt.ylabel(city_col, fontsize=11)
    plt.gca().invert_yaxis()

    for bar in bars:
        width = bar.get_width()
        plt.text(width + (width * 0.01), bar.get_y() + bar.get_height()/2,
                 f"{int(width)} counts", ha="left", va="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def generate_sales_trend_chart(df, output_path="charts/sales_trend_chart.png"):
    """Generates a LINE CHART showing dynamic time trend if date column is present."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    _, y_col, _, _, date_col = _get_dynamic_columns(df)
    
    if not date_col or not y_col:
        return output_path

    try:
        df_trend = df.copy()
        df_trend[date_col] = pd.to_datetime(df_trend[date_col], errors='coerce')
        df_trend = df_trend.dropna(subset=[date_col])
        
        # Monthly grouping
        monthly_sales = df_trend.groupby(df_trend[date_col].dt.to_period("M"))[y_col].sum().reset_index()
        monthly_sales[date_col] = monthly_sales[date_col].astype(str)

        if monthly_sales.empty:
            return output_path

        plt.figure(figsize=(10, 5))
        plt.plot(monthly_sales[date_col], monthly_sales[y_col], marker='o', color='#10b981', linewidth=2.5)
        
        plt.title(f"Trend Over Time ({y_col})", fontsize=14, fontweight="bold", pad=15)
        plt.xlabel("Timeline", fontsize=11)
        plt.ylabel(y_col, fontsize=11)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
    except Exception:
        pass # Safeguard against parsing errors
        
    return output_path


def generate_sales_distribution_chart(df, output_path="charts/sales_dist_chart.png"):
    """Generates a HISTOGRAM showing the distribution of the primary numeric column."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    _, y_col, _, _, _ = _get_dynamic_columns(df)
    
    if not y_col:
        return output_path
        
    plt.figure(figsize=(9, 5))
    sns.histplot(df[y_col], bins=20, kde=True, color="#3b82f6", edgecolor="black", alpha=0.7)

    plt.title(f"Distribution of {y_col} Values", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel(y_col, fontsize=11)
    plt.ylabel("Frequency", fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path
