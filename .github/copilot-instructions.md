# Vision AI Lecture repository instructions

Before editing this repository, read:

- `PROJECT_GUIDE.md`
- `HTML_DESIGN_RULES.md`
- `AGENTS.md`

This is a beginner-oriented Vision AI lecture site, not a generic web application.

Follow these rules:

- One core teaching message per slide.
- Prefer visual explanation over long prose.
- Make Input → Process → Output relationships visually obvious.
- Use HTML/SVG for precise technical relationships and tensor/math diagrams.
- Use repository image assets for real-world visual examples.
- Keep a professional white presentation style with restrained accent colors.
- Avoid dashboard-like card grids, excessive gradients, shadows, pills, and decorative UI.
- Do not solve overflow by shrinking an entire slide until text becomes hard to read.
- Reuse `docs/slide.css` and existing components before adding near-duplicate CSS.
- Do not add external CDNs.
- Verify tensor shapes, formulas, labels, and numerical examples before presenting them.
- Do not present generated illustrations as measured experimental results.
- Check adjacent slides so terminology, layout, and narrative flow remain consistent.
- After editing, verify HTML/CSS syntax, asset paths, slide numbering, overflow, clipping,
  overlap, and the impact of shared CSS changes on `intro.html`, `ai_basics.html`,
  and `vision_ai.html`.

When an old TODO conflicts with `PROJECT_GUIDE.md` or the user's latest request,
follow the newer instruction.
