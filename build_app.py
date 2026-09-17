# -*- coding: utf-8 -*-
"""
Script de génération de index.html pour Apps Mobiles 2
Assemble :
- Structure HTML5 sémantique et responsive
- CSS moderne avec tokens, Dark Mode / Light Mode, composants Android Studio / Material 3
- Simulateur Android réaliste interactif pour chaque leçon
- Colorateur syntaxique Kotlin natif sans dépendance externe
- Moteur de recherche instantanée avec autocomplétion
- Gestionnaire de persistance localStorage pour la progression et les favoris
- 12 leçons ultra-complètes de A à Z
"""

import json
from lessons_part1 import LESSONS_PART1
from lessons_part2 import LESSONS_PART2
from lessons_part3 import LESSONS_PART3

def build_index_html():
    all_lessons = {}
    all_lessons.update(LESSONS_PART1)
    all_lessons.update(LESSONS_PART2)
    all_lessons.update(LESSONS_PART3)

    lessons_json = json.dumps(all_lessons, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="fr" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Apps Mobiles 2 — Kotlin + Jetpack Compose + MVVM</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* ======================================================================
   TOKENS & PALETTES (Material 3 + Jetpack Compose / Kotlin)
   ====================================================================== */
:root {{
  --paper: #F8F9FC;
  --panel: #FFFFFF;
  --panel-card: #FFFFFF;
  --ink: #11141D;
  --ink-soft: #5C6272;
  --line: #E2E5EE;
  --line-strong: #CBD1E0;

  /* Accents */
  --kotlin: #7F52FF;
  --kotlin-hover: #6B3EE6;
  --kotlin-dim: #F0EBFF;
  --kotlin-text: #6032D6;

  --android: #1E8F72;
  --android-dim: #E3F5EF;
  --amber: #D98A1B;
  --amber-dim: #FBF0DD;
  --red: #C4453A;
  --red-dim: #FDECEB;
  --blue: #2563EB;
  --blue-dim: #EFF6FF;

  /* Code Syntax (Theme Clair) */
  --code-bg: #1A1C23;
  --code-ink: #ECEEF5;
  --code-border: #2B2E3C;
  --syn-kw: #C792EA;
  --syn-ann: #FFCB6B;
  --syn-str: #C3E88D;
  --syn-type: #82AAFF;
  --syn-fn: #89DDFF;
  --syn-num: #F78C6C;
  --syn-com: #717CB4;

  /* Dimensions & Ombres */
  --sidebar-w: 268px;
  --radius: 8px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.04);
  --shadow-lg: 0 12px 28px rgba(0,0,0,0.12), 0 4px 10px rgba(0,0,0,0.05);
}}

[data-theme="dark"] {{
  --paper: #0E1015;
  --panel: #16181F;
  --panel-card: #1D202A;
  --ink: #EDF0F7;
  --ink-soft: #9BA3B5;
  --line: #262A36;
  --line-strong: #383D4E;

  --kotlin: #9D7BFF;
  --kotlin-hover: #B295FF;
  --kotlin-dim: #251D3E;
  --kotlin-text: #D0BFFF;

  --android: #3DDC84;
  --android-dim: #133221;
  --amber: #F6AD55;
  --amber-dim: #382A14;
  --red: #FF7B72;
  --red-dim: #3A1817;
  --blue: #60A5FA;
  --blue-dim: #172A46;

  /* Code Syntax (Theme Sombre - Studio Dark) */
  --code-bg: #111217;
  --code-ink: #ECEEF5;
  --code-border: #232733;

  --shadow-sm: 0 1px 3px rgba(0,0,0,0.25);
  --shadow-md: 0 4px 14px rgba(0,0,0,0.35);
  --shadow-lg: 0 12px 30px rgba(0,0,0,0.5);
}}

* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{
  background: var(--paper);
  color: var(--ink);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  font-size: 15px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  transition: background-color .2s ease, color .2s ease;
}}

h1, h2, h3, h4 {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
  margin: 0 0 .4em 0;
  letter-spacing: -0.02em;
  color: var(--ink);
}}
code, pre, .mono {{
  font-family: 'JetBrains Mono', monospace;
}}
a {{ color: inherit; text-decoration: none; }}
button {{ font-family: inherit; cursor: pointer; border: none; }}
::selection {{ background: var(--kotlin-dim); color: var(--kotlin-text); }}

/* ======================================================================
   LAYOUT STRUCTURE
   ====================================================================== */
.shell {{
  display: flex;
  min-height: 100vh;
}}

/* SIDEBAR */
.sidebar {{
  width: var(--sidebar-w);
  flex-shrink: 0;
  background: var(--panel);
  border-right: 1px solid var(--line);
  padding: 20px 16px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  z-index: 10;
}}

.brand {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 4px 18px 4px;
  border-bottom: 1px solid var(--line);
  margin-bottom: 16px;
}}
.brand-mark {{
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: linear-gradient(135deg, var(--kotlin) 0%, #B241FF 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-family: 'JetBrains Mono';
  font-weight: 800;
  font-size: 16px;
  box-shadow: 0 3px 8px rgba(127, 82, 255, 0.35);
}}
.brand-text {{
  font-family: 'Plus Jakarta Sans';
  font-weight: 800;
  font-size: 15px;
  line-height: 1.2;
}}
.brand-text span {{
  display: block;
  font-family: 'Inter';
  font-weight: 500;
  color: var(--ink-soft);
  font-size: 11.5px;
  margin-top: 2px;
}}

.progress-widget {{
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 10px 12px;
  margin-bottom: 16px;
}}
.progress-widget-top {{
  display: flex;
  justify-content: space-between;
  font-size: 11.5px;
  font-weight: 600;
  color: var(--ink-soft);
  margin-bottom: 6px;
}}
.progress-bar-wrap {{
  height: 6px;
  background: var(--line);
  border-radius: 99px;
  overflow: hidden;
}}
.progress-bar-fill {{
  height: 100%;
  background: linear-gradient(90deg, var(--kotlin) 0%, var(--android) 100%);
  border-radius: 99px;
  transition: width .3s ease;
}}

.navgroup {{ margin-bottom: 18px; }}
.navgroup-label {{
  font-size: 11px;
  color: var(--ink-soft);
  padding: 0 10px 6px 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}
.navitem {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 11px;
  border-radius: var(--radius);
  font-size: 13.5px;
  font-weight: 500;
  color: var(--ink-soft);
  text-decoration: none;
  margin-bottom: 2px;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  transition: all .15s ease;
}}
.navitem:hover {{
  background: var(--paper);
  color: var(--ink);
}}
.navitem.active {{
  background: var(--kotlin-dim);
  color: var(--kotlin-text);
  font-weight: 700;
}}
.navitem svg {{ flex-shrink: 0; opacity: 0.8; }}
.navitem.active svg {{ opacity: 1; }}

.lesson-nav-btn {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 7px 10px;
  border-radius: var(--radius);
  font-size: 12.8px;
  color: var(--ink-soft);
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  transition: all .15s ease;
}}
.lesson-nav-btn:hover {{ background: var(--paper); color: var(--ink); }}
.lesson-nav-btn.active {{ background: var(--kotlin-dim); color: var(--kotlin-text); font-weight: 700; }}
.lesson-nav-btn .dot {{
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  background: var(--line);
  color: var(--ink-soft);
  flex-shrink: 0;
}}
.lesson-nav-btn.done .dot {{ background: var(--android); color: #fff; }}
.lesson-nav-btn .fav-icon {{ font-size: 11px; color: var(--amber); margin-left: auto; }}

/* TOPBAR */
main {{
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}}
.topbar {{
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--line);
  padding: 12px 32px;
  display: flex;
  gap: 16px;
  align-items: center;
}}
[data-theme="dark"] .topbar {{
  background: rgba(22, 24, 31, 0.85);
}}

.search-container {{
  position: relative;
  flex: 1;
  max-width: 520px;
}}
.searchbox {{
  display: flex;
  align-items: center;
  gap: 9px;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 7px 12px;
  transition: border-color .15s ease, box-shadow .15s ease;
}}
.searchbox:focus-within {{
  border-color: var(--kotlin);
  box-shadow: 0 0 0 3px var(--kotlin-dim);
  background: var(--panel);
}}
.searchbox input {{
  border: none;
  outline: none;
  background: none;
  flex: 1;
  font-family: inherit;
  font-size: 13.5px;
  color: var(--ink);
}}
.searchbox svg {{ opacity: 0.6; flex-shrink: 0; color: var(--ink-soft); }}
.search-shortcut {{
  font-size: 10.5px;
  background: var(--panel);
  border: 1px solid var(--line);
  color: var(--ink-soft);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'JetBrains Mono';
}}

/* Instant Search Dropdown */
.search-results-dropdown {{
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  max-height: 420px;
  overflow-y: auto;
  display: none;
  z-index: 100;
  padding: 6px;
}}
.search-results-dropdown.open {{ display: block; }}
.search-res-group {{
  padding: 6px 8px 4px 8px;
  font-size: 11px;
  font-weight: 700;
  color: var(--ink-soft);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}
.search-res-item {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13.5px;
  color: var(--ink);
  transition: background .15s ease;
}}
.search-res-item:hover {{
  background: var(--kotlin-dim);
  color: var(--kotlin-text);
}}
.search-res-item .subtag {{
  font-size: 11px;
  background: var(--paper);
  padding: 2px 7px;
  border-radius: 99px;
  border: 1px solid var(--line);
  color: var(--ink-soft);
}}

/* Actions topbar */
.topbar-actions {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
}}
.theme-btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius);
  background: var(--panel);
  border: 1px solid var(--line);
  color: var(--ink);
  font-size: 15px;
  transition: all .15s ease;
}}
.theme-btn:hover {{
  background: var(--paper);
  border-color: var(--kotlin);
}}
.menu-btn {{
  display: none;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid var(--line);
  background: var(--panel);
  border-radius: var(--radius);
  color: var(--ink);
  font-size: 16px;
}}

/* CONTENT CONTAINER */
.content {{
  padding: 36px 48px 100px 48px;
  max-width: 980px;
  width: 100%;
  margin: 0 auto;
}}

/* ======================================================================
   SHARED UI WIDGETS
   ====================================================================== */
.eyebrow-free-title {{
  margin-bottom: 24px;
}}
.eyebrow-free-title h1 {{
  font-size: 32px;
  line-height: 1.15;
}}
.sub {{
  color: var(--ink-soft);
  font-size: 16px;
  margin-top: 4px;
}}

.grid2 {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}}
@media(max-width:760px){{ .grid2 {{ grid-template-columns: 1fr; }} }}

.card {{
  background: var(--panel-card);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  padding: 20px 24px;
  box-shadow: var(--shadow-sm);
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}}
.card:hover {{
  border-color: var(--line-strong);
}}
.course-card {{
  border-left: 4px solid var(--kotlin);
  display: flex;
  flex-direction: column;
}}
.course-card h4 {{
  font-size: 16px;
  margin-bottom: 4px;
}}
.course-card .meta {{
  font-size: 12.5px;
  color: var(--ink-soft);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.course-card .btn-row {{
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
}}

.badge {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11.5px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 99px;
  line-height: 1.2;
}}
.badge.beg {{ background: var(--android-dim); color: var(--android); }}
.badge.mid {{ background: var(--amber-dim); color: var(--amber); }}
.badge.adv {{ background: var(--red-dim); color: var(--red); }}
.badge.dur {{ background: var(--paper); color: var(--ink-soft); border: 1px solid var(--line); font-weight: 500; }}

.go-btn {{
  border: 1px solid var(--kotlin);
  color: var(--kotlin);
  background: none;
  padding: 6px 14px;
  border-radius: var(--radius);
  font-size: 13px;
  font-weight: 600;
  transition: all .15s ease;
}}
.go-btn:hover {{
  background: var(--kotlin);
  color: #fff;
}}

.chip {{
  font-size: 12.8px;
  padding: 6px 13px;
  border-radius: 99px;
  border: 1px solid var(--line);
  background: var(--panel);
  color: var(--ink);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all .15s ease;
}}
.chip.linkable {{
  border-color: var(--kotlin);
  color: var(--kotlin-text);
  background: var(--kotlin-dim);
  cursor: pointer;
  font-weight: 600;
}}
.chip.linkable:hover {{
  background: var(--kotlin);
  color: #fff;
}}
.pill-row {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}}

/* ======================================================================
   LESSON VIEW SPECIFICS
   ====================================================================== */
