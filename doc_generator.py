"""
Document Generator for LEX Legal AI.

Uses a two-phase approach:
  1. LaTeX templates with named {{PLACEHOLDER}} markers
  2. A CrewAI agent that outputs ONLY a JSON dict of placeholder values
  3. Python does mechanical str.replace() — LLM never touches LaTeX

This completely prevents template corruption.
"""

import os
import re
import json
import uuid
import subprocess
import tempfile
import shutil

from crewai import Agent, Crew, Process, LLM

# ── Template mapping ─────────────────────────────────────────────────────────
CASE_TEMPLATE_MAP = {
    "CRPC":                   "0.tex",
    "IPC":                    "1.tex",
    "CPC":                    "2.tex",
    "EVIDENCE":               "3.tex",
    "PROPERTY":               "4.tex",
    "CORPORATE_PRACTICE":     "5.tex",
    "DIVORCE":                "6.tex",
    "MARRIAGE":               "7.tex",
    "CONSTITUTION":           "8.tex",
    "BANKING":                "9.tex",
    "MVA":                    "10.tex",
    "MINIMUM_WAGES":          "11.tex",
    "COMPANY_LAW":            "12.tex",
    "BANKRUPTCY":             "13.tex",
    "COPYRIGHT":              "14.tex",
    "PATENT":                 "14.tex",
    "TRADEMARK":              "14.tex",
    "DESIGN":                 "14.tex",
    "HUMAN_RIGHTS":           "15.tex",
    "ENVIRON":                "2.tex",
    "ADMIN":                  "2.tex",
    "INFORMATION_TECHNOLOGY": "2.tex",
    "TAX":                    "2.tex",
}

# ── Paths ────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_TEMPLATE_DIR = os.path.join(_HERE, "latex-templates")
_OUTPUT_DIR = os.path.join(_HERE, "generated_docs")
os.makedirs(_OUTPUT_DIR, exist_ok=True)

# ── LLM setup ────────────────────────────────────────────────────────────────
_KEY = os.environ.get("GROQ_KEY_RETRY") or os.environ.get("GROQ_KEY_LAWS")


def _get_llm():
    if not _KEY:
        raise ValueError("No GROQ API key found for document generation")
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=_KEY,
        temperature=0.1,
    )


