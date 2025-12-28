# Tasks: Frontend UI Enhancements

**Feature Branch**: `003-frontend-ui-enhancements`
**Input**: Design documents from `/specs/003-frontend-ui-enhancements/`
**Prerequisites**: plan.md, spec.md, research.md, contracts/components.md, quickstart.md

**Tests**: This feature follows visual testing strategy (no programmatic tests) as documented in plan.md constitution check. Testing consists of build validation + manual visual/responsive testing + Lighthouse audits.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic file structure

- [X] T001 Verify Docusaurus installation and dependencies in docs/package.json
- [X] T002 [P] Create component directory structure: docs/src/components/Hero/
- [X] T003 [P] Create component directory structure: docs/src/components/ChatbotWidget/
- [X] T004 [P] Create component directory structure: docs/src/components/ReadingProgress/
- [X] T005 [P] Create component directory structure: docs/src/components/ScrollToTop/
- [X] T006 [P] Create pages directory structure: docs/src/pages/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Design system and global styling that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Import Google Fonts (Inter, JetBrains Mono) in docs/docusaurus.config.js or custom.css
- [X] T008 Create CSS custom properties for color palette in docs/src/css/custom.css (:root section)
- [X] T009 Create CSS custom properties for dark mode colors in docs/src/css/custom.css ([data-theme='dark'] section)
- [X] T010 Define typography system (fonts, sizes, line height) in docs/src/css/custom.css
- [X] T011 Define spacing, shadows, border radius, transitions in docs/src/css/custom.css
- [X] T012 Define gradient definitions (--gradient-primary, --gradient-primary-light) in docs/src/css/custom.css
- [X] T013 Create animation keyframes (@keyframes fadeIn, slideUp, slideDown, float, pulse, bounce) in docs/src/css/custom.css
- [X] T014 Update Docusaurus config for dark mode support in docs/docusaurus.config.js (colorMode.respectPrefersColorScheme: true)

**Checkpoint**: Design system ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - First-Time Visitor Engagement (Priority: P1) 🎯 MVP

**Goal**: Create an interactive, professional landing page with hero section that engages visitors and provides clear calls-to-action

**Independent Test**: Navigate to http://localhost:3000/, verify hero section displays with animated background, feature cards show all 4 key topics, and both CTA buttons navigate correctly

### Implementation for User Story 1

- [X] T015 [P] [US1] Create Hero component structure: docs/src/components/Hero/index.tsx (empty component)
- [X] T016 [P] [US1] Create Hero component styles: docs/src/components/Hero/styles.module.css (empty stylesheet)
- [X] T017 [US1] Implement animated gradient background with 3 floating orbs in docs/src/components/Hero/styles.module.css
- [X] T018 [US1] Implement hero title with gradient text effect in docs/src/components/Hero/index.tsx
- [X] T019 [US1] Add tagline and 2 CTA buttons (Start Learning, View on GitHub) in docs/src/components/Hero/index.tsx
- [X] T020 [US1] Create 4 feature cards with icons and descriptions in docs/src/components/Hero/index.tsx
- [X] T021 [US1] Add button hover effects (scale, shadow, color change) in docs/src/components/Hero/styles.module.css
- [X] T022 [US1] Add card hover effects (lift animation, shadow increase) in docs/src/components/Hero/styles.module.css
- [X] T023 [US1] Implement fade-in animations for hero elements in docs/src/components/Hero/styles.module.css
- [X] T024 [US1] Add responsive breakpoints (mobile: 2rem title, desktop: 3.5rem) in docs/src/components/Hero/styles.module.css
- [X] T025 [US1] Create custom homepage: docs/src/pages/index.tsx with Layout wrapper
- [X] T026 [US1] Add SEO metadata (title, description, keywords) to docs/src/pages/index.tsx
- [X] T027 [US1] Import and render Hero component in docs/src/pages/index.tsx
- [X] T028 [US1] Create homepage styles: docs/src/pages/index.module.css
- [X] T029 [US1] Update docs/docs/intro.md slug from "/" to "/intro" to free up root URL for homepage

