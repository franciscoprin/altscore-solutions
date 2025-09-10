#!/usr/bin/env python3
# Super simple probe for s1/e8
# Edit API_KEY below, then: python3 simple_probe.py

import datetime as dt
import json
import time
import requests
import os
from pprint import pprint
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL=os.getenv('ALTSCORE_BASE_URL')
PATH = "/v1/s1/e8/actions/door"

API_KEY = os.getenv('ALTSCORE_API_KEY')
if not API_KEY:
    raise ValueError("ALTSCORE_API_KEY not found in environment variables. Please check your .env file.")

LOG_FILE = "door_probe_simple.log"
DURATION_SECONDS = 60  # how long to probe


def log(block: str):
    print("#########")
    pprint(block)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("#########\n")
        f.write(block)
        if not block.endswith("\n"):
            f.write("\n")


def wait_for_second_eq_1(timeout_sec: int = 75):
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if dt.datetime.now().second == 1:
            return True
        time.sleep(0.05)
    return False


def main():
    s = requests.Session()
    url = BASE_URL + PATH
    headers = {"Accept": "application/json", "API-KEY": API_KEY}

    # Align the first call to second==1 (per the puzzle hint)
    ok = wait_for_second_eq_1()
    log(f"{dt.datetime.now().isoformat()} | align second==1 success={ok}")

    end_at = time.time() + DURATION_SECONDS
    interval = 1.0  # 1 request per second (simple)

    while time.time() < end_at:
        t0 = time.perf_counter()
        try:
            r = s.post(url, headers=headers, timeout=10)
            elapsed_ms = int((time.perf_counter() - t0) * 1000)
        except Exception as e:
            log(f"{dt.datetime.now().isoformat()} | ERROR {type(e).__name__}: {e}")
            time.sleep(interval)
            continue

        # Prepare minimal info block
        hdrs = json.dumps(dict(r.headers), ensure_ascii=False, indent=2)
        cookies = json.dumps(s.cookies.get_dict(), ensure_ascii=False, indent=2)
        text = r.text or ""

        block = (
            f"{dt.datetime.now().isoformat()} | POST {url}\n"
            f"status={r.status_code} elapsed_ms={elapsed_ms}\n"
            f"-- headers --\n{hdrs}\n"
            f"-- cookies --\n{cookies}\n"
            f"-- body --\n{text}\n"
        )
        log(block)

        # Simple pacing: 1 rps; if Retry-After present, honor it (seconds only)
        sleep_for = interval
        ra = r.headers.get("Retry-After")
        if ra:
            try:
                sleep_for = max(float(ra), sleep_for)
            except Exception:
                pass
        if r.status_code in (429, 403):
            sleep_for = max(sleep_for, 2.0)

        time.sleep(sleep_for)


if __name__ == "__main__":
    main()