.lesson-header {{
  margin-bottom: 24px;
}}
.back-link {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--ink-soft);
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 12px;
  cursor: pointer;
}}
.back-link:hover {{ color: var(--kotlin); }}
.lesson-header h1 {{
  font-size: 32px;
  margin-bottom: 8px;
}}
.lesson-meta-bar {{
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--line);
}}

/* Sticky Sub-nav TOC (Sommaire rapide) */
.lesson-toc {{
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  padding: 10px 0 16px 0;
  position: sticky;
  top: 61px;
  background: var(--paper);
  z-index: 30;
  border-bottom: 1px solid var(--line);
  margin-bottom: 28px;
}}
.toc-pill {{
  font-size: 11.5px;
  padding: 4px 9px;
  border-radius: 99px;
  background: var(--panel);
  border: 1px solid var(--line);
  color: var(--ink-soft);
  font-weight: 600;
  text-decoration: none;
  transition: all .15s ease;
}}
.toc-pill:hover {{
  border-color: var(--kotlin);
  color: var(--kotlin);
  background: var(--kotlin-dim);
}}

.section-block {{
  margin-bottom: 34px;
  scroll-margin-top: 120px;
}}
.section-block h3 {{
  font-size: 17px;
  color: var(--ink);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 9px;
}}
.section-block h3 .num {{
  font-family: 'JetBrains Mono';
  background: var(--kotlin-dim);
  color: var(--kotlin-text);
  width: 26px;
  height: 26px;
  border-radius: 7px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}}
.section-block p {{
  margin: 0 0 12px 0;
  font-size: 15px;
  line-height: 1.65;
}}
.section-block b {{
  color: var(--ink);
}}

/* CODE TABS & CODEBOX */
.code-container {{
  border: 1px solid var(--code-border);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--code-bg);
  box-shadow: var(--shadow-sm);
  margin: 12px 0;
}}
.code-tabs {{
  display: flex;
  background: rgba(0,0,0,0.25);
  border-bottom: 1px solid var(--code-border);
  overflow-x: auto;
}}
.code-tab-btn {{
  padding: 9px 16px;
  font-size: 12.5px;
  font-weight: 600;
  color: #8C93A8;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  white-space: nowrap;
  transition: all .15s ease;
}}
.code-tab-btn:hover {{ color: #E7E9F2; }}
.code-tab-btn.active {{
  color: #FFFFFF;
  border-bottom-color: var(--kotlin);
  background: rgba(127,82,255,0.08);
}}
.code-tab-panel {{
  display: none;
  position: relative;
}}
.code-tab-panel.active {{ display: block; }}

.codebox {{
  padding: 16px 20px;
  overflow-x: auto;
  font-size: 13.5px;
  line-height: 1.65;
  color: var(--code-ink);
  margin: 0;
}}
.codebox pre {{
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
  white-space: pre;
}}

/* SYNTAX HIGHLIGHTING COLORS */
.kw {{ color: var(--syn-kw); font-weight: 600; }}
.ann {{ color: var(--syn-ann); font-weight: 600; }}
.str {{ color: var(--syn-str); }}
.type {{ color: var(--syn-type); }}
.fn {{ color: var(--syn-fn); }}
.num {{ color: var(--syn-num); }}
.com {{ color: var(--syn-com); font-style: italic; }}

.copy-btn {{
  position: absolute;
  top: 10px;
  right: 12px;
  background: rgba(255,255,255,0.12);
  color: #E2E6F2;
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 6px;
  padding: 5px 11px;
  font-size: 11.5px;
  font-family: 'JetBrains Mono';
  font-weight: 500;
  transition: all .15s ease;
  z-index: 5;
}}
.copy-btn:hover {{
  background: rgba(255,255,255,0.22);
  color: #fff;
}}

/* EXPLICATION TABLE */
.explain-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 13.8px;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  margin-top: 10px;
}}
.explain-table th {{
  text-align: left;
  background: var(--paper);
  font-size: 11.5px;
  color: var(--ink-soft);
  font-weight: 700;
  text-transform: uppercase;
  padding: 9px 14px;
  border-bottom: 1px solid var(--line);
}}
.explain-table td {{
  padding: 10px 14px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}}
.explain-table tr:last-child td {{ border-bottom: none; }}
.explain-table td:first-child code {{
  background: var(--kotlin-dim);
  color: var(--kotlin-text);
  padding: 2px 7px;
  border-radius: 4px;
  font-size: 12.5px;
  white-space: nowrap;
}}

/* ERRORS BOXES */
.err-item {{
  border: 1px solid var(--red-dim);
  background: #FFF8F8;
  border-left: 4px solid var(--red);
  border-radius: var(--radius);
  padding: 14px 16px;
  margin-bottom: 12px;
}}
[data-theme="dark"] .err-item {{
  background: #1F1517;
  border-color: #381B1C;
}}
.err-head {{
  font-family: 'JetBrains Mono';
  color: var(--red);
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}}
.err-fix {{
  font-size: 13.5px;
  color: var(--ink);
  line-height: 1.55;
}}

/* EXERCICE & QUIZ */
.exercise-box {{
  border: 1px solid var(--amber-dim);
  background: #FFFDF8;
  border-left: 4px solid var(--amber);
  border-radius: var(--radius);
  padding: 18px 20px;
}}
[data-theme="dark"] .exercise-box {{
  background: #1C1811;
  border-color: #362916;
}}
.exercise-title {{
  font-weight: 700;
  font-size: 15px;
  color: var(--ink);
  margin-bottom: 8px;
}}
.exercise-hint {{
  font-size: 13.5px;
  color: var(--ink-soft);
  margin: 8px 0 14px 0;
}}
.sol-btn {{
  background: var(--panel);
  border: 1px solid var(--amber);
  color: var(--amber);
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 12.5px;
  font-weight: 700;
  transition: all .15s ease;
}}
.sol-btn:hover {{
  background: var(--amber);
  color: #fff;
}}
.sol-content {{
  display: none;
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px dashed var(--line);
}}

.quiz-box {{
  border: 1px solid var(--line);
  background: var(--panel);
  border-radius: var(--radius-lg);
  padding: 22px 24px;
  box-shadow: var(--shadow-sm);
}}
.quiz-q {{
  font-weight: 700;
  font-size: 15.5px;
  margin-bottom: 14px;
  color: var(--ink);
}}
.quiz-opt {{
  display: block;
  width: 100%;
  text-align: left;
  padding: 11px 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--panel);
  color: var(--ink);
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  transition: all .15s ease;
}}
.quiz-opt:hover:not(:disabled) {{
  border-color: var(--kotlin);
  background: var(--paper);
}}
.quiz-opt.correct {{
  background: var(--android-dim) !important;
  border-color: var(--android) !important;
  color: var(--android) !important;
  font-weight: 700;
}}
.quiz-opt.wrong {{
  background: var(--red-dim) !important;
  border-color: var(--red) !important;
  color: var(--red) !important;
  font-weight: 700;
}}
.quiz-fb {{
  margin-top: 12px;
  padding: 12px 14px;
  border-radius: var(--radius);
  font-size: 13.5px;
  line-height: 1.5;
  display: none;
}}
.quiz-fb.correct {{ background: var(--android-dim); color: var(--android); display: block; }}
.quiz-fb.wrong {{ background: var(--red-dim); color: var(--red); display: block; }}

.retain-list {{
  list-style: none;
  margin: 0;
  padding: 0;
}}
.retain-list li {{
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 7px 0;
  font-size: 14.5px;
}}
.retain-list li::before {{
  content: "✓";
  color: var(--android);
  font-weight: 800;
  font-size: 15px;
  flex-shrink: 0;
}}

.lesson-nav-footer {{
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid var(--line);
}}
.lesson-nav-footer button {{
  padding: 10px 18px;
  border-radius: var(--radius);
  border: 1px solid var(--line);
  background: var(--panel);
  color: var(--ink);
  font-size: 13.5px;
  font-weight: 600;
  transition: all .15s ease;
}}
.lesson-nav-footer button:hover:not(:disabled) {{
  border-color: var(--kotlin);
}}
.lesson-nav-footer .finish-btn {{
  background: var(--android);
  color: #fff;
  border-color: var(--android);
}}
.lesson-nav-footer .finish-btn.done {{
  background: var(--android-dim);
  color: var(--android);
}}

/* ======================================================================
   ANDROIDS SMARTPHONE SIMULATOR
   ====================================================================== */
.phone-sim-wrap {{
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 16px 0;
}}
.sim-toggle-row {{
  display: flex;
  gap: 8px;
  margin-bottom: 18px;
}}
.sim-toggle-btn {{
  padding: 6px 14px;
  border-radius: 99px;
  border: 1px solid var(--line);
  background: var(--panel);
  color: var(--ink-soft);
  font-size: 12.5px;
  font-weight: 600;
  transition: all .15s ease;
}}
.sim-toggle-btn.active {{
  background: var(--kotlin);
  border-color: var(--kotlin);
  color: #fff;
}}

/* Phone Mockup Frame */
.smartphone-device {{
  width: 330px;
  min-height: 520px;
  background: #000;
  border-radius: 36px;
  padding: 10px;
  box-shadow: 0 16px 36px rgba(0,0,0,0.22), 0 0 0 4px #262933;
  display: flex;
  flex-direction: column;
  position: relative;
}}
.smartphone-screen {{
  flex: 1;
  background: #FDFDFE;
  color: #1A1C22;
  border-radius: 28px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
  font-family: 'Inter', sans-serif;
}}
[data-theme="dark"] .smartphone-screen {{
  background: #181A20;
  color: #ECEEF5;
}}

/* Status bar */
.phone-statusbar {{
  height: 26px;
  padding: 4px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  font-weight: 700;
  color: inherit;
  opacity: 0.85;
}}
.phone-notch {{
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #000;
}}

/* App Bar inside phone */
.phone-appbar {{
  background: var(--kotlin);
  color: #fff;
  padding: 10px 14px;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}}

/* Phone Content Viewport */
.phone-viewport {{
  flex: 1;
  padding: 14px;
  overflow-y: auto;
  font-size: 13px;
  position: relative;
}}

/* Gesture bar */
.phone-navbar {{
  height: 18px;
  display: flex;
  justify-content: center;
  align-items: center;
}}
.phone-nav-pill {{
  width: 90px;
  height: 4px;
  border-radius: 99px;
  background: rgba(0,0,0,0.35);
}}
[data-theme="dark"] .phone-nav-pill {{
  background: rgba(255,255,255,0.35);
}}

/* Schema View */
.schema-box {{
  width: 100%;
  max-width: 600px;
  background: var(--code-bg);
  color: var(--code-ink);
  padding: 18px 20px;
  border-radius: var(--radius);
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  white-space: pre;
  overflow-x: auto;
  display: none;
}}

/* RESPONSIVE */
@media(max-width: 860px) {{
  .sidebar {{
    position: fixed;
    left: -290px;
    top: 0;
    z-index: 100;
    transition: left .2s ease;
    box-shadow: none;
  }}
  .sidebar.open {{
    left: 0;
    box-shadow: 0 0 0 9999px rgba(0,0,0,.5);
  }}
  .menu-btn {{ display: flex; }}
  .content {{ padding: 20px 16px 90px 16px; }}
  .topbar {{ padding: 10px 16px; }}
  .smartphone-device {{ width: 290px; min-height: 480px; }}
}}
</style>
</head>
<body>

<div class="shell">
  <!-- SIDEBAR -->
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <div class="brand-mark">K</div>
      <div class="brand-text">Apps Mobiles 2<span>Kotlin · Jetpack Compose · MVVM</span></div>
    </div>

    <!-- Progession globale -->
    <div class="progress-widget">
      <div class="progress-widget-top">
        <span>Progression</span>
        <span id="sidePercent">0%</span>
      </div>
      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" id="sideBarFill" style="width:0%;"></div>
      </div>
    </div>

    <div class="navgroup">
      <div class="navitem-list" id="mainNav">
        <button class="navitem active" data-view="dashboard">🏠 Accueil & Synthèse</button>
        <button class="navitem" data-view="parcours">🧭 Parcours (10 Niveaux)</button>
        <button class="navitem" data-view="comment">💡 Comment faire ?</button>
        <button class="navitem" data-view="composants">🧩 Bibliothèque Composants</button>
        <button class="navitem" data-view="cheatsheets">⚡ Cheat Sheets & Mémos</button>
        <button class="navitem" data-view="glossaire">📖 Glossaire Android</button>
        <button class="navitem" data-view="quiz">📝 Quiz Général</button>
        <button class="navitem" data-view="favoris">⭐ Mes Favoris</button>
      </div>
    </div>

    <div class="navgroup" style="flex:1;">
      <div class="navgroup-label">Modules de Cours</div>
      <div id="lessonNavList"></div>
    </div>
  </aside>

  <!-- MAIN VIEWPORT -->
  <main>
    <header class="topbar">
      <button class="menu-btn" id="menuBtn" aria-label="Menu">☰</button>
      
      <div class="search-container">
        <div class="searchbox">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          <input id="searchInput" placeholder="Rechercher une notion, ex: « créer une liste », « API »…" autocomplete="off">
          <span class="search-shortcut">/</span>
        </div>
        <div class="search-results-dropdown" id="searchDropdown"></div>
      </div>

      <div class="topbar-actions">
        <button class="theme-btn" id="themeBtn" title="Changer de thème">🌙</button>
      </div>
    </header>

    <div class="content" id="content"></div>
  </main>
