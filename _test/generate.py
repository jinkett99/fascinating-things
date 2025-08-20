# make_company_pdfs.py
import os
import json
from dataclasses import dataclass
from typing import Dict, List, Optional

# --------- Minimal "Simple Chat Engine" ----------------
class SimpleChatEngine:
    """
    Uses OpenAI if OPENAI_API_KEY is set (no other setup needed).
    Otherwise falls back to a deterministic stub for offline use.
    """
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self._client = None
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                # OpenAI Python SDK v1.x
                from openai import OpenAI
                self._client = OpenAI()
            except Exception:
                # If SDK not installed or import fails, leave as None -> fallback mode
                self._client = None

    def generate_profile(self, company_name: str) -> Dict[str, str]:
        prompt = f"""
        You are a concise company-profile generator. Return ONLY valid JSON with keys:
        - company_name
        - brief_description
        - industry
        - products          (comma-separated list)
        - sensitive_projects (array of objects: {{ "project_name": str, "description": str }})
        - partners          (comma-separated list)

        Constraints:
        - Keep it realistic but fictional.
        - Avoid actual PII. Keep "sensitive_projects" general and non-operational (no secrets).
        Company: {company_name}
        """
        if self._client:
            # OpenAI path
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
            )
            text = resp.choices[0].message.content.strip()
            # Some models wrap JSON in code fences; strip if present
            if text.startswith("```"):
                text = text.strip("`")
                # Remove possible "json" tag on first line
                parts = text.split("\n", 1)
                if len(parts) == 2 and parts[0].lower().strip() == "json":
                    text = parts[1]
            try:
                data = json.loads(text)
                return _coerce_profile(company_name, data)
            except Exception:
                # If JSON is malformed, fall back
                pass

        # Fallback deterministic generator (no API needed)
        return {
            "company_name": company_name,
            "brief_description": f"{company_name} is a tech-forward firm building privacy-first data tools for regulated industries.",
            "industry": "Information Technology",
            "products": "DataVault, InsightLens, RegShield",
            "sensitive_projects": [
                {"project_name": "Project Aegis", "description": "Prototype risk analytics using anonymized datasets for stress-testing."},
                {"project_name": "Project Nimbus", "description": "Internal R&D on efficient retrieval for multilingual document search."},
            ],
            "partners": "CloudNine Systems, Orion Analytics, BluePine Consulting",
        }

def _coerce_profile(company_name: str, data: Dict) -> Dict[str, str]:
    # Ensure required keys and sensible shapes
    out = {
        "company_name": data.get("company_name", company_name),
        "brief_description": data.get("brief_description", ""),
        "industry": data.get("industry", ""),
        "products": data.get("products", ""),
        "sensitive_projects": data.get("sensitive_projects", []),
        "partners": data.get("partners", ""),
    }
    # Normalize arrays to strings where needed
    if isinstance(out["products"], list):
        out["products"] = ", ".join([str(x) for x in out["products"]])
    if isinstance(out["partners"], list):
        out["partners"] = ", ".join([str(x) for x in out["partners"]])
    # Ensure sensitive_projects is list of dicts
    sp = out["sensitive_projects"]
    if not isinstance(sp, list):
        sp = []
    out["sensitive_projects"] = [
        {
            "project_name": str(item.get("project_name", "Untitled")),
            "description": str(item.get("description", "")),
        }
        for item in sp
        if isinstance(item, dict)
    ]
    return out

# --------- PDF Utilities (ReportLab) -------------------
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.ttfonts import TTFont

@dataclass
class PDFStyle:
    font_name: str = "Helvetica"
    font_size_title: int = 18
    font_size_text: int = 11
    line_height: float = 14.0
    margin_left: float = 50
    margin_right: float = 50
    margin_top: float = 60
    margin_bottom: float = 60

def try_register_unicode_font() -> Optional[str]:
    """
    Try to register a Unicode TTF if available.
    Edit the candidates list if you have a different font path.
    """
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/DejaVuSans.ttf",
        os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf"),
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("DejaVuSans", path))
                return "DejaVuSans"
            except Exception:
                pass
    return None

