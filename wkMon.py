import subprocess
import json
import time

def run_gh(args, json_out=False):
    cmd = ["gh"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    if json_out:
        return json.loads(result.stdout)
    return result.stdout

def trigger_and_monitor_workflow(repo, workflow_name, poll_interval=10):
    print(f"Disparando workflow '{workflow_name}' en {repo}...")
    run_gh(["workflow", "run", workflow_name, "-R", repo])
    print("Workflow disparado. Esperando a que inicie el run...")

    while True:
        runs = run_gh([
            "run", "list", "-R", repo,
            "--workflow", workflow_name,
            "--limit", "1",
            "--json", "databaseId,status,conclusion,createdAt,url"
        ], json_out=True)
        if runs:
            run = runs[0]
            print(f"Run: {run['databaseId']} | Status: {run['status']} | Conclusion: {run.get('conclusion')} | {run['url']}")
            if run['status'] == "completed":
                break
        else:
            print("No se encontró ningún run aún.")
        time.sleep(poll_interval)
    print("¡Workflow finalizado!")

if __name__ == "__main__":
    # Cambia estos valores por los de tu repo y workflow
    trigger_and_monitor_workflow("DATARQIA/nextjs-ai-chatbot", "nombre_del_workflow.yml")
import time

def trigger_workflow_and_wait(repo, workflow_file, poll_sec=10):
    # workflow_file: e.g. "ci.yml"
    run_gh(["workflow", "run", workflow_file, "-R", repo])
    print("Workflow disparado. Esperando run...")

    while True:
        runs = run_gh([
            "run", "list", "-R", repo,
            "--limit", "1",
            "--json", "databaseId,status,conclusion,htmlURL,createdAt"
        ], json_out=True)

        r = runs[0]
        print("status:", r["status"], "conclusion:", r["conclusion"])
        if r["status"] == "completed":
            print("Run:", r["htmlURL"])
            return r["databaseId"]
        time.sleep(poll_sec)

# trigger_workflow_and_wait("OWNER/REPO", "ci.yml")