**Checkpoint**: At this point, User Story 1 should be fully functional - homepage displays with interactive hero section and works on all viewport sizes

---

## Phase 4: User Story 2 - Documentation Reader Comfort (Priority: P1)

**Goal**: Enable seamless theme switching between light/dark modes with automatic system preference detection

**Independent Test**: Open site with system dark mode enabled, verify automatic dark theme. Toggle theme manually and verify smooth transition within 300ms.

### Implementation for User Story 2

- [X] T030 [P] [US2] Style navbar with backdrop blur and semi-transparent background in docs/src/css/custom.css
- [X] T031 [P] [US2] Enhance navbar theme toggle button styling in docs/src/css/custom.css
- [X] T032 [US2] Add smooth color transition for all elements (300ms) in docs/src/css/custom.css
- [X] T033 [US2] Verify all text maintains WCAG AA contrast ratios (4.5:1) in both themes in docs/src/css/custom.css
- [X] T034 [US2] Test code block syntax highlighting in both light and dark modes in docs/src/css/custom.css
- [X] T035 [US2] Verify sidebar styling with active page gradient highlight in docs/src/css/custom.css
- [X] T036 [US2] Test admonition color-coding (note=blue, tip=green, warning=orange, danger=red) in both modes in docs/src/css/custom.css

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - hero section + seamless theme switching

---

## Phase 5: User Story 3 - Enhanced Reading Experience (Priority: P1)

**Goal**: Improve documentation readability with professional typography, reading progress indicator, and quick navigation

**Independent Test**: Open any documentation page, scroll through content, verify typography improvements, progress bar updates, and scroll-to-top button appears after scrolling

### Implementation for User Story 3

- [X] T037 [P] [US3] Apply Inter font to body text with line height 1.65 in docs/src/css/custom.css
- [X] T038 [P] [US3] Apply JetBrains Mono to code elements in docs/src/css/custom.css
- [X] T039 [P] [US3] Improve heading spacing and visual hierarchy in docs/src/css/custom.css
- [X] T040 [P] [US3] Style tables with gradient headers and row hover effects in docs/src/css/custom.css
- [X] T041 [P] [US3] Style blockquotes with gradient background and left border in docs/src/css/custom.css
- [X] T042 [P] [US3] Add external link arrow indicators in docs/src/css/custom.css
- [X] T043 [P] [US3] Create ReadingProgress component structure: docs/src/components/ReadingProgress/index.tsx
- [X] T044 [P] [US3] Create ReadingProgress styles: docs/src/components/ReadingProgress/styles.module.css
- [X] T045 [US3] Implement passive scroll listener in docs/src/components/ReadingProgress/index.tsx
- [X] T046 [US3] Calculate scroll percentage (scrollTop / totalHeight * 100) in docs/src/components/ReadingProgress/index.tsx
- [X] T047 [US3] Update progress bar width with GPU-accelerated transition in docs/src/components/ReadingProgress/styles.module.css
- [X] T048 [P] [US3] Create ScrollToTop component: docs/src/components/ScrollToTop/index.tsx
- [X] T049 [US3] Implement visibility threshold (show when scrollY > 300px) in docs/src/components/ScrollToTop/index.tsx
- [X] T050 [US3] Add smooth scroll to top behavior in docs/src/components/ScrollToTop/index.tsx
- [X] T051 [US3] Position button to avoid chatbot overlap in docs/src/components/ScrollToTop/index.tsx
- [X] T052 [US3] Integrate ReadingProgress into global layout via docs/src/theme/Root.tsx
- [X] T053 [US3] Integrate ScrollToTop into global layout via docs/src/theme/Root.tsx

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - hero + theme switching + enhanced reading experience

---

## Phase 6: User Story 4 - AI Assistant Accessibility (Priority: P2)

**Goal**: Provide easy access to AI chatbot from any page with enhanced ChatKit widget featuring custom theming

**Independent Test**: Click the chatbot FAB on any page, verify chat window opens, send test message, and verify minimize/maximize functionality works

