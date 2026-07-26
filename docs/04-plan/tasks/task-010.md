# Task 010: Add Fan-Out and Send Examples
**Status:** done
**Priority:** medium
**Assigned:** unassigned
**Blocked by:** —
**Effort:** S
**Created:** 2026-06-11
**Completed:** 2026-06-11

## Description
Add two runnable example scripts: one demonstrating static fan-out (`target: [list]`) and one demonstrating dynamic routing with `Send`. Currently only quickstart (linear) and conditional routing are covered. These two gap-filling examples let users see and run every edge type the library supports.

## Acceptance Criteria
- [x] `examples/fan_out/workflow.yaml` + `examples/fan_out/main.py` — static parallel fan-out
- [x] `examples/dynamic_routing/workflow.yaml` + `examples/dynamic_routing/main.py` — Send-based fan-out
- [x] Both scripts run successfully with `python3 examples/<name>/main.py`
- [x] Output clearly shows parallel branches executing
- [x] No new dependencies added

## Files
- `examples/fan_out/workflow.yaml` (create)
- `examples/fan_out/main.py` (create)
- `examples/dynamic_routing/workflow.yaml` (create)
- `examples/dynamic_routing/main.py` (create)

## Notes
- Keep examples minimal — just enough to demonstrate the feature, not a production app
- Fan-out example: 1 source node fans out to 2-3 parallel nodes, then converges
- Send example: router dynamically decides which nodes to invoke with custom state per Send
- Use `MessagesState` for consistency with existing examples
