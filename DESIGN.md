---
name: Vigilant Guard
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#464555'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#777587'
  outline-variant: '#c7c4d8'
  surface-tint: '#4d44e3'
  primary: '#3525cd'
  on-primary: '#ffffff'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#c3c0ff'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#684000'
  on-tertiary: '#ffffff'
  tertiary-container: '#885500'
  on-tertiary-container: '#ffd4a4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '800'
    lineHeight: 48px
    letterSpacing: -0.025em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '800'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  title-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.06em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

This design system establishes an institutional yet approachable digital presence engineered specifically for college students seeking career opportunities. The brand personality balances unyielding institutional vigilance with empathetic guidance, de-escalating anxiety around deceptive employment schemes while projecting authoritative verification standards.

The visual style blends **Corporate / Modern** fintech precision with supportive academic utility. The interface eschews frivolous decorative trends in favor of disciplined structural hierarchy, instant scannability, high-contrast readability, and unequivocal status indication. Every visual decision prioritizes immediate clarity, psychological safety, and rapid cognitive triage of verification results.

## Colors

The palette is engineered around high functional contrast and unambiguous cognitive signaling:

- **Primary (`#4F46E5`):** Deep Indigo commands the core interface actions, system navigation, and structural active states, instilling institutional credibility without appearing sterile.
- **Secondary (`#10B981`):** Crisp Emerald Green signals verified entities, authentic job offers, safe operational metrics, and positive reassurance.
- **Tertiary (`#F59E0B`):** Amber Warning denotes unverified parameters, medium-risk clauses, incomplete corporate profiles, and prompts requiring student caution.
- **Critical / Alert (`#EF4444`):** Vivid Rose provides uncompromising visibility for detected fraudulent domains, blacklisted contacts, payment solicitation scams, and severe danger flags.
- **Neutral Stack:** Grounded by Dark Slate (`#0F172A`) for foundational titles and primary data points, balanced with Slate Subtext (`#334155` and `#64748B`). Surfaces rest upon clean Slate canvas tones (`#F8FAFC` and `#F1F5F9`) contrasting with pure white interactive containers (`#FFFFFF`). Border boundaries strictly utilize `#E2E8F0`.

## Typography

Typography relies uniformly on **Inter** to maximize structural legibility, vertical metric balance, and reliable multi-device rendering. 

- Large titles feature optical negative letter spacing (`-0.025em` to `-0.015em`) to ensure crisp header compactness across mobile viewports.
- Running body text utilizes open line-height ratios (`1.55` to `1.625`) to reduce visual fatigue during dense offer letter and verification document reviews.
- Form inputs, tabular scores, validation flags, and risk indicators enforce `label-md` and `label-caps` with slight positive tracking for instantaneous readability under high stress.

## Layout & Spacing

The structural layout operates on a standard **8px base grid** with a maximum content container width of `1280px`. 

- **Desktop (1024px+):** 12-column responsive fluid grid, `1.5rem` (`24px`) gutters, and `2rem` (`32px`) margins. Two- and three-column verification dashboards allow side-by-side comparison between submitted text/documents and risk reports.
- **Tablet (768px - 1023px):** 8-column layout, `1rem` (`16px`) gutters, stacking analysis sidebars below core inspection inputs.
- **Mobile (<768px):** 4-column layout, strict `1rem` outer screen gutters and margins. Full-width touch targets allow rapid document photo submissions and one-tap risk lookups.
- Component padding strictly conforms to `space-md` (`16px`) for standard cards and `space-lg` (`24px`) for elevated inspection dialogs.

## Elevation & Depth

Visual hierarchy is maintained via crisp **tonal layering combined with ultra-subtle, low-opacity neutral shadows**. Heavy, blurry blurs and colored drop shadows are avoided to uphold institutional clarity.

