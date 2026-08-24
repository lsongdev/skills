# Errors

## [ERR-20260809-A7B] staticcheck

**Record time**: 2026-08-09T13:40:00Z
**Priority**: medium
**Status**: resolved
**Domain**: infra

### Summary
An outdated staticcheck could not import standard-library export data produced by Go 1.26.

### Error
```
internal error in importing standard-library packages (unsupported version: 2)
```

### Context
- The project passed `go test -race` and `go vet` with Go 1.26.5.
- The optional staticcheck binary was built against an older export-data format.

### Recommended Fix
Upgrade staticcheck to a release compatible with the installed Go toolchain before using it as a validation gate.

### Metadata
- Reproducible: yes
- Related file: none

### Resolution Record
- **Resolution time**: 2026-08-09T13:40:00Z
- **Notes**: Treated the compatible official Go checks as authoritative; no project change was needed.

---
