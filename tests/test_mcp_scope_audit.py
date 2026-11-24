"""MCP self-authorization transparency (DD follow-up).

bughunter_run_rtw_capability lets the MCP CALLER supply scope_domains
(server.py POLICY.set_scope(scope_domains or [target])) — the server
trusts the caller's scope declaration. Behavior is unchanged by design,
but the caller-supplied scope must be (a) documented and (b) logged to
the audit log.
"""

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MCP_DIR = REPO_ROOT / "bughunter" / "mcp" / "bughunter-mcp"


def _load_server():
    for p in (str(REPO_ROOT), str(MCP_DIR)):
        if p not in sys.path:
            sys.path.insert(0, p)
    import server  # noqa: PLC0415
    return server


def test_docs_mcp_documents_caller_supplied_scope():
    docs = (REPO_ROOT / "docs" / "mcp.md").read_text()
    assert "scope_domains" in docs
    assert "caller" in docs.lower()
    assert "self-author" in docs.lower() or "trusts the caller" in docs.lower()


def test_caller_supplied_scope_logged_to_audit(tmp_path, monkeypatch):
    server = _load_server()
    audit = tmp_path / "hunt-memory" / "audit.jsonl"
    monkeypatch.setenv("BUGHUNTER_AUDIT_FILE", str(audit))
    server._audit_caller_scope(
        "bughunter_run_rtw_capability", "CAP_DNS_PERMUT",
        "target.goodscope.example", ["*.goodscope.example"])
    entry = json.loads(audit.read_text().splitlines()[-1])
    assert entry["caller_scope_domains"] == ["*.goodscope.example"]
    assert entry["capability_id"] == "CAP_DNS_PERMUT"
    assert "bughunter_run_rtw_capability" in entry["error"]


def test_audit_failure_never_raises(tmp_path, monkeypatch):
    server = _load_server()
    monkeypatch.setenv("BUGHUNTER_AUDIT_FILE",
                       str(tmp_path / "nope" / "dir" / "audit.jsonl"))
    # parent dir does not exist and cannot be created (file in the way)
    blocker = tmp_path / "nope"
    blocker.write_text("not a dir")
    server._audit_caller_scope("t", "CAP_X", "x.example", ["*.x.example"])
