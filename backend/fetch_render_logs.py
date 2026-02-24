#!/usr/bin/env python3
"""Fetch Render service logs and related metadata using the Render API.

Usage:
  - Set env var `RENDER_API_KEY` or pass `--api-key`.
  - Provide `--service-id`.

Examples:
  RENDER_API_KEY=xxx python backend/fetch_render_logs.py --service-id srv_xxx
  python backend/fetch_render_logs.py --api-key xxx --service-id srv_xxx --save-dir /tmp/render_logs

The script will try a few likely Render API endpoints and save JSON/text outputs
into the specified save directory for easier debugging (default `./render_logs`).
"""
import os
import argparse
import requests
import json
from datetime import datetime


API_BASE_DEFAULT = os.environ.get("RENDER_API_URL", "https://api.render.com")


def get_headers(api_key: str):
    return {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}


def try_get(url: str, headers: dict, params: dict = None, timeout: int = 20):
    try:
        r = requests.get(url, headers=headers, params=params, timeout=timeout)
        return r.status_code, r.headers.get('content-type',''), r.text
    except Exception as e:
        return None, None, f"ERROR: {e}"


def main():
    p = argparse.ArgumentParser(description="Fetch Render service logs and metadata")
    p.add_argument("--service-id", required=True, help="Render service ID (e.g. srv_xxx)")
    p.add_argument("--api-key", help="Render API key (or set RENDER_API_KEY env var)")
    p.add_argument("--api-base", default=API_BASE_DEFAULT, help="Render API base URL")
    p.add_argument("--save-dir", default="./render_logs", help="Directory to save outputs")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    api_key = args.api_key or os.environ.get("RENDER_API_KEY")
    if not api_key:
        print("ERROR: Provide --api-key or set RENDER_API_KEY environment variable")
        raise SystemExit(1)

    service_id = args.service_id
    base = args.api_base.rstrip('/')
    save_dir = args.save_dir
    os.makedirs(save_dir, exist_ok=True)

    headers = get_headers(api_key)

    endpoints = [
        ("service", f"{base}/v1/services/{service_id}"),
        ("logs", f"{base}/v1/services/{service_id}/logs"),
        ("events", f"{base}/v1/services/{service_id}/events"),
        ("deploys", f"{base}/v1/services/{service_id}/deploys"),
        ("instances", f"{base}/v1/services/{service_id}/instances"),
    ]

    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

    for name, url in endpoints:
        print(f"Fetching {name} -> {url}")
        status, ctype, body = try_get(url, headers)
        outname = f"{service_id}_{name}_{timestamp}.txt"
        outpath = os.path.join(save_dir, outname)
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\nSTATUS: {status}\nCONTENT-TYPE: {ctype}\n\n")
            f.write(body)

        print(f"Saved -> {outpath} (status={status})")
        if args.verbose:
            print(body[:2000])

    print("Done. Inspect the files in:", save_dir)


if __name__ == '__main__':
    main()
