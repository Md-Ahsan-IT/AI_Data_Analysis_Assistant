"""
main.py
-------
AI-Powered Data Analysis Assistant
Track A - Explorer (Beginner to Intermediate)

Dataset: Kaggle "Superstore" sales dataset (dataset.csv)
"""

import os
import sys
import json
import urllib.request
import urllib.error

from analysis import DataAnalyzer
from visualization import generate_category_sales_chart, generate_region_orders_chart, generate_city_orders_chart

# Optional: load a .env file if python-dotenv is installed and a .env exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DATASET_PATH = "dataset.csv"

# ============================================================
#  >>> PUT YOUR GROQ API KEY HERE (gsk_...) <<<
# ============================================================
GROQ_API_KEY = "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"  # <-- Apni naye Groq wali key yahan quotes me paste karein

# Three fixed judge questions
JUDGE_QUESTIONS = [
    "Which product/sub-category generated the highest sales?",
    "Which city has the maximum orders?",
    "Which category appears most frequently?",
]


def call_gemini_api(prompt: str) -> str:
    HF_TOKEN = "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"  # Apni hf_... wali key yahan daalein
    
    # Hugging Face Server Endpoint (Meta Llama 3 model)
    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    
    payload = {
        "inputs": f"<|user|>\n{prompt}\n<|assistant|>",
        "parameters": {"max_new_tokens": 150, "temperature": 0.7}
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            # Hugging Face string text return karta hai array mein
            full_text = data[0]['generated_text']
            return full_text.split("<|assistant|>")[-1].strip()
    except Exception as e:
        print(f"[Info] AI API call skipped/failed ({e}). Using rule-based explanation instead.")
        return None

def rule_based_explanation(stats: dict) -> str:
    """Fallback explanation generator (no internet / no API key required)."""
    top_category = max(stats["category_distribution"], key=stats["category_distribution"].get)
    top_count = stats["category_distribution"][top_category]
    pct = (top_count / stats["total_records"]) * 100

    top_subcat = next(iter(stats["subcategory_sales_totals"]))
    top_subcat_total = stats["subcategory_sales_totals"][top_subcat]

    return (
        f"The dataset shows that '{top_category}' is the leading category, "
        f"making up about {pct:.1f}% of all {stats['total_records']} order lines. "
        f"The best-performing sub-category overall is '{top_subcat}', generating a total "
        f"of ${top_subcat_total:,.2f} in sales. Average sales per order line stand at "
        f"${stats['average_sales']:,.2f}, with a total profit of ${stats['total_profit']:,.2f} "
        f"across the dataset."
    )


def generate_ai_explanation(stats: dict) -> str:
    """Tries the Groq API first, falls back to rule-based logic."""
    prompt = (
        "You are a data analyst assistant. In 2-3 simple sentences, explain "
        "the key insight from this sales dataset for a non-technical audience.\n\n"
        f"Statistics: {json.dumps(stats, default=str)}"
    )

    ai_response = call_gemini_api(prompt)
    if ai_response:
        return ai_response
    return rule_based_explanation(stats)


def main():
    print("=" * 60)
    print("   AI-POWERED DATA ANALYSIS ASSISTANT (Track A - Explorer)")
    print("=" * 60)

    if not os.path.exists(DATASET_PATH):
        print(f"Error: '{DATASET_PATH}' not found in the project folder.")
        sys.exit(1)

    # ---- Step 1: Load Dataset ----
    analyzer = DataAnalyzer(DATASET_PATH)
    analyzer.load_data()
    analyzer.print_summary()

    # ---- Step 2: Analyze the Dataset ----
    stats = analyzer.compute_statistics()
    print("===== KEY STATISTICS =====")
    print(f"Total Records     : {stats['total_records']}")
    print(f"Average Sales     : ${stats['average_sales']:,.2f}")
    print(f"Maximum Sales     : ${stats['max_sales']:,.2f}")
    print(f"Minimum Sales     : ${stats['min_sales']:,.2f}")
    print(f"Total Profit      : ${stats['total_profit']:,.2f}")
    print(f"Average Discount  : {stats['average_discount']*100:.1f}%")
    print("Category Distribution:")
    for cat, count in stats["category_distribution"].items():
        print(f"  - {cat}: {count} orders")
    print("===========================\n")

    # ---- Step 3: Answer Natural Language Questions ----
    print("===== JUDGE QUESTIONS & ANSWERS =====")
    for question in JUDGE_QUESTIONS:
        answer = analyzer.answer_question(question)
        print(f"Q: {question}")
        print(f"A: {answer}\n")
    print("======================================\n")

    # ---- Step 4: Generate Chart(s) ----
    print("Generating charts...")
    chart1 = generate_category_sales_chart(analyzer.df)
    chart2 = generate_region_orders_chart(analyzer.df)
    chart3 = generate_city_orders_chart(analyzer.df)
    print(f"Chart saved: {chart1}")
    print(f"Chart saved: {chart2}")
    print(f"Chart saved: {chart3}\n")

    # ---- Step 5: AI Explanation ----
    print("Generating AI explanation of the results...")
    explanation = generate_ai_explanation(stats)
    print("\n===== AI EXPLANATION =====")
    print(explanation)
    print("===========================\n")

    print("Done! Check the 'charts' folder for the generated visualizations.")


if __name__ == "__main__":
    main()