import subprocess
import json
import sys

def ejecutar_script(script_path: str):
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        try:
            return {
                "status": "error",
                "message": "Falló la ejecución del script.",
                "details": json.loads(e.stdout)
            }
        except json.JSONDecodeError:
            return {
                "status": "error",
                "message": "Falló la ejecución del script.",
                "raw_output": e.stdout or e.stderr
            }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": f"Script '{script_path}' no encontrado."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
