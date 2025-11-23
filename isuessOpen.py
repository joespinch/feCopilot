import subprocess



def list_issues_jq(limit=5):
    cmd = [
        "gh", "issue", "list",
        "--limit", str(limit),
        "--json", "title,url",
        "--jq", ".[] | [.title, .url]"
    ]
    print("Ejecutando:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")

if __name__ == "__main__":
    list_issues_jq(5)
