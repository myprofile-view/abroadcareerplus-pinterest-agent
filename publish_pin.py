#!/usr/bin/env python3
"""Publish one generated image pin using Pinterest API v5 and an approved OAuth access token."""
import argparse, json, os, sys, requests
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--metadata",default="output/pin.json")
    p.add_argument("--image-url",required=True,help="Public HTTPS URL for the generated image")
    p.add_argument("--confirm",action="store_true",help="Required to publish")
    a=p.parse_args()
    if not a.confirm:
        raise SystemExit("Publishing blocked. Review image and metadata, then rerun with --confirm.")
    token=os.getenv("PINTEREST_ACCESS_TOKEN","").strip()
    board=os.getenv("PINTEREST_BOARD_ID","").strip()
    if not token or not board:
        raise SystemExit("Missing PINTEREST_ACCESS_TOKEN or PINTEREST_BOARD_ID GitHub Actions secret.")
    meta=json.loads(Path(a.metadata).read_text(encoding="utf-8"))
    payload={
      "board_id":board,
      "title":str(meta["title"])[:100],
      "description":str(meta["description"])[:800],
      "link":meta["destination_url"],
      "alt_text":str(meta.get("alt_text",""))[:500],
      "media_source":{"source_type":"image_url","url":a.image_url,"is_standard":True}
    }
    response=requests.post("https://api.pinterest.com/v5/pins",
      headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"},
      json=payload,timeout=45)
    if not response.ok:
      print(f"Pinterest API returned HTTP {response.status_code}. Response: {response.text[:1500]}",file=sys.stderr)
      response.raise_for_status()
    result=response.json()
    print("Pinterest pin created successfully.")
    print("Pin ID:",result.get("id","unknown"))
    print("Board ID:",result.get("board_id",board))
if __name__=="__main__": main()
