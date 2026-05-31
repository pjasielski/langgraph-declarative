# Changelog

## v0.1.0 (2026-05-31)

Initial release.

### Features

- **Registry** -- `@registry.node()` and `@registry.router()` decorators for function registration
- **YAML graph definition** -- declare nodes and edges in YAML
- **All edge types** -- simple, fan-out (parallel), conditional (mapped routing), dynamic (Send)
- **Schema validation** -- Pydantic-based YAML validation with clear error messages
- **Cross-validation** -- checks function/router refs exist, edge targets reference defined nodes
- **Typo suggestions** -- `difflib`-based "did you mean?" on lookup failures
- **`build_graph()`** -- one-line convenience function for YAML-to-compiled-graph
- **`GraphBuilder`** -- power-user class for more control over compilation
- **Default `MessagesState`** -- chatbot graphs need no explicit state class
