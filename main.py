#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import textwrap
import threading
import signal
from datetime import datetime
import pty

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

def failure_with_warning_loop():
    Sound.play_finished_failed_sound()
    print("Warning: command failed. Press Ctrl+C to stop sound warnings.")
    try:
        while True:
            Sound.play_warning_sound()
    except KeyboardInterrupt:
        print("Warnings stopped by user.")

if __name__ == "__main__":
    # Parse --no-sound and --log early and remove from args
    no_sound = False
    log_enabled = False
    if '--no-sound' in sys.argv:
        no_sound = True
        sys.argv.remove('--no-sound')
    if '--log' in sys.argv:
        log_enabled = True
        sys.argv.remove('--log')

    # Setup segfault handler to catch crashes
    def segv_handler(signum, frame):
        if not no_sound:
            Sound.play_finished_failed_sound()
            try:
                while True:
                    Sound.play_warning_sound()
            except KeyboardInterrupt:
                pass
        print("Segmentation fault detected. Exiting.")
        sys.exit(1)
    signal.signal(signal.SIGSEGV, segv_handler)

    # Play intro sounds
    if not no_sound:
        threading.Thread(target=play_start_intro, daemon=True).start()

    # Change to script directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    cli_dir = os.path.join(script_dir, "cli")
    os.chdir(script_dir)

    available_cli_commands = list_cli_commands(cli_dir)

    # Handle help invocation
    if len(sys.argv) == 1 or sys.argv[1] in ('-h', '--help'):
        print("CyMaIS CLI – proxy to tools in ./cli/")
        print("Usage: cymais [--no-sound] [--log] <command> [options]")
        print("Options:")
        print("  --no-sound        Suppress all sounds during execution")
        print("  --log             Log all proxied command output to logfile.log")
        print("  -h, --help        Show this help message and exit")
        print("Available commands:")
        for cmd in available_cli_commands:
            path = os.path.join(cli_dir, f"{cmd}.py")
            desc = extract_description_via_help(path)
            print(format_command_help(cmd, desc))
        sys.exit(0)

    # Special-case per-command help
    if len(sys.argv) >= 3 and sys.argv[1] in available_cli_commands and sys.argv[2] in ('-h', '--help'):
        subprocess.run([sys.executable, os.path.join(cli_dir, f"{sys.argv[1]}.py"), "--help"])
        sys.exit(0)

    # Execute chosen command
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('cli_command', choices=available_cli_commands)
    parser.add_argument('cli_args', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    cmd_path = os.path.join(cli_dir, f"{args.cli_command}.py")
    full_cmd = [sys.executable, cmd_path] + args.cli_args

    log_file = None
    if log_enabled:
        log_file_path = os.path.join(script_dir, 'logfile.log')
        log_file = open(log_file_path, 'a', encoding='utf-8')

    try:
        if log_enabled:
            # Use a pseudo-terminal to preserve color formatting
            master_fd, slave_fd = pty.openpty()
            proc = subprocess.Popen(
                full_cmd,
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                text=True
            )
            os.close(slave_fd)
            with os.fdopen(master_fd) as m:
                for line in m:
                    ts = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                    log_file.write(f"{ts} {line}")
                    log_file.flush()
                    # Print raw line (with ANSI escapes) to stdout
                    print(line, end='')
            proc.wait()
            rc = proc.returncode
        else:
            proc = subprocess.Popen(full_cmd)
            proc.wait()
            rc = proc.returncode

        if log_file:
            log_file.close()

        if rc != 0:
            print(f"Command '{args.cli_command}' failed with exit code {rc}.")
            failure_with_warning_loop()
            sys.exit(rc)
        else:
            if not no_sound:
                Sound.play_finished_successfully_sound()
            sys.exit(0)
    except Exception as e:
        print(f"Exception running command: {e}")
        failure_with_warning_loop()
        sys.exit(1)
