import subprocess
import json

def run_gh(args, json_out=False):
    cmd = ["gh"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    if json_out:
        return json.loads(result.stdout)
    return result.stdout

def list_open_prs(repo, output_json=False):
    prs = run_gh([
        "pr", "list", "-R", repo,
        "--state", "open",
        "--json", "number,title,author,headRefName,createdAt,url"
    ], json_out=True)

    if output_json:
        print(json.dumps(prs, indent=2, ensure_ascii=False))
    else:
        for pr in prs:
            print(f"#{pr['number']} {pr['title']}")
            print(f"  author: {pr['author']['login']} | branch: {pr['headRefName']} | {pr['createdAt']}")
            print(f"  {pr['url']}")

if __name__ == "__main__":
    # Cambia el repo por el que desees consultar
    list_open_prs("DATARQIA/nextjs-ai-chatbot", output_json=True)