def _read_template(template_filename: str) -> str:
    path = os.path.join(_TEMPLATE_DIR, template_filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ── LaTeX special character escaping ─────────────────────────────────────────

def _escape_latex(text: str) -> str:
    """Escape characters that are special in LaTeX so they render safely."""
    # Order matters: & must be escaped before we add any & ourselves
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


# ── Placeholder extraction ───────────────────────────────────────────────────

def _extract_placeholders(template: str) -> list[str]:
    """Find all {{PLACEHOLDER_NAME}} markers in a template."""
    return list(dict.fromkeys(re.findall(r"XXFIELDXX([A-Z0-9_]+)XXFIELDXX", template)))


# ── JSON-based template filling ──────────────────────────────────────────────

def _fill_template_with_agent(
    latex_template: str,
    user_query: str,
    ai_response: str,
) -> str:
    """
    Use a CrewAI agent to fill named placeholders in the LaTeX template.

    The agent receives ONLY the list of placeholder names and their context
    (from nearby text in the template). It returns a JSON object mapping
    placeholder names -> values. Python then does str.replace().

    The LLM NEVER sees or edits raw LaTeX commands.
    """
    from crewai import Task

    placeholders = _extract_placeholders(latex_template)

    if not placeholders:
        # No placeholders to fill — return template as-is
        return latex_template

    # Build a human-readable field list with context hints
    field_descriptions = []
    for ph in placeholders:
        # Convert PLACEHOLDER_NAME to readable: "Placeholder Name"
        readable = ph.replace("_", " ").title()
        field_descriptions.append(f'  "{ph}": "<{readable}>"')

    fields_json_hint = "{\n" + ",\n".join(field_descriptions) + "\n}"

    agent = Agent(
        role="Legal Document Data Extractor",
        goal=(
            "You extract structured data from legal case details and return "
            "it as a JSON object. You NEVER output LaTeX, HTML, or any markup. "
            "You output ONLY valid JSON — no explanation, no markdown fences, "
            "no commentary before or after the JSON."
        ),
        backstory=(
            "You are an expert Indian legal professional who reads case details "
            "and extracts the relevant information into structured fields. "
            "For any details not available in the case, you create realistic "
            "placeholder text in square brackets like [Petitioner Name]."
        ),
        tools=[],
        verbose=False,
        max_iter=1,
        llm=_get_llm(),
    )

    task = Task(
        description=(
            f"Given the following legal case details, fill in the JSON fields below.\n\n"
            f"USER'S CASE DETAILS:\n{user_query}\n\n"
            f"LEGAL ANALYSIS:\n{ai_response}\n\n"
            f"FIELDS TO FILL (return a JSON object with these exact keys):\n"
            f"{fields_json_hint}\n\n"
            f"RULES:\n"
            f"1. Return ONLY a valid JSON object. No explanation. No markdown.\n"
            f"2. Every key from the list above MUST appear in your response.\n"
            f"3. Values should be plain text — NO LaTeX commands, NO backslashes.\n"
            f"4. Use information from the case details to fill in values.\n"
            f"5. For unknown details, use descriptive placeholders in square brackets "
            f"like [Petitioner Name], [Date of Incident], [Court Name].\n"
            f"6. Keep values concise — typically a few words or a short sentence.\n"
            f"7. For date fields, use format like '15th April 2026'.\n"
            f"8. For amount fields, use format like '5,00,000'.\n"
            f"9. Your output must start with {{ and end with }}.\n"
        ),
        expected_output="A valid JSON object mapping field names to values.",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    raw_output = str(result).strip()

    # Parse the JSON from the LLM output
    values = _parse_json_output(raw_output)

    # Apply values to template
    filled = latex_template
    for ph in placeholders:
        value = values.get(ph, f"[{ph.replace('_', ' ').title()}]")
        safe_value = _escape_latex(str(value))
        filled = filled.replace("XXFIELDXX" + ph + "XXFIELDXX", safe_value)

    return filled


def _parse_json_output(raw: str) -> dict:
    """
    Robustly parse JSON from LLM output, handling common issues like
    markdown fences, extra text, etc.
    """
    # Strip markdown code fences
    raw = re.sub(r'^```(?:json)?\s*\n?', '', raw)
    raw = re.sub(r'\n?```\s*$', '', raw)
    raw = raw.strip()

    # Try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try to find the JSON object in the text
    match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # Try to find content between first { and last }
    first_brace = raw.find('{')
    last_brace = raw.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(raw[first_brace:last_brace + 1])
        except json.JSONDecodeError:
            pass

    # If all parsing fails, return empty dict — placeholders will get defaults
    print(f"  ⚠️  Could not parse JSON from LLM output. Using defaults.")
    return {}


# ── pdflatex ─────────────────────────────────────────────────────────────────

def _find_pdflatex() -> str:
    """Find pdflatex executable, checking common MiKTeX install paths."""
    # Try PATH first
    try:
        result = subprocess.run(
            ["pdflatex", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return "pdflatex"
    except FileNotFoundError:
        pass

    # Check common MiKTeX locations on Windows
    common_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"),
        r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe",
        r"C:\MiKTeX\miktex\bin\x64\pdflatex.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"),
    ]
    for p in common_paths:
        if os.path.isfile(p):
            return p

    raise FileNotFoundError(
        "pdflatex not found. Please install MiKTeX from https://miktex.org/ "
        "and restart your terminal."
    )


def _compile_latex(latex_content: str, output_dir: str) -> str:
    """Write LaTeX, compile with pdflatex, return path to PDF."""
    doc_id = uuid.uuid4().hex[:8]
    tex_name = f"legal_doc_{doc_id}.tex"
    pdf_name = f"legal_doc_{doc_id}.pdf"

    work_dir = tempfile.mkdtemp(prefix="lex_latex_")
    pdflatex = _find_pdflatex()

    try:
        tex_path = os.path.join(work_dir, tex_name)
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_content)

        # Compile twice (for cross-references)
        env = os.environ.copy()
        # Refresh PATH so newly-installed MiKTeX is found
        env["PATH"] = (
            os.environ.get("PATH", "")
            + ";" + os.path.dirname(pdflatex)
        )

        for pass_num in range(2):
            proc = subprocess.run(
                [
                    pdflatex,
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    tex_name,
                ],
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=60,
                env=env,
            )

        compiled_pdf = os.path.join(work_dir, pdf_name)
        if not os.path.exists(compiled_pdf):
            # Extract error from log
            log_path = os.path.join(work_dir, tex_name.replace(".tex", ".log"))
            error_msg = "pdflatex compilation failed."
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8", errors="ignore") as lf:
                    for line in lf:
                        if line.startswith("!"):
                            error_msg += f" {line.strip()}"
                            break
            raise RuntimeError(error_msg)

        final_pdf = os.path.join(output_dir, pdf_name)
        shutil.copy2(compiled_pdf, final_pdf)
        return final_pdf

    finally:
        try:
            shutil.rmtree(work_dir, ignore_errors=True)
        except Exception:
            pass


def generate_document(
    case_category: str,
    user_query: str,
    ai_response: str,
) -> str:
    """
    Generate a legal document PDF for the given case.

    Returns path to the generated PDF file.
    """
    category_upper = case_category.strip().upper()
    template_file = CASE_TEMPLATE_MAP.get(category_upper, "2.tex")
    print(f"  📄 Using template: {template_file} for category: {category_upper}")

    latex_template = _read_template(template_file)

    print(f"  ✍️  Extracting case data via AI agent...")
    filled_latex = _fill_template_with_agent(
        latex_template, user_query, ai_response
    )

    print(f"  🔨 Compiling PDF with pdflatex...")
    pdf_path = _compile_latex(filled_latex, _OUTPUT_DIR)

    print(f"  ✅ Document generated: {pdf_path}")
    return pdf_path
