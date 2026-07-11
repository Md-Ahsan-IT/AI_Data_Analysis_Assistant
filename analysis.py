"""
analysis.py
-----------
Handles CSV loading, dataset summary, statistical analysis,
and rule-based question answering for the AI Data Analysis Assistant.

Dataset used: Kaggle "Superstore" sales dataset.
Key columns used: Category, Sub-Category, Sales, Profit, Quantity,
City, Region, Order Date.
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
    # Step 2 - Analyze the Dataset
    # ------------------------------------------------------------------
    def compute_statistics(self) -> dict:
        """Calculates general statistics used across the assistant."""
        if self.df is None:
            self.load_data()

        df = self.df
        stats = {
            "total_records": len(df),
            "average_sales": round(df["Sales"].mean(), 2),
            "max_sales": round(df["Sales"].max(), 2),
            "min_sales": round(df["Sales"].min(), 2),
            "total_profit": round(df["Profit"].sum(), 2),
            "average_discount": round(df["Discount"].mean(), 3),
            "category_distribution": df["Category"].value_counts().to_dict(),
            "region_order_counts": df["Region"].value_counts().to_dict(),
            "city_order_counts": df["City"].value_counts().to_dict(),
            "subcategory_sales_totals": df.groupby("Sub-Category")["Sales"].sum()
            .sort_values(ascending=False).to_dict(),
        }
        return stats

    # ------------------------------------------------------------------
    # Step 3 - Answer Natural Language Questions (rule-based)
    # ------------------------------------------------------------------
    def answer_question(self, question: str) -> str:
        """
        Simple rule-based natural language question answering.
        Matches keywords in the question to the correct analysis.
        """
        if self.df is None:
            self.load_data()

        q = question.lower()
        df = self.df

        # Which product / sub-category generated the highest sales?
        if ("product" in q or "sub-category" in q or "subcategory" in q) and \
           ("highest" in q or "top" in q or "most sales" in q):
            top = df.groupby("Sub-Category")["Sales"].sum().idxmax()
            total = df.groupby("Sub-Category")["Sales"].sum().max()
            return f"'{top}' generated the highest sales with a total of ${total:,.2f}."

        # Which city has the maximum orders?
        if "city" in q and ("maximum" in q or "most" in q or "highest" in q):
            top_city = df["City"].value_counts().idxmax()
            count = df["City"].value_counts().max()
            return f"'{top_city}' has the maximum number of orders, with {count} orders."

        # Which category appears most frequently?
        if "category" in q and ("frequent" in q or "most" in q or "common" in q):
            top_cat = df["Category"].value_counts().idxmax()
            pct = (df["Category"].value_counts().max() / len(df)) * 100
            return (f"'{top_cat}' is the most frequent category, accounting for "
                    f"approximately {pct:.1f}% of all transactions.")

        # Which region has the highest sales?
        if "region" in q and ("highest" in q or "top" in q or "most" in q):
            top_region = df.groupby("Region")["Sales"].sum().idxmax()
            total = df.groupby("Region")["Sales"].sum().max()
            return f"The '{top_region}' region has the highest sales, totaling ${total:,.2f}."

        # Average discount / sales / profit
        if "average" in q and "discount" in q:
            return f"The average discount given is {df['Discount'].mean() * 100:.1f}%."

        if "average" in q and "sales" in q:
            return f"The average sales value per order line is ${df['Sales'].mean():,.2f}."

        if "total" in q and "profit" in q:
            return f"The total profit across all records is ${df['Profit'].sum():,.2f}."

        if "minimum" in q and "sales" in q:
            return f"The minimum sales value recorded is ${df['Sales'].min():,.2f}."

        if "total" in q and "record" in q:
            return f"The dataset contains a total of {len(df)} records."

        return ("I could not confidently match this question to a known pattern. "
                "Try asking about top sub-category/product, most frequent category, "
                "city with maximum orders, top region, or average sales/discount.")
