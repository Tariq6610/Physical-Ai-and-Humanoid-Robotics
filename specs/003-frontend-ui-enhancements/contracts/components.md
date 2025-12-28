# Component Contracts

**Feature**: 003-frontend-ui-enhancements
**Date**: 2025-12-27

## Component Interfaces

### Hero Component

**File**: `docs/src/components/Hero/index.tsx`

**Purpose**: Display interactive landing page hero section with animations

**Props**: None (uses Docusaurus `useDocusaurusContext`)

**State**:
- `isVisible`: boolean - Controls fade-in animation trigger

**Renders**:
- Animated gradient background with 3 floating orbs
- Site title with gradient text effect
- Tagline
- 2 CTA buttons (Start Learning, View on GitHub)
- 4 feature cards with icons

**Styling**: `Hero/styles.module.css` (CSS Modules)

**Animations**: fadeIn, slideUp, slideDown, float, pulse

**Responsive Behavior**:
- Mobile (< 768px): Title 2rem, stacked buttons, 1-column cards
- Desktop (>= 768px): Title 3.5rem, inline buttons, 4-column grid

---

### EnhancedChatbot Component

**File**: `docs/src/components/ChatbotWidget/EnhancedChatbot.tsx`

**Purpose**: Floating AI chatbot with ChatKit integration

**Props**: None (self-contained)

**State**:
- `mounted`: boolean - Client-side render guard
- `isOpen`: boolean - Chat window visibility
- `isMinimized`: boolean - Minimized state
- `hasNewMessage`: boolean - Notification indicator

**ChatKit Config**:
```typescript
{
  api: { getClientSecret: () => Promise<string> },
  theme: { colorScheme, radius, color },
  header: { enabled, title, subtitle },
  history: { enabled, showDelete, showRename },
  startScreen: { greeting, prompts },
  composer: { placeholder },
  threadItemActions: { feedback, retry }
}
```

**Renders**:
- Floating Action Button (FAB) with pulse animation
- Chat container with header, body, footer
- ChatKit component (when control available)
- Loading state (when initializing)

**Styling**: `ChatbotWidget/EnhancedChatbot.module.css`

**Animations**: slideIn, pulse, bounce, badgePop

**Responsive Behavior**:
- Mobile (< 480px): Full-screen chat
- Tablet/Desktop: Fixed 420x680px window

---

### ReadingProgress Component

**File**: `docs/src/components/ReadingProgress/index.tsx`

**Purpose**: Display reading progress bar at top of page

**Props**: None

**State**:
- `progress`: number (0-100) - Current scroll percentage

**Behavior**:
- Listens to scroll events (passive listener)
- Calculates: `(scrollTop / totalHeight) * 100`
- Updates progress bar width

**Styling**: `ReadingProgress/styles.module.css`

**Performance**:
- Passive scroll listener (non-blocking)
- GPU-accelerated width transition
- Debounced updates

**Responsive Behavior**:
- All viewports: Fixed at top, 3px height, full width

---

### ScrollToTop Component

**File**: `docs/src/components/ScrollToTop/index.tsx`

**Purpose**: Quick navigation back to page top

**Props**: None

**State**:
- `isVisible`: boolean - Shows when scrollY > 300px

**Behavior**:
- Appears when user scrolls down 300px
- Smooth scroll to top on click
- Positioned to avoid chatbot overlap

**Styling**: Inline CSS (uses global `.scroll-to-top` class from custom.css)

**Animations**: Fade in/out on visibility change

**Responsive Behavior**:
- Mobile: Position adjusted relative to chatbot
- Desktop: Fixed bottom-right, above chatbot

---

### Homepage Component

**File**: `docs/src/pages/index.tsx`

**Purpose**: Custom landing page at root URL

**Props**: Standard Docusaurus page props

**Renders**:
- Layout wrapper with SEO metadata
- Hero component
- Main content area (for future sections)

**Styling**: `pages/index.module.css`

**SEO**:
- Title: Site title from config
- Description: Full feature description
- Keywords: Robotics, AI, Physical AI, etc.

**Responsive Behavior**:
- Inherits from Hero component

---

## Design System Contract

### CSS Custom Properties

**File**: `docs/src/css/custom.css`

**Structure**:
```css
:root {
  /* Colors */
  --ifm-color-primary: #2e7ddb;
  --ifm-color-primary-{dark|darker|darkest|light|lighter|lightest}
  --ifm-color-accent: #25c2a0;
  --ifm-color-{success|info|warning|danger}

  /* Typography */
  --ifm-font-family-base: 'Inter', ...;
  --ifm-font-family-monospace: 'JetBrains Mono', ...;
  --ifm-line-height-base: 1.65;

  /* Spacing */
  --ifm-navbar-height: 4rem;

  /* Effects */
  --ifm-global-shadow-{lw|md|tl}
  --ifm-global-radius: 0.5rem;
  --ifm-transition-{fast|slow}

  /* Gradients */
  --gradient-primary: linear-gradient(135deg, #2e7ddb 0%, #25c2a0 100%);
  --gradient-primary-light: linear-gradient(..., 0.1 alpha);
}

[data-theme='dark'] {
  /* Override for dark mode */
  --ifm-color-primary: #4d90e1;
  --ifm-background-color: #0d1117;
  --ifm-background-surface-color: #161b22;
  ...
}
```

**Usage Pattern**:
- Components use `var(--variable-name)` in styles
- Ensures consistency across site
- Automatic dark mode switching via data-theme attribute
- Smooth transitions defined globally

---

## Technical Constraints

### Bundle Size
- Target: < 50KB increase from current bundle
- Achieved by: CSS-only animations, no new libraries, minimal components

### Build Time
- Target: < 60 seconds for full build
- Not impacted: Static CSS and React components don't increase build time significantly

### Browser Compatibility
- Target: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- Features used: CSS Grid, Flexbox, CSS custom properties, backdrop-filter
- Graceful degradation for older browsers (no backdrop-filter, simpler animations)

### Accessibility
- WCAG AA contrast ratios: All text combinations tested and verified
- Keyboard navigation: All interactive elements focusable
- Screen reader: Proper ARIA labels on buttons/links
- Motion preferences: Will respect prefers-reduced-motion (future enhancement)

---

## Implementation Notes

### File Organization
- Each major component in own directory with index.tsx + styles.module.css
- Global styles in single custom.css (easier to maintain than split files)
- CSS Modules for component-specific styles (scoped, no conflicts)

### Development Workflow
1. Update custom.css with design system variables
2. Create component directories
3. Implement components using design tokens
4. Test in dev server (npm start)
5. Verify build (npm run build)
6. Test responsive behavior (DevTools)
7. Validate accessibility (browser tools)

### Testing Strategy
- **Build Validation**: Automated via `npm run build` (catches broken links, TypeScript errors)
- **Visual Regression**: Manual comparison before/after
- **Responsive Testing**: DevTools viewport simulation (320px, 768px, 1024px, 1440px)
- **Cross-browser**: Manual testing on Chrome, Firefox, Safari
- **Accessibility**: WAVE tool, Lighthouse audit

---

## Reference Implementation

Complete working implementation exists on branch `feature/ui-enhancements` (commit d7f3720) and can be consulted for implementation details during development on this SpecKit branch.
