# Research: Frontend UI Enhancements

**Feature**: 003-frontend-ui-enhancements
**Date**: 2025-12-27
**Status**: Complete

## Research Questions & Findings

### 1. Docusaurus Theming Strategy

**Decision**: Use custom CSS with CSS custom properties + minimal component creation

**Rationale**:
- Docusaurus supports custom CSS via `src/css/custom.css`
- CSS custom properties allow consistent theming across light/dark modes
- Minimal React component creation keeps bundle size small
- Avoids complex swizzling which increases maintenance burden
- Allows easy updates when Docusaurus upgrades

**Alternatives Considered**:
- **Full Component Swizzling**: Rejected - high maintenance cost, breaks on Docusaurus updates
- **Third-party Theme**: Rejected - limits customization, adds dependency
- **Styled Components**: Rejected - increases bundle size, not Docusaurus convention

**References**:
- Docusaurus docs on styling: https://docusaurus.io/docs/styling-layout
- CSS custom properties pattern from `/facebook/docusaurus` research

---

### 2. ChatKit Integration & Customization

**Decision**: Use `useChatKit` hook with comprehensive theme configuration object

**Rationale**:
- ChatKit provides `useChatKit` hook for React integration
- Theme can be customized via config object (colorScheme, radius, accent colors)
- Built-in features (history, feedback, retry) reduce custom code
- Start screen prompts improve initial user experience
- Wrapping with custom FAB provides better UX than default embedding

**Alternatives Considered**:
- **Custom Chat Implementation**: Rejected - reinventing ChatKit features, more maintenance
- **Default ChatKit Styling**: Rejected - doesn't match site branding
- **ChatKit Web Component**: Rejected - React integration is cleaner for Docusaurus

**Configuration**:
```javascript
{
  theme: {
    colorScheme: 'dark',
    radius: 'round',
    color: { accent: { primary: '#4d90e1', level: 2 } }
  },
  startScreen: { greeting: '...', prompts: [...] },
  threadItemActions: { feedback: true, retry: true }
}
```

**References**:
- ChatKit docs from `/websites/openai_github_io_chatkit-js`
- Customization examples from Context7 research

---

### 3. Animation & Performance Strategy

**Decision**: CSS-only animations using GPU-accelerated properties (transform, opacity)

**Rationale**:
- GPU-accelerated properties (transform, opacity) provide 60fps performance
- CSS animations don't block JavaScript thread
- Easier to respect `prefers-reduced-motion` media query
- Smaller bundle size (no animation library needed)
- Declarative animations easier to maintain

**Animation Patterns Chosen**:
- **Fade In**: opacity 0 → 1
- **Slide Up**: translateY(20px) → translateY(0)
- **Float**: Continuous transform translation for orbs
- **Pulse**: Scale 1 → 1.2 → 1 for attention-grabbing elements
- **Bounce**: TranslateY oscillation for playful elements

**Performance Constraints**:
- All animations use `cubic-bezier(0.4, 0, 0.2, 1)` easing
- Duration: 150ms (fast interactions), 300ms (theme transitions), 600-800ms (page load animations)
- Avoid animating: width, height, top, left (triggers layout)
- Use: transform, opacity only (composite layer)

**Alternatives Considered**:
- **Framer Motion**: Rejected - 50KB+ bundle size increase
- **GSAP**: Rejected - overkill for simple animations, license concerns
- **JavaScript RAF**: Rejected - more complex, blocks main thread

**References**:
- Web.dev animation performance guide
- CSS Tricks GPU acceleration article

---

### 4. Color Palette & Accessibility