### Implementation for User Story 4

- [X] T054 [P] [US4] Verify @openai/chatkit-react is installed in docs/package.json
- [X] T055 [P] [US4] Create EnhancedChatbot component structure: docs/src/components/ChatbotWidget/EnhancedChatbot.tsx
- [X] T056 [P] [US4] Create EnhancedChatbot styles: docs/src/components/ChatbotWidget/EnhancedChatbot.module.css
- [X] T057 [US4] Implement client-side render guard (mounted state) in docs/src/components/ChatbotWidget/EnhancedChatbot.tsx
- [X] T058 [US4] Create ChatKit configuration object (theme, colors, radius) in docs/src/components/ChatbotWidget/EnhancedChatbot.tsx
- [X] T059 [US4] Configure start screen with greeting and 4 quick action prompts in docs/src/components/ChatbotWidget/EnhancedChatbot.tsx
- [X] T060 [US4] Enable conversation history, feedback, and retry features in docs/src/components/ChatbotWidget/EnhancedChatbot.tsx
- [X] T061 [US4] Implement Floating Action Button (FAB) with pulse animation in docs/src/components/ChatbotWidget/EnhancedChatbot.module.css
- [X] T062 [US4] Add FAB tooltip on hover in docs/src/components/ChatbotWidget/EnhancedChatbot.tsx
- [X] T063 [US4] Implement chat window structure (header, body, footer) in docs/src/components/ChatbotWidget/EnhancedChatbot.tsx
- [X] T064 [US4] Add minimize/maximize functionality in docs/src/components/ChatbotWidget/EnhancedChatbot.tsx
- [X] T065 [US4] Implement close button in docs/src/components/ChatbotWidget/EnhancedChatbot.tsx
- [X] T066 [US4] Add slide-in animation for chat window in docs/src/components/ChatbotWidget/EnhancedChatbot.module.css
- [X] T067 [US4] Style chat container with shadows and borders in docs/src/components/ChatbotWidget/EnhancedChatbot.module.css
- [X] T068 [US4] Create main export: docs/src/components/ChatbotWidget.tsx
- [X] T069 [US4] Integrate EnhancedChatbot into global layout via docs/src/theme/Root.tsx

**Checkpoint**: At this point, User Stories 1-4 should all work independently - hero + theme + reading + chatbot

---

## Phase 7: User Story 5 - Mobile Documentation Access (Priority: P2)

**Goal**: Ensure all UI elements adapt properly to mobile/tablet viewports without loss of functionality

**Independent Test**: View site on mobile viewport (320px-768px width), verify all components stack properly and remain functional

### Implementation for User Story 5

- [X] T070 [P] [US5] Add mobile breakpoint (< 768px) for hero section in docs/src/components/Hero/styles.module.css
- [X] T071 [P] [US5] Stack CTA buttons vertically on mobile in docs/src/components/Hero/styles.module.css
- [X] T072 [P] [US5] Convert feature cards to single column on mobile in docs/src/components/Hero/styles.module.css
- [X] T073 [P] [US5] Add mobile breakpoint for chatbot (< 480px full-screen) in docs/src/components/ChatbotWidget/EnhancedChatbot.module.css
- [X] T074 [P] [US5] Ensure reading progress bar is full-width on mobile in docs/src/components/ReadingProgress/styles.module.css
- [X] T075 [P] [US5] Adjust scroll-to-top button position on mobile in docs/src/components/ScrollToTop/index.tsx
- [X] T076 [US5] Test navbar responsiveness on mobile in docs/src/css/custom.css
- [X] T077 [US5] Test sidebar responsiveness on mobile in docs/src/css/custom.css
- [X] T078 [US5] Verify touch targets are 48x48px minimum on all interactive elements
- [X] T079 [US5] Test site at 320px, 375px, 768px viewports using browser DevTools

**Checkpoint**: All user stories 1-5 should now work on all viewport sizes (mobile, tablet, desktop)

---

## Phase 8: User Story 6 - Enhanced Code Learning (Priority: P3)

**Goal**: Improve code block presentation with enhanced styling and easy copy functionality

