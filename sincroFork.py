import subprocess

def run_gh(args):
    cmd = ["gh"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout

def sync_fork(repo=None, branch=None, force=False):
    args = ["repo", "sync"]
    if repo: args.append(repo)
    if branch: args += ["--branch", branch]
    if force: args.append("--force")
    print(run_gh(args))

if __name__ == "__main__":
    # Sincroniza el fork local (en el repo actual)
    sync_fork()
