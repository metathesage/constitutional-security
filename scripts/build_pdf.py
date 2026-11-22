#!/usr/bin/env python3
"""
Build PDF from markdown paper using pandoc with academic styling.
Requires: pandoc, pandoc-citeproc, LaTeX (xelatex), mermaid-filter (optional)
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PAPER_MD = ROOT / ".." / "ai-security-technical-paper.md"
OUTPUT_PDF = ROOT / ".." / "papers" / "constitutional-security.pdf"

def build_pdf():
    """Generate PDF from markdown using pandoc with Eisvogel template."""
    
    # Ensure output directory exists
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "pandoc",
        str(PAPER_MD),
        "-o", str(OUTPUT_PDF),
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=3",
        "--number-sections",
        "--highlight-style=tango",
        "--metadata=title:Constitutional Security: A Formal Framework for Provably Safe AI Deployment",
        "--metadata=author:Michael A. Scott (metathesage)",
        "--metadata=affiliation:PNTHR AI Research",
        "--metadata=date:November 2026",
        "--metadata=keywords:AI safety, formal verification, constitutional AI, abstract interpretation, runtime enforcement, language model security",
        "--variable=geometry:margin=1in",
        "--variable=fontsize:11pt",
        "--variable=mainfont:DejaVu Serif",
        "--variable=monofont:DejaVu Sans Mono",
        "--variable=colorlinks:true",
        "--variable=linkcolor:blue",
        "--variable=urlcolor:blue",
        "--variable=citecolor:blue",
    ]
    
    # Try with Eisvogel template if available
    template_path = Path.home() / ".local" / "share" / "pandoc" / "templates" / "eisvogel.latex"
    if template_path.exists():
        cmd.extend(["--template", str(template_path)])
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ PDF generated: {OUTPUT_PDF}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PDF generation failed: {e.stderr}")
        return False

def build_html():
    """Generate standalone HTML as fallback."""
    OUTPUT_HTML = ROOT / ".." / "papers" / "constitutional-security.html"
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "pandoc",
        str(PAPER_MD),
        "-o", str(OUTPUT_HTML),
        "--standalone",
        "--toc",
        "--toc-depth=3",
        "--number-sections",
        "--highlight-style=tango",
        "--metadata=title:Constitutional Security: A Formal Framework for Provably Safe AI Deployment",
        "--metadata=author:Michael A. Scott (metathesage)",
        "--metadata=affiliation:PNTHR AI Research",
        "--metadata=date:November 2026",
        "--css=https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css",
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ HTML generated: {OUTPUT_HTML}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ HTML generation failed: {e.stderr}")
        return False

if __name__ == "__main__":
    print("Building paper artifacts...")
    
    # Try PDF first, fallback to HTML
    if not build_pdf():
        print("Falling back to HTML...")
        build_html()
    
    print("Done!")