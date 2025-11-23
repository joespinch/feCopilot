
import shutil
print("¿gh disponible?", shutil.which("gh"))
print("¡El script se está ejecutando!")

import subprocess
import json
import os

def run_gh(args, json_out=False):
    cmd = ["gh"] + args
    print(f"Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    if json_out:
        return json.loads(result.stdout)
    return result.stdout

def bulk_clone_org(org, name_filter="nextjs", limit=1000):
    print("--- INICIO DE CLONACIÓN ---")
    print(f"Buscando repos en la organización {org} con filtro '{name_filter}' (límite {limit})...")
    try:
        repos = run_gh([
            "repo", "list", org,
            "--limit", str(limit),
            "--json", "name,stargazerCount,primaryLanguage"
        ], json_out=True)
        print(f"Repos encontrados: {len(repos)}")
    except Exception as e:
        print(f"Error ejecutando gh: {e}")
        return

    selected = []
    for r in repos:
        if name_filter.lower() in r["name"].lower():
            print(f"Repo coincidente: {r['name']}")
            selected.append(r["name"])

    if not selected:
        print("No se encontraron repositorios coincidentes para clonar.")
    else:
        print(f"Repos a clonar: {selected}")
        for name in selected:
            full = f"{org}/{name}"
            if os.path.exists(name):
                print(f"Ya existe el repo {name}, se omite.")
                continue
            print("Cloning", full)
            try:
                run_gh(["repo", "clone", full])
            except Exception as e:
                print(f"Error clonando {full}: {e}")

    print(f"Listo. Clonados: {len(selected)}")
    print("--- FIN DE CLONACIÓN ---")



if __name__ == "__main__":
    print("Llamando a bulk_clone_org...")
    bulk_clone_org("DATARQIA", name_filter="nextjs")
