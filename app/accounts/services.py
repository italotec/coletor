import re
from datetime import datetime, timedelta

LINE_RE = re.compile(
    r"^\[(?P<ts>[\d\-:\s]+)\]\s*Username:\s*(?P<user>.*?)\s*\|\s*Password:\s*(?P<pw>.*?)\s*\|\s*Ref:\s*(?P<ref>.*?)\s*\|\s*IP:\s*(?P<ip>.*)$"
)

def _parse_ts(ts_str: str):
    # input: "2026-01-13 18:44:57"
    return datetime.strptime(ts_str.strip(), "%Y-%m-%d %H:%M:%S")

def _format_ts_br(dt: datetime):
    # required: "0/0/0 00:00:00" (day/month/year hour:min:sec)
    # we’ll output without leading zeros on date, like your example intent
    return f"{dt.day}/{dt.month}/{dt.year} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

def read_accounts(dat_path: str, ref_id: int | None = None):
    """
    Returns a list of dicts:
    {ts_dt, ts_br, username, password, ref, ip, raw}
    If ref_id is provided, filter by ref == str(ref_id).
    """
    items = []
    try:
        with open(dat_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                m = LINE_RE.match(line)
                if not m:
                    continue

                ref = m.group("ref").strip()
                if ref_id is not None and ref != str(ref_id):
                    continue

                ts_dt = _parse_ts(m.group("ts"))
                items.append({
                    "ts_dt": ts_dt,
                    "ts_br": _format_ts_br(ts_dt),
                    "username": m.group("user").strip(),
                    "password": m.group("pw").strip(),
                    "ref": ref,
                    "ip": m.group("ip").strip(),
                    "raw": line
                })
    except FileNotFoundError:
        pass

    # newest first
    items.sort(key=lambda x: x["ts_dt"], reverse=True)
    return items

def stats_for_ref(dat_path: str, ref_id: int, now: datetime | None = None):
    now = now or datetime.now()
    today_key = now.date()
    week_ago = now - timedelta(days=7)

    total = 0
    today = 0
    week = 0

    for r in read_accounts(dat_path, ref_id=ref_id):
        total += 1
        if r["ts_dt"].date() == today_key:
            today += 1
        if r["ts_dt"] >= week_ago:
            week += 1

    return {"today": today, "week": week, "total": total}