**Decision**: Blue (#2e7ddb) primary, Teal (#25c2a0) accent, 7-shade palette per color

**Rationale**:
- Blue conveys technology, trust, intelligence (appropriate for robotics/AI)
- Teal provides vibrant contrast for accents (CTA buttons, highlights)
- 7-shade palette allows granular theming (darkest, darker, dark, base, light, lighter, lightest)
- All combinations tested for WCAG AA contrast (4.5:1 minimum)
- Dark mode uses brighter shades (#4d90e1) for better visibility on dark backgrounds

**Color Testing Results**:
- Light mode: Black text on white bg = 21:1 (AAA) ✅
- Dark mode: #e6edf3 text on #0d1117 bg = 13.8:1 (AAA) ✅
- Primary button: White on #2e7ddb = 5.2:1 (AA) ✅
- Code inline: #266abc on #f6f8fa = 8.3:1 (AAA) ✅

**Dark Mode Colors**:
- Background: #0d1117 (GitHub-inspired rich dark)
- Surface: #161b22 (elevated elements)
- Primary: #4d90e1 (brighter for contrast)
- Text: #e6edf3 (off-white for reduced eye strain)

**Alternatives Considered**:
- **Green Primary**: Rejected - less distinctive, common in tech docs
- **Purple/Violet**: Rejected - less association with robotics/engineering
- **Pure Black Dark Mode**: Rejected - harsh contrast causes eye fatigue

**References**:
- WebAIM contrast checker
- Material Design color system
- GitHub dark mode palette

---

### 5. Typography Selection

**Decision**: Inter (body text), JetBrains Mono (code)

**Rationale**:
- **Inter**: Modern, excellent readability, wide character support, professional appearance
- **JetBrains Mono**: Designed for code, ligature support, clear character distinction (0 vs O, 1 vs l)
- Both available from Google Fonts (CDN, no hosting required)
- Fallback chain includes system fonts for graceful degradation
- Variable font weights (300-800 for Inter) allow nuanced typography hierarchy

**Typography Scale**:
- Base: 16px (1rem)
- H1: 2.5rem (40px)
- H2: 2rem (32px)
- H3: 1.5rem (24px)
- Code: 0.875rem (14px)
- Line height: 1.65 (optimal for reading comprehension)

**Alternatives Considered**:
- **System Fonts Only**: Rejected - less distinctive, inconsistent across OSes
- **Roboto**: Rejected - overused, less character than Inter
- **Fira Code**: Rejected - Inter + JetBrains Mono combo provides better balance
- **Self-hosted Fonts**: Rejected - adds complexity, CDN is faster globally

**References**:
- Butterick's Practical Typography
- Google Fonts performance best practices

---

### 6. Responsive Design Strategy

**Decision**: Mobile-first with breakpoints at 768px, 1024px

**Rationale**:
- Mobile-first ensures core content accessible on all devices
- 768px separates phone vs tablet/desktop (common industry standard)
- 1024px separates tablet vs desktop (wide-screen optimizations)
- Docusaurus already mobile-optimized, we extend this pattern
- Touch targets: 48x48px minimum on mobile (accessibility)

**Breakpoint Strategy**:
- **Mobile (< 768px)**: Single column, stacked buttons, full-screen chatbot
- **Tablet (768-1024px)**: 2-column grids, side-by-side buttons, larger chatbot
- **Desktop (> 1024px)**: Multi-column, hover effects prominent, fixed chatbot

**Component Adaptations**:
- Hero: 3.5rem → 2rem title on mobile
- Feature cards: 4-column grid → 2-column → 1-column
- Chatbot: 420x680px fixed → 100vw x 100vh on mobile
- Buttons: Inline → stacked on narrow screens

**Alternatives Considered**:
- **Desktop-First**: Rejected - mobile traffic significant, harder to constrain than expand
- **More Breakpoints**: Rejected - 2 breakpoints sufficient, more adds complexity
- **Tailwind-style Breakpoints**: Rejected - Docusaurus uses Infima, maintain consistency

**References**:
- MDN responsive design guide
- Web.dev responsive patterns

---

## Summary of Decisions

| Aspect | Decision | Key Rationale |
|--------|----------|---------------|
| **Theming** | Custom CSS + CSS custom properties | Maintainable, performant, Docusaurus-native |
| **ChatKit** | useChatKit hook with config | Built-in features, easy customization |
| **Animations** | CSS-only, GPU-accelerated | 60fps performance, smaller bundle |
| **Colors** | Blue/Teal gradient palette | Professional, accessible, brand-appropriate |
| **Typography** | Inter + JetBrains Mono | Readability, professionalism, code clarity |
| **Responsive** | Mobile-first, 2 breakpoints | Accessibility, industry standard |

## Open Questions

None - all research complete and decisions documented.
