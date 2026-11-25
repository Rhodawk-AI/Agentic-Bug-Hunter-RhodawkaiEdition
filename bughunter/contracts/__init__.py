"""Typed data contracts shared across BugHunter pipelines.

Commit 2 introduces the scope contract: a deterministic, hashed,
self-verifying representation of a bug-bounty program's scope that the
compiler (`bughunter/tools/scope_compiler.py`) produces and every downstream
consumer (recon gate, scope checker, MCP servers) can trust byte-for-byte.
"""

from .scope import CompiledScopeManifest, ScopeAssetMeta

__all__ = ["CompiledScopeManifest", "ScopeAssetMeta"]