</div>

<script>
/* ======================================================================
   BASE DE DONNÉES ENRICHE DE TOUTES LES LEÇONS (DE A À Z)
   ====================================================================== */
const LESSONS = {lessons_json};

const LEVELS = [
  {{n:1, title:"Fondations Android & Kotlin", items:["Android Studio Giraffe/Hedgehog","Structure app & Gradle kts","Variables val/var & typage","Fonctions & Lambdas Kotlin","Classes & Data Class"], lessons:[]}},
  {{n:2, title:"Interface Déclarative (UI)", items:["Fonctions @Composable","Column, Row, Box & Alignments","Modifier & chaînage strict","Card Material 3","Boutons, Textes & Typographie"], lessons:["layout","card"]}},
  {{n:3, title:"Interface Avancée & Structures", items:["Scaffold Material 3 & Insets","TopAppBar, FAB & SnackbarHost","Listes défilantes LazyColumn","LazyRow & Grilles virtuelles","Champs texte & Formulaires"], lessons:["scaffold","lazycolumn"]}},
  {{n:4, title:"Gestion de l'État & Recomposition", items:["mutableStateOf & remember","rememberSaveable & Rotations","Pattern State Hoisting","ViewModel AndroidX","StateFlow & Coroutines Scope"], lessons:["state","viewmodel"]}},
  {{n:5, title:"Architecture Applicative", items:["Architecture MVVM Google","Pattern Repository (Source unique)","Sealed Interface UiState","Flux Unidirectionnel (UDF)"], lessons:["mvvm"]}},
  {{n:6, title:"Persistance des Données", items:["Jetpack DataStore Preferences","Base SQLite locale avec Room","Entity, DAO & Queries SQL","CRUD Complet (Create/Read/Update/Delete)"], lessons:["datastore","room","crud"]}},
  {{n:7, title:"Connexion Réseau & API", items:["Client HTTP Retrofit 2","Moshi Converter (JSON -> Kotlin)","Gestion des erreurs & Hors-ligne","Pattern DTO (Data Transfer Object)"], lessons:["api"]}},
  {{n:8, title:"Navigation Multi-Écrans", items:["Navigation Compose (NavHost)","NavController & Pile BackStack","Passage d'arguments typés","Single-Activity Architecture"], lessons:["navigation"]}},
  {{n:9, title:"Fonctionnalités Avancées", items:["Side-effects & LaunchedEffect","Gestion des Permissions Android","Notifications système","Thématisation dynamique Material You"], lessons:[]}},
  {{n:10, title:"Projet Fil Rouge Intégral", items:["Mini E-Commerce complet : Navigation, Room, Retrofit, ViewModel & Compose UI"], lessons:[]}}
];

const COMMENT_FAIRE = [
  {{q:"Comment aligner des éléments verticalement ou horizontalement ?", id:"layout"}},
  {{q:"Comment créer une carte Material 3 avec coins arrondis ?", id:"card"}},
  {{q:"Comment structurer un écran avec une TopBar et un FAB ?", id:"scaffold"}},
  {{q:"Comment afficher une liste défilante performante ?", id:"lazycolumn"}},
  {{q:"Comment gérer un compteur ou une saisie avec remember ?", id:"state"}},
  {{q:"Comment conserver les données après une rotation d'écran ?", id:"viewmodel"}},
  {{q:"Comment organiser son code selon l'architecture MVVM ?", id:"mvvm"}},
  {{q:"Comment sauvegarder le mode sombre ou des préférences ?", id:"datastore"}},
  {{q:"Comment créer une base de données locale SQLite ?", id:"room"}},
  {{q:"Comment faire un CRUD complet (Ajouter, Lire, Modifier, Supprimer) ?", id:"crud"}},
  {{q:"Comment appeler une API REST et parser du JSON ?", id:"api"}},
  {{q:"Comment naviguer entre 2 écrans et passer un ID ?", id:"navigation"}}
];

const CHEATSHEETS = {{
  "Modifiers Jetpack Compose": [
    ["Modifier.fillMaxWidth()", "Occupe 100% de la largeur disponible"],
    ["Modifier.fillMaxSize()", "Occupe toute la surface écran"],
    ["Modifier.padding(16.dp)", "Marge intérieure ou extérieure selon position"],
    ["Modifier.size(48.dp)", "Fixe largeur ET hauteur"],
    ["Modifier.background(Color.White)", "Applique une couleur de fond"],
    ["Modifier.clip(RoundedCornerShape(12.dp))", "Découpe le composant selon une forme"],
    ["Modifier.clickable {{ }}", "Rend n'importe quel composant cliquable avec onde ripple"],
    ["Modifier.weight(1f)", "Distribue l'espace restant proportionnellement dans Row/Column"],
    ["Modifier.align(Alignment.Center)", "Aligne un enfant spécifique dans un Box ou Row/Column"]
  ],
  "Kotlin Memento": [
    ["val", "Variable immuable en lecture seule (à privilégier)"],
    ["var", "Variable réassignable"],
    ["data class", "Classe modèle auto-générant copy(), equals(), toString()"],
    ["val x: String?", "Type nullable pouvant valoir null"],
    ["x?.length", "Appel sécurisé (Safe Call) : null si x est null"],
    ["x ?: 'Défaut'", "Opérateur Elvis : valeur par défaut si x est null"],
    ["suspend fun", "Fonction asynchrone non-bloquante pour Coroutine"],
    ["sealed interface", "Hiérarchie fermée d'états pour un when exhaustif"]
  ],
  "Compose & State": [
    ["@Composable", "Marque une fonction génératrice d'UI"],
    ["by remember {{ mutableStateOf(x) }}", "État local observable conservé en recomposition"],
    ["rememberSaveable {{ ... }}", "État conservé même lors d'une rotation d'écran"],
    ["collectAsStateWithLifecycle()", "Collecte sécurisée d'un StateFlow dans Compose"],
    ["LaunchedEffect(key) {{ }}", "Exécute une Coroutine liée au cycle de vie d'un Composable"]
  ],
  "Room & SQLite": [
    ["@Entity(tableName = 't')", "Définit une table SQL"],
    ["@PrimaryKey(autoGenerate = true)", "Clé primaire auto-incrémentée"],
    ["@Dao", "Interface regroupant les requêtes"],
    ["@Query('SELECT * FROM t')", "Requête SQL retournant un Flow<List<T>>"],
    ["@Insert(onConflict = REPLACE)", "Insertion ou remplacement sans plantage"],
    ["@Delete / @Update", "Suppression ou modification d'une ligne"]
  ]
}};

const GLOSSARY = [
  ["API REST", "Interface web permettant d'échanger des données en HTTP/JSON avec un serveur."],
  ["BackStack", "Pile de navigation gérant l'historique des écrans pour le bouton retour."],
  ["Composable", "Fonction Kotlin annotée @Composable qui émet des éléments d'interface."],
  ["Coroutine", "Mécanisme Kotlin léger pour exécuter des tâches asynchrones sans bloquer l'UI."],
  ["CRUD", "Create, Read, Update, Delete — les 4 actions fondamentales sur des données."],
  ["DAO", "Data Access Object — interface Room contenant les requêtes SQL typées."],
  ["DataStore", "Solution moderne de persistance asynchrone pour les préférences clé-valeur."],
  ["Entity", "Classe Kotlin annotée @Entity représentant une table SQLite dans Room."],
  ["Flow", "Flux asynchrone réactif Kotlin émettant plusieurs valeurs au fil du temps."],
  ["KSP", "Kotlin Symbol Processing — compilateur rapide remplaçant KAPT pour générer le code Room."],
  ["Material 3", "Dernière spécification de design de Google (couleurs dynamiques, coins arrondis)."],
  ["Modifier", "Objet chaîné servant à décorer, dimensionner ou rendre interactif un Composable."],
  ["MVVM", "Architecture Model-View-ViewModel séparant affichage, logique et sources de données."],
  ["Recomposition", "Ré-exécution intelligente par Compose des fonctions dont l'état a changé."],
  ["Repository", "Couche d'abstraction arbitrant entre cache local (Room) et réseau (API)."],
  ["Retrofit", "Bibliothèque HTTP de référence sous Android pour consommer des APIs."],
  ["Scaffold", "Structure standard d'écran Material 3 avec TopBar, FAB et SnackbarHost."],
  ["State", "Donnée observable dont la modification déclenche la mise à jour de l'écran."],
  ["StateFlow", "Flow spécialisé conservant toujours la dernière valeur connue d'un état."],
  ["State Hoisting", "Bonne pratique consistant à remonter l'état pour rendre un composant pur (stateless)."],
  ["ViewModel", "Composant Android survivant aux rotations d'écran et gérant la logique métier."]
];

const COMPONENTS = [
  ["Column", "Disposition", "Empilement vertical d'éléments"],
  ["Row", "Disposition", "Alignement horizontal côte à côte"],
  ["Box", "Disposition", "Superposition de calques"],
  ["Card", "Conteneur", "Carte Material 3 avec coins arrondis et élévation"],
  ["Surface", "Conteneur", "Surface de couleur de fond Material"],
  ["Scaffold", "Structure", "Squelette d'écran avec TopBar, FAB et Snackbar"],
  ["TopAppBar", "Structure", "Barre d'action supérieure"],
  ["LazyColumn", "Listes", "Liste verticale performante recyclée"],
  ["LazyRow", "Listes", "Carrousel horizontal défilant"],
  ["Text", "Affichage", "Affichage de typographie riche"],
  ["Button", "Interaction", "Bouton d'action standard avec ripple"],
  ["IconButton", "Interaction", "Bouton icône circulaire"],
  ["FloatingActionButton", "Interaction", "Bouton flottant proéminent (FAB)"],
  ["OutlinedTextField", "Saisie", "Champ de saisie texte avec bordure"],
  ["Switch", "Saisie", "Interrupteur à bascule (Toggle on/off)"],
  ["Checkbox", "Saisie", "Case à cocher pour sélection"],
  ["CircularProgressIndicator", "Indicateur", "Roue de chargement circulaire animée"],
  ["AlertDialog", "Popup", "Boîte de dialogue modale de confirmation"],
  ["SnackbarHost", "Notification", "Bannière temporaire d'information en bas d'écran"]
];

/* ======================================================================
   GESTIONNAIRE D'ÉTAT & PERSISTANCE (localStorage)
   ====================================================================== */
const APP = {{
  completed: new Set(),
  favorites: new Set(),
  theme: "light",
  currentView: "dashboard",
  currentLesson: null,

  init() {{
    try {{
      const savedDone = localStorage.getItem("app2_completed");
      if (savedDone) this.completed = new Set(JSON.parse(savedDone));

      const savedFavs = localStorage.getItem("app2_favorites");
      if (savedFavs) this.favorites = new Set(JSON.parse(savedFavs));

      const savedTheme = localStorage.getItem("app2_theme");
      if (savedTheme) {{
        this.theme = savedTheme;
        document.documentElement.setAttribute("data-theme", savedTheme);
      }}
    }} catch(e) {{
      console.warn("Stockage local indisponible :", e);
    }}
  }},

  save() {{
    try {{
      localStorage.setItem("app2_completed", JSON.stringify([...this.completed]));
      localStorage.setItem("app2_favorites", JSON.stringify([...this.favorites]));
      localStorage.setItem("app2_theme", this.theme);
    }} catch(e) {{}}
    updateGlobalProgress();
  }}
}};

APP.init();

function lessonOrder() {{ return Object.keys(LESSONS); }}

function updateGlobalProgress() {{
  const total = lessonOrder().length;
  const done = APP.completed.size;
  const pct = total ? Math.round((done / total) * 100) : 0;

  const sidePercent = document.getElementById('sidePercent');
  const sideBarFill = document.getElementById('sideBarFill');
  if (sidePercent) sidePercent.textContent = pct + "%";
  if (sideBarFill) sideBarFill.style.width = pct + "%";
}}

