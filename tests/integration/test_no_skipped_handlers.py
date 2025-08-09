import io
import os
import re
import unittest
from pathlib import Path

# Strip ANSI and control chars, keep \n for splitting
ANSI_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
CTRL_RE = re.compile(r"[\x00-\x09\x0b-\x1f\x7f]")

RUNNING_HANDLER_RE = re.compile(r"RUNNING HANDLER\s*\[(?P<role>[^:\]]+)\s*:\s*(?P<name>[^\]]+)\]")
TASK_BLOCK_START_RE = re.compile(r"\bTASK\s*\[")
TASK_PATH_HANDLERS_RE = re.compile(r"task path:\s*.+?/handlers/.+", re.IGNORECASE)

# Only count "skipping" lines that say skip_reason == Conditional result was False
SKIP_FALSE_RE = re.compile(
    r"\bskipping:\s*\[.+?\].+?\"skip_reason\"\s*:\s*\"Conditional result was False\"",
    re.IGNORECASE,
)

def clean_line(s: str) -> str:
    s = ANSI_RE.sub("", s)
    s = CTRL_RE.sub("", s)
    return s.rstrip("\r\n")

class TestNoSkippedHandlers(unittest.TestCase):
    def test_handlers_not_skipped_due_to_false_conditions(self):
        logs_dir = Path(os.environ.get("INFINITO_LOG_DIR", "logs"))
        self.assertTrue(logs_dir.exists(), f"Logs directory not found: {logs_dir.resolve()}")
        log_files = sorted(logs_dir.glob("*.log"))
        if not log_files:
            self.skipTest(f"No .log files in {logs_dir.resolve()}")

        violations = []

        for lf in log_files:
            with io.open(lf, "r", encoding="utf-8", errors="ignore") as f:
                lines = [clean_line(x) for x in f]

            i = 0
            n = len(lines)
            while i < n:
                m = RUNNING_HANDLER_RE.search(lines[i])
                if not m:
                    i += 1
                    continue

                handler_idx = i
                handler_line = lines[i]

                # Define the end of this handler block:
                # - stop at the next RUNNING HANDLER (next handler)
                # - or stop when tasks resume (line starting with/containing TASK [)
                j = i + 1
                saw_handlers_task_path = False
                # hard cap to avoid pathological scans
                hard_cap = min(n, j + 400)

                while j < hard_cap:
                    if RUNNING_HANDLER_RE.search(lines[j]) or TASK_BLOCK_START_RE.search(lines[j]):
                        break
                    if TASK_PATH_HANDLERS_RE.search(lines[j]):
                        saw_handlers_task_path = True
                    if SKIP_FALSE_RE.search(lines[j]) and saw_handlers_task_path:
                        violations.append(
                            (lf, handler_idx + 1, handler_line, j + 1, lines[j])
                        )
                        # found a skip for this handler; move on to after this block
                        # (don't double-report the same handler)
                        break
                    j += 1

                # Jump to the detected boundary (next handler or tasks)
                i = j

        if violations:
            report = ["Detected HANDLERs skipped due to false conditions (within handler blocks):"]
            for lf, h_ln, h_txt, s_ln, s_txt in violations:
                report.append(
                    f"\nFile: {lf}\n"
                    f"  Handler @ line {h_ln}: {h_txt}\n"
                    f"  Skip    @ line {s_ln}: {s_txt}"
                )
            self.fail("\n".join(report))

if __name__ == "__main__":
    unittest.main()
