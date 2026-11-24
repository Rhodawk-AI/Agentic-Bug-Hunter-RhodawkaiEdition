# Changelog

## 6.1.1.1 — DD hardening (recon)

### Fixed
- **[B1] `--no-scope-check` no longer kills canonical fusion** — `recon_fusion.py fuse` accepts the flag and records `scope_enforced: false`; a failed fuse prints a visible `CANONICAL FUSION FAILED` warning and records a `FAILED` `FUSION` row in `rtw_manifest.json` (tool_health) instead of being swallowed.
- **[B2] Scoped CLI recon/hunt stop following redirects out of scope** — `engine.py cmd_recon/cmd_hunt` set `SCOPE_ENFORCED=1` whenever scoping is active; redirect destinations are recorded as findings in `live/redirects.txt`, classified through the same scope rules, and only in-scope destinations are probed.
- **[B3] Discovered out-of-scope hosts/URLs are filtered before probing** — the engine applies the ScopeChecker filter at the four merge points (post-Phase-1, post-1.5, post-URL-collection, post-5.5); dropped lines land in `<recon_dir>/scope/dropped_oos.txt` and the count in the Summary + `recon_truth.json` (`counts.scope_dropped`).
- **[B4] `delta.json` port attribution** — open ports are attributed only to hosts they can be joined to (nmap target hostname, or an IP with exactly ONE resolving host); anything unjoinable goes to `unattributed_ports` (the shared-loopback E9 case no longer reports port 80 on unrelated hosts).
- **[B5] Re-runs are isolated from stale artifacts** — each run archives the previous truth to `.prev_run/` and clears the rest; the Summary counts the current run only (`Live hosts: 0` when httpx is gone).
- **[B6] `.run_incomplete` marker** — a killed run is recorded as `previous_run_incomplete: true` in the next truth with a warning.
- **[B7] Fusion certifies its inputs** — `input_integrity` per input file (ok/empty/missing/unparseable); an unparseable required input sets `status: DEGRADED` (exit code unchanged).
- **[C10] host:port targets key their own recon dir** (`127.0.0.1_8082`) across target_normalize/engine.py/hunt.py/recon_engine.sh.
- **[PIN] The adapter re-verifies the reconFTW commit at run time** — HEAD != `RTW_COMMIT_PIN` returns SKIPPED ('pin mismatch') and records it for tool_health.
- **[UX] `:port` / `/path` scope patterns warn at construction** instead of failing closed silently.
- **[B9] README `tool_health` status names match the adapter enum**; `commands/recon.md` marks dnsx/Chaos/gf/Arjun/LinkFinder steps as NOT implemented.
- **[B10] BUILD-MANIFEST.txt regenerated from the real git diff with correct counts, test totals and version; "454 of 461 byte-identical" wording fixed; the "one functional addition" claim replaced with the real feature set.

### Docs
- README/PLAYBOOK: "0 packets" claims scoped to the blocked target; discovered hosts are filtered before probing; `--no-scope-check` disables scoping; recon output path corrected (both `~/.bughunter/recon/` and the writable-clone `bughunter/recon/` layouts documented).
- BENCHMARKS.md: new "Limitations" section (single run per cell, scoped-vs-unscoped comparison caveat, 3-of-5 slower targets, reconFTW DNF wording, unexplained Live hosts=0, single-target CDN savings).

## 6.1.1 — npm + PyPI release

### Added
- **PyPI release 6.1.1** with the `rhodawk` CLI entrypoint (`pyproject.toml` console script).
- **npm package** `agentic-bug-hunter-rhodawkai-edition@6.1.1` (CLI wrapper publishing the `rhodawk` command).
- **BENCHMARKS.md** — timed 3-way recon benchmark (RhodawkAI Edition vs upstream ABH vs standalone reconFTW) against 5 authorized domains, with per-domain timings and honest telemetry notes.

## 6.1.0 — RhodawkAI Edition

