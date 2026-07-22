# Product Quality Data Analysis System - Manual Layout & Structure (Stage 1)

This document archives the Stage 1 Layout and Structuring specification for the Data Analysis Dashboard Manual pages (`data_analysis_manual_ko.md` & `data_analysis_manual_en.md`), as mandated by the 3-Stage Design Workflow in `.agents/GEMINI.md`.

## 1. Information Architecture & Page Hierarchy
The user manual is structured as a single-page, high-density reference sheet. It contains three logical blocks:
1. **Introductory Callout Banner**: Sets the system's business purpose and establishes brand context.
2. **Section 1 (Dashboard Guide)**: High-end SVG Visual Guide with structured annotations.
3. **Section 2 (Compatibility Matrix)**: High-density interactive accordion of tab features and their compatibility across modes.

## 2. Layout Grid & Spacing System
All spacing utilizes the CSS custom variables defined in `manual.css` to maintain theme consistency:
- **Outer Page Padding**: Maintained by the parent container (`.premium-manual-container`).
- **Section Spacing**: Separated by clean horizontal dividers with vertical margins of `1.5rem` (`var(--space-6)`).
- **Accordion Wrapper Spacing**: Bottom margin of `1.0rem` (`var(--space-4)`) on each `<details>` container to create a balanced rhythm.
- **Card Grid Spacing**: Utilizes `.metrics-grid` with `repeat(auto-fit, minmax(280px, 1fr))` and a gap of `12px` (`var(--space-3)`) for high-density, balanced grid flow on desktop, collapsing cleanly to 1-column on mobile.
- **Card Spacing**: Padding of `12px` (`var(--space-3)`) inside each `.metric-card-spec` card.

## 3. Design Token Mapping
To ensure light/dark mode adaptability and brand integrity, we lock design tokens to the following system variables:

| Visual Element | Design Token | Fallback Value (Light / Dark) | Purpose |
| :--- | :--- | :--- | :--- |
| **Page Text** | `var(--text-color)` | `#1f2937` / `#f3f4f6` | Default typography reading ink. |
| **Accordion Frame** | `var(--secondary-background-color)` | `#f9fafb` / `#1e293b` | Accentuated border frame background. |
| **Grid Card Body** | `var(--background-color)` | `#ffffff` / `#0f172a` | Solid card fill for visual hierarchy. |
| **Interactive Badges** | OKLCH / RGB Transparencies | Green / Blue / Purple 10% Alpha | Soft pill markers for system status. |
| **Outer Border** | `1px solid rgba(128,128,128,0.2)` | Gray alpha | Section boundaries and frame borders. |
| **Inner Border** | `1px solid rgba(128,128,128,0.15)`| Gray alpha | Card borders and card separators. |
| **Corner Radius** | `var(--radius-lg)` | `8px` - `12px` | Modern, consistent rounding. |

## 4. Mobile Layout Collapse Strategy
- On viewports `< 768px` (mobile), the grid automatically collapses to a single-column layout via native media-query flex/grid properties, setting card width to `w-full`.
- Text sizes inside cards downscale by `5%` for comfortable reading on small screens, which is automatically handled by the responsive typography engine in `manual.css`.
