import fitz  # PyMuPDF
import os
import json
import re
import sys
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

ROOT = r""  # Set this to the root directory containing year folders with PDFs
OUTPUT_FILE = r""
PROGRESS_FILE = r""


# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(pdf_path, max_pages=15):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            text += page.get_text() + "\n"
        doc.close()
        return text.strip()
    except:
        return ""


# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\d+\s*\n\s*SUPREME COURT REPORTS.*?\n', '\n', text, flags=re.IGNORECASE)
    return text.strip()


# ---------------- CASE NAME ----------------
def extract_case_name_from_filename(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r'_1$', '', name)
    name = re.sub(r'_on_\d+_\w+_\d{4}', '', name)
    return name.replace('_', ' ').strip()


# ---------------- FAST KEY SENTENCES ----------------
KEY_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r'[^.]*\b(?:held that|holds that)\b[^.]*\.',
        r'[^.]*\b(?:ruled that|rules that)\b[^.]*\.',
        r'[^.]*\b(?:the court held|this court held|the court holds)\b[^.]*\.',
        r'[^.]*\b(?:we hold|we are of the opinion|we are of opinion)\b[^.]*\.',
        r'[^.]*\b(?:appeal is? (?:allowed|dismissed))\b[^.]*\.',
        r'[^.]*\b(?:conviction (?:is |was )?(?:upheld|set aside|quashed))\b[^.]*\.',
        r'[^.]*\b(?:the question (?:is|was) whether)\b[^.]*\.',
        r'[^.]*\b(?:the issue (?:is|was) whether)\b[^.]*\.',
        r'[^.]*\b(?:in our opinion|in my opinion)\b[^.]*\.',
        r'[^.]*\b(?:for (?:these|the above|the foregoing) reasons)\b[^.]*\.',
        r'[^.]*\b(?:we (?:accordingly|therefore) (?:allow|dismiss|set aside))\b[^.]*\.',
        r'[^.]*\b(?:it is (?:hereby |)ordered)\b[^.]*\.',
    ]
]


def find_key_sentences(text):
    results = []
    for pattern in KEY_PATTERNS:
        results.extend(pattern.findall(text))
    return [s.strip() for s in results if 20 < len(s) < 500]


# ---------------- FIRST PARAGRAPH ----------------
def get_first_substantive_paragraph(text, min_len=100):
    paragraphs = text.split('\n\n')
    for para in paragraphs:
        para = para.strip()
        if len(para) < min_len:
            continue
        if para.upper() == para and len(para) < 200:
            continue
        return para
    return paragraphs[0] if paragraphs else ""


# ---------------- SUMMARY ----------------
def summarize_case(text, filename, year):
    if not text or len(text) < 100:
        return "Summary not available due to insufficient text."

    cleaned = clean_text(text)

    key_sentences = find_key_sentences(cleaned)
    first_para = get_first_substantive_paragraph(cleaned)

    parts = []

    if first_para:
        if len(first_para) > 600:
            sentences = re.split(r'(?<=[.!?])\s+', first_para)
            intro = ""
            for s in sentences:
                if len(intro) + len(s) > 500:
                    break
                intro += s + " "
            first_para = intro.strip()
        parts.append(first_para)

    seen = set()
    for s in key_sentences:
        norm = s.lower().strip()
        if norm not in seen and len(s) > 30:
            seen.add(norm)
            parts.append(s)
        if len(parts) >= 4:
            break

    summary = " ".join(parts)

    if len(summary) > 1000:
        summary = summary[:1000]

    return summary


# ---------------- FILE HANDLING ----------------
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return set(json.load(f))
    return set()


def save_progress(processed):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(list(processed), f)


def load_existing_summaries():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_summaries(summaries):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)


# ---------------- PARALLEL WORKER ----------------
def process_single_file(args):
    year, pdf_name = args
    pdf_path = os.path.join(ROOT, str(year), pdf_name)

    try:
        text = extract_text_from_pdf(pdf_path)
        summary = summarize_case(text, pdf_name, year)

        return {
            "case_id": pdf_name,
            "year": year,
            "summary": summary,
            "file_key": f"{year}/{pdf_name}"
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------- MAIN FAST PROCESS ----------------
def process_all_years_fast(start_year=1968, end_year=2025):
    processed = load_progress()
    summaries = load_existing_summaries()

    print(f"🚀 Processing {start_year} → {end_year}")
    print(f"Existing summaries: {len(summaries)}")

    tasks = []

    for year in range(start_year, end_year + 1):
        year_path = os.path.join(ROOT, str(year))
        if not os.path.isdir(year_path):
            continue

        pdfs = sorted([f for f in os.listdir(year_path) if f.lower().endswith('.pdf')])

        for pdf in pdfs:
            key = f"{year}/{pdf}"
            if key not in processed:
                tasks.append((year, pdf))

    print(f"Total files to process: {len(tasks)}")

    workers = max(2, multiprocessing.cpu_count() - 1)
    print(f"Using {workers} CPU cores 🔥")

    new_count = 0
    error_count = 0

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_single_file, t) for t in tasks]

        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()

            if "error" in result:
                error_count += 1
                continue

            summaries.append({
                "case_id": result["case_id"],
                "year": result["year"],
                "summary": result["summary"]
            })

            processed.add(result["file_key"])
            new_count += 1

            # Save every 100 files
            if i % 100 == 0:
                save_summaries(summaries)
                save_progress(processed)
                print(f"Saved at {i} files...")

    save_summaries(summaries)
    save_progress(processed)

    print(f"\n✅ Done! New: {new_count}, Errors: {error_count}")
    print(f"Total summaries: {len(summaries)}")


# ---------------- RUN ----------------
if __name__ == "__main__":
    process_all_years_fast(1950, 2025)