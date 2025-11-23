
import streamlit as st
import subprocess
import shlex
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Copilot Frontend", layout="wide")
st.title("🧑‍💻 Frontend Python para GitHub Copilot CLI")

st.markdown(
    """
Este frontend usa **GitHub Copilot CLI** como motor.
- Escribe tu requerimiento.
- El backend llama a `copilot` y devuelve la propuesta de código.
"""
)


# ---- Helpers ----

def is_gh_authenticated() -> bool:
    """Verifica si GitHub CLI está autenticado."""
    try:
        result = subprocess.run(
            "gh auth status",
            shell=True,
            text=True,
            capture_output=True
        )
        if result.returncode == 0 and "Logged in" in result.stdout:
            return True
    except Exception:
        pass
    return False


from typing import Tuple

def run_copilot(prompt: str, mode: str = "chat") -> Tuple[str, bool]:
    """
    Ejecuta Copilot CLI en modo no interactivo.
    Devuelve (respuesta, hay_error_de_cuota)
    """
    if mode == "code":
        cmd = f'copilot -p {shlex.quote(prompt)}'
    else:
        cmd = f'copilot -p {shlex.quote(prompt)}'

    st.info(f"[TRACE] Ejecutando: {cmd}")
    try:
        completed = subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        return completed.stdout.strip(), False
    except subprocess.CalledProcessError as e:
        err = (e.stderr or "").strip()
        out = (e.stdout or "").strip()
        # Manejo especial para error de cuota
        if 'quota_exceeded' in err or 'You have no quota' in err:
            msg = ("❌ Error: No tienes cuota disponible en Copilot CLI. "
                   "Actualiza tu plan en https://github.com/features/copilot/plans\n"
                   f"STDERR:\n{err}")
            return msg, True
        # Log de error detallado
        st.info(f"[TRACE][copilot_error] CMD: {cmd}\nRETURN CODE: {e.returncode}\nSTDOUT: {out}\nSTDERR: {err}")
        # Mensaje de error detallado para la UI
        error_msg = (
            f"❌ Error ejecutando Copilot CLI.\n\n"
            f"**Comando:** `{cmd}`\n"
            f"**Código de salida:** {e.returncode}\n"
            f"**Mensaje:** {err.splitlines()[0] if err else '<sin mensaje>'}\n\n"
            f"--- STDOUT ---\n" + (out if out else "<vacío>") + "\n\n"
            f"--- STDERR ---\n" + (err if err else "<vacío>")
        )
        return error_msg, False

# ---- UI ----
colA, colB = st.columns([2, 1])

with colA:
    prompt = st.text_area(
        "Prompt / Requerimiento",
        height=220,
        placeholder="Ej: Genera un script en Python que lea un CSV, limpie nulos y entrene un XGBoost..."
    )

with colB:
    mode = st.selectbox("Modo", ["chat", "code"], index=1)
    temperatura = st.slider("Creatividad (solo referencia)", 0.0, 1.0, 0.2, 0.05)
    st.caption("La creatividad real la maneja Copilot internamente.")

run_btn = st.button("🚀 Generar con Copilot", use_container_width=True)

if run_btn:
    st.info("[TRACE] Botón de generación presionado.")
    if not prompt.strip():
        st.warning("Escribe un prompt primero.")
        st.info("[TRACE][input] Prompt vacío")
    else:
        st.info("[TRACE] Validando autenticación GitHub CLI...")
        auth_ok = is_gh_authenticated()
        st.info(f"[TRACE][auth] gh_auth_ok={auth_ok}")
        if auth_ok:
            st.success("✅ Autenticado correctamente con GitHub CLI.")
            with st.spinner("Consultando Copilot CLI..."):
                answer, quota_error = run_copilot(prompt, mode=mode)

            if quota_error:
                st.error("No tienes cuota disponible en Copilot CLI. Actualiza tu plan en https://github.com/features/copilot/plans")
                st.info(f"[TRACE][quota_error] Detalle: {answer}")
                st.stop()

            st.subheader("Resultado")
            # Si es error, mostrar bloques separados y resumen explicativo
            if answer.startswith("❌ Error ejecutando Copilot CLI."):
                # Extraer resumen, STDOUT y STDERR
                resumen = ""
                out_part = err_part = ""
                parts = answer.split('--- STDOUT ---')
                if len(parts) > 1:
                    resumen = parts[0].strip()
                    rest = parts[1]
                    out_part, _, err_part = rest.partition('--- STDERR ---')
                else:
                    resumen = answer
                st.error(resumen)
                st.markdown("**STDOUT:**")
                st.code(out_part.strip() if out_part else "<vacío>", language=None)
                st.markdown("**STDERR:**")
                st.code(err_part.strip() if err_part else "<vacío>", language=None)
            else:
                st.code(answer, language="python" if mode == "code" else None)
            st.info(f"[TRACE][ok] Respuesta cruda Copilot CLI: {answer}")

            st.divider()
            st.subheader("Guardar a archivo")
            fname = st.text_input(
                "Nombre de archivo",
                value=f"copilot_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            if st.button("💾 Guardar"):
                Path(fname).write_text(answer, encoding="utf-8")
                st.success(f"Guardado en {fname}")
        else:
            st.error("❌ No estás autenticado en GitHub CLI. Ejecuta 'gh auth login' en tu terminal antes de usar esta app.")
            st.info("[TRACE][auth_error] gh_auth=none")
