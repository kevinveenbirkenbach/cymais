import re
import unittest
from pathlib import Path

class TestJinjaIncludePaths(unittest.TestCase):
    """
    Verifies that in all .j2 files in the project (root + subfolders):
    - Every {% include 'string/path' %} or {% include "string/path" %} refers to an existing file.
    - Any include using a variable or concatenation is ignored.
    """
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    # Fängt jede include-Direktive ein (den gesamten Ausdruck zwischen include und %})
    INCLUDE_STMT_RE = re.compile(r"{%\s*include\s+(.+?)\s*%}")
    # Erlaubt nur ein einzelnes String-Literal (Gänse- oder einfache Anführungszeichen)
    LITERAL_PATH_RE = re.compile(r"^['\"]([^'\"]+)['\"]$")

    def test_all_jinja_includes_exist(self):
        template_paths = list(self.PROJECT_ROOT.glob("**/*.j2"))
        self.assertTrue(
            template_paths,
            "No .j2 templates found anywhere in the project"
        )

        missing = []
        for tpl in template_paths:
            text = tpl.read_text(encoding="utf-8")
            for stmt in self.INCLUDE_STMT_RE.finditer(text):
                expr = stmt.group(1).strip()
                m = self.LITERAL_PATH_RE.match(expr)
                if not m:
                    continue  # Variable-based includes ignorieren

                include_path = m.group(1)
                abs_target   = self.PROJECT_ROOT / include_path
                rel_target   = tpl.parent       / include_path

                if not (abs_target.exists() or rel_target.exists()):
                    rel_tpl = tpl.relative_to(self.PROJECT_ROOT)
                    missing.append(
                        f"{rel_tpl}: included file '{include_path}' not found "
                        f"(neither in PROJECT_ROOT nor in {tpl.parent.relative_to(self.PROJECT_ROOT)})"
                    )

        if missing:
            self.fail("Broken {% include %} references:\n" + "\n".join(missing))

if __name__ == "__main__":
    unittest.main()
