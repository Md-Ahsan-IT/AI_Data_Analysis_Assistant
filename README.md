# AI-Powered Data Analysis Assistant
### Track A – Explorer (Beginner to Intermediate)

Reads a CSV dataset, answers natural language questions, generates
charts, and uses **Google Gemini (AI Studio)** to explain the
findings in plain language.

**Dataset:** Real Kaggle **"Superstore" sales dataset** (100 rows,
21 columns — Order ID, Category, Sub-Category, Sales, Profit,
Quantity, Discount, City, Region, Order Date, etc.)

---

## ⚠️ Does this need internet / an API key? — IMPORTANT

**No, it doesn't have to.** The project runs 100% end-to-end even
with **no API key and no internet**, because it automatically falls
back to a built-in rule-based explanation if the AI call isn't
available. This was tested and confirmed working with zero setup.

The API key is only needed if you want the **live AI-generated
explanation** in Step 5 (a nicer touch, and satisfies the "AI
Integration" grading criterion more fully). It is **not** a
web app and does **not** need to be "deployed to a live server" —
this is a local Python desktop script, per the task document's own
project structure (`main.py`, run from the command line).

---

## STEP-BY-STEP: Starting From Zero on Your Desktop

### 1. Create a folder
On your Desktop, create a new folder, e.g. `AI_Data_Analysis_Assistant`.
Put ALL the files from this project (main.py, analysis.py,
visualization.py, dataset.csv, requirements.txt, README.md) directly
inside that folder — not in a sub-folder.

### 2. Install Python (if you don't have it)
- Download from https://www.python.org/downloads/ (choose "Add
  Python to PATH" during install on Windows).
- Check it worked by opening Command Prompt / Terminal and typing:
  ```
  python --version
  ```

### 3. Open a terminal inside the project folder
- Windows: open the folder in File Explorer, click the address bar,
  type `cmd`, press Enter.
- Mac: right-click the folder → "New Terminal at Folder" (or `cd`
  into it manually).

### 4. Install the required libraries
```
pip install -r requirements.txt
```

### 5. (Optional) Get a free Gemini API key from Google AI Studio
1. Go to **https://aistudio.google.com/app/apikey**
2. Sign in with a Google account.
3. Click **"Create API key"** and copy the key it gives you.

### 6. Put the API key in the project — EXACT location
Open **`main.py`** in any text editor (Notepad, VS Code, etc.).
Find this block near the top (around **line 34**):

```python
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")  # <-- line 34
```

You have two options:

**Option A (quick, for demos):** replace that line with your key
directly:
```python
GEMINI_API_KEY = "YOUR_KEY_HERE"
```

**Option B (recommended, safer):** don't touch main.py. Instead,
create a new file named exactly `.env` in the same folder, with
this one line inside it:
```
GEMINI_API_KEY=YOUR_KEY_HERE
```
The code automatically reads it from there.

If you skip this step entirely, the project still runs — it just
uses the built-in rule-based explanation instead of a live AI call.

### 7. Run the program
```
python main.py
```

You'll see the dataset summary, statistics, answers to 3 judge
questions, two generated charts (saved in the `charts/` folder), and
a final AI explanation — all printed in the terminal.

---

## Project Structure

```
AI_Data_Analysis_Assistant/
│
├── main.py                # Entry point - run this file
├── analysis.py             # CSV loading, statistics, question answering
├── visualization.py        # Chart generation
├── dataset.csv              # Real Kaggle Superstore dataset (100 rows)
├── requirements.txt
├── README.md
└── charts/                 # Generated charts are saved here
```

## Dataset Source

This is a genuine excerpt of the well-known **Kaggle "Superstore"
sales dataset** (originally ~9,994 rows; a 100-row real slice is
included here so the project stays lightweight and quick to run/grade).
Original dataset: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

Columns include: `Order ID`, `Order Date`, `Category`,
`Sub-Category`, `City`, `Region`, `Sales`, `Quantity`, `Discount`,
`Profit`.

If your judges specifically want the full ~9,994-row version, download
it directly from the Kaggle link above and replace `dataset.csv`
with it — the code will work unchanged since the column names match.

## How It Works

1. **Load Dataset** – Reads `dataset.csv`, shows rows, columns,
   column names, missing values, data types.
2. **Analyze the Dataset** – Computes total sales, averages, max/min,
   total profit, average discount, category/region/city breakdowns.
3. **Answer Natural Language Questions** – Rule-based keyword
   matching answers questions like:
   - Which sub-category/product generated the highest sales?
   - Which city has the maximum orders?
   - Which category appears most frequently?
   - Which region has the highest sales?
4. **Generate Charts** – A bar chart (sales by category) and a pie
   chart (orders by region), saved as PNGs in `charts/`.
5. **AI Explanation** – Calls Google Gemini for a natural-language
   summary; falls back automatically to a rule-based explanation if
   no key/internet is available.

## Notes for Judges

- Runs end-to-end with one command: `python main.py`
- No manual code modification required to get it working (API key
  is optional, not required).
- This is a local script, not a hosted web app — matches the task
  document's own "Project Structure" and "User Flow" sections
  exactly (main.py run from the command line).
