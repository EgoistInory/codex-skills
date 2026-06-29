# Interaction Motion Playbook

Use this reference when improving a frontend's interaction quality, motion, delight, or sense of play. The goal is a usable product that feels alive, not a decorative demo.

## First Pass

1. Inspect the current product purpose, core workflow, design language, and performance budget.
2. Identify the emotional target in plain terms: calm, studio-grade, playful, cinematic, tactile, precise, editorial, or utilitarian.
3. Choose 2-4 high-value moments instead of animating every component.
4. Preserve existing data, routing, forms, and accessibility behavior.
5. Verify rendered behavior in browser after implementation.

## Good Motion Targets

- First meaningful load: stagger only major regions, keep content readable quickly.
- Primary action feedback: pressed, loading, success, failure, disabled, and retry states.
- Navigation transitions: sidebar, drawer, tabs, command palette, modal open/close.
- Content reveal: filters, search results, cards, detail panels, image previews.
- Empty/error states: subtle personality with a real recovery path.
- Media surfaces: image hover depth, before/after reveal, zoom preview, scrubber, comparison slider.

## Interaction Patterns

- Use CSS transitions for simple opacity, transform, color, shadow, and background changes.
- Use CSS keyframes for deterministic loops, one-shot reveals, shimmer, progress, or ambient details.
- Use requestAnimationFrame or a motion library only when stateful gesture/physics behavior is genuinely needed and already fits the stack.
- Prefer transform and opacity over layout-affecting animation.
- Keep hover effects paired with focus-visible styles; touch users need equivalent feedback.
- Add reduced-motion fallbacks with `@media (prefers-reduced-motion: reduce)`.

## Fun Without Gimmicks

- Tie delight to the domain: archive cards can feel like contact sheets, prompt copy can feel like a precise instrument, image previews can feel like a light table.
- Add small surprises at decision points: copy confirmation, upload completion, search empty state, detail expansion.
- Use sound only if explicitly requested and controllable.
- Avoid random motion that distracts from reading or editing.
- Avoid decorative particles, blobs, or loops unless they communicate product state.

## Product Guardrails

- Do not hide important content behind slow intro animation.
- Do not make controls move away from the pointer.
- Do not animate dimensions in dense dashboards unless the layout remains stable.
- Do not add fake controls, teaser buttons, or unfinished routes.
- Do not introduce a dependency for effects that CSS can handle clearly.
- Do not make motion depend on private browser state or unreliable timers.

## Implementation Checklist

- Define motion tokens in CSS variables when the project has global styles:
  - `--motion-fast`: 120ms-180ms
  - `--motion-medium`: 220ms-320ms
  - `--motion-slow`: 420ms-700ms
  - `--ease-standard`: cubic-bezier tuned for the brand
  - `--ease-emphasis`: for entrance or primary action feedback
- Keep interactive elements at stable dimensions across idle, hover, active, loading, and error states.
- Use semantic buttons and inputs before adding custom gesture layers.
- Give asynchronous work visible state and a way to recover from failure.
- Add or update tests only for behavior contracts that can regress; rely on browser checks for visual motion quality.

## Browser Verification

Check at least:

- Initial render has no layout overlap or unreadable text.
- Keyboard focus reaches animated controls and remains visible.
- `prefers-reduced-motion` does not leave content hidden.
- Main workflow still works after animation changes.
- Mobile/touch behavior is usable without hover.
- Console has no new runtime errors.

For production-track sites, also verify build output and avoid claiming completion until the repository's normal acceptance gates pass.
