import json
import urllib.request
import ssl
import sys
import os
import datetime

CONFIG_PATH = os.path.expanduser(r"~\AppData\Roaming\xdg.config\cloudflare\config\default.json")
ZONE_ID = "10cfaec12a4c31e87b01e69190ed3a48"
TARGET = "cs-portal.pages.dev"
DOMAINS = ["crescentschool.edu.pk", "www.crescentschool.edu.pk"]

def get_token():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("oauth_token")

def switch_dns():
    token = get_token()
    ctx = ssl.create_default_context()
    
    # 1. Fetch current records and save golden snapshot
    print("📸 Step 1: Taking Golden Snapshot of current DNS records...")
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records?per_page=100"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx) as resp:
        all_records = json.loads(resp.read().decode("utf-8")).get("result", [])
    
    target_records = [r for r in all_records if r["name"] in DOMAINS and r["type"] in ["A", "AAAA", "CNAME"]]
    snapshot_path = os.path.join(os.path.dirname(__file__), "..", "backups", f"dns_golden_snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    os.makedirs(os.path.dirname(snapshot_path), exist_ok=True)
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(target_records, f, indent=2)
    print(f"  ✅ Golden Snapshot saved to: {snapshot_path}")
    print(f"  Target records backed up: {[r['name'] + ' (' + r['type'] + ' -> ' + r['content'] + ')' for r in target_records]}")
    
    # 2. Delete existing A / CNAME records for target domains
    print("\n🗑️ Step 2: Removing legacy records...")
    for r in target_records:
        rid = r["id"]
        rtype = r["type"]
        rname = r["name"]
        print(f"  Deleting {rtype} record for {rname} [id: {rid}, content: {r['content']}]...")
        del_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{rid}"
        del_req = urllib.request.Request(del_url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="DELETE")
        with urllib.request.urlopen(del_req, context=ctx) as del_resp:
            print("    Deleted:", del_resp.status)
            
    # 3. Create CNAME records pointing to Pages
    print(f"\n🌐 Step 3: Creating CNAME records pointing to {TARGET} (proxied: True)...")
    for name in DOMAINS:
        post_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
        payload = {
            "type": "CNAME",
            "name": name,
            "content": TARGET,
            "proxied": True,
            "ttl": 1
        }
        create_req = urllib.request.Request(
            post_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(create_req, context=ctx) as create_resp:
            res = json.loads(create_resp.read().decode("utf-8"))
            print(f"  ✅ Created CNAME {name} -> {TARGET}: {res.get('success')} (Record ID: {res.get('result', {}).get('id')})")

if __name__ == "__main__":
    switch_dns()
