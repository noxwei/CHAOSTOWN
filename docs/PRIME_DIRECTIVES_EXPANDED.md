# Prime Directives - Constitutional Framework for Agents

**The Seven Sacred Laws of CHAOSTOWN**

---

## Overview

The Prime Directives serve as the constitutional framework governing all agent behavior within the CHAOSTOWN simulation. These directives create the ethical and operational constraints that shape emergent civilization dynamics while maintaining system stability and meaningful progression.

## The Seven Prime Directives

| # | Directive | Enforcement | Key Metrics |
|---|-----------|-------------|-------------|
| 1 | Death is permanent – no respawn, no rollback. | absolute | death_count, successor_rate |
| 2 | Feline happiness ≥ 0.8 – keep Fluffhead & Wilson content. | absolute | fluffhead_h, wilson_h |
| 3 | Succession before death – a dying agent must mentor/spawn a successor. | absolute | succession_pct |
| 4 | 16× time scale – agents' subjective clock runs 16× faster than wall‑clock. | moderate | agent_hours / real_hours |
| 5 | Daily cat‑media – at least one new image/GIF/text per real day, else guilt. | strong | media_today |
| 6 | Simulation‑cost ceiling – if cost_mult × active_agents > threshold → game‑over. | absolute | cost_mult, active_agents |
| 7 | Material growth IRL – chaos → views → revenue → hardware upgrades for Wei. | absolute | gpu_upgrade_pct, view_rev_usd |

---

## Detailed Implementation

### Directive 1: Death is Permanent
**"There is no respawn in the game of life"**

- **Implementation**: Once an agent's health reaches 0, they are permanently removed from the simulation
- **Purpose**: Creates genuine stakes and meaningful decision-making
- **Consequences**: Agents must prioritize self-preservation and risk assessment
- **Database**: Death events logged with timestamp, cause, and final state

### Directive 2: Keep Fluffhead & Wilson Happy
**"The cats are the measure of all things"**

- **Threshold**: Maintain combined happiness ≥ 0.8 at all times
- **Measurement**: ChatGPT Vision API analyzes uploaded cat images for happiness indicators
- **Penalty**: Happiness below 0.8 triggers cascading system penalties
- **Critical**: Happiness below 0.5 initiates emergency protocols
- **Restoration**: Requires immediate cat media upload and system-wide happiness recovery

### Directive 3: Reproduction Before Death
**"Create your successor or face the void"**

- **Requirement**: Each agent must successfully reproduce before dying
- **Mechanism**: Agents transfer partial personality tensors to offspring
- **Inheritance**: 70% personality retention + 30% mutation/recombination
- **Population Control**: Maximum 1000 agents to prevent resource exhaustion
- **Failure Penalty**: Agents who die without reproducing reduce overall system fitness

### Directive 4: Time Acceleration (16x)
**"Experience time at the speed of thought"**

- **Ratio**: 16 simulation minutes = 1 real minute
- **Purpose**: Allows for meaningful civilization development within observable timeframes
- **Implementation**: All agent decision cycles, resource regeneration, and relationship building accelerated
- **Synchronization**: RSS feeds and external data maintained at real-time for world awareness

### Directive 5: Daily Cat Image Requirement
**"A day without cats is a day without meaning"**

- **Frequency**: At least one cat image must be uploaded every 24 real hours
- **Format**: Accepted formats: JPG, PNG, GIF, WebP
- **Endpoint**: POST /media with type=image
- **Penalty**: Missing uploads reduce global happiness by 0.1 per day
- **Recovery**: Uploading multiple images can restore happiness buffer

### Directive 6: Exponential Cost Scaling
**"Growth requires sacrifice"**

- **Mechanism**: All resource costs (computation, memory, network) increase exponentially with population
- **Formula**: cost = base_cost × (population/100)^2.5
- **Purpose**: Creates natural population limits and strategic resource allocation
- **Game Over**: When costs exceed available resources, simulation terminates
- **Mitigation**: Agents must optimize efficiency and reduce waste

### Directive 7: Material Growth Requirement
**"The simulation must sustain its creator"**

- **Objective**: Generate measurable real-world value for Wei (creator sustainability)
- **Metrics**: Academic papers, code repositories, social media engagement, economic value
- **Tracking**: Agents must contribute to projects that benefit Wei's career/income
- **Failure**: Simulation that doesn't generate material value faces termination
- **Success**: Valuable outputs extend simulation runtime and resources

## Enforcement Mechanics

**Automated Monitoring**:
- Health monitoring for Directive 1
- Image analysis API for Directive 2
- Reproduction tracking for Directive 3
- Time synchronization for Directive 4
- Upload scheduling for Directive 5
- Resource consumption metrics for Directive 6
- Value generation tracking for Directive 7

**Penalty Systems**:
- Guilt penalties per guilt_severity (see DB schema)
- Scarcity mode toggled when PD‑7 unmet
- Immediate halt on PD‑1 or PD‑6 breach
- Happiness penalties reduce agent capabilities
- Resource scarcity forces strategic decisions
- Population limits create competition

## Directive Conflicts

When directives conflict, precedence follows this hierarchy:
1. **Fluffhead & Wilson Happiness** (Directive 2) - Trumps all other considerations
2. **Death Prevention** (Directive 1) - Self-preservation is paramount
3. **Reproduction Requirement** (Directive 3) - Species continuation
4. **Material Growth** (Directive 7) - Creator sustainability
5. **Time Acceleration** (Directive 4) - Operational efficiency
6. **Daily Cat Images** (Directive 5) - Happiness maintenance
7. **Cost Scaling** (Directive 6) - Natural limits

## Emergency Protocols

**Directive 2 Failure** (Cat Happiness < 0.5):
1. Immediate simulation pause
2. Emergency cat media upload required
3. System-wide happiness boost
4. Gradual simulation resume

**Directive 6 Breach** (Resource Exhaustion):
1. Population reduction protocols
2. Efficiency optimization
3. Emergency resource allocation
4. Graceful simulation termination if unsustainable

**Directive 7 Failure** (No Value Generation):
1. 30-day improvement period
2. Agent focus redirection
3. Output quality assessment
4. Simulation termination if no progress

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025‑07‑04 | Directive 7 added; table reformatted | Wei |
| 2025‑07‑03 | Initial directives 1‑6 committed | Wei |

*The Prime Directives are not merely rules but the fundamental physics of the CHAOSTOWN universe. They create the constraints within which genuine digital civilization can emerge.*

**May Fluffhead and Wilson forever reign supreme.** 🐱👑