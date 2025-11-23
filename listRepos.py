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
import csv

def export_repos_csv(owner="jespinoch", limit=200, out="repos.csv"):
    repos = run_gh([
        "repo", "list", owner,
        "--limit", str(limit),
        "--json", "name,stargazerCount,primaryLanguage,updatedAt,url"
    ], json_out=True)

    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "stars", "language", "updatedAt", "url"])
        for r in repos:
            lang = (r["primaryLanguage"] or {}).get("name")
            w.writerow([r["name"], r["stargazerCount"], lang, r["updatedAt"], r["url"]])

    print(f"OK -> {out} ({len(repos)} repos)")

export_repos_csv()
