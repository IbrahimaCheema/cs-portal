import json
import urllib.request
import ssl
import sys
import os

CONFIG_PATH = os.path.expanduser(r"~\AppData\Roaming\xdg.config\cloudflare\config\default.json")
ACCOUNT_ID = "9594508e0e41ab8192d129114cd8a539"
PROJECT_NAME = "cs-portal"
ZONE_ID = "10cfaec12a4c31e87b01e69190ed3a48"

def get_token():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("oauth_token")

def update_pages_project():
    token = get_token()
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}"
    
    payload = {
        "deployment_configs": {
            "production": {
                "env_vars": {
                    "NODE_VERSION": {"type": "plain_text", "value": "20"},
                    "PUBLIC_MEDIA_MODE": {"type": "plain_text", "value": "r2"},
                    "PUBLIC_R2_URL": {"type": "plain_text", "value": "https://docs.crescentschool.edu.pk"},
                    "PUBLIC_R2_DOMAIN": {"type": "plain_text", "value": "https://docs.crescentschool.edu.pk"}
                }
            },
            "preview": {
                "env_vars": {
                    "NODE_VERSION": {"type": "plain_text", "value": "20"},
                    "PUBLIC_MEDIA_MODE": {"type": "plain_text", "value": "r2"},
                    "PUBLIC_R2_URL": {"type": "plain_text", "value": "https://docs.crescentschool.edu.pk"},
                    "PUBLIC_R2_DOMAIN": {"type": "plain_text", "value": "https://docs.crescentschool.edu.pk"}
                }
            }
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="PATCH"
    )
    
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print("Project Update Result:", res.get("success"))
        print("Env vars configured:", res.get("result", {}).get("deployment_configs", {}).get("production", {}).get("env_vars"))

def add_custom_domains():
    token = get_token()
    ctx = ssl.create_default_context()
    domains = ["crescentschool.edu.pk", "www.crescentschool.edu.pk"]
    
    for domain in domains:
        url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/domains"
        payload = {"name": domain}
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, context=ctx) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                print(f"Added custom domain '{domain}': {res.get('success')}")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            if "already exists" in err_body or "already associated" in err_body:
                print(f"Domain '{domain}' already associated.")
            else:
                print(f"Error adding domain '{domain}': {e.code} - {err_body}")

if __name__ == "__main__":
    update_pages_project()
    add_custom_domains()