- **Level 0 (Base Canvas):** `#F8FAFC` foundation. Neutral, non-glare canvas.
- **Level 1 (Card & Containers):** `#FFFFFF` surface bounded by a crisp `1px solid #E2E8F0` hairline border and ambient elevation: `0 1px 3px 0 rgba(15, 23, 42, 0.05), 0 1px 2px -1px rgba(15, 23, 42, 0.05)`.
- **Level 2 (Hover States & Dropdowns):** `#FFFFFF` with expanded ambient lift: `0 4px 6px -1px rgba(15, 23, 42, 0.07), 0 2px 4px -2px rgba(15, 23, 42, 0.05)`.
- **Level 3 (Modals & Urgent Scam Alerts):** Pure white container encased in a reinforced border, cast with assertive separation: `0 20px 25px -5px rgba(15, 23, 42, 0.1), 0 8px 10px -6px rgba(15, 23, 42, 0.05)`.
- **Status Reinforcement:** Risk containers (Safe, Warning, Critical Alert) use 1px perimeter tints coupled with low-saturation interior surface washes (`#ECFDF5` for Safe, `#FFFBEB` for Warning, `#FEF2F2` for Scam Alert) rather than heavy drop shadows.

## Shapes

The design system maintains a **Rounded (Level 2)** shape standard:

- **Core Elements (Inputs, Buttons, Badges):** Standard elements use `0.5rem` (`8px`) for compact tactile reliability.
- **Content Cards & Verification Panels:** Primary surfaces enforce `1rem` (`16px`, matching `rounded-lg`) corner radii to provide approachable framing while remaining neat and structurally grounded.
- **Inspection Drawers & Hero Callouts:** Major breakout areas implement `1.5rem` (`24px`, matching `rounded-xl`).
- **Safety Shields & Status Pills:** Metric indicators, risk chips, and safety score indicators use full pill curvature (`9999px`) to create clear semantic differentiation against rectangular form controls.

## Components

### Buttons
- **Primary:** Background `#4F46E5`, text `#FFFFFF`, border-radius `0.5rem`, padding `0.75rem 1.5rem`. Hover `#4338CA`, active `#3730A3`. Focus ring: `2px solid #FFFFFF` offset with `2px solid #4F46E5`.
- **Secondary / Neutral:** Background `#FFFFFF`, text `#0F172A`, border `1px solid #E2E8F0`, hover `#F8FAFC`.
- **Critical Action:** Background `#EF4444`, text `#FFFFFF`, hover `#DC2626`. Used strictly for reporting scams and triggering blacklist submissions.

### Cards & Verification Surfaces
- Constructed on `#FFFFFF` with `1rem` (`16px`) corner radius, surrounded by a `1px solid #E2E8F0` border.
- Cards maintain interior padding of `1.5rem` (`24px`).
- Header areas host an authoritative icon alongside clear metadata labels.

### Badges & Status Chips
- Height `24px` to `28px`, pill radius (`9999px`), horizontal padding `0.75rem`, font `label-caps`.
- **Safe:** Surface `#ECFDF5`, text `#065F46`, border `1px solid #A7F3D0`.
- **Suspicious:** Surface `#FFFBEB`, text `#92400E`, border `1px solid #FDE68A`.
- **Scam Alert:** Surface `#FEF2F2`, text `#991B1B`, border `1px solid #FECACA`.

### Input Fields & Offer Analyzers
- Background `#FFFFFF`, border `1px solid #CBD5E1`, text `#0F172A`, radius `0.5rem`.
- Padding `0.75rem 1rem`. Focus state triggers border `#4F46E5` and a `3px` focus ring in `rgba(79, 70, 229, 0.15)`.
- Includes high-contrast placeholder styling in `#94A3B8`. Error inputs transition to border `#EF4444`.

### Lists & Audit Items
- Divided using clean hairline separators (`1px solid #F1F5F9`).
- Each row contains a leading shield status indicator, a structured title/meta block, and a trailing verification action.

### Checkboxes & Radios
- Size `18px x 18px`, radius `4px` (checkbox) or circular (radio), border `2px solid #94A3B8`.
- Checked state transitions immediately to `#4F46E5` background with a crisp white glyph.

### Specialized Safety Components
- **Trust Score Shield:** An elevated summary widget displaying a composite safety rating (0–100), bounded by a dynamic status-colored ring (`#10B981`, `#F59E0B`, or `#EF4444`).
- **Red Flag Callout Banner:** A prominent notice block with `#FEF2F2` background, `1px solid #F87171` border, `16px` radius, and bulleted analysis exposing known scam patterns (e.g., registration fee demands, unofficial messaging channels).