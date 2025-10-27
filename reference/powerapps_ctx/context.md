# VA AI Assistant – Power Apps Reference Context

**Purpose:** Use this as authoritative reference to rebuild the app in Python while keeping Start and Notice pages as implemented. Model all remaining UX, behavior, and data flow on this Power App.

## Screens (source of truth)

- (No screens parsed from Controls.json; refer to .msapp for full control tree)

## Data Sources

- (No DataSources.json found; if data is SharePoint/Dataverse, enumerate tables/columns manually.)

## App State Contracts

### Global Variables (Set)
- (none detected)

### Collections (Collect/ClearCollect)
- (none detected)

## Navigation Graph (Navigate)

- (No Navigate() edges detected; check OnSelect properties in controls.)

## Implementation Guidance for the Python Rebuild

- **Keep Start and Notice pages as-is.** All other pages must replicate the Power Apps screens’ control layout, visibility logic, and navigation.
- **UI Layer:** Recommend FastAPI + Jinja2 (server-rendered) or Flask + Jinja2. For rich SPA behavior, FastAPI backend + React (Next.js) frontend. Map each Power Apps screen to a route/component.
- **State:** Replace `Set()` with a typed global/session state (e.g., signed cookies or server session). Replace `UpdateContext({ ... })` with component/page-local state.
- **Collections:** Replace `Collect/ClearCollect` with in-memory lists or query results. Persist via DB calls when needed.
- **Data Sources:** Mirror each data source with a repository class. If original source is SharePoint/Dataverse, create a data access adapter with identical entity names/columns.
- **Formulas:** Port Power Fx formulas to Python/TypeScript equivalents. Preserve validation, `Visible`, `DisplayMode`, `Items`, and `OnSelect` logic one-by-one.
- **Navigation:** Convert `Navigate(TargetScreen, ...)` to route transitions (e.g., `router.push('/TargetScreen')`). Keep screen names stable.
- **Styling:** Extract theme tokens (colors, font sizes) from Themes.json or Properties.json; define a centralized design system (Tailwind or CSS vars).
- **Accessibility:** Preserve tab order, control roles, keyboard activation for all `OnSelect` actions.


## VS Code Prompt Template (Paste into ChatGPT/Codex/Copilot Chat)

You are my coding pair. Rebuild the remaining pages of this app in Python, modeling every detail on the referenced Power App export I've provided in the workspace under `powerapps_ctx/msapp_unpacked/`.

**Hard constraints**
- Do **not** modify the Start and Notice pages I already built.
- Preserve screen names, control hierarchies, visibility, and navigation semantics found in `Controls.json`.
- Mirror data sources, variables, and collections exactly. Keep names identical unless illegal in Python; if illegal, map via a deterministic name map.
- Before coding a page, print a concise plan: routes/components, state shape, data queries, and event handlers.
- Generate code with tests. Include fixtures that mimic the Power Apps collections.
- For each `OnSelect`/formula you port, include a comment with the original Power Fx snippet and the file/line where it's implemented.

**Artifacts to read**
- `/mnt/data/powerapps_ctx/msapp_unpacked/Controls.json` (control tree, per-control properties)
- `/mnt/data/powerapps_ctx/msapp_unpacked/App.json` or `/mnt/data/powerapps_ctx/msapp_unpacked/Properties.json` (app-level props)
- `/mnt/data/powerapps_ctx/msapp_unpacked/DataSources.json` (if present)
- `/mnt/data/powerapps_ctx/msapp_unpacked/Themes.json` (theme tokens)

**Porting rules**
- `Set(name, value)` → `session['name']=value` (or global store); add types.
- `UpdateContext({k:v})` → component/page local state.
- `Navigate(ScreenX, ...)` → route transition to `/ScreenX`.
- `Collect(tbl, rec)` / `ClearCollect(tbl, ...)` → repository/DAO insert or state update.
- `Patch(ds, ...)` → repository update with optimistic UI; handle concurrency.
- `Filter/Sort/Search` → translate to ORM/SQL or in-memory filters.
- Control.Properties like `Visible`, `DisplayMode`, `Items`, `Text`, `OnSelect` → re-implement exactly.

**Deliverables (per screen)**
1) routes/components, 2) UI layout, 3) state + data contracts, 4) handlers mapped from Power Fx, 5) tests.

Start by listing all screens and proposing a build order based on dependency (collections, navigation). Then implement the first screen end-to-end.
