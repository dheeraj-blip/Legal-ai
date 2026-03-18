import os
import json
import pdfplumber
from tqdm import tqdm
from groq import Groq
from dotenv import load_dotenv
import time

# -----------------------------
# 🔹 LOAD ENV
# -----------------------------
load_dotenv()

# -----------------------------
# 🔹 API KEYS
# -----------------------------
API_KEYS = [
    os.getenv("GROQ_API_KEY_1"),
    os.getenv("GROQ_API_KEY_2"),
    os.getenv("GROQ_API_KEY_11"),
]

API_KEYS = [k for k in API_KEYS if k]

current_key_index = 0

def get_client():
    return Groq(api_key=API_KEYS[current_key_index])

client = get_client()

# -----------------------------
# 🔹 CONFIG
# -----------------------------
ROOT_FOLDER = r"C:\Users\sirid\.cache\kagglehub\datasets\adarshsingh0903\legal-dataset-sc-judgments-india-19502024\versions\1\supreme_court_judgments"
OUTPUT_FILE = "output/summaries.json"

START_YEAR = "1951"
START_INDEX = 72   # 0-based → 73rd file

os.makedirs("output", exist_ok=True)

# -----------------------------
# 🔹 SWITCH API KEY
# -----------------------------
def switch_api_key():
    global current_key_index, client

    current_key_index += 1

    if current_key_index >= len(API_KEYS):
        print("⏳ All keys exhausted. Waiting...")
        time.sleep(60 * 60)
        current_key_index = 0

    print(f"🔁 Switching to API key #{current_key_index + 1}")
    client = get_client()

# -----------------------------
# 🔹 EXTRACT TEXT
# -----------------------------
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"❌ Error reading {pdf_path}: {e}")
    return text

# -----------------------------
# 🔹 CLEAN TEXT
# -----------------------------
def clean_text(text, max_chars=4000):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text[:max_chars]

# -----------------------------
# 🔹 YEAR EXTRACTION
# -----------------------------
def extract_year_from_path(path):
    for part in path.split(os.sep):
        if part.isdigit() and 1951 <= int(part) <= 2025:
            return int(part)
    return None

# -----------------------------
# 🔹 SUMMARIZE
# -----------------------------
def summarize_text(text):
    global client

    if len(text.strip()) < 200:
        return None

    while True:
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a Supreme Court legal expert. "
                            "Summarize the judgment in ONE concise paragraph including facts, issue, reasoning, and final ruling."
                        ),
                    },
                    {"role": "user", "content": text},
                ],
                temperature=0.2,
                max_tokens=180,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"⚠️ API Error: {e}")
            switch_api_key()

# -----------------------------
# 🔹 LOAD EXISTING JSON
# -----------------------------
def load_existing_data(file):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# -----------------------------
# 🔹 MAIN PROCESS
# -----------------------------
def process_dataset(root_folder, output_file):
    results = load_existing_data(output_file)

    started = False
    processed_count = 0

    for root, dirs, files in os.walk(root_folder):
        year = extract_year_from_path(root)

        if not year:
            continue

        if str(year) < START_YEAR:
            continue

        pdf_files = sorted([f for f in files if f.lower().endswith(".pdf")])

        if not pdf_files:
            continue

        print(f"\n📂 Processing Year: {year} ({len(pdf_files)} files)")

        # Start logic
        start_idx = 0
        if not started and str(year) == START_YEAR:
            start_idx = START_INDEX
            started = True

        for i in tqdm(range(start_idx, len(pdf_files)), desc=f"{year}"):

            file = pdf_files[i]
            file_path = os.path.join(root, file)

            text = extract_text_from_pdf(file_path)
            if not text.strip():
                continue

            cleaned_text = clean_text(text)
            summary = summarize_text(cleaned_text)

            if not summary:
                continue

            record = {
                "case_id": file,
                "year": year,
                "summary": summary
            }

            results.append(record)
            processed_count += 1

            # 💾 Save every 10
            if processed_count % 10 == 0:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"💾 Saved {processed_count} new records")

    # Final save
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ DONE! Added {processed_count} new records")

# -----------------------------
# 🔹 RUN
# -----------------------------
if __name__ == "__main__":
    process_dataset(ROOT_FOLDER, OUTPUT_FILE)