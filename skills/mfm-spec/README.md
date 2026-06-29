# MFM Spec

MFM Spec is the hosted MadeForMachine product for service-backed MFM Specs. It stores
the canonical spec in the MFM service, exposes minimal-context reads and fine-grained
validated mutations through MCP, and keeps revision history in the service database.

Use `mfm-spec-local` for local file-backed specs. Use `mfm-spec` when the `mfm_spec_*`
MCP tools are available and the user wants a hosted, versioned spec memory.

## Status

Alpha and not public. The skill names the intended MCP surface while the product spec leads
the implementation.
