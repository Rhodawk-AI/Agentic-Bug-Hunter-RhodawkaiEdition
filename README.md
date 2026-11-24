<div align="center">

<img src="assets/rhodawk-banner.png" alt="Agentic Bug Hunter — RhodawkAI Edition" width="100%"/>

**Fail-closed, CDN-aware autonomous bug bounty reconnaissance & attack-surface prioritization — 100% open-source, self-hostable, zero closed-model lock-in.**

[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](https://github.com/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition/blob/main/LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition/blob/main/pyproject.toml)
[![CI](https://github.com/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition/actions/workflows/ci.yml)
[![GitHub Stars](https://img.shields.io/github/stars/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition?style=for-the-badge&color=F59E0B)](https://github.com/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition/stargazers)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA_NIM-Open_Weights-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://github.com/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition#-open-weight--multi-provider-ai)
[![Ollama](https://img.shields.io/badge/Ollama-100%25_Local-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://github.com/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition#-open-weight--multi-provider-ai)
[![PyPI](https://img.shields.io/pypi/v/agentic-bug-hunter-rhodawkai-edition?style=for-the-badge&logo=pypi&logoColor=white&color=3775A9)](https://pypi.org/project/agentic-bug-hunter-rhodawkai-edition/)
[![npm](https://img.shields.io/npm/v/agentic-bug-hunter-rhodawkai-edition?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/agentic-bug-hunter-rhodawkai-edition)


**[Demo](#-live-demo) · [What Is This](#-what-is-this) · [Benchmark](#-head-to-head-benchmark) · [Quick Start](#-quick-start-5-commands) · [AI Providers](#-open-weight--multi-provider-ai) · [reconFTW Delegation](#-deterministic-reconftw-delegation) · [Commands & MCP](#-cli-commands-mcp--project-structure) · [Acknowledgments](#-acknowledgments--branded-footer)**

</div>

---

## 🎬 Live Demo

<p align="center">
  <img src="assets/rhodawk-demo.gif" alt="RhodawkAI Edition Live Terminal Demo" width="100%"/>
</p>

<p align="center">
  <em>Recorded live on an 8-vCPU Ubuntu VPS: <code>rhodawk doctor</code> (<code>0 FAIL</code>, <code>&lt;5s</code>) → fail-closed OOS scope block (<code>0</code> packets) → live CDN-aware recon on <code>rhodawkai.com</code> → canonical <code>recon_truth.json</code> + NVIDIA NIM <code>recon_brief.md</code>.</em>
  <br/>
  <a href="assets/rhodawk-demo-1080p.mp4">▶ Download / Watch Full 1080p MP4</a>
</p>

---

## 🛡️ What Is This?

RhodawkAI Edition fixes the deterministic plumbing *before* an LLM ever sees the data: scope enforcement, CDN classification, bounded reconFTW delegation, and canonical state fusion are all plain, auditable code — not prompt hopes. The model is only invited at the end, to rank an already-clean and already-honest attack surface, never to decide what runs.

- 🔒 **Fail-Closed Scope Gate (`0` packets on OOS):** Targets outside `--scope-domain` abort before any scanner runs — the engine refuses to send a single packet to an out-of-scope host.
- 🌐 **CDN & Origin Isolation:** Classifies live hosts into `CDN_EDGE` vs. `FIRST_PARTY_ORIGIN` via DNS CNAME/A + `httpx` tech tags, skipping `nmap` on CDN edges (`0s` / `0` packets wasted on Vercel/Cloudflare IPs).
- ⚙️ **Bounded `reconFTW` Gap-Fillers + Honest Telemetry:** Pins reconFTW (`3925211`) and invokes targeted `-c <fn>` modules in isolated workdirs instead of the monolithic `-r` run — printing a 6-row `tool_health` table (`COMPLETED_EMPTY`, `SKIPPED_SILENT`, `FAILED`) so nothing ever fails silently.
- 🧩 **Canonical State, Clustering & Diffs:** Fuses ~20 loose raw outputs into `recon_truth.json` (with SimHash host clustering so agents don't burn tokens on duplicate pages) + `delta.json` run-to-run diffs.
- 🩺 **Managed Chromium SPA Crawling & 5-Second Diagnostics:** A single managed Chromium (`bash install_tools.sh --browser`) powers `katana` SPA crawling, and `rhodawk doctor` verifies all 8 core binaries, reconFTW, Chromium, MCP imports, and live LLM connectivity in `<5s`.
- 🧠 **Open-Weight AI Prioritization:** Generates `recon_brief.md` via **NVIDIA NIM** or local **Ollama** — zero closed-model lock-in.

> [!IMPORTANT]
> **What it is *not* (yet):** Stages 1–2 recon & attack-surface prioritization are live today — **1,288 passing tests, green CI**. Sandboxed Docker exploit execution and a clean-room `pytest`/Playwright PoC validator are next on the roadmap. Until then RhodawkAI Edition is recon-only: it maps and prioritizes, it does not attack — and it never leaves your approved scope anyway.

---

## ⚡ Head-to-Head Benchmark

<img src="assets/benchmark.png" alt="Head-to-Head Benchmark" width="100%"/>

All three runners, same target (`rhodawkai.com`), same 8-vCPU / 32 GB Ubuntu VPS:

| Runner | Wall Time | Where the Time Went | Determinism & Telemetry |
|:---|:---|:---|:---|
| 🔴 `reconFTW (-r full recon @ 3925211)` | **`>31m` (hung)** | `9m 57s` OSINT (`third_party_misconfigs`), then hung `21m+` in `sub_brute` (`puredns`) | Killed manually; ignored `-o` and wrote to `Recon/` |
| 🟡 Original Agentic-Bug-Hunter | **`6m 45s`** (`6m44.7s`) | Wasted **`104.79s`** port-scanning the Vercel CDN edge `216.198.79.1` | Loose `.txt` files, no fail-closed scope gate, unclustered hosts, no `tool_health` |
| 🟢 RhodawkAI Edition | **`~5m 00s`** | **`0s` / `0` packets** on CDN edges; bounded `-c` gap-fillers (`0.4s–0.5s` each) | Fail-closed scope gate, `recon_truth.json` (`2` hosts → `1` SimHash cluster), `delta.json`, 6-row `tool_health`, NVIDIA NIM `recon_brief.md` |

---
---
<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="./benchmarks.md">📊 Live Benchmarks</a> •
  <a href="./CONTRIBUTING.md">Contributing</a> •
  <a href="./SECURITY.md">Security</a> •
  <a href="./LICENSE">MIT License</a>
</p>

---


## 🚀 Quick Start (5 Commands)


 # Python / PyPI (Recommended on Ubuntu 24.04 / Debian 12 / Kali)
```bash
pipx install agentic-bug-hunter-rhodawkai-edition

```
# Node.js / npm (CLI wrapper around the PyPI package)
``` bash
npm install -g agentic-bug-hunter-rhodawkai-edition
# or run directly:
npx agentic-bug-hunter-rhodawkai-edition doctor
```

```bash
# 1. Clone the brand repo + install the standalone agent (no subscription needed)
git clone https://github.com/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition.git && cd Agentic-Bug-Hunter-RhodawkaiEdition && ./install.sh --agent standalone

# 2. Install the external arsenal + the single managed Chromium (katana SPA crawling)
bash install_tools.sh && bash install_tools.sh --browser

# 3. Verify everything in <5 seconds
rhodawk doctor

# 4. Prove the fail-closed scope gate — an out-of-scope target aborts with 0 packets sent
rhodawk evil.example -recon --scope-domain "*.goodscope.example"

# 5. Run live, CDN-aware recon
rhodawk rhodawkai.com -recon --scope-domain "*.rhodawkai.com" --scope-domain "rhodawkai.com"
```

Then read the canonical truth — one JSON instead of 20 loose text files:

```bash
jq '{schema_version, counts, tool_health}' bughunter/recon/rhodawkai.com/recon_truth.json
cat bughunter/recon/rhodawkai.com/recon_brief.md
```

> [!TIP]
> No AI key yet? Steps 1–4 are fully deterministic and work with **zero** API keys — the AI layer only kicks in for `recon_brief.md` prioritization. Add **NVIDIA NIM** or **Ollama** whenever you're ready (next section).

---

## 🧠 Open-Weight & Multi-Provider AI

The same deterministic pipeline can write `recon_brief.md` through **NVIDIA NIM** (hosted open weights) or a fully local **Ollama** model — or any of the 16+ providers the multi-provider brain already speaks. Your recon data never depends on a closed model.

### 🥇 NVIDIA NIM — open weights, hosted

```bash
export NVIDIA_API_KEY="nvapi-your-key-here"   # free credits → https://build.nvidia.com
rhodawk setup --provider nvidia               # aliases: nim · nvidia-nim
rhodawk doctor                                # expect: [PASS] LLM provider nvidia — responded READY
```

- Default model: `nvidia/nemotron-3-ultra-550b-a55b`
- Self-hosting a NIM container? Point `NVIDIA_NIM_BASE_URL` at your own endpoint (default: `https://integrate.api.nvidia.com/v1`).

### 🥈 Ollama — 100% free, fully offline

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen2.5:14b                       # ~9 GB, one-time download
rhodawk setup --provider ollama --model qwen2.5:14b
```

After the pull, nothing ever leaves your machine — scope gate, fusion, and the AI brief all run locally.

### Also supported (auto-detected, free-first)

| Provider | Env var | Get a key |
|:---|:---|:---|
| **Groq** | `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) — free tier, very fast |
| **DeepSeek** | `DEEPSEEK_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com) — very cheap |
| **OpenRouter** | `OPENROUTER_API_KEY` | [openrouter.ai/keys](https://openrouter.ai/keys) — 100+ models, one key |
| **LiteLLM** | `LITELLM_API_KEY` (+ `LITELLM_BASE_URL`) | one gateway in front of keys you already own |
| **Claude API** | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| **OpenAI** | `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) |
| **Grok (xAI)** | `XAI_API_KEY` | [console.x.ai](https://console.x.ai) |
| **Nvidia** | `NVIDIA_API_KEY` | .[build.nvdia.com](https://build.nvdia.com).|

Providers are auto-detected free-first (**Ollama → Groq → DeepSeek → … → OpenRouter → Claude → OpenAI**); LiteLLM stays opt-in so it never preempts a provider you already configured. Switch anytime with `rhodawk setup` (interactive), `rhodawk setup --provider ollama --model qwen2.5:14b` (non-interactive), or inspect with `rhodawk providers` / `rhodawk models`.

---

## 🔧 Deterministic reconFTW Delegation

<details>
<summary><b>7 capability gaps filled by reconFTW <code>-c</code> modules — pinned <code>3925211</code>, isolated workdirs, honest telemetry</b></summary>
<br>

Wherever the built-in recon pipeline hits a capability it doesn't own, the routing decision is **deterministic code, not an LLM judgment call**: `bughunter/tools/rtw_adapter.py` decides what runs, identically across all four runtimes (CLI engine, ReAct agent, interactive harness, MCP server).

| Capability | reconFTW `-c` function | Pipeline slot |
|:---|:---|:---|
| ASN/CIDR enum (`CAP_ASN_ENUM`) | `sub_asn` | Phase 1.5 (before httpx) |
| DNS brute/permutation (`CAP_DNS_PERMUT`) | `sub_permut` | Phase 1.5 (before httpx) |
| CDN/origin isolation (`CAP_CDN_ISOLATE`) | `cdnprovider` | Phase 1.5 (before httpx) |
| JS source-map/AST secrets (`CAP_JS_SOURCEMAPS`) | `jschecks` | Phase 5.5 (before ffuf) |
| Virtual-host discovery (`CAP_VHOSTS`) | `virtualhosts` | Phase 5.5 (before ffuf) |
| TLS IP pivots (`CAP_TLS_PIVOTS`) | `tls_ip_pivots` | Phase 5.5 (before ffuf) |
| Favicon fingerprint (`CAP_FAVICON`) | `favirecon_tech` | Phase 5.5 (before ffuf) |

> [!TIP]
> **Guardrails, not vibes:** `install.sh` clones reconFTW at the pinned commit `3925211` and auto-persists `rtw_home` into `~/.bughunter/config.json` (override anytime with `RTW_HOME=...`). Each delegation runs one targeted `-c <fn>` module in an isolated workdir — never the monolithic `-r` — and every output file is scope-filtered post-call. `modules/vulns.sh` is never delegated: RhodawkAI's verifier spine stays the only thing allowed to promote a finding. Results are traced in `~/.bughunter/recon/<host>/rtw_manifest.json` (identical schema across runtimes, 7-day TTL), and the `tool_health` rows in `recon_truth.json` report every capability as `COMPLETED`, `COMPLETED_EMPTY`, `SKIPPED_SILENT`, or `FAILED`.

</details>

---

## 💻 CLI Commands, MCP & Project Structure

<details>
<summary><b>CLI reference · MCP setup · the real repository tree</b></summary>
<br>

`rhodawk` is the primary brand command; `bughunter` is the original engine command — same binary, same flags, pick your alias. Both are installed by `./install.sh --agent standalone`.

| Command | What it does |
|:---|:---|
| `rhodawk doctor` | <5s diagnostic — 8 core binaries, pinned reconFTW, managed Chromium, MCP import, live LLM `READY` probe |
| `rhodawk <target> -recon --scope-domain "*.example.com"` | CDN-aware recon — fail-closed scope gate → subdomain enum → httpx probe → CDN/origin split → bounded reconFTW → `recon_truth.json` + `delta.json` |
| `rhodawk <target> hunt` | ReAct hunt loop — tests IDOR · auth bypass · SSRF · XSS · SQLi · logic flaws and more |
| `rhodawk validate "<finding>"` | 7-Question Gate — kills weak findings before you waste time writing |
| `rhodawk report` | Submission-ready report for HackerOne · Bugcrowd · Intigriti · Immunefi |
| `rhodawk chat` | Interactive AI hunting shell |
| `rhodawk providers` / `rhodawk models` | List AI providers / models and show the active one |
| `rhodawk setup [--provider nvidia --model …]` | Connect or switch AI providers, fully scriptable |
| `rhodawk h <t>` / `r <t>` / `v "<f>"` | Short aliases for hunt / recon / validate |

### MCP — drive RhodawkAI from any agent

```text
AI Agent → RhodawkAI MCP → Scope → Recon → Hunt → Validate → Report
```

```bash
pip install 'mcp>=2.2.0'
./install.sh --agent mcp
bughunter mcp doctor     # verify the server imports + policy engine
bughunter mcp serve      # expose tools to Cursor · Claude Code · Codex · OpenCode
```

MCP is an adapter over the existing research engine — not a second scanner. Active tools require scope and explicit approval; full details in [docs/mcp.md](https://github.com/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition/blob/main/docs/mcp.md).

### Project structure (the real tree)

```text
Agentic-Bug-Hunter-RhodawkaiEdition/
├── assets/                    # rhodawk-banner · architecture · benchmark · logo (png/webp) · demo 1080p
├── bughunter/                 # the package
│   ├── engine.py              #   standalone CLI — the 'rhodawk' / 'bughunter' command
│   ├── brain.py               #   multi-provider LLM layer (NVIDIA NIM · Ollama · Groq · DeepSeek · …)
│   ├── agent.py               #   ReAct hunting agent
│   ├── agents/                #   9 specialist prompts (recon, validator, report-writer, …)
│   ├── mcp/                   #   native MCP server + Burp / Caido / HackerOne clients
│   ├── memory/                #   cross-session hunt memory (pattern DB · audit log · rotation)
│   ├── tools/                 #   scanner pipeline — recon_engine.sh · recon_fusion.py · rtw_adapter.py · …
│   └── wordlists/             #   curated wordlists
├── tests/                     # 1,288-test pytest suite — no network, no API keys required
├── commands/                  # slash-command references (/recon /hunt /validate /report …)
├── skills/                    # AI knowledge bases loaded by agent harnesses
├── docs/                      # extended docs (mcp.md · CAPABILITY-GAPS.md · TUTORIAL.md · …)
├── .github/workflows/ci.yml   # green CI gate: bash -n + pytest -q on every push/PR
├── install.sh                 # standalone install · pinned reconFTW clone · 'rhodawk' alias
├── install_tools.sh           # subfinder · httpx · nuclei · katana · ffuf · nmap · … + --browser Chromium
├── pyproject.toml             # package metadata — agentic-bug-hunter-rhodawkai-edition 6.1.0
└── requirements.txt           # requests · pytest · mcp
```

</details>

---

## 🤝 Operational Rules & Contributing

**Operational rules** — the non-negotiables:

1. **Scope first, always.** Every run requires `--scope-domain`; the gate is fail-closed and aborts before any scanner fires (`0` packets on OOS).
2. **Recon-only today.** Exploit execution is roadmap, not reality — never point the agent at anything you're not authorized to test.
3. **Honest telemetry or nothing.** A capability that came back `SKIPPED_SILENT` or `FAILED` is printed in the `tool_health` table — never swallowed.
4. **Validate before report.** Weak findings die at the 7-Question Gate, not at a triager's desk.
5. **Impact first.** Test the bugs with the worst consequences before the clever ones.

**Contributing** — four lines from clone to green CI:

```bash
git clone https://github.com/Rhodawk-AI/Agentic-Bug-Hunter-RhodawkaiEdition.git && cd Agentic-Bug-Hunter-RhodawkaiEdition
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
bash -n bughunter/tools/recon_engine.sh install.sh install_tools.sh && pytest -q   # 1,288 tests, no network needed
git checkout -b feat/your-contribution && git commit -m "feat: short description" && git push   # open the PR 🚀
```

---

## ❤️ Acknowledgments & Branded Footer

RhodawkAI Edition stands on the shoulders of open-source builders:

- **[Agentic-Bug-Hunter](https://github.com/Awarexone/Agentic-Bug-Hunter)** by **AwareXone** — the original MIT framework this edition hardens and extends.
- **[reconFTW](https://github.com/six2dez/reconftw)** by **six2dez** — the modular `-c <fn>` recon capabilities behind our bounded delegation.
- **[ProjectDiscovery](https://github.com/projectdiscovery) & the Open-Source Security Community** — [`subfinder`](https://github.com/projectdiscovery/subfinder) · [`httpx`](https://github.com/projectdiscovery/httpx) · [`katana`](https://github.com/projectdiscovery/katana) · [`nuclei`](https://github.com/projectdiscovery/nuclei) · [`ffuf`](https://github.com/ffuf/ffuf) · [`gau`](https://github.com/lc/gau) · [`nmap`](https://nmap.org) · [Playwright](https://playwright.dev/python/).

<div align="center">

<a href="https://rhodawkai.com"><img src="assets/rhodawkai-logo.webp" alt="RhodawkAI" width="160"/></a>

🌐 **[rhodawkai.com](https://rhodawkai.com)** · 🐙 **[github.com/Rhodawk-AI](https://github.com/Rhodawk-AI)** · ✉️ **[manager@rhodawkai.com](mailto:manager@rhodawkai.com)**

**Made with ♥ · Telegram [@rhodawk1](https://t.me/rhodawk1)**

<sub>MIT License · For authorized security testing only. Always test within an approved bug bounty program scope.</sub>

</div>
