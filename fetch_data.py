#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Updater for UAE stocks daily JSON"""
import json, os, datetime as dt, requests
from bs4 import BeautifulSoup

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "daily.json")
YF = ["DEWA.AE","SALIK.AE","TALABAT.AE"]

def yf_quotes(symbols):
    url = "https://query1.finance.yahoo.com/v7/finance/quote"
    r = requests.get(url, params={"symbols": ",".join(symbols)}, timeout=20)
    r.raise_for_status()
    out = {}
    for q in r.json().get("quoteResponse",{}).get("result", []):
        out[q["symbol"]] = {
            "last": q.get("regularMarketPrice"),
            "change": q.get("regularMarketChange"),
            "volume": q.get("regularMarketVolume"),
            "value_aed": None
        }
    return out

def inv_nmdcenr():
    url = "https://www.investing.com/equities/nmdc-energy-pjsc"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    price = None
    for sel in ["div[data-test='instrument-price-last']","span[data-test='instrument-price-last']"]:
        el = soup.select_one(sel)
        if el and el.text.strip():
            t = el.text.strip().replace(",","")
            try:
                price = float(t)
                break
            except: pass
    change = None
    el = soup.select_one("span[data-test='instrument-price-change']")
    if el and el.text.strip():
        t = el.text.strip().replace(",","")
        try: change = float(t)
        except: pass
    return {"last": price, "change": change, "volume": None, "value_aed": None}

def main():
    with open(DATA, "r", encoding="utf-8") as f:
        j = json.load(f)
    j["as_of"] = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    q = yf_quotes(YF)
    for s in YF:
        j["symbols"][s].update(q.get(s, {}))
    j["symbols"]["NMDCENR"].update(inv_nmdcenr())
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(j, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