**Independent Test**: View pages with code blocks, verify enhanced styling with shadows/borders, hover effects work, and copy button is prominent

### Implementation for User Story 6

- [X] T080 [P] [US6] Enhance code block styling (shadows, borders, rounded corners) in docs/src/css/custom.css
- [X] T081 [P] [US6] Style code block copy button with prominent appearance in docs/src/css/custom.css
- [X] T082 [P] [US6] Add copy button hover effects (highlight, scale) in docs/src/css/custom.css
- [X] T083 [P] [US6] Style inline code snippets with colored background in docs/src/css/custom.css
- [X] T084 [P] [US6] Add language badge styling for code blocks in docs/src/css/custom.css
- [X] T085 [US6] Verify code block styling in both light and dark modes
- [X] T086 [US6] Test copy functionality on various code blocks

**Checkpoint**: All user stories 1-6 complete - full feature implementation done

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, optimization, and quality assurance

- [X] T087 [P] Run npm run build from docs/ directory to validate build
- [X] T088 [P] Test responsive layouts at 320px, 768px, 1024px, 1440px viewports
- [X] T089 [P] Verify theme switching works correctly in all components
- [ ] T090 Test ChatKit integration (session endpoint, messages, history)
- [ ] T091 Verify all animations are smooth (60fps) and respect prefers-reduced-motion
- [ ] T092 Run Lighthouse audit (performance score 85+, accessibility score 90+)
- [ ] T093 [P] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] T094 [P] Manual accessibility testing with WAVE tool
- [ ] T095 [P] Verify WCAG AA contrast ratios for all text combinations
- [ ] T096 Test keyboard navigation for all interactive elements
- [ ] T097 Verify bundle size increase is < 50KB compared to baseline
- [ ] T098 Confirm page load time increase is < 500ms compared to baseline
- [ ] T099 Follow quickstart.md testing checklist for final validation
- [ ] T100 Document any issues or follow-up tasks needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order: US1 (P1) → US2 (P1) → US3 (P1) → US4 (P2) → US5 (P2) → US6 (P3)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - Independent of US1, US2
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Independent of all P1 stories
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - Should be done after other stories to ensure proper responsive behavior testing
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - Independent of all other stories

### Within Each User Story

**User Story 1** (Hero & Homepage):
- T015-T016 (create files) before T017-T024 (implement features)
- T025-T028 (homepage) requires T015-T024 (Hero component) to be complete
- T029 (update intro.md slug) can be done anytime in parallel

**User Story 2** (Theme Switching):
- All tasks can proceed in parallel once Foundational phase is complete
- All tasks modify the same file (custom.css) so coordinate to avoid conflicts

**User Story 3** (Reading Experience):
- T037-T042 (typography/styling) can all run in parallel
- T043-T044 (ReadingProgress structure) before T045-T047 (implementation)
- T048 (ScrollToTop structure) before T049-T051 (implementation)
- T052-T053 (integration) requires components to be complete

**User Story 4** (Chatbot):
- T054-T056 (setup) before T057-T067 (implementation)
- T057-T060 (ChatKit config) can be done together
- T061-T067 (UI features) can proceed after basic structure is in place
- T068-T069 (export and integration) must be last

**User Story 5** (Mobile Responsive):
- All tasks can be done in parallel by adding mobile breakpoints to existing components
- Final testing (T079) should be done after all mobile adjustments

**User Story 6** (Code Blocks):
- All styling tasks (T080-T084) can run in parallel
- Testing tasks (T085-T086) should be done after styling is complete

### Parallel Opportunities

- All Setup tasks (T002-T006) marked [P] can run in parallel
- All Foundational tasks within categories can run in parallel (but respect the CSS cascade)
- Once Foundational phase completes, **all 6 user stories can start in parallel** (if team capacity allows)
- Within each user story, tasks marked [P] can run in parallel
- Polish phase tasks marked [P] can run in parallel (T087-T088-T089, T092-T093-T094-T095)

---

## Parallel Example: Foundation Phase