### Added
- **reconFTW on-demand capability delegation (recon phase only)** — wherever ABH's own recon pipeline hits a capability it doesn't have, it transparently delegates to reconFTW's equivalent function. The routing decision is **deterministic code, not an LLM judgment call**: `tools/capability_registry.py` builds `~/.bughunter/capabilities.json` (`NATIVE | RTW_AVAILABLE | RTW_MISSING_DEPS` per capability — a boot-time registry with pinned per-capability go-install and an ABH-style Req/Opt API-key banner), and `tools/rtw_adapter.py` runs a fixed six-step flow (typed ID → native guard → 7-day-TTL dedup against `~/.bughunter/recon/<host>/rtw_manifest.json` → availability → fail-closed scope gate → reconFTW's supported single-function interface with an ephemeral `rtw_override.cfg`). The 7 verified gap map: ASN/CIDR enum (`sub_asn`), DNS brute/permutation (`sub_permut`), CDN/origin isolation (`cdnprovider`), JS source-map/AST secrets (`jschecks`), virtual-host discovery (`virtualhosts`), TLS IP pivots (`tls_ip_pivots`), favicon fingerprinting (`favirecon_tech`). `modules/vulns.sh` is never delegated; every output file is scope-filtered post-call.
- **Split gap-fill phases in `recon_engine.sh`** — Phase 1.5 (subdomain/infra gap-fill: ASN enum, DNS permutation, CDN isolation) runs between Phase 1 and Phase 2 so newly discovered subdomains are merged into `subdomains/all.txt` and probed by httpx in the same run; Phase 5.5 (web/JS/TLS gap-fill: jschecks, virtualhosts, TLS pivots, favicon) runs between Phase 5 and Phase 6 so JS endpoints/routes merge into `urls/all.txt` before fuzzing and the Summary. With `RTW_HOME` unset the engine behaves exactly as upstream.
- **Fail-closed scope flags on `recon_engine.sh`** — repeatable `--scope-domain` / `--scope-exclude` (forwarded verbatim to the gap-fill adapter) plus an explicit `--no-scope-check` opt-out for local demo testing. Without either, reconFTW delegation fails closed (no reconFTW subprocess, block logged to `hunt-memory/audit.jsonl`) while the native pipeline continues. All callers forward the active ScopeChecker patterns: `bughunter/engine.py` (`recon`/`hunt` CLI flags), `tools/hunt.py run_recon` (global checker), and the MCP `adapters.run_recon`.
- **4th runtime: MCP `run_rtw_capability`** — `bughunter mcp serve` registers `bughunter_run_rtw_capability` alongside the existing 25 tools, routed through the same PolicyEngine gate (scope required → fail-closed BLOCK, `approve=true` required, output redaction) and delegating through the same `rtw_adapter.run_capability` — identical `rtw_manifest.json` schema across all four runtimes (CLI engine, ReAct agent, interactive harness, MCP server).
- **ReAct agent tool** — `run_rtw_capability(capability_id, force)` registered in `agent.py` TOOLS with the 7 typed IDs as an enum, wired into NETWORK_TOOLS/TOOL_METHODS (GET, scope-gated), and the rule "If recon_summary flags a capability gap and capabilities.json marks it RTW_AVAILABLE, call run_rtw_capability before proceeding." added to AGENT_SYSTEM — worded identically in `commands/recon.md`, `bughunter/agents/recon-agent.md`, and `skills/web2-recon/SKILL.md`.

### Changed
- **Rebrand** — package `agentic-bug-hunter-rhodawkai-edition` v6.1.0 (upstream ABH 6.0.1 + this integration); README leads with the capability table. Standalone release: secrets stay entirely within this fork's own `config.json` / reconFTW's `secrets.cfg` — no external secrets source, config format, or dependency is wired in.
- **install.sh** — after the 7-target dispatch, clones reconFTW at the pinned commit `39252113a854bdac0b785f144b9fae1fa8ca35fc` into `RTW_HOME` (default `~/Tools/reconftw`, override with `RTW_HOME`) and rebuilds `capabilities.json`. Missing clone is not an error — the fork runs as upstream without it.
- **install_tools.sh** — new `--rtw-deps` mode installs ONLY the 7 capabilities' backing binaries via pinned go-install (`puredns@v2.1.1`, `tlsx@v1.1.7` from reconFTW's tools.lock; pin-on-first-install for the rest). reconFTW's own installer is never run wholesale.

## Unreleased (upstream 6.0.1)

