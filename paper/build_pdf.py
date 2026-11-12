"""Typeset a paper markdown into PDF (headless Chrome).   python paper/build_pdf.py [draft.md] [DesignGrad]
Defaults: paper/draft.md -> paper/DesignGrad.pdf. The L5 version: python paper/build_pdf.py draft_L5.md DesignGrad_L5
Figures: SVG where available (vector in the PDF), PNG otherwise."""
import re, subprocess
from pathlib import Path

from markdown_it import MarkdownIt

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@page { size: A4; margin: 18mm 17mm 18mm 17mm; }
:root { --ink:#1d2433; --ink2:#5b6170; --rule:#e3e4e8; --accent:#2a78d6; }
html { font-size: 10pt; }
body { font-family: Charter, 'Iowan Old Style', Georgia, serif; color: var(--ink); line-height: 1.42; margin: 0;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; hyphens: auto; }
h1, h2, h3, .sub, .byline, table, figcaption, .abstract-label { font-family: 'Avenir Next', 'Helvetica Neue', Helvetica, sans-serif; }
h1 { font-size: 21pt; line-height: 1.15; margin: 0 0 4pt; font-weight: 700; letter-spacing: -0.2pt; }
.sub { font-size: 11.5pt; color: var(--ink2); margin: 0 0 6pt; font-style: normal; }
.byline { font-size: 8.5pt; color: var(--ink2); margin-bottom: 12pt; padding-bottom: 10pt; border-bottom: 1.5pt solid var(--ink); }
h2 { font-size: 12.5pt; margin: 15pt 0 5pt; font-weight: 700; break-after: avoid; }
h3 { font-size: 10.5pt; margin: 11pt 0 4pt; font-weight: 600; color: #2b3242; break-after: avoid; }
p { margin: 0 0 6pt; text-align: justify; }
ul, ol { margin: 0 0 6pt; padding-left: 15pt; } li { margin: 0 0 2.5pt; }
.abstract { background: #f5f7fa; border-left: 3pt solid var(--accent); padding: 8pt 11pt; margin: 0 0 6pt; font-size: 9.5pt; }
.abstract p { margin: 0; }
table { border-collapse: collapse; width: 100%; font-size: 8.4pt; margin: 4pt 0 10pt; break-inside: avoid; }
th { text-align: left; font-weight: 600; border-bottom: 1.2pt solid var(--ink); padding: 3pt 5pt; }
td { padding: 2.6pt 5pt; border-bottom: 0.5pt solid var(--rule); }
tr:last-child td { border-bottom: 1.2pt solid var(--ink); }
td:not(:first-child), th:not(:first-child) { white-space: nowrap; }
figure { margin: 8pt 0 12pt; break-inside: avoid; text-align: center; }
figure img { max-width: 100%; height: auto; }
figure img.w90 { width: 92%; } figure img.w80 { width: 82%; } figure img.w66 { width: 68%; } figure img.w100 { width: 100%; }
figcaption { font-size: 8.4pt; color: var(--ink2); text-align: left; margin-top: 4pt; line-height: 1.35; }
figcaption b { color: var(--ink); }
.tcap { font-family: 'Avenir Next', sans-serif; font-size: 8.6pt; margin: 8pt 0 2pt; break-after: avoid; }
p:has(+ pre) { break-after: avoid; }
pre { break-inside: avoid; background:#f5f7fa; border-radius:4pt; padding:6pt 9pt; margin:2pt 0 8pt; font-size:8pt; line-height:1.45; }
pre code { background:none; padding:0; }
code { font-family: 'SF Mono', Menlo, monospace; font-size: 8.2pt; background: #f1f2f4; padding: 0 2pt; border-radius: 2pt; }
.refs p, .refs li { font-size: 8pt; line-height: 1.3; margin: 0 0 1.5pt; text-align: left; }
.refs.two { columns: 2; column-gap: 8mm; }
strong { font-weight: 700; }
a { color: var(--accent); text-decoration: none; }
"""

WIDTH = {"fig1_loop": "w100", "fig2_loop_health": "w80", "fig3_results": "w100", "fig4_designs": "w90", "fig5_rounds": "w100",
         "v3_fig1_loop": "w100", "v3_fig2_measure": "w100", "v3_fig3_results": "w100", "v3_fig4_designs": "w100", "v3_fig5_chain": "w100",
         "v3_fig6_twoloops": "w100", "v3_fig7_mass": "w80",
         "v4_fig_loop": "w100", "v4_fig_results": "w100", "v4_fig_gallery": "w100", "v4_ex_bracket": "w100", "v4_ex_motor": "w100",
         "v6_fig_results": "w90", "v6_fig_gallery": "w100", "v6_fig_control": "w100", "v6_fig_limits": "w100", "v6_fig_rounds": "w100", "v6_fig_parts": "w90",
         "v6_fig_prompts": "w90", "v6_ex_motor": "w100", "v6_ex_bracket": "w100", "v6_ex_motor2": "w100"}


def _size(path):
    """width/height attributes, so the browser knows each figure's height before it paginates (else figures jump to the next page)."""
    try:
        if path.suffix == ".svg":
            head = path.read_text()[:2000]
            vb = re.search(r'viewBox="([\d.\s-]+)"', head)
            if vb:
                w, h = vb.group(1).split()[2:4]
            else:
                w, h = re.search(r'width="([\d.]+)', head).group(1), re.search(r'height="([\d.]+)', head).group(1)
            return f' width="{float(w):.0f}" height="{float(h):.0f}"'
        from PIL import Image
        w, h = Image.open(path).size
        return f' width="{w}" height="{h}"'
    except Exception:
        return ""


def build(src_md="draft.md", out_name="DesignGrad"):
    md = (HERE / src_md).read_text()
    # figures: an image line followed by a "> **Fig. N.** caption" blockquote -> <figure>
    def fig(m):
        name = Path(m.group(1)).stem
        src = f"figs/{name}.svg" if (HERE / "figs" / f"{name}.svg").exists() and name != "fig1_loop" else f"figs/{name}.png"
        if name == "fig1_loop":
            src = "figs/fig1_loop.svg"
        cap = MarkdownIt().renderInline(m.group(2).strip())
        return f'\n<figure><img class="{WIDTH.get(name, "w90")}" src="{src}"{_size(HERE / src)}><figcaption>{cap}</figcaption></figure>\n'
    md = re.sub(r"!\[[^\]]*\]\(([^)]+)\)\s*\n\s*\n> (\*\*Fig\. \d+\.\*\*[^\n]*)", fig, md)
    # title block
    lines = md.split("\n")
    title = lines[0].lstrip("# ").strip()
    if lines[2].startswith("*") and not lines[2].startswith("**"):      # optional subtitle line
        sub = lines[2].strip("* "); byline = lines[4]; body = "\n".join(lines[5:])
    else:
        sub = ""; byline = lines[2]; body = "\n".join(lines[3:])
    mdit = MarkdownIt("commonmark", {"html": True, "typographer": True}).enable("table")
    html = mdit.render(body)
    html = re.sub(r"<h2>Abstract</h2>\s*<p>(.*?)</p>", r'<div class="abstract"><p><b>Abstract.</b> \1</p></div>', html, flags=re.S)
    html = re.sub(r"<p><strong>(Table \d+\..*?)</p>", r'<p class="tcap"><strong>\1</p>', html)
    html = html.replace("<h2>References</h2>", '<h2>References</h2><div class="refs' + (" two" if src_md.startswith("draft_v4") else "") + '">') + "</div>"
    html = re.sub(r'(<div class="refs[^"]*">)\s*<p>(.*?)</p>', lambda m: m.group(1) + "".join(f"<p>{x}</p>" for x in m.group(2).split("\n")), html, flags=re.S)
    doc = (f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>"
           f"<h1>{title}</h1>{f"<p class='sub'>{sub}</p>" if sub else ""}<div class='byline'>{MarkdownIt().renderInline(byline)}</div>{html}</body></html>")
    out_html = HERE / f"{out_name}.html"; out_html.write_text(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HERE / (out_name + '.pdf')}",
                    out_html.as_uri()], check=True, capture_output=True)
    print("wrote", HERE / f"{out_name}.pdf")


if __name__ == "__main__":
    import sys
    build(*sys.argv[1:3])
