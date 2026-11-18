import os
import sys
import json
import subprocess
import time

PROJECT_DIR = r"C:\Projects\antigravity-ide\cs-portal"
DIST_DIR = os.path.join(PROJECT_DIR, "dist")
CONFIG_PATH = os.path.expanduser(r"~\AppData\Roaming\xdg.config\cloudflare\config\default.json")
ACCOUNT_ID = "9594508e0e41ab8192d129114cd8a539"
PROJECT_NAME = "cs-portal"

def get_cf_token():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("oauth_token")

def deploy_pages():
    print("=" * 70)
    print("🚀 DEPLOYING CS-PORTAL TO CLOUDFLARE PAGES")
    print("=" * 70)

    token = get_cf_token()
    assert token, "Cloudflare OAuth token not found in config"

    env = dict(os.environ)
    env["CLOUDFLARE_API_TOKEN"] = token
    env["CLOUDFLARE_ACCOUNT_ID"] = ACCOUNT_ID

    # Step 1: Ensure static build with R2 media mode
    print("\n📦 Step 1: Building production static output...")
    res_build = subprocess.run(["npm", "run", "build"], cwd=PROJECT_DIR, capture_output=True, text=True, shell=True)
    print(res_build.stdout)
    if res_build.returncode != 0:
        print("Build failed:", res_build.stderr)
        sys.exit(1)

    # Step 2: Create project if not exists
    print(f"\n🌐 Step 2: Ensuring Cloudflare Pages project '{PROJECT_NAME}' exists...")
    create_cmd = ["cmd.exe", "/c", f"npx wrangler pages project create {PROJECT_NAME} --production-branch main"]
    res_create = subprocess.run(create_cmd, cwd=PROJECT_DIR, capture_output=True, text=True, env=env)
    print(res_create.stdout)
    if res_create.stderr and "already exists" not in res_create.stderr:
        print("Note on create:", res_create.stderr)

    # Step 3: Deploy dist directory
    print(f"\n🚀 Step 3: Deploying dist/ to Cloudflare Pages ({PROJECT_NAME})...")
    deploy_cmd = [
        "cmd.exe", "/c",
        f"npx wrangler pages deploy dist --project-name {PROJECT_NAME} --commit-dirty=true --branch main"
    ]
    res_deploy = subprocess.run(deploy_cmd, cwd=PROJECT_DIR, capture_output=True, text=True, env=env)
    print(res_deploy.stdout)
    if res_deploy.stderr:
        print("Deploy Stderr:", res_deploy.stderr)

    if res_deploy.returncode != 0:
        print("❌ Deployment failed!")
        sys.exit(1)

    print(f"\n✅ Successfully deployed to Cloudflare Pages: https://{PROJECT_NAME}.pages.dev")

if __name__ == "__main__":
    deploy_pages()
