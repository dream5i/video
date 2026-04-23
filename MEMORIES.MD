# Project Memories

## Project goal

- Build an AI workflow product for ecommerce short videos that turns a winning video link or product brief into analysis, script, shot plan, and a prefilled generation workflow.

## Decisions

- Start from a neutral scaffold.
- Treat `全新项目` as the only active project line in this workspace.
- Use `SoraTK` as the first reference competitor for AI ecommerce video workflow products.
- Keep a second-layer market document that combines hands-on competitor testing with public market and GitHub research.
- Define the first product scope around the shortest usable loop: intake -> analysis -> prefilled workflow -> result.
- Use a prefilled storyboard-style workflow instead of a blank node canvas for the MVP UX.
- Recommend a split architecture: Next.js web, FastAPI API, Redis-backed workers, PostgreSQL, and S3-compatible object storage.
- Reuse bottom-layer media tools and selected MIT-friendly implementation ideas, but keep product UX, domain models, state machine, storyboard schema, and provider adapters as core self-built layers.
- Treat GPL/AGPL reference projects as architecture inspiration or sidecar candidates, not as default code-level dependencies for the core product.
- For the engineering stack, choose an OpenAI-first, Anthropic-compatible, Harness-later strategy: OpenAI as primary AI coding/agent substrate, Anthropic as secondary/reviewer/fallback path, and Harness as a later platform-engineering layer rather than an MVP-critical dependency.
- Use a main-controller operating model: the main agent owns architecture, integration, and final review; sub-agents are used only for bounded non-overlapping tasks; high-risk changes get an extra review pass; scaffold and shared contracts start single-threaded.
- Freeze the first implementation line around repository governance, shared contract stability, storyboard schema stability, and an OpenAI-first provider path before expanding product features.
- Keep the MVP main flow explicit and fixed as: intake -> analysis -> prefilled workflow -> run -> result -> history.
- If the target shifts toward enterprise-grade delivery, prioritize evals, tracing/audit, auth/roles, budget and rate-limit control, prompt/version governance, and data-retention policy before expanding feature breadth.
- For enterprise AI coding governance, explicitly define do-not-feed data boundaries, command allow/prompt/deny layers, cloud-vs-local usage limits, human approval gates for high-risk changes, OSS/license controls, and evidence/audit requirements for AI-generated code.
- Treat “highest permissions” as controlled local execution ability rather than unlimited authority: keep production access, data boundaries, plugin/MCP scope, and final approvals under explicit governance.
- The current documentation set is sufficient to support long-term project building on the main line, but it still needs continued补齐 around ADRs, database design, testing, release/runbook docs, and eventual workspace path normalization.

## Next action

- Initialize git, clean generated artifacts, and continue contract/provider scaffolding against the frozen roadmap.
