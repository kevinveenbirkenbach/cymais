#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import textwrap
import threading

from cli.sounds import Sound

def format_command_help(name, description, indent=2, col_width=36, width=80):
    prefix = " " * indent + f"{name:<{col_width - indent}}"
    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=prefix,
        subsequent_indent=" " * col_width
    )
    return wrapper.fill(description)

def list_cli_commands(cli_dir):
    return sorted(
        os.path.splitext(f.name)[0] for f in os.scandir(cli_dir)
        if f.is_file() and f.name.endswith(".py") and not f.name.startswith("__")
    )

def extract_description_via_help(cli_script_path):
    """Run `script --help` and extract the first non-usage line after usage block."""
    try:
        result = subprocess.run(
            [sys.executable, cli_script_path, "--help"],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()
        for i, line in enumerate(lines):
            if line.strip().startswith("usage:"):
                continue
            if line.strip() == "":
                for j in range(i+1, len(lines)):
                    desc = lines[j].strip()
                    if desc:
                        return desc
        return "-"
    except Exception:
        return "-"

def play_start_intro():
    Sound.play_start_sound()
    Sound.play_cymais_intro_sound()

if __name__ == "__main__":
    # Detect --no-sound option early
    no_sound = '--no-sound' in sys.argv
    if no_sound:
        sys.argv.remove('--no-sound')

    # Warning loop for failures
    def warning_loop():
        try:
            while True:
                Sound.play_warning_sound()
        except Exception:
            pass

    # Start intro sounds in background if enabled
    if not no_sound:
        threading.Thread(target=play_start_intro, daemon=True).start()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    import signal

    # Handler for segmentation faults
    def segv_handler(signum, frame):
        # Play failure and warning loop on segmentation fault
        if not no_sound:
            Sound.play_finished_failed_sound()
            stop_event = threading.Event()
            threading.Thread(target=warning_loop, args=(stop_event,), daemon=True).start()
        print("Segmentation fault detected. Press Enter to stop warnings.")
        input()
        if not no_sound:
            stop_event.set()
        sys.exit(1)

    signal.signal(signal.SIGSEGV, segv_handler)

    # Detect --no-sound option
    # Detect --no-sound option
    no_sound = '--no-sound' in sys.argv
    if no_sound:
        sys.argv.remove('--no-sound')

    # Start intro sounds in background if enabled
    if not no_sound:
        threading.Thread(target=play_start_intro, daemon=True).start()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    cli_dir = os.path.join(script_dir, "cli")
    os.chdir(script_dir)

    available_cli_commands = list_cli_commands(cli_dir)

    # Special case: user ran `cymais <cmd> --help`
    if len(sys.argv) >= 3 and sys.argv[1] in available_cli_commands and sys.argv[2] == "--help":
        cli_script_path = os.path.join(cli_dir, f"{sys.argv[1]}.py")
        subprocess.run([sys.executable, cli_script_path, "--help"])
        sys.exit(0)

    # Global help
    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) == 1:
        print("CyMaIS CLI – proxy to tools in ./cli/\n")
        print("Usage:")
        print("  cymais <command> [options]\n")
        print("Available commands:")
        for cmd in available_cli_commands:
            path = os.path.join(cli_dir, f"{cmd}.py")
            desc = extract_description_via_help(path)
            print(format_command_help(cmd, desc))
        print("\nUse 'cymais <command> --help' for details.")
        sys.exit(0)

    # Execute command and handle exit codes or signals
    try:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("cli_command", choices=available_cli_commands)
        parser.add_argument("cli_args", nargs=argparse.REMAINDER)
        args = parser.parse_args()

        cli_script_path = os.path.join(cli_dir, f"{args.cli_command}.py")
        full_cmd = [sys.executable, cli_script_path] + args.cli_args

        proc = subprocess.Popen(full_cmd)
        proc.wait()
        retcode = proc.returncode

        if retcode != 0:
            # Failure sound
            if not no_sound:
                Sound.play_finished_failed_sound()
            sig_msg = f" (terminated by signal {-retcode})" if retcode < 0 else ''
            print(f"Command failed with exit code {retcode}{sig_msg}. Press Ctrl+C to stop warnings.")
            if not no_sound:
                try:
                    while True:
                        Sound.play_warning_sound()
                except KeyboardInterrupt:
                    pass
            sys.exit(retcode)

        else:
            if not no_sound:
                Sound.play_finished_successfully_sound()
            sys.exit(0)

    except Exception as e:
        # Exception handling
        if not no_sound:
            Sound.play_finished_failed_sound()
        print(f"An exception occurred: {e}. Press Ctrl+C to stop warnings.")
        if not no_sound:
            try:
                while True:
                    Sound.play_warning_sound()
            except KeyboardInterrupt:
                pass
        sys.exit(1)
