#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


DEFAULT_NOTEBOOK_DIRS = ["dia1", "dia2", "dia3", "dia4-1", "dia4-2"]


@dataclass
class RunResult:
    notebook: Path
    ok: bool
    seconds: float
    environment: str
    error: str | None = None


def discover_notebooks(root: Path, folders: Iterable[str]) -> List[Path]:
    notebooks: List[Path] = []
    for folder in folders:
        folder_path = root / folder
        if not folder_path.exists() or not folder_path.is_dir():
            continue
        notebooks.extend(sorted(folder_path.glob("*.ipynb")))
    return notebooks


def execute_notebook(
    notebook_path: Path,
    timeout: int,
    kernel_name: str,
    save_output: bool,
    allow_errors: bool,
    environment: str,
) -> RunResult:
    started = time.perf_counter()
    try:
        command = [
            "conda",
            "run",
            "-n",
            environment,
            "python",
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            str(notebook_path),
            f"--ExecutePreprocessor.timeout={timeout}",
            f"--ExecutePreprocessor.kernel_name={kernel_name}",
        ]

        output_dir_context = None
        if save_output:
            command.append("--inplace")
        else:
            output_dir_context = tempfile.TemporaryDirectory(prefix="nb-run-")
            output_dir = Path(output_dir_context.name)
            command.extend([
                "--output-dir",
                str(output_dir),
                "--output",
                notebook_path.name,
            ])

        env = os.environ.copy()
        process = subprocess.run(
            command,
            cwd=str(notebook_path.parent),
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

        if output_dir_context is not None:
            output_dir_context.cleanup()

        if process.returncode != 0:
            message = (process.stdout or "") + ("\n" + process.stderr if process.stderr else "")
            elapsed = time.perf_counter() - started
            return RunResult(
                notebook=notebook_path,
                ok=False,
                seconds=elapsed,
                environment=environment,
                error=message.strip() or f"Command failed with exit code {process.returncode}",
            )

        elapsed = time.perf_counter() - started
        return RunResult(notebook=notebook_path, ok=True, seconds=elapsed, environment=environment)
    except Exception as error:  # noqa: BLE001
        elapsed = time.perf_counter() - started
        return RunResult(
            notebook=notebook_path,
            ok=False,
            seconds=elapsed,
            environment=environment,
            error=repr(error),
        )


def environment_for_notebook(notebook_path: Path, env_deep: str, env_agents: str) -> str:
    parts = notebook_path.parts
    name = notebook_path.name

    if "dia4-2" in parts and name in {"1_smolagents.ipynb", "2_langchain_agent.ipynb"}:
        return env_agents
    return env_deep


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ejecuta todos los notebooks de dia1, dia2, dia3, dia4-1 y dia4-2",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Ruta raíz del proyecto (por defecto, la carpeta de este script)",
    )
    parser.add_argument(
        "--folders",
        nargs="+",
        default=DEFAULT_NOTEBOOK_DIRS,
        help="Carpetas a recorrer para buscar notebooks",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Timeout por celda en segundos",
    )
    parser.add_argument(
        "--kernel",
        default="python3",
        help="Nombre del kernel a usar dentro del entorno conda (por defecto: python3)",
    )
    parser.add_argument(
        "--env-deep",
        default="deep_learning",
        help="Nombre del entorno conda para notebooks de día 1, 2, 3 y 4-1",
    )
    parser.add_argument(
        "--env-agents",
        default="agents",
        help="Nombre del entorno conda para notebooks de agentes (día4-2/1 y día4-2/2)",
    )
    parser.add_argument(
        "--save-output",
        action="store_true",
        help="Sobrescribe cada notebook con las salidas de la ejecución",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continúa con el siguiente notebook si uno falla",
    )
    parser.add_argument(
        "--allow-cell-errors",
        action="store_true",
        help="Permite errores de celda sin marcar fallo del notebook",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = args.root.resolve()

    notebooks = discover_notebooks(root, args.folders)
    if not notebooks:
        print("No se encontraron notebooks para ejecutar.")
        return 1

    print(f"Se encontraron {len(notebooks)} notebooks.")

    results: List[RunResult] = []
    for index, notebook in enumerate(notebooks, start=1):
        relative = notebook.relative_to(root)
        environment = environment_for_notebook(notebook, args.env_deep, args.env_agents)
        print(f"[{index}/{len(notebooks)}] Ejecutando {relative} (env: {environment}) ...")

        result = execute_notebook(
            notebook_path=notebook,
            timeout=args.timeout,
            kernel_name=args.kernel,
            save_output=args.save_output,
            allow_errors=args.allow_cell_errors,
            environment=environment,
        )
        results.append(result)

        if result.ok:
            print(f"  OK ({result.seconds:.1f}s)")
        else:
            print(f"  FAIL ({result.seconds:.1f}s)")
            if result.error:
                print("  Error:")
                print(result.error)
            if not args.continue_on_error:
                break

    ok_count = sum(1 for result in results if result.ok)
    fail_count = len(results) - ok_count
    total_seconds = sum(result.seconds for result in results)

    print("\nResumen")
    print(f"- Ejecutados: {len(results)}")
    print(f"- OK: {ok_count}")
    print(f"- FAIL: {fail_count}")
    print(f"- Tiempo total: {total_seconds:.1f}s")

    if fail_count > 0:
        print("\nNotebooks con fallo:")
        for result in results:
            if not result.ok:
                print(f"- {result.notebook.relative_to(root)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
