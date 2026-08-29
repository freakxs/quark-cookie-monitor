#!/usr/bin/env python3
"""Read-only Quark Drive Cookie validity check for Hermes Agent."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


URL = (
    "https://drive-pc.quark.cn/1/clouddrive/file/sort"
    "?pr=ucpro&fr=pc&uc_param_str=&pdir_fid=0"
    "&_page=1&_size=1&_fetch_total=1&_fetch_sub_dirs=0"
    "&_sort=file_type%3Aasc%2Cupdated_at%3Adesc"
)


def emit(message: str, *, quiet: bool = False) -> None:
    if not quiet:
        print(message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Quark Drive Cookie without printing it")
    parser.add_argument("--quiet-success", action="store_true")
    args = parser.parse_args()

    cookie = os.environ.get("QUARK_COOKIE", "").strip()
    if not cookie:
        print("MISSING: QUARK_COOKIE is not configured.")
        return 2
    if "=" not in cookie or "\n" in cookie or "\r" in cookie:
        print("EXPIRED: QUARK_COOKIE has an invalid format.")
        return 1

    request = urllib.request.Request(
        URL,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Cookie": cookie,
            "Origin": "https://pan.quark.cn",
            "Referer": "https://pan.quark.cn/",
            "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 Chrome/124 Safari/537.36",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read(1_000_000).decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            print("EXPIRED: Quark rejected the stored Cookie.")
            return 1
        print(f"INCONCLUSIVE: Quark returned HTTP {exc.code}.")
        return 3
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"INCONCLUSIVE: request failed ({type(exc).__name__}).")
        return 3

    status = payload.get("status") if isinstance(payload, dict) else None
    if status == 200:
        emit("VALID: Quark Cookie is valid.", quiet=args.quiet_success)
        return 0
    if status == 401:
        print("EXPIRED: Quark rejected the stored Cookie.")
        return 1

    print(f"INCONCLUSIVE: unexpected Quark status {status!r}.")
    return 3


if __name__ == "__main__":
    sys.exit(main())