### Added
- **Requesty provider** (`requesty`) for standalone `bughunter` / `brain.py`: OpenAI-compatible gateway at `https://router.requesty.ai/v1` via `REQUESTY_API_KEY` (optional `REQUESTY_BASE_URL`, e.g. `https://router.eu.requesty.ai/v1` for the EU region). Not in the auto-detect priority list; choose option 11 in `bughunter setup`, `BRAIN_PROVIDER=requesty`, or `--provider requesty`. Default model `anthropic/claude-sonnet-4-6` and a short curated model list (same pattern as OpenRouter).
- **Fluxion AI provider** (`fluxion`) for standalone `bughunter` / `brain.py` — optional OpenAI-compatible gateway at `https://fluxionai.world/v1` via `FLUXION_API_KEY`. Not the default; choose option 9 in `bughunter setup`, `BRAIN_PROVIDER=fluxion`, or `--provider fluxion`. README partner placement + setup docs link [docs](https://docs.fluxionai.world/user-guide/help-center) and [Model Plaza](https://fluxionai.world/model-plaza).
- **Claude Code plugin manifest** (`.claude-plugin/plugin.json`) — declares skills, commands, agents, and hooks so the repo passes Claude Code / marketplace plugin validation.
- **LiteLLM provider** (`litellm`) for standalone `bughunter` / `brain.py` — one gateway reaches 100+ LLM backends (OpenAI, Anthropic, Gemini, Bedrock, Vertex, Groq, …), routed by the `provider/model` prefix using each provider's own key, or via a LiteLLM proxy (`LITELLM_API_KEY` / `LITELLM_API_BASE`). Choose option 9 in `bughunter setup` or set `BRAIN_PROVIDER=litellm`. Uses `drop_params=True` for cross-provider compatibility, omits blank creds so each provider's own env var is honored, and lists models via live discovery (proxy `/models`, or `get_valid_models()` in SDK mode) — no hardcoded list. Opt-in in auto-detect so it never preempts an already-configured provider.
- **DOM XSS confirmation harness** (`/domxss`, `tools/dom_xss_harness.py`) — drives headless Chromium via Playwright, injects uniquely-tagged canary payloads into every query + URL-fragment parameter, and reports `[CONFIRMED]` **only when the browser actually executes** the payload (dialog / hooked sink / console), vs `[POSSIBLE]` for reflected-but-neutralized. Turns the toolkit's biggest "confirmation-poor" gap (client-side/JS-execution bugs) into proven findings, and captures a screenshot for the report. Payload generation, URL injection, and verdict classification are pure and unit-tested; Playwright is lazy-imported so the suite needs no browser. Playwright registered in `external_arsenal.sh`.
- **Continuous integration** — `.github/workflows/tests.yml` runs the full `pytest` suite on every push to `main` and every pull request, across Python 3.10 / 3.11 / 3.12. A status badge is shown in the README.

### Changed
- **Minimum Python is now stated as 3.10** (was advertised as 3.9). The codebase uses PEP 604 `X | None` unions at runtime (e.g. `memory/schemas.py`), which raise `TypeError` on 3.9 — CI confirmed 3.9 never actually worked. README badge updated to match.

### Fixed
- **Go / Dependency Graph package identity** — add `go.mod` declaring `module github.com/awarexone/Agentic-Bug-Hunter` (matches GitHub `go-import`). Pre-rename tags were indexed by the Go proxy as `github.com/shuvonsec/claude-bug-bounty` `+incompatible`, which is why Insights → Dependents showed that path. Old requires still resolve via the repo redirect.
- **`tests/test_bypass_403_review_fixes.py`** re-pointed at the current WAF-aware bypass verdict pipeline (block-baseline sampling + `_is_real_bypass` signature/length gating + confirmed-vs-uncertain output split). It was still asserting the pre-#40 `_normalize_body` internals that the rewrite removed, so it failed on every run once CI was added.
- **Port/service scanning** (`/portscan`, `tools/port_scanner.py`) — wraps `naabu` with an `smap` passive fallback and flags the non-web services the HTTP-only recon pipeline can't see (Redis, Docker API, exposed DBs, RDP, SMB). Parsing + service classification are pure and unit-tested. Closes a `[registered-not-wired]` gap.
- **Visual triage / PoC screenshots** (`/screenshot`, `tools/visual_triage.py`) — screenshots live hosts via `eyewitness`/`aquatone`/`httpx -screenshot` into a self-contained HTML gallery that doubles as report evidence. Tool selection, command build, and gallery rendering are unit-tested. Closes a `[registered-not-wired]` gap and the "no automatic PoC capture" gap.
- **SAST source audit** (`/sast`, `tools/sast_scan.py`) — runs Semgrep security packs over fetched JS/source and normalizes results into the toolkit's severity + `POSSIBLE` confidence model (SAST is a lead, not proof — `/validate` still requires a runtime PoC). Result parsing is unit-tested. Closes a `[registered-not-wired]` gap.
- **AwareXone sponsorship & branding** — README now leads with an "Open for Sponsorship" callout and a "Powered by AwareXone.com" credit (hero badge + footer). Same credit added to the project site footer, plus a `.github/FUNDING.yml` so the repo shows a Sponsor button.
- **OpenRouter provider** (`openrouter`) for standalone `bughunter` / `brain.py` — set `OPENROUTER_API_KEY`, choose option 7 in `bughunter setup`, or `BRAIN_PROVIDER=openrouter`. OpenAI-compatible gateway with default model `anthropic/claude-sonnet-4.6` and a short curated model list (same pattern as other cloud providers).
- **OrcaRouter provider** (`orcarouter`) for standalone `bughunter` / `brain.py` — set `ORCAROUTER_API_KEY`, choose option 8 in `bughunter setup`, or `BRAIN_PROVIDER=orcarouter`. OpenAI-compatible gateway with default model `openai/gpt-4o` and a short curated model list (same pattern as other cloud providers).
- **Explicit Ollama model selection** — `bughunter setup` now lists installed local models and persists the selected provider/model pair; `bughunter setup --provider ollama --model <name>` supports non-interactive configuration. `--model` / `BRAIN_MODEL` provide one-off overrides, and explicit choices no longer silently fall back to or race a different model.
- **Standalone installer updates** — rerunning `install.sh --agent standalone` now refreshes the active managed `bughunter` path instead of allowing an older system installation to shadow a newer user-local link, and verifies the updated symlink target.
- **SDK-free Ollama fallback** — standalone provider setup and chat now use Ollama's local HTTP API when the Python `ollama` package is unavailable; dependency installation failures are reported instead of silently ignored.
- **Expanded uninstaller** — `uninstall.sh` now covers standalone and every supported agent harness, with managed-file checks, confirmation, configuration preservation by default, explicit `--purge-config` support, and compatibility with its previous `--claude` / `--opencode` / `--both` flags.

## v4.3.2 — AI Hunt Playbook (Jun 2026)

### Added
- AI-assisted hunt guidance in `skills/bb-methodology/SKILL.md` and `skills/bug-bounty/SKILL.md`: use the model for feature decomposition, sibling-endpoint diffing, role matrices, and chain planning, while keeping proof requirements anchored to live requests and cross-account deltas.
- AI-assisted planning signals in `tools/mindmap.py` so generated hunt checklists now surface hypothesis expansion and validation-gate reminders alongside the traditional vuln-class checklist.

## v4.3.1 — Bug Fixes + Hardening (Jun 2026)

### Fixed
- **`tools/vuln_scanner.sh` parse failure** — removed the broken duplicate XSS merge block and restored a single dalfox path against `urls/with_params.txt`.
- **macOS bash 3.2 auth crashes** — replaced empty-array auth splats with the bash 3.2-safe form across recon/scanning scripts so anonymous runs no longer abort under `set -u`.
- **`tools/scope_checker.py` CLI gap** — added a real deterministic CLI with asset checks, URL filtering, JSON output, and clean missing-file errors.
- **`tools/hai_probe.py` / `tools/zendesk_idor_test.py` help-path crashes** — both tools now handle missing `requests` gracefully and print useful `--help` output without importing the dependency first.

### Added
- `requirements.txt` for the Python helper tools and test runner.
- `tests/test_scope_checker.py` coverage for the new deterministic scope checker CLI.

### Changed
- `install.sh` now supports Claude Code, OpenCode, Pi Agent, Codex-style installs, shared Agent Skills, and project-local installs.
- `install_tools.sh` attempts to install Python dependencies after the binary tool pass.
- `tools/validate.py` persists `submission-notes.md` and `validation.json` beside each report skeleton.
- `tools/vuln_scanner.sh` now writes `summary.json` so validation can ingest the scanner confidence and tier counts directly.
- `tools/validate.py` now accepts `--scanner-summary` and records the scanner handoff in `validation.json` and the report skeleton.
- `tools/bypass_403.sh` now compares normalized response bodies before marking a bypass confirmed.
- Added regression coverage for the scanner handoff, bypass normalization, and false-positive classes that commonly come back N/A.

## v4.2.3 — Auto-rotation Stop Hook (May 2026)

### Added
- **`.claude/settings.json`** with a `Stop` hook that runs `python3 -m tools.memory_gc --rotate` (quietly, non-blocking via `async: true`) whenever a Claude Code session ends. Long-running hunts that never trigger an inline write-time rotation now still get GC'd at session end. Hook is a no-op if `tools/memory_gc.py` is missing or the working dir isn't the repo root, so it is safe to ship in the project file.

---

## v4.2.2 — Restore ReconAdapter (May 2026)

### Fixed
- **`tools/recon_adapter.py`** was missing the `ReconAdapter` class that `tests/test_recon_adapter.py` imports — the test file had been silently uncollectable since the rename in 0db9640. Added the class with read accessors for the subdir-nested layout that `recon_engine.sh` writes (`subdomains/all.txt`, `live/urls.txt`, `urls/with_params.txt`, `js/potential_secrets.txt`, etc.), graphql extraction, fallback path resolution, summary counts, and a `normalize()` method that creates the derived files brain.py expects (`priority/`, `api_specs/`, `urls/graphql.txt`, `subdomains/resolved.txt`).

### Tests
- 31 previously-uncollectable tests in `tests/test_recon_adapter.py` now run and pass. Suite total: **215 passing** (was 184).

---

## v4.2.1 — PatternDB Perf Fix (May 2026)

### Fixed
- **`PatternDB.save()` was O(n²)** — every save re-read the entire JSONL file to dedup. At 10k entries this pegged CPU for 5+ minutes per insert pass. Replaced with an in-memory dedup index of `(target, vuln_class, technique)` tuples, populated lazily on first save and updated per write. 10k saves now complete in ~2 seconds instead of 5+ minutes.

### Added
- `tests/test_pattern_db.py::TestPatternPerformance`: 4 new tests covering the perf bound, dedup correctness at 10k entries, lazy-load via reopen, and corrupted-line resilience.

### Resolved
- **TODO-8 (final item)** — `PatternDB.save()` performance test at 10,000 entries.

---

## v4.2.0 — Memory Rotation (Apr 2026)

### Added
- `memory/rotation.py`: size-based JSONL rotator under `fcntl.LOCK_EX`. Default cap 10 MB, keep 3 backups.
- `tools/memory_gc.py` + `/memory-gc` slash command: scan, rotate, or purge backups across the hunt-memory tree.
- `tests/test_rotation.py`: 22 tests covering rotation primitives, auto-rotation in `AuditLog`/`PatternDB`, multi-process concurrent writes (with and without rotation), and disk-full OSError propagation.

### Changed
- `memory/audit_log.py` `AuditLog.log()`: calls `rotate_if_needed` before each append.
- `memory/pattern_db.py` `PatternDB.save()`: calls `rotate_if_needed` before each append.
- `memory/__init__.py`: exports rotation helpers.

### Resolved
- **TODO-7** — memory GC / rotation policy.
- **TODO-8** (partial) — concurrent-write stress test + disk-full OSError propagation test.

---

## v4.1.0 — Patch: Bug Fixes + Assets (Apr 2026)

### Fixed
- **TODO-4 resolved**: `hunt.py` BASE_DIR path resolution — `hunt.py` was relocated to `tools/` so `TOOLS_DIR`/`BASE_DIR`/`RECON_DIR`/`FINDINGS_DIR` now resolve correctly. All 5 open TODOs are now closed.

### Added
- `logo-banner.svg` and `logo-icon.svg` — SVG vector assets for banner and icon variants

---

## v4.0.0 — Meme Coin Security Module (Apr 2026)

### Added — New Skill Domain
- `skills/meme-coin-audit/SKILL.md`: **Meme coin rug pull detection + 8 token bug classes**
  - Mint authority / freeze authority checks
  - Bonding curve exploit patterns
  - LP lock verification
  - Honeypot detection
  - Token metadata tampering
  - Solana-specific audit path (SPL token checks)
  - Pre-dive kill signals for obvious rugs

### Added — Tool
- `tools/token_scanner.py`: automated token red flag scanner supporting EVM + Solana
  - EVM: ABI analysis, ownership checks, hidden mint functions, transfer tax detection
  - Solana: SPL token account authority checks, metadata validation

### Changed
- `CLAUDE.md`: Skills count 8 → 9, added `meme-coin-audit` to skill table; Commands 13 → 14, added `/token-scan`
- `README.md`: Updated skill domain count

---

## v3.1.1 — CI/CD GitHub Actions Security Expansion (Mar 2026)

### Changed — Existing Skill Enhancement
- `SKILL.md` CI/CD Pipeline section: **5 checklist items → 6 categories, 30+ checks, PoC templates, hunting workflow, and GHSA reference table**
  - **Category 1: Code Injection & Expression Safety** — expression injection, envvar/envpath/output clobbering, argument injection, SSRF via workflow, taint source catalog, fix patterns (env var extraction, heredoc delimiters, end-of-options markers)
  - **Category 2: Pipeline Poisoning & Untrusted Checkout** — untrusted checkout on `pull_request_target`/`workflow_run`, TOCTOU with label-gated approvals, reusable workflow taint, cache poisoning, artifact poisoning, artipacked credential leakage
  - **Category 3: Supply Chain & Dependency Security** — unpinned actions (tag → SHA), impostor commits from fork network, ref confusion, known vulnerable actions, archived actions, unpinned container images
  - **Category 4: Credential & Secret Protection** — secret exfiltration, secrets in artifacts, unmasked `fromJson()` bypass, excessive `secrets: inherit`, hardcoded credentials
  - **Category 5: Triggers & Access Control** — dangerous triggers without/with partial mitigation, label-based approval bypass, bot condition spoofing, excessive GITHUB_TOKEN permissions, self-hosted runners in public repos, OIDC token theft
  - **Category 6: AI Agent Security** — unrestricted AI triggers, excessive tool grants to AI agents, prompt injection via workflow context
  - **Hunting workflow** — 6-step recon→scan→triage→verify→PoC→prove pipeline
  - **Expression injection PoC template** — ready-to-use `gh issue create` payload
  - **10 real-world GHSAs** — proven Critical/High advisories with affected actions
  - **A→B signal chains** — 7 CI/CD-specific escalation paths
  - **Tooling**: integrated [sisakulint](https://sisaku-security.github.io/lint/) — 52 rules, taint propagation, 81.6% GHSA coverage
  - **Deep-dive guide**: Decision tree for verifying sisakulint findings based on 36 real-world paid reports (Bazel $13K, Flank $7.5K, PyTorch $5.5K, GitHub $20K, DEF CON $250K+)

### Added — Tool Integration
- `tools/cicd_scanner.sh`: standalone sisakulint wrapper — org/repo scanning, recursive reusable workflow analysis, parsed summary output with per-rule breakdown
- `install_tools.sh`: sisakulint binary auto-download with OS/arch detection (v0.2.11, linux/darwin, amd64/arm64/armv6), cicd_scanner install now optional (`--with-cicd-scanner`)
- `tools/recon_engine.sh` Phase 8: auto-detects GitHub orgs from recon data (httpx, JS endpoints, URLs), invokes `cicd_scanner.sh` per org
- `tools/hunt.py`: surfaces CI/CD findings between recon and vuln scan stages via `check_cicd_results()`
- `tests/test_cicd_scanner.sh`: shell tests for cicd_scanner (syntax check + CLI behavior)

## v3.1.0 — Hunting Methodology Skill (Mar 2026)

### Added — New Skill Domain
- `skills/bb-methodology/SKILL.md`: **Hunting mindset + 5-phase non-linear workflow** — the "HOW to think" layer that was missing from the toolkit
  - **Part 1: Mindset** — Define/Select/Execute discipline, 4 thinking domains (critical, multi-perspective, tactical, strategic), developer psychology reverse-engineering, Amateur vs Pro 7-phase comparison, Feature-based vs Vuln-based route selection, anti-patterns
  - **Part 2: Workflow** — 5-phase non-linear flow (Recon → Map → Find → Prove → Report) with decision trees per phase, input-type → vuln-class routing, Error vs Blind detection cascade, escalation decision trees per vuln class
  - **Part 3: Navigation & Timing** — "I'm stuck because..." quick reference table, 20-minute rotation clock, tool routing by phase with rationale, session start/end checklists

### Changed
- `CLAUDE.md`: Skills count 7 → 8, added `bb-methodology` to skill table
- `README.md`: Updated skill domain count to 8
- `SKILL.md`: Added cross-reference to `bb-methodology` after CRITICAL RULES section

## v3.1.0 — CVSS 4.0 + TODO Fixes (Mar 2026)

### Changed — CVSS 3.1 → 4.0
- `tools/validate.py`: Full CVSS 4.0 interactive scorer. Replaces 8-metric CVSS 3.1 with 11-metric CVSS 4.0. New metrics: AT (Attack Requirements), VC/VI/VA (Vulnerable System), SC/SI/SA (Subsequent System, incl. Safety). Scope metric removed. UI now has three values (None / Passive / Active). Score verified via FIRST.org calculator link in output.
- `agents/report-writer.md`: Updated CVSS section to 4.0. New metric descriptions, updated common-pattern examples, verification link.

### Fixed — TODOs resolved
- `agents/autopilot.md` already implemented TODO-2 (safe HTTP methods) and TODO-3 (circuit breaker) — marked resolved in TODOS.md
- `tools/hunt.py` BASE_DIR path resolution was already correct (TODO-4 was based on wrong assumption about file location) — marked resolved
- `tools/recon_adapter.py` created (TODO-5): auto-detects nested vs flat recon format, returns unified `ReconData`. `normalize_to_nested()` migrates legacy flat output. CLI: `python3 tools/recon_adapter.py example.com --migrate`

---

## v2.1.0 — 20 Vuln Classes + Payload Expansion (Mar 2026)

### Config
- Recon commands now read the Chaos API key from the `$CHAOS_API_KEY` environment variable for cleaner setup across different environments.

### Added — New Vuln Classes
- `web2-vuln-classes`: **MFA/2FA Bypass** (class 19) — 7 bypass patterns: rate limit, OTP reuse, response manipulation, workflow skip, race, backup codes, device trust escalation
- `web2-vuln-classes`: **SAML/SSO Attacks** (class 20) — XML signature wrapping (XSW), comment injection, signature stripping, XXE in assertion, NameID manipulation + SAMLRaider workflow

### Added — security-arsenal Payloads
- **NoSQL injection**: MongoDB `$ne`/`$gt`/`$regex`/`$where` operators, URL-encoded GET parameter injection
- **Command injection**: Basic probes, blind OOB (curl/nslookup), space/keyword bypass techniques, Windows payloads, filename injection context
- **SSTI detection**: Universal probe for all 6 engines (Jinja2, Twig, Freemarker, ERB, Spring, EJS) + RCE payloads for each
- **HTTP smuggling payloads**: CL.TE, TE.CL, TE.TE obfuscation variants, H2.CL
- **WebSocket testing**: IDOR/auth bypass messages, CSWSH PoC, Origin validation test, injection via messages
- **MFA bypass payloads**: OTP brute force (ffuf), race async script, response manipulation, device trust cookie test
- **SAML attack payloads**: XSW XML templates, comment injection, signature stripping workflow, XXE payload, SAMLRaider CLI

### Added — web2-recon Skill
- **Setup section**: `$CHAOS_API_KEY` export instructions, subfinder config.yaml with 5 API sources, nuclei-templates update command
- **crt.sh** passive subdomain source (no API key needed) added as Step 0
- **Port scanning**: naabu command for non-standard ports (8080/8443/3000/9200/6379/etc.)
- **Secret scanning**: trufflehog + SecretFinder JS bundle scan, grep patterns
- **GitHub dorking**: `gh search code` commands, GitDorker integration for org-wide secret search

### Added — report-writing Skill
- **Intigriti template**: Full format with platform-specific notes (video PoC preference, safe harbor stance)
- **CVSS 4.0 quick reference**: Key differences from CVSS 3.1, score examples for common findings, calculator link

### Added — rules/hunting.md
- **Rule 18**: Mobile = different attack surface (APK decompile workflow, key targets)
- **Rule 19**: CI/CD is attack surface (GitHub Actions expression injection, dangerous workflow patterns)
- **Rule 20**: SAML/SSO = highest auth bug density (test checklist)

### Updated
- README: CHAOS_API_KEY setup section with free key instructions and optional subfinder API keys
- README: Updated vuln class count from 18 → 20, updated skill descriptions
- `web2-vuln-classes` description updated to reflect 20 classes and new additions

---

## v2.0.0 — ECC-Style Plugin Architecture (Mar 2026)

Major restructure into a full Claude Code plugin with multi-component architecture.

### Added
- `skills/` directory with 7 focused skill domains (split from monolithic SKILL.md)
  - `skills/bug-bounty/` — master workflow (unchanged from v1)
  - `skills/web2-recon/` — recon pipeline, subdomain enum, 5-minute rule
  - `skills/web2-vuln-classes/` — 18 bug classes with bypass tables
  - `skills/security-arsenal/` — payloads, bypass tables, never-submit list
  - `skills/web3-audit/` — 10 smart contract bug classes, Foundry template
  - `skills/report-writing/` — H1/Bugcrowd/Intigriti/Immunefi templates
  - `skills/triage-validation/` — 7-Question Gate, 4 gates, always-rejected list
- `commands/` directory with 8 slash commands
  - `/recon` — full recon pipeline
  - `/hunt` — start hunting a target
  - `/validate` — 4-gate finding validation
  - `/report` — submission-ready report generator
  - `/chain` — A→B→C exploit chain builder
  - `/scope` — asset scope verification
  - `/triage` — quick 7-Question Gate
  - `/web3-audit` — smart contract audit
- `agents/` directory with 5 specialized agents
  - `recon-agent` — runs recon pipeline, uses claude-haiku-4-5 for speed
  - `report-writer` — generates reports, uses claude-opus-4-6 for quality
  - `validator` — validates findings, uses claude-sonnet-4-6
  - `web3-auditor` — audits contracts, uses claude-sonnet-4-6
  - `chain-builder` — builds exploit chains, uses claude-sonnet-4-6
- `hooks/hooks.json` — session start/stop hooks with hunt reminders
- `rules/hunting.md` — 17 critical hunting rules (always active)
- `rules/reporting.md` — 12 report quality rules (always active)
- `CLAUDE.md` — plugin overview and quick-start guide
- `install.sh` — one-command skill installation

### Content Added to Skills
- SSRF IP bypass table: 11 techniques (decimal, octal, hex, IPv6, redirect chain, DNS rebinding)
- Open redirect bypass table: 11 techniques for OAuth chaining
- File upload bypass table: 10 techniques + magic bytes reference
- Agentic AI ASI01-ASI10 table: OWASP 2026 agentic AI security framework
- Pre-dive kill signals for web3: TVL formula, audit check, line-count heuristic
- Conditionally valid with chain table: 12 entries
- Report escalation language for payout downgrade defense

---

## v1.0.0 — Initial Release (Early 2026)

- Monolithic SKILL.md (1,200+ lines) covering full web2+web3 workflow
- Python tools: `hunt.py`, `learn.py`, `validate.py`, `report_generator.py`, `mindmap.py`
- Vulnerability scanners: `h1_idor_scanner.py`, `h1_mutation_idor.py`, `h1_oauth_tester.py`, `h1_race.py`
- AI/LLM testing: `hai_probe.py`, `hai_payload_builder.py`, `hai_browser_recon.js`
- Shell tools: `recon_engine.sh`, `vuln_scanner.sh`
- Utilities: `sneaky_bits.py`, `target_selector.py`, `zero_day_fuzzer.py`, `cve_hunter.py`
- Web3 skill chain: 10 files in `web3/` directory
- Wordlists: 5 wordlists in `wordlists/` directory
- Docs: `docs/payloads.md`, `docs/advanced-techniques.md`, `docs/smart-contract-audit.md`
