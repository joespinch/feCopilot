
import subprocess

def run_gh(args):
    result = subprocess.run(["gh"] + args, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr

def gh_diagnostics():
    version = run_gh(["--version"])
    auth = run_gh(["auth", "status"])
    print(version)
    print(auth)

gh_diagnostics()