/* ======================================================================
   COLORATEUR SYNTAXIQUE KOTLIN LÉGER & BLUFFANT
   ====================================================================== */
function highlightKotlin(rawCode) {{
  let code = rawCode.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // Commentaires mono-ligne
  code = code.replace(/(\\/\\/.*$)/gm, '<span class="com">$1</span>');

  // Chaînes entre guillemets
  code = code.replace(/(".*?")/g, '<span class="str">$1</span>');

  // Annotations @Composable, @Entity, etc.
  code = code.replace(/(@[A-Za-z0-9_]+)/g, '<span class="ann">$1</span>');

  // Mots-clés Kotlin
  const keywords = "\\\\b(package|import|class|interface|object|fun|val|var|by|remember|rememberSaveable|mutableStateOf|private|public|protected|internal|set|get|override|suspend|return|if|else|when|for|while|is|in|as|null|true|false|data|abstract|sealed|open|companion|init|constructor)\\\\b";
  code = code.replace(new RegExp(keywords, 'g'), '<span class="kw">$1</span>');

  // Types principaux
  const types = "\\\\b(String|Int|Boolean|Double|Float|Long|List|Map|Set|Flow|StateFlow|MutableStateFlow|Modifier|Context|Unit|Any|NavController|NavHostController|PaddingValues|Arrangement|Alignment|Color|Dp|Text|Card|Button|Column|Row|Box|Scaffold|TopAppBar|SnackbarHostState|LazyColumn)\\\\b";
  code = code.replace(new RegExp(types, 'g'), '<span class="type">$1</span>');

  // Chiffres et dimensions
  code = code.replace(/\\\\b(\\\\d+(\\\\.\\\\d+)?(\\\\.[a-z]+)?)\\\\b/g, '<span class="num">$1</span>');

  return code;
}}

/* ======================================================================
   NAVIGATION SIDEBAR
   ====================================================================== */
function buildSidebarLessons() {{
  const el = document.getElementById('lessonNavList');
  if (!el) return;
  el.innerHTML = "";

  lessonOrder().forEach((id, idx) => {{
    const l = LESSONS[id];
    const isDone = APP.completed.has(id);
    const isFav = APP.favorites.has(id);

    const btn = document.createElement('button');
    btn.className = "lesson-nav-btn " + (isDone ? "done" : "") + (APP.currentLesson === id ? " active" : "");
    btn.dataset.lesson = id;
    btn.innerHTML = `
      <span style="display:flex;align-items:center;gap:8px;min-width:0;">
        <span class="dot">${{isDone ? '✓' : (idx + 1)}}</span>
        <span style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${{l.title.split(':')[0].trim()}}</span>
      </span>
      ${{isFav ? '<span class="fav-icon">★</span>' : ''}}
    `;
    btn.onclick = () => openLesson(id);
    el.appendChild(btn);
  }});
  updateGlobalProgress();
}}

document.getElementById('mainNav').addEventListener('click', (e) => {{
  const btn = e.target.closest('.navitem');
  if (!btn) return;
  setActiveNav(btn);
  renderView(btn.dataset.view);
}});

function setActiveNav(activeEl) {{
  document.querySelectorAll('.navitem').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.lesson-nav-btn').forEach(b => b.classList.remove('active'));
  if (activeEl) activeEl.classList.add('active');
}}

// Mobile drawer toggle
document.getElementById('menuBtn').addEventListener('click', () => {{
  document.getElementById('sidebar').classList.toggle('open');
}});

// Dark / Light Theme Toggle
document.getElementById('themeBtn').addEventListener('click', () => {{
  APP.theme = APP.theme === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', APP.theme);
  document.getElementById('themeBtn').textContent = APP.theme === 'light' ? '🌙' : '☀️';
  APP.save();
}});
document.getElementById('themeBtn').textContent = APP.theme === 'light' ? '🌙' : '☀️';

/* ======================================================================
   RECHERCHE INSTANTANÉE AVEC AUTOCOMPLÉTION
   ====================================================================== */
const searchInput = document.getElementById('searchInput');
const searchDropdown = document.getElementById('searchDropdown');

function executeInstantSearch(q) {{
  q = q.trim().toLowerCase();
  if (!q) {{
    searchDropdown.classList.remove('open');
    searchDropdown.innerHTML = "";
    return;
  }}

  let html = "";
  const matchedLessons = [];
  const matchedQA = [];

  // 1. Recherche leçons
  lessonOrder().forEach(id => {{
    const l = LESSONS[id];
    if (l.title.toLowerCase().includes(q) || l.quoi.toLowerCase().includes(q)) {{
      matchedLessons.push({{ id, title: l.title }});
    }}
  }});

  // 2. Recherche questions pratiques
  COMMENT_FAIRE.forEach(item => {{
    if (item.q.toLowerCase().includes(q)) {{
      matchedQA.push(item);
    }}
  }});

  if (matchedLessons.length === 0 && matchedQA.length === 0) {{
    html = `<div style="padding:12px;font-size:13px;color:var(--ink-soft);text-align:center;">Aucun résultat pour « ${{escapeHTML(q)}} ». Essayez « liste », « API », « state », « Room »…</div>`;
  }} else {{
    if (matchedLessons.length > 0) {{
      html += `<div class="search-res-group">Leçons correspondantes</div>`;
      matchedLessons.forEach(m => {{
        html += `<div class="search-res-item" data-open="${{m.id}}">
          <span>📘 ${{escapeHTML(m.title)}}</span>
          <span class="subtag">Cours</span>
        </div>`;
      }});
    }}
    if (matchedQA.length > 0) {{
      html += `<div class="search-res-group">Questions pratiques</div>`;
      matchedQA.forEach(qa => {{
        html += `<div class="search-res-item" data-open="${{qa.id}}">
          <span>💡 ${{escapeHTML(qa.q)}}</span>
          <span class="subtag">Solution</span>
        </div>`;
      }});
    }}
  }}

  searchDropdown.innerHTML = html;
  searchDropdown.classList.add('open');

  searchDropdown.querySelectorAll('[data-open]').forEach(item => {{
    item.onclick = () => {{
      openLesson(item.dataset.open);
      searchDropdown.classList.remove('open');
      searchInput.value = "";
    }};
  }});
}}

searchInput.addEventListener('input', (e) => executeInstantSearch(e.target.value));

document.addEventListener('click', (e) => {{
  if (!e.target.closest('.search-container')) {{
    searchDropdown.classList.remove('open');
  }}
}});

// Raccourci clavier "/"
window.addEventListener('keydown', (e) => {{
  if (e.key === '/' && document.activeElement !== searchInput) {{
    e.preventDefault();
    searchInput.focus();
  }} else if (e.key === 'Escape') {{
    searchDropdown.classList.remove('open');
    searchInput.blur();
  }}
}});

/* ======================================================================
   RENDER : DASHBOARD ACCUEIL
   ====================================================================== */
function renderDashboard() {{
  const total = lessonOrder().length;
  const done = APP.completed.size;
  const pct = total ? Math.round((done / total) * 100) : 0;

  return `
    <div class="eyebrow-free-title">
      <h1>Apps Mobiles 2 — Kotlin & Compose</h1>
      <p class="sub">Plateforme pédagogique complète : Maîtrisez le développement Android moderne avec Jetpack Compose, l'architecture MVVM, Room et Retrofit.</p>
    </div>

    <!-- CARTE DE PROGRESSION -->
    <div class="card" style="margin-bottom:24px;background:linear-gradient(135deg, var(--panel) 0%, var(--paper) 100%);">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div>
          <div style="font-size:12px;font-weight:700;text-transform:uppercase;color:var(--kotlin);letter-spacing:0.05em;">Votre Parcours d'Apprentissage</div>
          <div style="font-size:22px;font-weight:800;margin-top:2px;">${{done}} sur ${{total}} leçons complétées</div>
        </div>
        <div style="font-size:28px;font-weight:800;color:var(--kotlin);font-family:'JetBrains Mono';">${{pct}}%</div>
      </div>
      <div class="progress-bar-wrap" style="height:10px;">
        <div class="progress-bar-fill" style="width:${{pct}}%;"></div>
      </div>
      <div style="display:flex;gap:16px;margin-top:14px;font-size:13px;color:var(--ink-soft);">
        <span>⏱ Temps estimé restant : <b>${{Math.max(0, (total - done) * 15)}} min</b></span>
        <span>⭐ Favoris enregistrés : <b>${{APP.favorites.size}}</b></span>
      </div>
    </div>

    <h3 style="font-size:16px; margin-bottom:12px;">Reprendre l'apprentissage</h3>
    <div class="grid2" id="dashLessonsGrid"></div>

    <hr style="border:none;border-top:1px solid var(--line);margin:32px 0;">

    <h3 style="font-size:16px; margin-bottom:12px;">Besoin d'une solution immédiate ?</h3>
    <div class="pill-row" id="quickActionsPills"></div>
  `;
}}

function afterDashboardRender() {{
  const grid = document.getElementById('dashLessonsGrid');
  if (grid) {{
    lessonOrder().slice(0, 6).forEach(id => {{
      const l = LESSONS[id];
      const isDone = APP.completed.has(id);
      const card = document.createElement('div');
      card.className = "card course-card";
      card.innerHTML = `
        <h4>${{l.title}}</h4>
        <div class="meta">
          ${{badgeHTML(l.level)}}
          <span class="badge dur">⏱ ${{l.duration}}</span>
        </div>
        <p style="font-size:13px;color:var(--ink-soft);margin-bottom:14px;line-height:1.5;">${{l.quoi.replace(/<[^>]*>/g, '').slice(0, 95)}}...</p>
        <div class="btn-row">
          <span style="font-size:12px;font-weight:600;color:${{isDone ? 'var(--android)' : 'var(--ink-soft)'}};">${{isDone ? '✓ Validé' : 'À découvrir'}}</span>
          <button class="go-btn" data-open="${{id}}">${{isDone ? 'Revoir' : 'Commencer →'}}</button>
        </div>
      `;
      grid.appendChild(card);
    }});
    grid.querySelectorAll('[data-open]').forEach(b => b.onclick = () => openLesson(b.dataset.open));
  }}

  const pills = document.getElementById('quickActionsPills');
  if (pills) {{
    COMMENT_FAIRE.forEach(qa => {{
      const b = document.createElement('button');
      b.className = "chip linkable";
      b.textContent = qa.q;
      b.onclick = () => openLesson(qa.id);
      pills.appendChild(b);
    }});
  }}
}}

/* ======================================================================
   RENDER : PARCOURS (10 NIVEAUX)
   ====================================================================== */
function renderParcours() {{
  let html = `<div class="eyebrow-free-title"><h1>Parcours d'Apprentissage</h1><p class="sub">10 niveaux structurés pour passer de zéro à la création d'applications Android complètes.</p></div>`;
  
  LEVELS.forEach(lv => {{
    const lessonsInLevel = lv.lessons;
    const doneCount = lessonsInLevel.filter(id => APP.completed.has(id)).length;
    
    html += `
      <div class="card" style="margin-bottom:14px;border-left:4px solid ${{lessonsInLevel.length ? 'var(--kotlin)' : 'var(--line)'}};">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
          <div>
            <span style="font-family:'JetBrains Mono';font-weight:800;color:var(--kotlin);margin-right:8px;">NIVEAU ${{lv.n}}</span>
            <span style="font-weight:700;font-size:16px;">${{lv.title}}</span>
          </div>
          ${{lessonsInLevel.length ? `<span class="badge ${{doneCount === lessonsInLevel.length ? 'beg' : 'dur'}}">${{doneCount}} / ${{lessonsInLevel.length}} validés</span>` : ''}}
        </div>
        <div class="pill-row" style="margin-bottom:12px;">
          ${{lv.items.map(it => `<span class="chip" style="font-size:12px;">${{it}}</span>`).join('')}}
        </div>
        ${{lessonsInLevel.length ? `
          <div style="display:flex;gap:8px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:10px;">
            ${{lessonsInLevel.map(id => `
              <button class="chip linkable" data-open="${{id}}">
                ${{APP.completed.has(id) ? '✓' : '📘'}} ${{LESSONS[id].title.split(':')[0]}}
              </button>
            `).join('')}}
          </div>
        ` : `<div style="font-size:12.5px;color:var(--ink-soft);font-style:italic;">Contenu théorique couvert dans les travaux pratiques et le projet final.</div>`}}
      </div>
    `;
  }});

  return html;
}}

function afterParcoursRender() {{
  document.querySelectorAll('#content [data-open]').forEach(b => b.onclick = () => openLesson(b.dataset.open));
}}

