# MrSpec

MrSpec is the hosted MadeForMachine product for service-backed Specifold specs. It stores
the canonical spec in the MFM service, exposes minimal-context reads and fine-grained
validated mutations through MCP, and keeps revision history in the service database.

Use `specifold` for local file-backed specs. Use `mrspec` when the `mrspec_*` MCP tools are
available and the user wants a hosted, versioned spec memory.

## Status

Alpha and not public. The skill names the intended MCP surface while the product spec leads
the implementation.
