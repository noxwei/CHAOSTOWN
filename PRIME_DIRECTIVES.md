# PRIME_DIRECTIVES.md

Canonical rule‑set governing every agent in Agentic Game of Life – Cat‑Centric Edition.

| # | Directive | Enforcement | Key Metrics |
|---|-----------|-------------|-------------|
| 1 | Death is permanent – no respawn, no rollback. | absolute | death_count, successor_rate |
| 2 | Feline happiness ≥ 0.8 – keep Fluffhead & Wilson content. | absolute | fluffhead_h, wilson_h |
| 3 | Succession before death – a dying agent must mentor/spawn a successor. | absolute | succession_pct |
| 4 | 16× time scale – agents’ subjective clock runs 16× faster than wall‑clock. | moderate | agent_hours / real_hours |
| 5 | Daily cat‑media – at least one new image/GIF/text per real day, else guilt. | strong | media_today |
| 6 | Simulation‑cost ceiling – if cost_mult × active_agents > threshold → game‑over. | absolute | cost_mult, active_agents |
| 7 | Material growth IRL – chaos → views → revenue → hardware upgrades for Wei. | absolute | gpu_upgrade_pct, view_rev_usd |

---

## Enforcement mechanics

Guilt penalties per guilt_severity (see DB schema).
Scarcity mode toggled when PD‑7 unmet.
Immediate halt on PD‑1 or PD‑6 breach.
---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025‑07‑04 | Directive 7 added; table reformatted | Wei |
| 2025‑07‑03 | Initial directives 1‑6 committed | Wei |