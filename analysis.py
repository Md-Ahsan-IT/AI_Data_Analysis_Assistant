"""
analysis.py
-----------
Handles CSV loading, dataset summary, statistical analysis,
and rule-based question answering for the AI Data Analysis Assistant.
Fully dynamic to prevent crashes on different datasets.
"""

import pandas as pd


class DataAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None

    # ------------------------------------------------------------------
    # Step 1 - Load Dataset
    # ------------------------------------------------------------------
    def load_data(self) -> pd.DataFrame:
        """Reads the CSV file into a pandas DataFrame."""
        self.df = pd.read_csv(self.csv_path)
        return self.df

    def dataset_summary(self) -> dict:
        """Returns basic information about the dataset."""
        if self.df is None:
            self.load_data()

        summary = {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1],
            "column_names": list(self.df.columns),
            "missing_values": self.df.isnull().sum().to_dict(),
            "data_types": self.df.dtypes.astype(str).to_dict(),
        }
        return summary

    def print_summary(self):
        summary = self.dataset_summary()
        print("\n===== DATASET SUMMARY =====")
        print(f"Total Rows       : {summary['rows']}")
        print(f"Total Columns    : {summary['columns']}")
        print(f"Column Names     : {', '.join(summary['column_names'])}")
        print("\nMissing Values per Column:")
        any_missing = False
        for col, val in summary["missing_values"].items():
            if val > 0:
                print(f"  - {col}: {val}")
                any_missing = True
        if not any_missing:
            print("  (no missing values)")
        print("\nData Types:")
        for col, dtype in summary["data_types"].items():
            print(f"  - {col}: {dtype}")
        print("============================\n")

    # ------------------------------------------------------------------
    # Step 2 - Analyze the Dataset (Fixed Indentation & Safe Fallbacks)
    # ------------------------------------------------------------------
    def compute_statistics(self):
        stats = {}
        if self.df is None:
            self.load_data()
            
        stats['total_records'] = len(self.df)
        stats['total_rows'] = len(self.df)
        stats['total_columns'] = len(self.df.columns)
        stats['column_names'] = ", ".join(self.df.columns)

        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        sales_col = 'Sales' if 'Sales' in self.df.columns else (numeric_cols[0] if numeric_cols else None)
        profit_col = 'Profit' if 'Profit' in self.df.columns else (numeric_cols[1] if len(numeric_cols) > 1 else (numeric_cols[0] if numeric_cols else None))

        if sales_col:
            stats['average_sales'] = round(self.df[sales_col].mean(), 2)
            stats['max_sales'] = round(self.df[sales_col].max(), 2)
            stats['min_sales'] = round(self.df[sales_col].min(), 2)
        else:
            stats['average_sales'] = 0.0
            stats['max_sales'] = 0.0
            stats['min_sales'] = 0.0

        if profit_col:
            stats['total_profit'] = round(self.df[profit_col].sum(), 2)
        else:
            stats['total_profit'] = 0.0
            
        stats['average_discount'] = round(self.df['Discount'].mean(), 3) if 'Discount' in self.df.columns else 0.0

        text_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        cat_col = 'Category' if 'Category' in self.df.columns else (text_cols[0] if text_cols else None)
        subcat_col = 'Sub-Category' if 'Sub-Category' in self.df.columns else (text_cols[1] if len(text_cols) > 1 else (text_cols[0] if text_cols else None))
        city_col = 'City' if 'City' in self.df.columns else (text_cols[2] if len(text_cols) > 2 else (text_cols[0] if text_cols else None))

        if cat_col:
            stats['category_distribution'] = self.df[cat_col].value_counts().head(5).to_dict()
        else:
            stats['category_distribution'] = {"No Category Found": 0}

        stats['highest_sales_product'] = self.df[subcat_col].value_counts().index[0] if subcat_col else "N/A"
        stats['highest_sales_value'] = f"{stats['max_sales']:,}"
        stats['avg_customer_age'] = round(self.df['CustomerAge'].mean(), 1) if 'CustomerAge' in self.df.columns else "N/A"
        
        if city_col:
            top_city_data = self.df[city_col].value_counts()
            stats['max_orders_city'] = top_city_data.index[0] if not top_city_data.empty else "N/A"
            stats['max_orders_count'] = int(top_city_data.iloc[0]) if not top_city_data.empty else 0
        else:
            stats['max_orders_city'] = "N/A"
            stats['max_orders_count'] = 0

        return stats

    # ------------------------------------------------------------------
    # Step 3 - Answer Natural Language Questions (Now Fully Dynamic!)
    # ------------------------------------------------------------------
    def answer_question(self, question: str) -> str:
        if self.df is None:
            self.load_data()

        q = question.lower()
        df = self.df
        
        # Dynamic Column Discovery for QA Fallbacks
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        text_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        sales_col = 'Sales' if 'Sales' in df.columns else (numeric_cols[0] if numeric_cols else None)
        profit_col = 'Profit' if 'Profit' in df.columns else (numeric_cols[1] if len(numeric_cols) > 1 else (numeric_cols[0] if numeric_cols else None))
        cat_col = 'Category' if 'Category' in df.columns else (text_cols[0] if text_cols else None)
        subcat_col = 'Sub-Category' if 'Sub-Category' in df.columns else (text_cols[1] if len(text_cols) > 1 else (text_cols[0] if text_cols else None))
        city_col = 'City' if 'City' in df.columns else (text_cols[2] if len(text_cols) > 2 else (text_cols[0] if text_cols else None))
        region_col = 'Region' if 'Region' in df.columns else (text_cols[3] if len(text_cols) > 3 else (text_cols[0] if text_cols else None))

        # 1. Product/Sub-category highest sales
        if ("product" in q or "sub-category" in q or "subcategory" in q) and ("highest" in q or "top" in q or "most sales" in q):
            if subcat_col and sales_col:
                top = df.groupby(subcat_col)[sales_col].sum().idxmax()
                total = df.groupby(subcat_col)[sales_col].sum().max()
                return f"'{top}' generated the highest values in '{sales_col}' with a total of ${total:,.2f}."
            return "Required columns for product sales analysis are missing."

        # 2. Maximum orders city
        if "city" in q and ("maximum" in q or "most" in q or "highest" in q):
            if city_col:
                top_city = df[city_col].value_counts().idxmax()
                count = df[city_col].value_counts().max()
                return f"'{top_city}' has the maximum number of entries/orders, with {count} records."
            return "No text column available to determine city/group orders."

        # 3. Category frequency
        if "category" in q and ("frequent" in q or "most" in q or "common" in q):
            if cat_col:
                top_cat = df[cat_col].value_counts().idxmax()
                pct = (df[cat_col].value_counts().max() / len(df)) * 100
                return f"'{top_cat}' is the most frequent category group, accounting for approximately {pct:.1f}% of all transactions."
            return "No categorical column found."

        # 4. Highest sales region
        if "region" in q and ("highest" in q or "top" in q or "most" in q):
            if region_col and sales_col:
                top_region = df.groupby(region_col)[sales_col].sum().idxmax()
                total = df.groupby(region_col)[sales_col].sum().max()
                return f"The '{top_region}' region lead in {sales_col}, totaling ${total:,.2f}."
            return "Region or Sales equivalent data missing."

        # 5. Averages and Totals
        if "average" in q and "discount" in q:
            return f"The average discount given is {df['Discount'].mean() * 100:.1f}%." if 'Discount' in df.columns else "Discount column missing."

        if "average" in q and "sales" in q:
            return f"The average value per line is ${df[sales_col].mean():,.2f}." if sales_col else "No numeric column found."

        if "total" in q and "profit" in q:
            return f"The total summary across all records is ${df[profit_col].sum():,.2f}." if profit_col else "No secondary numeric column found."

        if "minimum" in q and "sales" in q:
            return f"The minimum value recorded is ${df[sales_col].min():,.2f}." if sales_col else "No numeric column found."

        if "total" in q and "record" in q:
            return f"The dataset contains a total of {len(df)} records."

        return ("I could not confidently match this question to a known pattern. "
                "Try asking about top sub-category/product, most frequent category, "
                "city with maximum orders, top region, or average sales/discount.")