/* ======================================================================
   RENDER : COMMENT FAIRE ?
   ====================================================================== */
function renderComment() {{
  let html = `<div class="eyebrow-free-title"><h1>Comment faire ?</h1><p class="sub">Accès direct aux fiches pratiques répondant aux problématiques de développement les plus fréquentes.</p></div><div class="grid2">`;
  
  COMMENT_FAIRE.forEach(item => {{
    const l = LESSONS[item.id];
    html += `
      <div class="card" style="display:flex;flex-direction:column;justify-content:space-between;">
        <div>
          <div style="font-weight:700;font-size:15px;margin-bottom:6px;">${{item.q}}</div>
          <div style="font-size:12.5px;color:var(--ink-soft);margin-bottom:12px;">Lié à : <b>${{l.title}}</b></div>
        </div>
        <button class="go-btn" data-open="${{item.id}}" style="align-self:flex-start;">Voir la solution A à Z →</button>
      </div>
    `;
  }});

  html += `</div>`;
  return html;
}}

function afterCommentRender() {{
  document.querySelectorAll('#content [data-open]').forEach(b => b.onclick = () => openLesson(b.dataset.open));
}}

/* ======================================================================
   RENDER : BIBLIOTHÈQUE DE COMPOSANTS
   ====================================================================== */
function renderComposants() {{
  let html = `<div class="eyebrow-free-title"><h1>Bibliothèque de Composants</h1><p class="sub">Les composants Jetpack Compose les plus utilisés sous Android.</p></div><div class="grid2">`;

  COMPONENTS.forEach(([name, cat, desc]) => {{
    const linkedId = Object.keys(LESSONS).find(k => LESSONS[k].title.toLowerCase().includes(name.toLowerCase()) || name.toLowerCase() === k);
    html += `
      <div class="card" ${{linkedId ? `data-open="${{linkedId}}" style="cursor:pointer;"` : ''}}>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
          <code style="font-size:15px;font-weight:700;color:var(--kotlin);">${{name}}</code>
          <span class="badge dur">${{cat}}</span>
        </div>
        <p style="font-size:13.5px;color:var(--ink-soft);margin:0 0 10px 0;">${{desc}}</p>
        ${{linkedId ? `<span style="font-size:12px;color:var(--kotlin);font-weight:600;">Ouvrir le cours complet →</span>` : ''}}
      </div>
    `;
  }});

  html += `</div>`;
  return html;
}}

function afterComposantsRender() {{
  document.querySelectorAll('.card[data-open]').forEach(card => {{
    card.onclick = () => openLesson(card.dataset.open);
  }});
}}

/* ======================================================================
   RENDER : CHEAT SHEETS
   ====================================================================== */
function renderCheatsheets() {{
  let html = `<div class="eyebrow-free-title"><h1>Cheat Sheets & Mémos Rapides</h1><p class="sub">Rappels de syntaxe essentiels pour coder sans perdre de temps.</p></div>`;

  Object.entries(CHEATSHEETS).forEach(([titre, rows]) => {{
    html += `
      <div class="card" style="margin-bottom:20px;">
        <h3 style="font-size:17px;margin-bottom:14px;color:var(--kotlin);">${{titre}}</h3>
        <table class="explain-table" style="margin:0;">
          <tr><th>Instruction</th><th>Description</th></tr>
          ${{rows.map(([code, desc]) => `
            <tr>
              <td><code>${{escapeHTML(code)}}</code></td>
              <td>${{desc}}</td>
            </tr>
          `).join('')}}
        </table>
      </div>
    `;
  }});

  return html;
}}

/* ======================================================================
   RENDER : GLOSSAIRE
   ====================================================================== */
function renderGlossaire() {{
  let html = `<div class="eyebrow-free-title"><h1>Glossaire Android & Compose</h1><p class="sub">Tous les concepts techniques expliqués simplement avec rigueur.</p></div><div class="card">`;

  GLOSSARY.sort((a,b) => a[0].localeCompare(b[0])).forEach(([terme, def]) => {{
    html += `
      <div style="padding:12px 0;border-bottom:1px solid var(--line);">
        <div style="font-family:'JetBrains Mono';font-weight:700;font-size:14.5px;color:var(--kotlin);">${{terme}}</div>
        <div style="font-size:13.8px;color:var(--ink-soft);margin-top:3px;line-height:1.5;">${{def}}</div>
      </div>
    `;
  }});

  html += `</div>`;
  return html;
}}

/* ======================================================================
   RENDER : QUIZ GÉNÉRAL
   ====================================================================== */
function renderQuiz() {{
  return `
    <div class="eyebrow-free-title">
      <h1>Quiz de Révision Général</h1>
      <p class="sub">Testez votre compréhension globale sur l'ensemble des modules du cours.</p>
    </div>
    <div id="generalQuizContainer"></div>
  `;
}}

function afterQuizRender() {{
  const container = document.getElementById('generalQuizContainer');
  if (!container) return;

  const ids = lessonOrder();
  let score = 0;
  let currentIdx = 0;

  function displayQuestion() {{
    if (currentIdx >= ids.length) {{
      container.innerHTML = `
        <div class="card" style="text-align:center;padding:36px 20px;">
          <h2>🎉 Quiz terminé !</h2>
          <p style="font-size:18px;margin:12px 0;">Votre score : <b>${{score}} / ${{ids.length}}</b></p>
          <button class="go-btn" id="restartQuizBtn" style="padding:8px 20px;font-size:14px;">Recommencer le quiz</button>
        </div>
      `;
      document.getElementById('restartQuizBtn').onclick = () => {{
        score = 0; currentIdx = 0; displayQuestion();
      }};
      return;
    }}

    const lesson = LESSONS[ids[currentIdx]];
    container.innerHTML = `
      <div style="font-size:13px;color:var(--ink-soft);margin-bottom:8px;font-weight:600;">Question ${{currentIdx + 1}} sur ${{ids.length}} · Module : ${{lesson.title}}</div>
      ${{quizBoxHTML(lesson, false)}}
      <button class="go-btn" id="nextQuizBtn" style="margin-top:16px;display:none;">Question suivante →</button>
    `;

    bindQuizBox(container.querySelector('.quiz-box'), lesson, (isCorrect) => {{
      if (isCorrect) score++;
      const nextBtn = document.getElementById('nextQuizBtn');
      if (nextBtn) {{
        nextBtn.style.display = "inline-block";
        nextBtn.onclick = () => {{
          currentIdx++;
          displayQuestion();
        }};
      }}
    }});
  }}

  displayQuestion();
}}

/* ======================================================================
   RENDER : FAVORIS
   ====================================================================== */
function renderFavoris() {{
  let html = `<div class="eyebrow-free-title"><h1>Mes Leçons Favorites</h1><p class="sub">Accédez en un clic à vos cours mis de côté.</p></div>`;

  if (APP.favorites.size === 0) {{
    html += `<div class="card" style="text-align:center;padding:48px 20px;color:var(--ink-soft);">
      <div style="font-size:32px;margin-bottom:10px;">⭐</div>
      <div style="font-weight:700;font-size:16px;color:var(--ink);">Aucun favori enregistré</div>
      <div style="font-size:13.5px;margin-top:4px;">Cliquez sur « ☆ Ajouter aux favoris » en haut de n'importe quel cours pour le retrouver ici.</div>
    </div>`;
    return html;
  }}

  html += `<div class="grid2">`;
  APP.favorites.forEach(id => {{
    const l = LESSONS[id];
    if (!l) return;
    html += `
      <div class="card course-card">
        <h4>${{l.title}}</h4>
        <div class="meta">${{badgeHTML(l.level)}} · ⏱ ${{l.duration}}</div>
        <div class="btn-row">
          <button class="go-btn" data-open="${{id}}">Consulter le cours →</button>
        </div>
      </div>
    `;
  }});
  html += `</div>`;
  return html;
}}

function afterFavorisRender() {{
  document.querySelectorAll('#content [data-open]').forEach(b => b.onclick = () => openLesson(b.dataset.open));
}}

/* ======================================================================
   RENDER : PAGE DE LEÇON (FORMAT EN 13 PARTIES + SIMULATEUR ANDROID)
   ====================================================================== */
