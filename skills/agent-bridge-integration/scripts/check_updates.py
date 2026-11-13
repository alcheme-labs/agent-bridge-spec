#!/usr/bin/env python3
"""Read public GitHub releases; persist local check/notice decisions, never install."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import http.client
import json
import math
import os
from pathlib import Path
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

SKILL_DIR = Path(__file__).resolve().parent.parent
VERSION_PATTERN = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")
REPOSITORY_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9_.-]{1,100}\Z")
MAX_PAGE_BYTES = 2 * 1024 * 1024
NOTICE_LEASE = 15 * 60


class CheckError(Exception):
    pass


def version(value):
    if not isinstance(value, str) or not VERSION_PATTERN.fullmatch(value):
        raise CheckError("invalid_version")
    return tuple(int(n) for n in value.split("."))


def load_source(path):
    source = json.loads(Path(path).read_text(encoding="utf-8"))
    repository = source.get("repository")
    prefix = source.get("tag_prefix")
    interval = source.get("check_interval_hours")
    if repository is not None and (not isinstance(repository, str) or not REPOSITORY_PATTERN.fullmatch(repository)):
        raise CheckError("invalid_repository")
    if not isinstance(prefix, str) or not re.fullmatch(r"[A-Za-z0-9-]{1,80}", prefix):
        raise CheckError("invalid_tag_prefix")
    if isinstance(interval, bool) or not isinstance(interval, (float, int)) or not math.isfinite(interval) or interval <= 0:
        raise CheckError("invalid_check_interval")
    return {"repository": repository.lower() if repository else None,
            "tag_prefix": prefix, "check_interval_hours": interval}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_releases(source):
    """Only fixed HTTPS GitHub API URLs; all remote text remains data."""
    opener = urllib.request.build_opener(NoRedirect())
    deadline = time.monotonic() + 15
    releases = []
    for page in range(1, 6):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise CheckError("network_timeout")
        url = f"https://api.github.com/repos/{source['repository']}/releases?per_page=100&page={page}"
        request = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2026-03-10",
            "User-Agent": "agent-bridge-integration-update-check"})
        try:
            with opener.open(request, timeout=min(5, remaining)) as response:
                chunks, length = [], 0
                while True:
                    if time.monotonic() >= deadline:
                        raise CheckError("network_timeout")
                    chunk = response.read1(min(65536, MAX_PAGE_BYTES + 1 - length))
                    if not chunk:
                        break
                    chunks.append(chunk)
                    length += len(chunk)
                    if length > MAX_PAGE_BYTES:
                        raise CheckError("response_too_large")
                payload = b"".join(chunks)
                if getattr(response, "length", None) not in (None, 0):
                    raise CheckError("incomplete_http_response")
            if len(payload) > MAX_PAGE_BYTES:
                raise CheckError("response_too_large")
            items = json.loads(payload)
        except urllib.error.HTTPError as error:
            code = error.code
            error.close()
            raise CheckError(f"github_http_{code}") from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise CheckError("network_unavailable") from None
        except http.client.HTTPException:
            raise CheckError("invalid_http_response") from None
        except (ValueError, UnicodeError):
            raise CheckError("invalid_response") from None
        if time.monotonic() > deadline:
            raise CheckError("network_timeout")
        if not isinstance(items, list) or len(items) > 100:
            raise CheckError("invalid_response")
        releases.extend(items)
        if len(items) < 100:
            return releases
    raise CheckError("release_list_incomplete")


def select_releases(items, source):
    selected = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("tag_name"), str):
            raise CheckError("invalid_response")
        if not isinstance(item.get("draft"), bool) or not isinstance(item.get("prerelease"), bool):
            raise CheckError("invalid_response")
        tag = item["tag_name"]
        if item["draft"] or item["prerelease"] or not tag.startswith(source["tag_prefix"]):
            continue
        candidate = tag[len(source["tag_prefix"]):]
        if not VERSION_PATTERN.fullmatch(candidate):
            continue
        body = "" if item.get("body") is None else item["body"]
        title = tag if item.get("name") is None else item["name"]
        if not isinstance(body, str) or not isinstance(title, str):
            raise CheckError("invalid_response")
        selected[candidate] = {"version": candidate, "tag": tag, "title": title[:300],
            "url": f"https://github.com/{source['repository']}/releases/tag/{urllib.parse.quote(tag, safe='')}",
            "notes": body[:4000], "notes_truncated": len(body) > 4000}
    return sorted(selected.values(), key=lambda r: version(r["version"]), reverse=True)


def state_path(source, root=None):
    if root is None:
        base = os.environ.get("XDG_STATE_HOME")
        root = (Path(base) if base else Path.home() / ".local" / "state") / "agent-bridge-integration"
    root = Path(root).expanduser().absolute()
    repository_root = SKILL_DIR.parent.parent
    if root.resolve() == repository_root or repository_root in root.resolve().parents:
        raise CheckError("state_directory_must_be_outside_repository")
    key = hashlib.sha256(f"{source['repository']}:{source['tag_prefix']}".encode()).hexdigest()[:24]
    return root / f"{key}.json"


@contextlib.contextmanager
def locked(path):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(path.with_suffix(".lock")), flags, 0o600)
    try:
        if os.name == "nt":
            import msvcrt
            if os.fstat(fd).st_size == 0:
                os.write(fd, b"0")
            os.lseek(fd, 0, os.SEEK_SET)
            try:
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            except OSError:
                raise CheckError("check_in_progress") from None
        else:
            import fcntl
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise CheckError("check_in_progress") from None
        yield
    finally:
        os.close(fd)


def read_state(path, source):
    if path.is_symlink():
        raise CheckError("state_file_is_symlink")
    if not path.exists():
        return {"schema": 1, "source": source, "next_check_at": 0, "releases": [], "decisions": {}}
    if path.stat().st_size > 4 * 1024 * 1024:
        raise CheckError("state_too_large")
    state = json.loads(path.read_text(encoding="utf-8"))
    # Interval is a local policy: changing it does not reset notice decisions.
    if (not isinstance(state, dict) or state.get("schema") != 1 or
            not isinstance(state.get("source"), dict) or
            any(state["source"].get(k) != source[k] for k in ("repository", "tag_prefix")) or
            not isinstance(state.get("releases"), list) or not isinstance(state.get("decisions"), dict)):
        raise CheckError("invalid_state")
    for field in ("next_check_at", "last_checked_at", "last_attempt_at"):
        if field in state and (type(state[field]) not in (int, float) or not math.isfinite(state[field])):
            raise CheckError("invalid_state")
    for release in state["releases"]:
        version(release["version"])
        if any(not isinstance(release.get(k), str) for k in ("tag", "title", "url", "notes")):
            raise CheckError("invalid_state")
    for target, entry in state["decisions"].items():
        version(target)
        if not isinstance(entry, dict) or entry.get("decision") not in ("notified", "ignore", "later"):
            raise CheckError("invalid_state")
        if entry["decision"] == "later" and (type(entry.get("until")) not in (int, float) or not math.isfinite(entry["until"])):
            raise CheckError("invalid_state")
    pending = state.get("pending_notice")
    if pending is not None:
        if (not isinstance(pending, dict) or not isinstance(pending.get("id"), str) or
                type(pending.get("until")) not in (int, float) or not math.isfinite(pending["until"])):
            raise CheckError("invalid_state")
        version(pending.get("version"))
    return state


def save_state(path, state):
    fd, temporary = tempfile.mkstemp(prefix=".update-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(state, output, ensure_ascii=False, indent=2, allow_nan=False)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def check(source, installed, root=None, force=False, fetch=fetch_releases, now=None):
    now = time.time() if now is None else now
    version(installed)
    if not source["repository"]:
        return {"status": "not_configured", "notify": False, "installed_version": installed}
    path = state_path(source, root)
    with locked(path):
        state = read_state(path, source)
        if now < state.get("last_attempt_at", 0):
            # Only an unacknowledged lease loses its clock basis; durable user
            # choices and acknowledged notices remain valid after a clock jump.
            state.pop("pending_notice", None)
        if state["source"].get("check_interval_hours") != source["check_interval_hours"]:
            delay = 3600 if state.get("last_error") else source["check_interval_hours"] * 3600
            state["next_check_at"] = state.get("last_attempt_at", 0) + delay
            state["source"] = source
        cached = not force and state.get("last_attempt_at", 0) <= now < state["next_check_at"]
        if not cached:
            state["last_attempt_at"] = now
            try:
                state["releases"] = select_releases(fetch(source), source)
            except CheckError as error:
                state["last_error"] = str(error)
                state["next_check_at"] = now + 3600
                save_state(path, state)
                return {"status": "check_failed", "notify": False, "reason": str(error)}
            state["last_checked_at"] = now
            state["next_check_at"] = now + source["check_interval_hours"] * 3600
            state.pop("last_error", None)
        result = {"status": "up_to_date", "notify": False, "installed_version": installed,
            "cached": cached, "last_checked_at": state.get("last_checked_at"),
            "state_file": str(path)}
        if state.get("last_error"):
            return {**result, "status": "check_failed", "reason": state["last_error"]}
        newer = [r for r in state["releases"] if version(r["version"]) > version(installed)]
        if not newer:
            if not state["releases"]:
                result["status"] = "no_skill_release"
            elif version(installed) > version(state["releases"][0]["version"]):
                result["status"] = "local_ahead"
        else:
            latest = newer[0]
            result.update(status="update_available", latest=latest, changes=newer[:10],
                          omitted_release_count=max(0, len(newer) - 10))
            decision = state["decisions"].get(latest["version"], {})
            pending = state.get("pending_notice") or {}
            if decision.get("decision") in ("notified", "ignore"):
                result["suppressed_by"] = decision["decision"]
            elif decision.get("decision") == "later" and now < decision["until"]:
                result["suppressed_by"] = "later"
            elif pending.get("version") == latest["version"] and now < pending.get("until", 0):
                result["suppressed_by"] = "pending_display"
            else:
                notice_id = uuid.uuid4().hex
                state["pending_notice"] = {"version": latest["version"], "id": notice_id,
                                           "until": now + NOTICE_LEASE}
                result.update(notify=True, notice_id=notice_id)
        save_state(path, state)
        return result


def record(source, target, decision, root=None, notice_id=None, days=7, now=None):
    now = time.time() if now is None else now
    version(target)
    if not source["repository"]:
        raise CheckError("source_not_configured")
    if decision not in ("notified", "ignore", "later"):
        raise CheckError("invalid_decision")
    if not math.isfinite(days) or days <= 0:
        raise CheckError("invalid_snooze_days")
    path = state_path(source, root)
    with locked(path):
        state = read_state(path, source)
        if target not in {r["version"] for r in state["releases"]}:
            raise CheckError("unknown_release")
        pending = state.get("pending_notice") or {}
        previous = state["decisions"].get(target, {})
        if decision == "notified" and notice_id and previous.get("notice_id") == notice_id:
            return {"status": "recorded", "version": target, "decision": decision, "notify": False, "duplicate": True}
        if decision == "notified" and (not notice_id or pending.get("id") != notice_id or pending.get("version") != target):
            raise CheckError("notice_does_not_match")
        state["decisions"][target] = {"decision": decision, "at": now,
                                     **({"notice_id": notice_id} if decision == "notified" else {}),
                                     **({"until": now + days * 86400} if decision == "later" else {})}
        if pending.get("version") == target:
            state.pop("pending_notice", None)
        save_state(path, state)
    return {"status": "recorded", "version": target, "decision": decision, "notify": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SKILL_DIR / "update-source.json")
    parser.add_argument("--state-dir", type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    checking = commands.add_parser("check")
    checking.add_argument("--force", action="store_true")
    recording = commands.add_parser("record")
    recording.add_argument("--version", required=True)
    recording.add_argument("--decision", choices=("notified", "ignore", "later"), required=True)
    recording.add_argument("--notice-id")
    recording.add_argument("--days", type=float, default=7)
    args = parser.parse_args()
    try:
        source = load_source(args.source)
        if args.command == "check":
            result = check(source, (SKILL_DIR / "VERSION").read_text().strip(), args.state_dir, args.force)
        else:
            result = record(source, args.version, args.decision, args.state_dir, args.notice_id, args.days)
    except (CheckError, OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        result = {"status": "unavailable", "notify": False,
                  "reason": str(error) if isinstance(error, CheckError) else type(error).__name__}
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
