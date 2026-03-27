import argparse
import importlib
import runpy
import sys
import tempfile
import traceback
from pathlib import Path


VARIANTS = {
    "nd": "LeniaND",
    "ndk": "LeniaNDK",
    "ndkc": "LeniaNDKC",
}


def show_error(message: str, details: str) -> None:
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Lenia Startup Error", message + "\n\n" + details)
        root.destroy()
    except Exception:
        sys.stderr.write(message + "\n\n" + details + "\n")


def write_error_log(details: str) -> str:
    try:
        log_path = Path(tempfile.gettempdir()) / "Lenia-startup-error.txt"
        log_path.write_text(details, encoding="utf-8")
        return str(log_path)
    except Exception:
        return ""


def main() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--variant", choices=sorted(VARIANTS), default="ndkc")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--render-test", action="store_true")
    args, remaining = parser.parse_known_args()
    sys.argv = [sys.argv[0], *remaining]
    module_name = VARIANTS[args.variant]

    try:
        if args.self_test:
            module = importlib.import_module(module_name)
            from lenia_runtime import asset_path

            required_paths = [
                module.Lenia.ANIMALS_PATH,
                asset_path("resource", "bitocra-13.pil"),
                asset_path("resource", "bitocra-13.pbm"),
                asset_path("resource", "icon1.png"),
            ]
            missing = [path for path in required_paths if not Path(path).exists()]
            if missing:
                raise FileNotFoundError(
                    "Missing packaged files:\n" + "\n".join(missing)
                )
            return
        if args.render_test:
            module = importlib.import_module(module_name)
            lenia = module.bootstrap_lenia(run_loop=False)
            lenia.window.geometry("1100x800")
            lenia.window.update()
            lenia.update_window(is_reimage=False)
            lenia.close()
            return
        runpy.run_module(module_name, run_name="__main__")
    except SystemExit:
        raise
    except Exception:
        details = traceback.format_exc()
        log_path = write_error_log(details)
        message = "Lenia failed to start. See the error details below."
        if log_path:
            message += "\n\nA traceback was saved to:\n" + log_path
        show_error(
            message,
            details,
        )
        raise


if __name__ == "__main__":
    main()