function renderLesson(id) {{
  const l = LESSONS[id];
  const isFav = APP.favorites.has(id);
  const isDone = APP.completed.has(id);
  const order = lessonOrder();
  const pos = order.indexOf(id);
  const prevId = order[pos - 1], nextId = order[pos + 1];

  return `
    <div class="lesson-header">
      <a class="back-link" id="backLink">← Retour au parcours d'apprentissage</a>
      <h1>${{l.title}}</h1>
      <div class="lesson-meta-bar">
        ${{badgeHTML(l.level)}}
        <span class="badge dur">⏱ Durée : ${{l.duration}}</span>
        <button class="go-btn" id="favBtn" style="margin-left:auto;">
          ${{isFav ? '★ En favoris' : '☆ Ajouter aux favoris'}}
        </button>
        <button class="go-btn" id="markDoneTopBtn" style="${{isDone ? 'background:var(--android-dim);color:var(--android);border-color:var(--android);' : ''}}">
          ${{isDone ? '✓ Validé' : 'Marquer comme terminé'}}
        </button>
      </div>
    </div>

    <!-- SOMMAIRE RAPIDE STICKY -->
    <div class="lesson-toc">
      <a href="#sec1" class="toc-pill">1. Concept</a>
      <a href="#sec4" class="toc-pill">4. Syntaxe</a>
      <a href="#sec6" class="toc-pill">6. Ligne par ligne</a>
      <a href="#sec7" class="toc-pill">7. Code de A à Z</a>
      <a href="#sec8" class="toc-pill">8. Simulateur Android</a>
      <a href="#sec9" class="toc-pill">9. Paramètres</a>
      <a href="#sec10" class="toc-pill">10. Pièges & Erreurs</a>
      <a href="#sec11" class="toc-pill">11. Exercice</a>
      <a href="#sec12" class="toc-pill">12. Quiz</a>
      <a href="#sec13" class="toc-pill">13. À retenir</a>
    </div>

    <!-- SECTION 1 : QUOI -->
    <div class="section-block" id="sec1">
      <h3><span class="num">1</span> Qu'est-ce que c'est ?</h3>
      <p>${{l.quoi}}</p>
    </div>

    <!-- SECTION 2 : POURQUOI -->
    <div class="section-block" id="sec2">
      <h3><span class="num">2</span> Pourquoi l'utiliser ?</h3>
      <p>${{l.pourquoi}}</p>
    </div>

    <!-- SECTION 3 : QUAND -->
    <div class="section-block" id="sec3">
      <h3><span class="num">3</span> Quand l'utiliser en pratique ?</h3>
      <p>${{l.quand}}</p>
    </div>

    <!-- SECTION 4 : SYNTAXE -->
    <div class="section-block" id="sec4">
      <h3><span class="num">4</span> Signature & Syntaxe de Base</h3>
      <div class="code-container">
        <div class="codebox"><button class="copy-btn" data-code="${{encodeURIComponent(l.syntaxe)}}">Copier</button><pre>${{highlightKotlin(l.syntaxe)}}</pre></div>
      </div>
    </div>

    <!-- SECTION 5 : EXEMPLE MINIMAL -->
    <div class="section-block" id="sec5">
      <h3><span class="num">5</span> Exemple Minimal</h3>
      <div class="code-container">
        <div class="codebox"><button class="copy-btn" data-code="${{encodeURIComponent(l.exempleMin)}}">Copier</button><pre>${{highlightKotlin(l.exempleMin)}}</pre></div>
      </div>
    </div>

    <!-- SECTION 6 : EXPLICATION LIGNE PAR LIGNE -->
    <div class="section-block" id="sec6">
      <h3><span class="num">6</span> Explication Ligne par Ligne (Le Pourquoi du Code)</h3>
      <table class="explain-table">
        <tr><th>Instruction Kotlin</th><th>Rôle et justification technique</th></tr>
        ${{l.explication.map(([c, exp]) => `
          <tr>
            <td><code>${{escapeHTML(c)}}</code></td>
            <td>${{exp}}</td>
          </tr>
        `).join('')}}
      </table>
    </div>

    <!-- SECTION 7 : EXEMPLE COMPLET DE A À Z (AVEC ONGLETS) -->
    <div class="section-block" id="sec7">
      <h3><span class="num">7</span> Exemple Complet de A à Z (Prêt pour Android Studio)</h3>
      <p style="font-size:13.5px;color:var(--ink-soft);">Ce code est complet et autonome. Vous pouvez le copier-coller directement dans votre projet Android Studio.</p>
      
      <div class="code-container">
        <div class="code-tabs">
          <button class="code-tab-btn active" data-tab="tab-a2z">⭐ Code Complet Kotlin (A à Z)</button>
          <button class="code-tab-btn" data-tab="tab-gradle">📦 Dépendances build.gradle.kts</button>
          <button class="code-tab-btn" data-tab="tab-min">⚡ Exemple Minimal</button>
        </div>

        <div class="code-tab-panel active" id="tab-a2z">
          <div class="codebox"><button class="copy-btn" data-code="${{encodeURIComponent(l.exempleReel)}}">Copier le fichier complet</button><pre>${{highlightKotlin(l.exempleReel)}}</pre></div>
        </div>
        <div class="code-tab-panel" id="tab-gradle">
          <div class="codebox"><button class="copy-btn" data-code="${{encodeURIComponent(l.gradle)}}">Copier Gradle</button><pre>${{highlightKotlin(l.gradle)}}</pre></div>
        </div>
        <div class="code-tab-panel" id="tab-min">
          <div class="codebox"><button class="copy-btn" data-code="${{encodeURIComponent(l.exempleMin)}}">Copier</button><pre>${{highlightKotlin(l.exempleMin)}}</pre></div>
        </div>
      </div>
    </div>

    <!-- SECTION 8 : RÉSULTAT & SIMULATEUR ANDROID INTERACTIF -->
    <div class="section-block" id="sec8">
      <h3><span class="num">8</span> Résultat Visuel & Simulateur Interactif</h3>
      
      <div class="phone-sim-wrap">
        <div class="sim-toggle-row">
          <button class="sim-toggle-btn active" id="btnSimDevice">📱 Rendu Interactif Smartphone</button>
          <button class="sim-toggle-btn" id="btnSimSchema">📐 Schéma Architectural & Flux</button>
        </div>

        <!-- Smartphone Device Frame -->
        <div class="smartphone-device" id="phoneMockup">
          <div class="smartphone-screen">
            <div class="phone-statusbar">
              <span>12:00</span>
              <div class="phone-notch"></div>
              <span>5G 100%</span>
            </div>
            
            <div class="phone-appbar">
              <span id="phoneTitle">${{l.title.split(':')[0]}}</span>
              <span style="font-size:12px;">Android 14</span>
            </div>

            <div class="phone-viewport" id="phoneInteractiveViewport">
              ${{getInteractiveWidgetHTML(id)}}
            </div>

            <div class="phone-navbar">
              <div class="phone-nav-pill"></div>
            </div>
          </div>
        </div>

        <!-- Schema View Box -->
        <div class="schema-box" id="phoneSchemaBox">${{escapeHTML(l.resultat)}}</div>
      </div>
    </div>

    <!-- SECTION 9 : PARAMÈTRES IMPORTANTS -->
    <div class="section-block" id="sec9">
      <h3><span class="num">9</span> Paramètres Importants & Propriétés</h3>
      <table class="explain-table">
        <tr><th>Propriété / Paramètre</th><th>Description et impact sur le composant</th></tr>
        ${{l.params.map(([p, d]) => `
          <tr>
            <td><code>${{escapeHTML(p)}}</code></td>
            <td>${{d}}</td>
          </tr>
        `).join('')}}
      </table>
    </div>

    <!-- SECTION 10 : ERREURS FRÉQUENTES -->
    <div class="section-block" id="sec10">
      <h3><span class="num">10</span> Pièges & Erreurs Fréquentes en Entreprise</h3>
      ${{l.erreurs.map(([err, fix]) => `
        <div class="err-item">
          <div class="err-head">⚠ ${{escapeHTML(err)}}</div>
          <div class="err-fix"><b>Solution :</b> ${{fix}}</div>
        </div>
      `).join('')}}
    </div>

    <!-- SECTION 11 : EXERCICE PRATIQUE -->
    <div class="section-block" id="sec11">
      <h3><span class="num">11</span> Exercice Pratique</h3>
      <div class="exercise-box">
        <div class="exercise-title">🎯 Défi à réaliser :</div>
        <p style="margin:0 0 8px 0;font-size:14.5px;">${{l.exercice.enonce}}</p>
        <div class="exercise-hint">💡 <b>Indice :</b> ${{l.exercice.indice}}</div>
        <button class="sol-btn" id="toggleSolutionBtn">👁 Afficher la solution de A à Z</button>
        
        <div class="sol-content" id="solutionContainer">
          <div style="font-weight:700;font-size:13px;color:var(--amber);margin-bottom:6px;">Solution commentée :</div>
          <div class="code-container" style="margin:0;">
            <div class="codebox"><pre>${{highlightKotlin(l.exercice.solution)}}</pre></div>
          </div>
        </div>
      </div>
    </div>

    <!-- SECTION 12 : QUIZ INTERACTIF -->
    <div class="section-block" id="sec12">
      <h3><span class="num">12</span> Quiz de Validation</h3>
      <div id="lessonQuizContainer">${{quizBoxHTML(l, false)}}</div>
    </div>

    <!-- SECTION 13 : CE QU'IL FAUT RETENIR -->
    <div class="section-block" id="sec13">
      <h3><span class="num">13</span> Ce qu'il faut absolument retenir</h3>
      <div class="card">
        <ul class="retain-list">
          ${{l.retenir.map(r => `<li>${{r}}</li>`).join('')}}
        </ul>
      </div>
    </div>

    <!-- NAVIGATION EN BAS DE LEÇON -->
    <div class="lesson-nav-footer">
      <button id="footerPrevBtn" ${{!prevId ? 'disabled style="opacity:.4"' : ''}}>
        ← ${{prevId ? LESSONS[prevId].title.split(':')[0] : 'Précédent'}}
      </button>
      
      <button id="footerDoneBtn" class="finish-btn ${{isDone ? 'done' : ''}}">
        ${{isDone ? '✓ Cours Validé' : 'Marquer comme validé ✓'}}
      </button>
      
      <button id="footerNextBtn" ${{!nextId ? 'disabled style="opacity:.4"' : ''}}>
        ${{nextId ? LESSONS[nextId].title.split(':')[0] : 'Suivant'}} →
      </button>
    </div>
  `;
}}

/* ======================================================================
   WIDGETS INTERACTIFS DANS LE SMARTPHONE VIRTUEL
   ====================================================================== */
