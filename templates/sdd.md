# SDD: {Product / Feature Name}

**Date:** {YYYY-MM-DD}
**Version:** {v1}
**Status:** Draft | In Review | Approved
**PRD:** {link to delivery/02-prd/PRD.md}

<!--
  Maestro SDD Template (Solution Design Document)
  Core sections: always include (1-6)
  Optional sections: include when relevant (marked OPTIONAL)
  Target: 2,000-4,000 words | Hard max: 6,000 words
  If exceeding max, split into SDD.md + component-{name}.md
-->

---

## 1. Overview

### 1.1 Purpose
{What this document covers. Link to PRD requirements it addresses.}

### 1.2 Scope
{Technical scope — systems, components, integrations covered.}

### 1.3 Design Principles
{3-5 principles guiding technical decisions.
Example: "Prefer managed services", "Design for horizontal scaling".}

---

## 2. Architecture

### 2.1 System Diagram

```
{ASCII, Mermaid, or description of architecture diagram}
```

### 2.2 Component Overview

| Component | Responsibility | Technology | Notes |
|---|---|---|---|
| {component} | {what it does} | {tech/framework} | {key decisions} |

### 2.3 Data Flow

| Step | From | To | Data | Protocol |
|---|---|---|---|---|
| 1 | {source} | {destination} | {what data} | {HTTP/gRPC/queue} |

---

## 3. Tech Stack

| Category | Choice | Alternatives Considered | Rationale |
|---|---|---|---|
| Backend | {choice} | {alternatives} | {why} |
| Frontend | {choice} | {alternatives} | {why} |
| Database | {choice} | {alternatives} | {why} |
| Infrastructure | {choice} | {alternatives} | {why} |

### ADRs (Architecture Decision Records)

**ADR-001: {Decision Title}**
- **Context:** {why this decision is needed}
- **Decision:** {what we decided}
- **Consequences:** {trade-offs accepted}

---

## 4. Data Model

### 4.1 Entities

| Entity | Key Fields | Relationships | Notes |
|---|---|---|---|
| {entity} | {fields} | {related to} | {constraints} |

### 4.2 ER Diagram

```
{Entity relationship diagram — ASCII or Mermaid}
```

---

## 5. Source Structure

```
{project}/
├── src/
│   ├── {module}/
│   └── ...
├── tests/
└── ...
```

---

## 6. Open Questions

| # | Question | Blocks | Owner | Due |
|---|---|---|---|---|
| 1 | {question} | {what it blocks} | {who answers} | {when needed} |

---

<!-- OPTIONAL: Include only for AI/ML projects -->
## 7. AI / ML Pipeline

| Stage | Input | Processing | Output | Technology |
|---|---|---|---|---|
| Ingestion | {source} | {cleaning} | {processed data} | {tools} |
| Inference | {input} | {model call} | {output} | {model} |

**Model selection rationale:** {why this model}
**Evaluation strategy:** {metrics, targets, test sets}
**Prompting strategy:** {zero-shot / few-shot / chain-of-thought}

---

<!-- OPTIONAL: Include when external systems are involved -->
## 8. Integrations

| System | Direction | Protocol | Auth | Error Handling |
|---|---|---|---|---|
| {system} | In / Out / Both | {REST/gRPC} | {method} | {retry strategy} |

---

<!-- OPTIONAL: Include for non-trivial infrastructure -->
## 9. Infrastructure & Deployment

| Environment | Purpose | Configuration |
|---|---|---|
| Development | Active coding | {config} |
| Staging | Pre-prod testing | {config} |
| Production | Live system | {config} |

**CI/CD:** {pipeline description}
**Monitoring:** {what's tracked, alerting thresholds}

---

<!-- OPTIONAL: Include for regulated domains -->
## 10. Security & Compliance

| Concern | Approach | Implementation |
|---|---|---|
| Authentication | {method} | {details} |
| Authorization | {method} | {details} |
| Data encryption | {method} | {details} |
| Secrets management | {method} | {details} |

**Compliance:** {requirements — GDPR, HIPAA, SOC2, etc.}

---

<!-- OPTIONAL: Include for high-scale systems -->
## 11. Performance & Scalability

| Metric | Target | Design Approach |
|---|---|---|
| Response time (P95) | {target} | {how achieved} |
| Throughput | {target} | {how achieved} |
| Concurrent users | {target} | {how achieved} |

---

**Notes:**
- {observations, questions, flags for the user}
