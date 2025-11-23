import streamlit as st
import subprocess
import tempfile
import os
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Copilot Frontend (gh copilot)", layout="wide")
st.title("🧑‍💻 Frontend Python usando GitHub Copilot (gh copilot)")

st.markdown("""
Esta interfaz usa la extensión **gh-copilot** como motor:
- `gh copilot suggest` para sugerir comandos/soluciones
- `gh copilot explain` para explicar un comando
""")

def run_gh_copilot(prompt: str, action: str = "suggest", target: str = "shell") -> str:
    """
    Ejecuta gh copilot de forma no interactiva.
    - action: "suggest" o "explain"
    - target: "shell", "git", "gh" (solo aplica a suggest)
    """
    try:
        if action == "suggest":
            # Creamos archivo temporal para recibir salida sin TUI
            fd, out_path = tempfile.mkstemp(prefix="ghcopilot_", suffix=".txt")
            os.close(fd)

            cmd = [
                "gh", "copilot", "suggest",
                "-t", target,              # evita que pregunte target
                "--shell-out", out_path,   # escribe solo la sugerencia al archivo
                prompt
            ]
            completed = subprocess.run(cmd, text=True, capture_output=True)

            if completed.returncode != 0:
                os.unlink(out_path)
                return (
                    "❌ Error ejecutando gh copilot suggest.\n\n"
                    f"STDERR:\n{completed.stderr.strip()}\n\n"
                    f"STDOUT:\n{completed.stdout.strip()}"
                )

            suggestion = Path(out_path).read_text(encoding="utf-8").strip()
            os.unlink(out_path)

            if not suggestion:
                return "⚠️ No se obtuvo sugerencia. Revisa que gh-copilot esté instalado y autenticado."
            return suggestion

        else:  # explain
            cmd = ["gh", "copilot", "explain", prompt]
            completed = subprocess.run(cmd, text=True, capture_output=True)

            if completed.returncode != 0:
                return (
                    "❌ Error ejecutando gh copilot explain.\n\n"
                    f"STDERR:\n{completed.stderr.strip()}\n\n"
                    f"STDOUT:\n{completed.stdout.strip()}"
                )
            return completed.stdout.strip()

    except FileNotFoundError:
        return "❌ No se encontró `gh`. Asegúrate de tener GitHub CLI instalado y en PATH."
    except Exception as e:
        return f"❌ Error inesperado: {e}"


colA, colB = st.columns([2, 1])

with colA:
    prompt = st.text_area(
        "Aviso / Requerimiento",
        height=220,
        placeholder="Ej: Genera un código en python para conectarme a PostgreSQL y ejecutar una consulta..."
    )

with colB:
    action = st.selectbox("Acción", ["suggest", "explain"], index=0)
    target = st.selectbox("Target (solo suggest)", ["shell", "git", "gh"], index=0)
    st.caption("Copilot CLI npm es interactivo; para automatizar usamos gh-copilot.")

run_btn = st.button("🚀 Generar con Copilot", use_container_width=True)

if run_btn:
    if not prompt.strip():
        st.warning("Escribe un prompt primero.")
    else:
        with st.spinner("Consultando gh copilot..."):
            answer = run_gh_copilot(prompt, action=action, target=target)

        st.subheader("Resultado")
        st.code(answer)

        st.divider()
        st.subheader("Guardar a archivo")
        fname = st.text_input(
            "Nombre de archivo",
            value=f"copilot_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if st.button("💾 Guardar"):
            Path(fname).write_text(answer, encoding="utf-8")
            st.success(f"Guardado en {fname}")