function getInteractiveWidgetHTML(id) {{
  if (id === "layout") {{
    return `
      <div style="text-align:center;">
        <div style="font-size:12px;font-weight:600;margin-bottom:8px;color:var(--ink-soft);">Mode conteneur :</div>
        <div style="display:flex;gap:6px;justify-content:center;margin-bottom:14px;">
          <button class="go-btn layout-btn active" data-mode="column" style="padding:4px 8px;font-size:11px;">Column</button>
          <button class="go-btn layout-btn" data-mode="row" style="padding:4px 8px;font-size:11px;">Row</button>
          <button class="go-btn layout-btn" data-mode="box" style="padding:4px 8px;font-size:11px;">Box</button>
        </div>

        <div id="layoutSimTarget" style="display:flex;flex-direction:column;gap:8px;padding:12px;background:rgba(127,82,255,0.08);border-radius:12px;min-height:160px;position:relative;transition:all .2s ease;">
          <div class="sim-box" style="background:#7F52FF;color:#fff;padding:10px;border-radius:8px;font-weight:700;">Box 1</div>
          <div class="sim-box" style="background:#3DDC84;color:#fff;padding:10px;border-radius:8px;font-weight:700;">Box 2</div>
          <div class="sim-box" style="background:#D98A1B;color:#fff;padding:10px;border-radius:8px;font-weight:700;">Box 3</div>
        </div>
        <div id="layoutSimDesc" style="font-size:11px;color:var(--ink-soft);margin-top:8px;">Column : empilement vertical</div>
      </div>
    `;
  }} else if (id === "card") {{
    return `
      <div style="background:#fff;border-radius:14px;padding:14px;box-shadow:0 4px 10px rgba(0,0,0,0.1);color:#111;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span style="background:#C4453A;color:#fff;font-size:10px;font-weight:800;padding:2px 6px;border-radius:4px;">-33% PROMO</span>
          <button id="cardSimFav" style="background:none;border:none;font-size:18px;cursor:pointer;">♡</button>
        </div>
        <div style="font-weight:800;font-size:15px;margin:8px 0 2px 0;">Casque Bluetooth ANC</div>
        <div style="color:#1E8F72;font-size:16px;font-weight:800;">99.99 € <span style="font-size:12px;color:gray;text-decoration:line-through;">149.99 €</span></div>
        <button id="cardSimBuy" style="width:100%;margin-top:12px;padding:8px;background:#7F52FF;color:#fff;border:none;border-radius:8px;font-weight:700;cursor:pointer;">🛒 Ajouter au panier</button>
        <div id="cardSimToast" style="display:none;margin-top:8px;padding:6px;background:#E3F5EF;color:#1E8F72;border-radius:6px;font-size:11px;text-align:center;font-weight:700;">Article ajouté au panier !</div>
      </div>
    `;
  }} else if (id === "scaffold") {{
    return `
      <div style="display:flex;flex-direction:column;height:100%;min-height:220px;position:relative;">
        <div style="background:#EFEBFF;color:#6032D6;padding:8px 10px;border-radius:6px;font-weight:700;font-size:12px;display:flex;justify-content:space-between;">
          <span>TopAppBar: Mes Notes</span>
          <span>🔍</span>
        </div>
        <div style="padding:10px 0;flex:1;">
          <div style="background:rgba(0,0,0,0.05);padding:8px;border-radius:6px;margin-bottom:6px;font-size:12px;">📝 Note #1 : Réviser Compose</div>
          <div style="background:rgba(0,0,0,0.05);padding:8px;border-radius:6px;font-size:12px;">📝 Note #2 : Préparer l'examen MVVM</div>
        </div>
        <button id="scaffoldFab" style="position:absolute;bottom:30px;right:4px;width:38px;height:38px;border-radius:50%;background:#7F52FF;color:#fff;border:none;font-size:20px;cursor:pointer;box-shadow:0 3px 8px rgba(0,0,0,0.2);">+</button>
        <div id="scaffoldSnackbar" style="display:none;background:#222;color:#fff;padding:8px 12px;border-radius:6px;font-size:11px;display:none;justify-content:space-between;align-items:center;">
          <span>Nouvelle note créée !</span>
          <span style="color:#3DDC84;cursor:pointer;font-weight:700;">OK</span>
        </div>
      </div>
    `;
  }} else if (id === "lazycolumn") {{
    return `
      <div>
        <input id="simLazySearch" placeholder="Filtrer les contacts..." style="width:100%;padding:6px 10px;font-size:12px;border-radius:6px;border:1px solid #ccc;margin-bottom:8px;box-sizing:border-box;">
        <div id="simLazyList" style="display:flex;flex-direction:column;gap:6px;max-height:200px;overflow-y:auto;"></div>
      </div>
    `;
  }} else if (id === "state") {{
    return `
      <div style="text-align:center;padding:10px;">
        <div style="font-size:12px;color:gray;">Composant Interactif (State)</div>
        <div id="simStateCount" style="font-size:36px;font-weight:800;color:#7F52FF;margin:8px 0;">0</div>
        <div style="display:flex;gap:8px;justify-content:center;">
          <button id="simStateMinus" class="go-btn" style="padding:6px 14px;font-size:16px;">-</button>
          <button id="simStatePlus" class="go-btn" style="padding:6px 14px;font-size:16px;background:#7F52FF;color:#fff;">+</button>
          <button id="simStateReset" class="go-btn" style="padding:6px 10px;font-size:12px;">↺</button>
        </div>
        <div style="margin-top:14px;font-size:11px;background:rgba(127,82,255,0.1);padding:6px;border-radius:6px;">
          Recompositions déclenchées : <b id="simRecomposeCount" style="color:#7F52FF;">1</b>
        </div>
      </div>
    `;
  }} else if (id === "viewmodel") {{
    return `
      <div>
        <div style="font-weight:700;font-size:13px;margin-bottom:8px;">Formulaire Authentification</div>
        <input id="simVmEmail" placeholder="Email (ex: test@kotlin.com)" style="width:100%;padding:6px;font-size:11px;border-radius:6px;border:1px solid #ccc;margin-bottom:6px;box-sizing:border-box;">
        <input id="simVmPass" type="password" placeholder="Mot de passe" style="width:100%;padding:6px;font-size:11px;border-radius:6px;border:1px solid #ccc;margin-bottom:8px;box-sizing:border-box;">
        <button id="simVmRotate" style="width:100%;padding:7px;background:#383D4E;color:#fff;border:none;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer;">🔄 Simuler Rotation d'Écran</button>
        <div id="simVmFeedback" style="font-size:11px;color:#1E8F72;margin-top:6px;font-weight:600;display:none;">✓ Données conservées intactes dans le ViewModel !</div>
      </div>
    `;
  }} else if (id === "mvvm") {{
    return `
      <div>
        <div style="display:flex;gap:4px;margin-bottom:10px;">
          <button class="go-btn mvvm-state-btn active" data-s="loading" style="padding:4px 6px;font-size:10px;">Chargement</button>
          <button class="go-btn mvvm-state-btn" data-s="success" style="padding:4px 6px;font-size:10px;">Succès</button>
          <button class="go-btn mvvm-state-btn" data-s="error" style="padding:4px 6px;font-size:10px;">Erreur</button>
        </div>
        <div id="simMvvmTarget" style="min-height:140px;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.03);border-radius:8px;padding:12px;"></div>
      </div>
    `;
  }} else if (id === "datastore") {{
    return `
      <div>
        <div style="font-weight:700;font-size:13px;margin-bottom:8px;">Préférences DataStore</div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
          <span style="font-size:12px;">Mode Sombre</span>
          <input type="checkbox" id="simDsDark">
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
          <span style="font-size:12px;">Notifications</span>
          <input type="checkbox" id="simDsNotif" checked>
        </div>
        <input id="simDsName" value="Alexandre" placeholder="Nom" style="width:100%;padding:6px;font-size:11px;border-radius:6px;border:1px solid #ccc;box-sizing:border-box;margin-bottom:8px;">
        <button id="simDsRestart" style="width:100%;padding:6px;background:#7F52FF;color:#fff;border:none;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer;">⚡ Fermer et Relancer l'App</button>
        <div id="simDsFeedback" style="font-size:11px;color:#1E8F72;margin-top:6px;display:none;">Données restaurées depuis le fichier .preferences_pb !</div>
      </div>
    `;
  }} else if (id === "room") {{
    return `
      <div>
        <div style="font-weight:700;font-size:12px;margin-bottom:6px;">Console SQLite Room : Table 'articles'</div>
        <div style="display:flex;gap:4px;margin-bottom:8px;">
          <input id="simRoomTitle" placeholder="Nouvel article..." style="flex:1;padding:5px;font-size:11px;border:1px solid #ccc;border-radius:4px;">
          <button id="simRoomInsert" style="padding:5px 8px;background:#3DDC84;color:#fff;border:none;border-radius:4px;font-size:11px;font-weight:700;cursor:pointer;">INSERT</button>
        </div>
        <div id="simRoomList" style="display:flex;flex-direction:column;gap:4px;max-height:140px;overflow-y:auto;"></div>
      </div>
    `;
  }} else if (id === "crud") {{
    return `
      <div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
          <span style="font-weight:700;font-size:12px;">CRUD Produits</span>
          <button id="simCrudAdd" style="padding:3px 8px;background:#7F52FF;color:#fff;border:none;border-radius:4px;font-size:11px;font-weight:700;cursor:pointer;">+ Ajouter</button>
        </div>
        <div id="simCrudList" style="display:flex;flex-direction:column;gap:5px;max-height:160px;overflow-y:auto;"></div>
        <div id="simCrudModal" style="display:none;position:absolute;inset:10px;background:#fff;border-radius:12px;padding:12px;box-shadow:0 8px 24px rgba(0,0,0,0.3);z-index:10;color:#111;">
          <div style="font-weight:700;font-size:13px;margin-bottom:6px;">Confirmer Suppression ?</div>
          <p style="font-size:11px;color:gray;margin:0 0 10px 0;">Supprimer définitivement l'article de la base ?</p>
          <div style="display:flex;gap:8px;justify-content:flex-end;">
            <button id="simCrudCancel" style="padding:4px 8px;border:1px solid #ccc;background:#eee;border-radius:4px;font-size:11px;">Annuler</button>
            <button id="simCrudConfirmDelete" style="padding:4px 8px;border:none;background:#C4453A;color:#fff;border-radius:4px;font-size:11px;font-weight:700;">Supprimer</button>
          </div>
        </div>
      </div>
    `;
  }} else if (id === "api") {{
    return `
      <div>
        <div style="font-size:11px;font-family:'JetBrains Mono';color:#7F52FF;margin-bottom:6px;">GET /products (Retrofit)</div>
        <button id="simApiFetch" style="width:100%;padding:6px;background:#7F52FF;color:#fff;border:none;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer;">📡 Envoyer la requête HTTP</button>
        <div id="simApiTarget" style="margin-top:8px;min-height:130px;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.03);border-radius:6px;padding:8px;">
          <span style="font-size:11px;color:gray;">Prêt à interroger l'API</span>
        </div>
      </div>
    `;
  }} else if (id === "navigation") {{
    return `
      <div id="simNavScreen1">
        <div style="font-weight:700;font-size:12px;margin-bottom:6px;">Écran 1 : Catalogue</div>
        <div style="display:flex;flex-direction:column;gap:6px;">
          <div class="sim-nav-item" data-id="101" data-name="MacBook Pro" data-price="1999 €" style="padding:8px;background:rgba(0,0,0,0.04);border-radius:6px;display:flex;justify-content:space-between;cursor:pointer;font-size:12px;">
            <span>💻 MacBook Pro</span>
            <span style="color:#7F52FF;font-weight:700;">1999 € ›</span>
          </div>
          <div class="sim-nav-item" data-id="102" data-name="Clavier Sans-Fil" data-price="119 €" style="padding:8px;background:rgba(0,0,0,0.04);border-radius:6px;display:flex;justify-content:space-between;cursor:pointer;font-size:12px;">
            <span>⌨ Clavier Sans-Fil</span>
            <span style="color:#7F52FF;font-weight:700;">119 € ›</span>
          </div>
        </div>
      </div>
      <div id="simNavScreen2" style="display:none;">
        <button id="simNavBack" style="background:none;border:none;color:#7F52FF;font-weight:700;font-size:11px;cursor:pointer;padding:0;margin-bottom:8px;">← Retour Catalogue</button>
        <div style="background:#fff;color:#111;padding:10px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.1);">
          <div id="simNavDetailName" style="font-weight:800;font-size:14px;">Nom</div>
          <div id="simNavDetailPrice" style="color:#1E8F72;font-weight:800;margin:4px 0;">Prix</div>
          <div style="font-size:10px;color:gray;background:#eee;padding:4px;border-radius:4px;margin-top:6px;">Argument de route reçu : <b id="simNavArg">id=101</b></div>
        </div>
      </div>
    `;
  }}
  return `<div style="font-size:12px;color:gray;text-align:center;padding:20px;">Aperçu interactif disponible pour ce module.</div>`;
}}

function bindInteractiveWidgets(id) {{
  if (id === "layout") {{
    const btns = document.querySelectorAll('.layout-btn');
    const target = document.getElementById('layoutSimTarget');
    const desc = document.getElementById('layoutSimDesc');
    btns.forEach(b => {{
      b.onclick = () => {{
        btns.forEach(x => x.classList.remove('active'));
        b.classList.add('active');
        const mode = b.dataset.mode;
        if (mode === "column") {{
          target.style.flexDirection = "column";
          target.querySelectorAll('.sim-box').forEach(sb => sb.style.position = "static");
          desc.textContent = "Column : empilement vertical fluide";
        }} else if (mode === "row") {{
          target.style.flexDirection = "row";
          target.querySelectorAll('.sim-box').forEach(sb => sb.style.position = "static");
          desc.textContent = "Row : alignement horizontal côte à côte";
        }} else if (mode === "box") {{
          target.style.flexDirection = "column";
          const boxes = target.querySelectorAll('.sim-box');
          boxes[0].style.position = "absolute"; boxes[0].style.top = "10px"; boxes[0].style.left = "10px";
          boxes[1].style.position = "absolute"; boxes[1].style.top = "25px"; boxes[1].style.left = "25px";
          boxes[2].style.position = "absolute"; boxes[2].style.top = "40px"; boxes[2].style.left = "40px";
          desc.textContent = "Box : calques superposés les uns sur les autres";
        }}
      }};
    }});
  }} else if (id === "card") {{
    const fav = document.getElementById('cardSimFav');
    const buy = document.getElementById('cardSimBuy');
    const toast = document.getElementById('cardSimToast');
    if (fav) fav.onclick = () => fav.textContent = fav.textContent === "♡" ? "❤️" : "♡";
    if (buy) buy.onclick = () => {{
      toast.style.display = "block";
      setTimeout(() => toast.style.display = "none", 1600);
    }};
  }} else if (id === "scaffold") {{
    const fab = document.getElementById('scaffoldFab');
    const sb = document.getElementById('scaffoldSnackbar');
    if (fab && sb) {{
      fab.onclick = () => {{
        sb.style.display = "flex";
        setTimeout(() => sb.style.display = "none", 2500);
      }};
    }}
  }} else if (id === "lazycolumn") {{
    const contacts = [
      {{ id: 1, name: "Alice Dubois", cat: "Amis" }},
      {{ id: 2, name: "Antoine Martin", cat: "Amis" }},
      {{ id: 3, name: "Béatrice Roux", cat: "Famille" }},
      {{ id: 4, name: "Damien Vallet", cat: "Travail" }},
      {{ id: 5, name: "Claire Petit", cat: "Travail" }}
    ];
    const listEl = document.getElementById('simLazyList');
    const searchEl = document.getElementById('simLazySearch');
    function renderContacts(filter = "") {{
      if (!listEl) return;
      listEl.innerHTML = "";
      contacts.filter(c => c.name.toLowerCase().includes(filter.toLowerCase())).forEach(c => {{
        const row = document.createElement('div');
        row.style.cssText = "padding:6px 8px;background:rgba(0,0,0,0.04);border-radius:6px;display:flex;justify-content:space-between;align-items:center;font-size:11.5px;";
        row.innerHTML = `<span>👤 <b>${{c.name}}</b> (${{c.cat}})</span><button style="background:none;border:none;color:red;cursor:pointer;">🗑</button>`;
        row.querySelector('button').onclick = () => {{
          const idx = contacts.findIndex(x => x.id === c.id);
          if (idx !== -1) {{ contacts.splice(idx, 1); renderContacts(searchEl.value); }}
        }};
        listEl.appendChild(row);
      }});
    }}
    renderContacts();
    if (searchEl) searchEl.oninput = (e) => renderContacts(e.target.value);
  }} else if (id === "state") {{
    let count = 0; let recompose = 1;
    const countEl = document.getElementById('simStateCount');
    const recEl = document.getElementById('simRecomposeCount');
    function update() {{
      countEl.textContent = count;
      recompose++;
      recEl.textContent = recompose;
    }}
    document.getElementById('simStatePlus').onclick = () => {{ count++; update(); }};
    document.getElementById('simStateMinus').onclick = () => {{ count--; update(); }};
    document.getElementById('simStateReset').onclick = () => {{ count = 0; update(); }};
  }} else if (id === "viewmodel") {{
    const btn = document.getElementById('simVmRotate');
    const fb = document.getElementById('simVmFeedback');
    if (btn) btn.onclick = () => {{
      fb.style.display = "block";
      const phone = document.getElementById('phoneMockup');
      phone.style.transform = "rotate(-4deg) scale(0.98)";
      setTimeout(() => phone.style.transform = "none", 300);
    }};
  }} else if (id === "mvvm") {{
    const target = document.getElementById('simMvvmTarget');
    const btns = document.querySelectorAll('.mvvm-state-btn');
    function setMvvm(s) {{
      btns.forEach(b => b.classList.toggle('active', b.dataset.s === s));
      if (s === "loading") {{
        target.innerHTML = `<span style="font-size:12px;color:gray;">⏳ CircularProgressIndicator()...</span>`;
      }} else if (s === "success") {{
        target.innerHTML = `<div style="width:100%;font-size:11px;display:flex;flex-direction:column;gap:4px;"><div style="background:#fff;padding:6px;border-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">📦 Article 1: Compose UI</div><div style="background:#fff;padding:6px;border-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,0.1);">📦 Article 2: MVVM Architecture</div></div>`;
      }} else if (s === "error") {{
        target.innerHTML = `<div style="color:red;font-size:11px;text-align:center;">❌ Erreur HTTP 500 : Serveur indisponible<br><button class="go-btn" style="margin-top:6px;font-size:10px;">Réessayer</button></div>`;
      }}
    }}
    btns.forEach(b => b.onclick = () => setMvvm(b.dataset.s));
    setMvvm("loading");
  }} else if (id === "datastore") {{
    const restart = document.getElementById('simDsRestart');
    const fb = document.getElementById('simDsFeedback');
    if (restart) restart.onclick = () => {{
      fb.style.display = "block";
      setTimeout(() => fb.style.display = "none", 2000);
    }};
  }} else if (id === "room") {{
    let items = [
      {{ id: 1, title: "Lait demi-écrémé" }},
      {{ id: 2, title: "Café en grains" }}
    ];
    const listEl = document.getElementById('simRoomList');
    const inputEl = document.getElementById('simRoomTitle');
    const btn = document.getElementById('simRoomInsert');
    function renderRoom() {{
      if (!listEl) return;
      listEl.innerHTML = "";
      items.forEach(it => {{
        const row = document.createElement('div');
        row.style.cssText = "padding:4px 6px;background:#fff;border-radius:4px;display:flex;justify-content:space-between;font-size:11px;box-shadow:0 1px 2px rgba(0,0,0,0.06);";
        row.innerHTML = `<span>#${{it.id}} <b>${{it.title}}</b></span><button style="background:none;border:none;color:red;cursor:pointer;">✕</button>`;
        row.querySelector('button').onclick = () => {{
          items = items.filter(x => x.id !== it.id);
          renderRoom();
        }};
        listEl.appendChild(row);
      }});
    }}
    renderRoom();
    if (btn) btn.onclick = () => {{
      if (inputEl.value.trim()) {{
        items.push({{ id: items.length ? items[items.length - 1].id + 1 : 1, title: inputEl.value.trim() }});
        inputEl.value = "";
        renderRoom();
      }}
    }};
  }} else if (id === "crud") {{
    let prods = [
      {{ id: 1, name: "Clavier Pro", price: "89.99 €" }},
      {{ id: 2, name: "Souris Ergonomique", price: "45.00 €" }}
    ];
    let toDeleteId = null;
    const listEl = document.getElementById('simCrudList');
    const modal = document.getElementById('simCrudModal');
    function renderCrud() {{
      if (!listEl) return;
      listEl.innerHTML = "";
      prods.forEach(p => {{
        const d = document.createElement('div');
        d.style.cssText = "padding:6px 8px;background:#fff;border-radius:6px;display:flex;justify-content:space-between;align-items:center;font-size:11.5px;box-shadow:0 1px 3px rgba(0,0,0,0.08);";
        d.innerHTML = `<div><b>${{p.name}}</b> <span style="color:#1E8F72;">${{p.price}}</span></div><button style="background:none;border:none;color:red;cursor:pointer;">🗑</button>`;
        d.querySelector('button').onclick = () => {{
          toDeleteId = p.id;
          modal.style.display = "block";
        }};
        listEl.appendChild(d);
      }});
    }}
    renderCrud();
    document.getElementById('simCrudCancel').onclick = () => modal.style.display = "none";
    document.getElementById('simCrudConfirmDelete').onclick = () => {{
      prods = prods.filter(x => x.id !== toDeleteId);
      modal.style.display = "none";
      renderCrud();
    }};
    document.getElementById('simCrudAdd').onclick = () => {{
      const n = prompt("Nom du produit :", "Écran 4K");
      if (n) {{ prods.push({{ id: Date.now(), name: n, price: "299.00 €" }}); renderCrud(); }}
    }};
  }} else if (id === "api") {{
    const btn = document.getElementById('simApiFetch');
    const target = document.getElementById('simApiTarget');
    if (btn) btn.onclick = () => {{
      target.innerHTML = `<span style="font-size:11px;color:#7F52FF;">⏳ Requête HTTP en cours...</span>`;
      setTimeout(() => {{
        target.innerHTML = `<div style="font-size:11px;width:100%;"><div style="background:#fff;padding:6px;border-radius:4px;margin-bottom:4px;box-shadow:0 1px 3px rgba(0,0,0,0.1);"><b>Casque Audio</b> : 99.99 $</div><div style="background:#fff;padding:6px;border-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,0.1);"><b>Sac à Dos</b> : 45.00 $</div></div>`;
      }}, 700);
    }};
  }} else if (id === "navigation") {{
    const s1 = document.getElementById('simNavScreen1');
    const s2 = document.getElementById('simNavScreen2');
    const nameEl = document.getElementById('simNavDetailName');
    const priceEl = document.getElementById('simNavDetailPrice');
    const argEl = document.getElementById('simNavArg');
    document.querySelectorAll('.sim-nav-item').forEach(it => {{
      it.onclick = () => {{
        nameEl.textContent = it.dataset.name;
        priceEl.textContent = it.dataset.price;
        argEl.textContent = "produitId=" + it.dataset.id;
        s1.style.display = "none";
        s2.style.display = "block";
      }};
    }});
    document.getElementById('simNavBack').onclick = () => {{
      s2.style.display = "none";
      s1.style.display = "block";
    }};
  }}
}}