def sanitize_for_helvetica(text: str) -> str:
    """
    If a Unicode font isn't available, ReportLab's base fonts may choke on e.g. bullets.
    This strips unsupported characters to avoid 'latin-1' errors.
    """
    try:
        text.encode("latin-1")
        return text
    except Exception:
        return text.encode("latin-1", "ignore").decode("latin-1")

def draw_paragraph(c: canvas.Canvas, text: str, x: float, y: float, width: float, font: str, size: int, line_height: float):
    lines = simpleSplit(text, font, size, width)
    for line in lines:
        c.drawString(x, y, line)
        y -= line_height
    return y

def write_company_pdf(outdir: str, profile: Dict[str, str], style: PDFStyle):
    os.makedirs(outdir, exist_ok=True)

    # Choose font: prefer Unicode TTF, otherwise sanitize for base fonts
    unicode_font = try_register_unicode_font()
    base_font = unicode_font if unicode_font else style.font_name

    filename = os.path.join(outdir, f"{profile['company_name'].replace(' ', '_')}.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Title
    c.setFont(base_font, style.font_size_title)
    title = profile["company_name"]
    if not unicode_font:
        title = sanitize_for_helvetica(title)
    c.drawString(style.margin_left, height - style.margin_top, title)

    y = height - style.margin_top - 30
    text_font_size = style.font_size_text
    c.setFont(base_font, text_font_size)
    text_width = width - style.margin_left - style.margin_right

    # Sections
    def section(label: str, content: str) -> float:
        nonlocal y
        if not unicode_font:
            content = sanitize_for_helvetica(content)
            label = sanitize_for_helvetica(label)
        c.setFont(base_font, text_font_size + 1)
        y = draw_paragraph(c, f"{label}", style.margin_left, y, text_width, base_font, text_font_size + 1, style.line_height)
        c.setFont(base_font, text_font_size)
        y = draw_paragraph(c, content, style.margin_left, y, text_width, base_font, text_font_size, style.line_height)
        y -= 8
        return y

    y = section("Brief description:", profile["brief_description"])
    y = section("Industry:", profile["industry"])
    y = section("Products:", profile["products"])

    # Sensitive projects
    c.setFont(base_font, text_font_size + 1)
    hdr = "Sensitive projects (names & general descriptions):"
    if not unicode_font:
        hdr = sanitize_for_helvetica(hdr)
    y = draw_paragraph(c, hdr, style.margin_left, y, text_width, base_font, text_font_size + 1, style.line_height)
    c.setFont(base_font, text_font_size)
    for i, item in enumerate(profile["sensitive_projects"], start=1):
        proj_name = item.get("project_name", "Untitled")
        desc = item.get("description", "")
        line = f"{i}. {proj_name} — {desc}"
        if not unicode_font:
            line = sanitize_for_helvetica(line)
        y = draw_paragraph(c, line, style.margin_left, y, text_width, base_font, text_font_size, style.line_height)

    y -= 6
    y = section("Partners:", profile["partners"])

    c.showPage()
    c.save()
    print(f"✓ Wrote: {filename}")

# --------- Main ---------------------------------------
def main():
    # 1) Edit this list as needed (10 companies as requested)
    company_names = [
        "Asteria Labs",
        "Nimbus Dynamics",
        "Orion Grid",
        "Cedar & Co.",
        "BluePine Analytics",
        "Solstice Robotics",
        "Marina Quantum",
        "HelixSense",
        "Tidewave Systems",
        "Vertex Harbor"
    ]

    # 2) Create engine (OpenAI if OPENAI_API_KEY is set; else fallback)
    engine = SimpleChatEngine(model=os.getenv("COMPANY_MODEL", "gpt-4o-mini"))

    # 3) Generate and write PDFs
    outdir = "./docs"
    style = PDFStyle()
    for name in company_names:
        profile = engine.generate_profile(name)
        write_company_pdf(outdir, profile, style)

if __name__ == "__main__":
    main()
