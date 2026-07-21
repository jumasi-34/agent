# Stitch Design System: Antigravity Quality Analytics Dashboard

## 1. Visual Theme & Atmosphere
The Antigravity dashboard is a high-agency, cockpit-dense software interface designed for precision B2B manufacturing quality analysis. It demands extreme data clarity and exact visual anchors. 
* **Visual Density:** `8/10` (Cockpit Dense) - Vertical rhythm is tightly grouped, padding is compact, and negative space is calculated mathematically to present massive amounts of statistical data without visual clutter.
* **Layout Variance:** `4/10` (Offset Symmetric) - A highly ordered, balanced, and symmetric 12-column grid layout that respects technical cockpit alignment, with subtle asymmetric widths for metadata and metrics cards.
* **Motion Intensity:** `5/10` (Static Restrained) - Smooth spring-physics animations reserved for chart rendering (Plotly and ECharts) and hover transitions. Zero decorative loop animations.

---

## 2. Color Palette & Roles
The color hierarchy is grounded in a 95% monochromatic Grayscale canvas with a 5% high-contrast accent rule, supporting a strict semantic categorization exception.

### Grayscale Base (95% Canvas)
* **Carbon Slate Ink** (`colors.slate_800`, `#1e293b`) — Primary text, title labels, and main production trend lines.
* **Muted Steel** (`colors.slate_400`, `#94a6b8`) — Secondary text, control chart guidelines (UCL/LCL), and non-critical data.
* **Whisper Background** (`colors.slate_200`, `#e2e8f0`) — Subtle shading layers, disabled elements, and non-critical Pareto bars.
* **Canvas Gradient** — Cards use a high-contrast monochromatic backdrop gradient: 
  `linear-gradient(135deg, var(--app-surface) 0%, var(--app-background) 50%, var(--app-surface-muted) 100%)`

### Semantic Anomaly Accent (5% High-Alert)
* **Out-of-Spec Orange** (`colors.orange_500`, `#f97316`) — Exclusively reserved for statistical fails, out-of-control limits, or elements requiring immediate human intervention (e.g. scrap alerts, reject rates).

### Categorical Exception (IBM Carbon 14-Color Sequence)
Multi-categorical data (such as CQMS Registration Records and Spec Revisions) cannot be forced into Grayscale without losing informational fidelity. This data class uses the WCAG-compliant IBM Carbon Sequence:
* **Categorical 1 (Purple 70)** (`colors.carbon_purple_70`, `#6929c4`) — Quality Issues / Mass Volume Spec (V).
* **Categorical 2 (Cyan 50)** (`colors.carbon_cyan_50`, `#1192e8`) — 4M Change / SOP Spec (S).
* **Categorical 3 (Teal 70)** (`colors.carbon_teal_70_seq`, `#005d5d`) — Audits / Prototype Spec (P).
* **Categorical 4 (Magenta 70)** (`colors.carbon_magenta_70`, `#9f1853`) — Material Spec (M).
* **Categorical 5 (Red 50)** (`colors.carbon_red_50_seq`, `#fa4d56`) — Test Spec (T).

---

## 3. Typography Rules
* **Grotesque Display:** `Satoshi` or `Geist` — Tight tracking, controlled letter-spacing (floor: `-0.04em`), and line-height `1.1` to `1.2`. Used exclusively for Display headlines and Metric values.
* **Cockpit Mono:** `Geist Mono` or `JetBrains Mono` — Enforced for all quantitative data, timestamps, M-Codes, and KPI figures to ensure tabular digit alignment and clear numerical comparison.
* **Banned Patterns:** 
  * Emojis are strictly forbidden anywhere in visible text, tab names, or markdown content.
  * `Inter` is banned as a default.
  * All Em-dashes (`—` and `–`) are completely banned. Use the standard regular hyphen (`-`) instead.

---

## 4. Component Stylings

### Metric Cards
* **Vertical Metric Cards** (Production, Qty, PPM): Forced to `min-height: 165px !important` and `padding: 0.85rem 1rem !important`. Internal content is tightly grouped in a vertical stack using `justify-content: center !important` and `gap: 0.35rem !important` to prevent large empty space in the middle.
* **Custom TOP 3 Defect Card**: Uses `display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: space-between !important;` to bypass markdown wrapper vertical overrides.
* **Hover State**: Hover scale/translate (`transform: translateY(-1px)`) and diffused whisper shadows (`box-shadow: 0 4px 6px ...`) are synchronized across all 5 cards for total tactile cohesion.

### Empty States
* **No Raw-Data Failures**: Rendering empty blank charts or bare grids on missing data is banned. 
* **Resolution**: When a raw query is empty, call the unified `render_empty_state` from `app/core/design_system/components/states.py` immediately below the card row, presenting a Vercel-style clean illustration and clear guide text.

---

## 5. Layout & Spacing Principles
* **Stretch Alignment**: Elements like vertical card dividers must use `align-self: stretch;` instead of hardcoded percentage heights, ensuring the 1px gray border stretches perfectly to card boundaries on any screen width.
* **Padding Harmony**: All card elements strictly share `padding: 0.85rem 1rem !important` top/bottom and left/right padding to maintain a single visual vertical anchor line across the dashboard.
* **No Layout Overlapping**: No absolute-positioned stacking of content is allowed; elements must sit in their own mathematically bounded columns.

---

## 6. Motion & Interaction
* **Animated Transition**: Smooth page tab and chart entrance reveals powered by spring physics (`stiffness: 100, damping: 20`).
* **Hover Micro-Interactions**: Hover highlights on ECharts timeline dots include a subtle outline (`borderColor: "#ffffff"`) and a glowing blur radius (`shadowBlur: 6`) to maintain dimensional depth against overlapping lines.

---

## 7. Anti-Patterns (Banned AI Tells)
* NO emojis or taglines.
* NO raw hex codes in components; colors must use semantic constants.
* NO em-dashes (`—` or `–`) in body text or headers.
* NO vertical space-between stretching in metrics cards (center grouping mandatory).
* NO sketchy hand-drawn SVGs or diagonal stripe backgrounds.
* NO "Jane Doe" fake placeholder data.
