# Product Quality Data Analysis System - Spacing & Color Polishing (Stage 2)

This document archives the Stage 2 Spacing, Margins, and Color Polishing specification for the Data Analysis Dashboard Manual pages (`data_analysis_manual_ko.md` & `data_analysis_manual_en.md`), as mandated by the 3-Stage Design Workflow in `.agents/GEMINI.md`.

## 1. Callout Banner Polishing (Introduction)
- **Container Styling**: Replaced the raw `<p>` block with a beautifully designed card with `border-left: 4px solid var(--primary-color)`.
- **Card Background**: Configured to match the theme-adaptable `var(--secondary-background-color)`.
- **Inner Padding**: Standardized at `16px 20px` (`var(--space-4) var(--space-5)`) with a subtle `1px` top/right/bottom border of `rgba(128,128,128,0.12)` to mimic Apple-like frosted-glass materiality and physical edge refraction.
- **Brand Accents**: The key platform name is highlighted using a bold, high-contrast label matching `var(--primary-color)`.

## 2. Spacing & Margin Calibration
- **Margin Bottom**: Set `margin-bottom: 2rem` after the introductory banner to let the hero element breathe, preventing cognitive clutter.
- **Section Headers**: Structured as clean, vertical stacks with standard bottom spacing. Avoided the clichéd "split-header" or floating top-right sub-text.
- **Line Heights**: Card description text (`.card-desc`) increased to `line-height: 1.45` to optimize textual legibility.

## 3. High-End Color Palette & Contrast
- **Removal of Hardcoded Colors**: Eradicated all hardcoded color hex values (e.g. `#ea580c`, `#16a34a`, `#94a3b8`) inside elements.
- **RGBA Soft Badges**: Configured compatibility badges using software-based Alpha transparency fills:
  - **IQM Plus Only / IQM Plus**: Green accent (`rgba(22, 163, 74, 0.12)`) with deep green border.
  - **Period Analysis**: Blue accent (`rgba(59, 130, 246, 0.12)`) with solid blue border.
  - **Break Point**: Purple accent (`rgba(168, 85, 247, 0.12)`) with deep purple border.
- **High Contrast Assurance**: Assured WCAG AA contrast (minimum 4.5:1 ratio) in both light and dark mode contexts by referencing semantic theme tokens (`var(--text-color)`, `var(--primary-color)`).

## 4. Visual Consistency Locks
- **Shape Consistency Lock**: All interactive card borders are locked to `var(--radius-md)` and accordion borders to `var(--radius-lg)` to match the primary application frame corner scales.
- **Theme Lock**: The page theme is locked to the parent application's global theme context, reacting dynamically to light/dark toggles without color inversion bugs.