Launch all foundational tasks together (coordinate file edits):

```bash
Task: "Import Google Fonts in docusaurus.config.js"
Task: "Create color palette CSS custom properties"
Task: "Create dark mode overrides"
Task: "Define typography system"
Task: "Define spacing, shadows, transitions"
Task: "Define gradients"
Task: "Create animation keyframes"
Task: "Update Docusaurus config for dark mode"
```

---

## Parallel Example: User Story 1 (Hero)

Launch structure creation tasks together:

```bash
Task: "Create Hero component structure: docs/src/components/Hero/index.tsx"
Task: "Create Hero component styles: docs/src/components/Hero/styles.module.css"
```

Then launch styling tasks in parallel (different CSS sections):

```bash
Task: "Implement animated gradient background"
Task: "Add button hover effects"
Task: "Add card hover effects"
Task: "Implement fade-in animations"
Task: "Add responsive breakpoints"
```

---

## Parallel Example: Multiple User Stories

With 3+ developers, after Foundational phase:

```bash
Developer A: User Story 1 (Hero & Homepage) - T015 through T029
Developer B: User Story 2 (Theme Switching) - T030 through T036
Developer C: User Story 3 (Reading Experience) - T037 through T053
```

All three can work simultaneously without conflicts (different files/components).

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only - All P1)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T014) - CRITICAL
3. Complete Phase 3: User Story 1 - Hero & Homepage (T015-T029)
4. **VALIDATE**: Test hero section independently on all viewports
5. Complete Phase 4: User Story 2 - Theme Switching (T030-T036)
6. **VALIDATE**: Test light/dark mode switching across all components
7. Complete Phase 5: User Story 3 - Reading Experience (T037-T053)
8. **VALIDATE**: Test typography, progress bar, scroll-to-top on doc pages
9. Complete Phase 9: Polish (T087-T100) for MVP scope
10. **DEPLOY MVP**: Core P1 features ready

### Incremental Delivery

1. Foundation → MVP (P1 Stories) → **Demo/Deploy**
2. Add User Story 4 (Chatbot - P2) → **Demo/Deploy**
3. Add User Story 5 (Mobile - P2) → **Demo/Deploy**
4. Add User Story 6 (Code Blocks - P3) → **Demo/Deploy**
5. Each increment adds value without breaking previous functionality

### Full Feature (All Stories)

1. Complete Setup + Foundational → Foundation ready
2. Work through all user stories in priority order (or in parallel if staffed)
3. Complete Polish phase
4. Full feature ready for production deployment

---

## Notes

- **[P] tasks** = different files or different sections, no dependencies, can run in parallel
- **[Story] label** maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **No programmatic tests** per constitution check in plan.md - testing is build validation + manual visual/responsive + Lighthouse audits
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Reference implementation available on branch `feature/ui-enhancements` (commit d7f3720)

---

## Summary

- **Total Tasks**: 100 tasks
- **User Story 1** (P1 - Hero): 15 tasks (T015-T029)
- **User Story 2** (P1 - Theme): 7 tasks (T030-T036)
- **User Story 3** (P1 - Reading): 17 tasks (T037-T053)
- **User Story 4** (P2 - Chatbot): 16 tasks (T054-T069)
- **User Story 5** (P2 - Mobile): 10 tasks (T070-T079)
- **User Story 6** (P3 - Code): 7 tasks (T080-T086)
- **Setup**: 6 tasks (T001-T006)
- **Foundational**: 8 tasks (T007-T014)
- **Polish**: 14 tasks (T087-T100)

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phases 3-5 (User Stories 1-3, all P1 priority) = 46 tasks

**Parallel Opportunities**:
- 5 setup tasks can run in parallel
- Most foundational tasks can run in parallel (coordinate CSS edits)
- All 6 user stories can start in parallel after foundation
- Within stories: ~40% of tasks marked [P] can run in parallel
- Polish phase: ~50% of tasks can run in parallel

**Independent Test Criteria**: Each user story has clear acceptance criteria in spec.md that can be tested independently without requiring other stories to be complete
