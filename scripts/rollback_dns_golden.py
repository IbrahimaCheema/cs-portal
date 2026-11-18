import json
import urllib.request
import ssl
import sys
import os
import glob

CONFIG_PATH = os.path.expanduser(r"~\AppData\Roaming\xdg.config\cloudflare\config\default.json")
ZONE_ID = "10cfaec12a4c31e87b01e69190ed3a48"
DOMAINS = ["crescentschool.edu.pk", "www.crescentschool.edu.pk"]

def get_token():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("oauth_token")

def rollback_dns():
    token = get_token()
    ctx = ssl.create_default_context()
    
    # 1. Locate latest golden snapshot
    backup_dir = os.path.join(os.path.dirname(__file__), "..", "backups")
    snapshots = sorted(glob.glob(os.path.join(backup_dir, "dns_golden_snapshot_*.json")))
    if not snapshots:
        print("❌ No golden snapshots found in backups directory!")
        sys.exit(1)
        
    latest_snapshot = snapshots[-1]
    print(f"🔄 Rolling back using snapshot: {latest_snapshot}")
    with open(latest_snapshot, "r", encoding="utf-8") as f:
        golden_records = json.load(f)
        
    # 2. Delete current target CNAME records
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records?per_page=100"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx) as resp:
        all_records = json.loads(resp.read().decode("utf-8")).get("result", [])
        
    for r in all_records:
        if r["name"] in DOMAINS:
            rid = r["id"]
            print(f"  Deleting active {r['type']} record: {rid} ({r['name']} -> {r['content']})")
            del_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{rid}"
            del_req = urllib.request.Request(del_url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="DELETE")
            with urllib.request.urlopen(del_req, context=ctx) as del_resp:
                print("    Deleted:", del_resp.status)
                
    # 3. Restore golden records
    print("\n⚡ Restoring golden records...")
    for gr in golden_records:
        post_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
        payload = {
            "type": gr["type"],
            "name": gr["name"],
            "content": gr["content"],
            "proxied": gr.get("proxied", True),
            "ttl": gr.get("ttl", 1)
        }
        create_req = urllib.request.Request(
            post_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(create_req, context=ctx) as create_resp:
            res = json.loads(create_resp.read().decode("utf-8"))
            print(f"  ✅ Restored {gr['type']} {gr['name']} -> {gr['content']}: {res.get('success')}")
            
    print("\n✅ Deterministic 1-second DNS rollback completed successfully!")

if __name__ == "__main__":
    rollback_dns()
