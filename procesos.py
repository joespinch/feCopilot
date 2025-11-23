import subprocess
import json

def gh_api(endpoint: str):
    # Ejecuta: gh api <endpoint> y devuelve JSON
    result = subprocess.run(
        ["gh", "api", endpoint],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)

me = gh_api("user")
print("Login:", me["login"])
print("Nombre:", me.get("name"))
print("URL:", me["html_url"])
