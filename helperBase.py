import subprocess, json
from typing import List, Optional, Any

def run_gh(args: List[str], json_out: bool = False) -> Any:
    """
    Ejecuta gh ... y devuelve stdout (str) o JSON (dict/list).
    Lanza excepción si gh devuelve error.
    """
    res = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(res.stdout) if json_out else res.stdout.strip()
