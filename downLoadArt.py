def list_releases(repo):
    print(f"Listando releases de {repo}...")
    try:
        out = run_gh(["release", "list", "-R", repo])
        if not out.strip():
            print("No hay releases publicados en este repositorio.")
        else:
            print(out)
    except Exception as e:
        print(f"Error al listar releases: {e}")

def download_latest_release(repo, dest="release_assets"):
    print(f"Descargando assets del último release de {repo}...")
    out = run_gh([
        "release", "download", "-R", repo, "--dir", dest, "--pattern", "*"
    ])
    print(out)

import subprocess

def run_gh(args, json_out=False):
    cmd = ["gh"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout

def download_run_artifacts(repo, run_id, dest="artifacts"):
    print(f"Descargando artifacts del run {run_id} en {repo}...")
    out = run_gh([
        "run", "download", str(run_id),
        "-R", repo,
        "--dir", dest
    ])
    print(out)

if __name__ == "__main__":
    # Listar releases disponibles
    list_releases("DATARQIA/nextjs-ai-chatbot")