function afterLessonRender(id) {{
  // Back link
  document.getElementById('backLink').onclick = () => {{
    setActiveNav(document.querySelector('[data-view="parcours"]'));
    renderView('parcours');
  }};

  // Favorite toggle
  const favBtn = document.getElementById('favBtn');
  favBtn.onclick = () => {{
    if (APP.favorites.has(id)) APP.favorites.delete(id);
    else APP.favorites.add(id);
    APP.save();
    openLesson(id);
    buildSidebarLessons();
  }};

  // Done toggles
  const markDone = () => {{
    if (APP.completed.has(id)) APP.completed.delete(id);
    else APP.completed.add(id);
    APP.save();
    openLesson(id);
    buildSidebarLessons();
  }};
  document.getElementById('markDoneTopBtn').onclick = markDone;
  document.getElementById('footerDoneBtn').onclick = markDone;

  // Previous & Next navigation
  const order = lessonOrder();
  const pos = order.indexOf(id);
  const prevBtn = document.getElementById('footerPrevBtn');
  const nextBtn = document.getElementById('footerNextBtn');
  if (prevBtn && order[pos - 1]) prevBtn.onclick = () => openLesson(order[pos - 1]);
  if (nextBtn && order[pos + 1]) nextBtn.onclick = () => openLesson(order[pos + 1]);

  // Code tabs
  document.querySelectorAll('.code-tab-btn').forEach(tabBtn => {{
    tabBtn.onclick = () => {{
      const container = tabBtn.closest('.code-container');
      container.querySelectorAll('.code-tab-btn').forEach(b => b.classList.remove('active'));
      container.querySelectorAll('.code-tab-panel').forEach(p => p.classList.remove('active'));
      tabBtn.classList.add('active');
      const targetPanel = container.querySelector('#' + tabBtn.dataset.tab);
      if (targetPanel) targetPanel.classList.add('active');
    }};
  }});

  // Toggle Solution Exercice
  const solBtn = document.getElementById('toggleSolutionBtn');
  const solContent = document.getElementById('solutionContainer');
  if (solBtn && solContent) {{
    solBtn.onclick = () => {{
      const isHidden = solContent.style.display === "none" || !solContent.style.display;
      solContent.style.display = isHidden ? "block" : "none";
      solBtn.textContent = isHidden ? "🙈 Masquer la solution" : "👁 Afficher la solution de A à Z";
    }};
  }}

  // Simulateur vs Schéma toggle
  const btnDev = document.getElementById('btnSimDevice');
  const btnSch = document.getElementById('btnSimSchema');
  const phoneMock = document.getElementById('phoneMockup');
  const schemaBox = document.getElementById('phoneSchemaBox');
  if (btnDev && btnSch) {{
    btnDev.onclick = () => {{
      btnDev.classList.add('active');
      btnSch.classList.remove('active');
      phoneMock.style.display = "flex";
      schemaBox.style.display = "none";
    }};
    btnSch.onclick = () => {{
      btnSch.classList.add('active');
      btnDev.classList.remove('active');
      phoneMock.style.display = "none";
      schemaBox.style.display = "block";
    }};
  }}

  // Bind copy buttons & quizzes & widgets
  bindCopyButtons();
  bindQuizBox(document.getElementById('lessonQuizContainer'), LESSONS[id], () => {{}});
  bindInteractiveWidgets(id);
}}

/* ======================================================================
   HELPERS & COMMON BINDINGS
   ====================================================================== */
function badgeHTML(level) {{
  const map = {{
    beg: ["🟢 Débutant", "beg"],
    mid: ["🟡 Intermédiaire", "mid"],
    adv: ["🔴 Avancé", "adv"]
  }};
  const [lbl, cls] = map[level] || map.beg;
  return `<span class="badge ${{cls}}">${{lbl}}</span>`;
}}

function escapeHTML(s) {{
  return (s || "").replace(/[&<>]/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;"}}[c]));
}}

function quizBoxHTML(l, showTitle) {{
  return `
    <div class="quiz-box">
      ${{showTitle ? `<div style="font-size:12px;font-weight:700;color:var(--kotlin);margin-bottom:6px;">${{l.title}}</div>` : ''}}
      <div class="quiz-q">${{l.quiz.q}}</div>
      ${{l.quiz.options.map((opt, i) => `
        <button class="quiz-opt" data-i="${{i}}">${{opt}}</button>
      `).join('')}}
      <div class="quiz-fb" id="quizFb"></div>
    </div>
  `;
}}

function bindQuizBox(container, l, onAnswer) {{
  if (!container) return;
  const opts = container.querySelectorAll('.quiz-opt');
  const fb = container.querySelector('.quiz-fb');

  opts.forEach(opt => {{
    opt.onclick = () => {{
      const chosen = parseInt(opt.dataset.i);
      opts.forEach(o => o.disabled = true);

      const isCorrect = chosen === l.quiz.correct;
      if (isCorrect) {{
        opt.classList.add('correct');
        fb.className = "quiz-fb correct";
        fb.innerHTML = "<b>✓ Exact !</b> " + l.quiz.exp;
      }} else {{
        opt.classList.add('wrong');
        opts[l.quiz.correct].classList.add('correct');
        fb.className = "quiz-fb wrong";
        fb.innerHTML = "<b>✗ Pas tout à fait :</b> " + l.quiz.exp;
      }}
      if (onAnswer) onAnswer(isCorrect);
    }};
  }});
}}

function bindCopyButtons() {{
  document.querySelectorAll('.copy-btn').forEach(btn => {{
    btn.onclick = () => {{
      const text = decodeURIComponent(btn.dataset.code);
      navigator.clipboard?.writeText(text).catch(() => {{}});
      const original = btn.textContent;
      btn.textContent = "Copié ✓";
      btn.style.background = "var(--android)";
      btn.style.color = "#fff";
      setTimeout(() => {{
        btn.textContent = original;
        btn.style.background = "";
        btn.style.color = "";
      }}, 1500);
    }};
  }});
}}

/* ======================================================================
   ROUTER CENTRAL
   ====================================================================== */
function renderView(view) {{
  APP.currentView = view;
  APP.currentLesson = null;
  const content = document.getElementById('content');
  
  if (view === "dashboard") content.innerHTML = renderDashboard();
  else if (view === "parcours") content.innerHTML = renderParcours();
  else if (view === "comment") content.innerHTML = renderComment();
  else if (view === "composants") content.innerHTML = renderComposants();
  else if (view === "cheatsheets") content.innerHTML = renderCheatsheets();
  else if (view === "glossaire") content.innerHTML = renderGlossaire();
  else if (view === "quiz") content.innerHTML = renderQuiz();
  else if (view === "favoris") content.innerHTML = renderFavoris();

  if (view === "dashboard") afterDashboardRender();
  else if (view === "parcours") afterParcoursRender();
  else if (view === "comment") afterCommentRender();
  else if (view === "composants") afterComposantsRender();
  else if (view === "quiz") afterQuizRender();
  else if (view === "favoris") afterFavorisRender();

  document.getElementById('sidebar').classList.remove('open');
  window.scrollTo(0, 0);
}}

function openLesson(id) {{
  if (!LESSONS[id]) return;
  APP.currentView = "lesson";
  APP.currentLesson = id;
  
  setActiveNav(document.querySelector(`[data-lesson="${{id}}"]`));
  document.getElementById('content').innerHTML = renderLesson(id);
  afterLessonRender(id);
  
  document.getElementById('sidebar').classList.remove('open');
  window.scrollTo(0, 0);
}}

/* ======================================================================
   INITIALISATION GLOBALE
   ====================================================================== */
buildSidebarLessons();
renderView('dashboard');
</script>
</body>
</html>
"""

    with open("c:/dev/app2/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Fichier index.html généré avec succès !")

if __name__ == "__main__":
    build_index_html()
