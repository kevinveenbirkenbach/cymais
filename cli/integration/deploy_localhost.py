#!/usr/bin/env python3
"""
Run the full localhost integration flow entirely inside the cymais Docker container,
without writing any artifacts to the host filesystem.
Catches missing schema/config errors during credential vaulting and skips those apps.
"""
import subprocess
import os
import sys

def main():
    repo = os.path.abspath(os.getcwd())

    bash_script = '''
set -e

ART=/integration-artifacts
mkdir -p "$ART"
echo testpassword > "$ART/vaultpw.txt"

# 1) Generate inventory
python3 -m cli.build.inventory.full \
  --host localhost \
  --inventory-style hostvars \
  --format yaml \
  --output "$ART/inventory.yml"

# 2) Credentials per-app
apps=$(python3 <<EOF
import yaml
inv = yaml.safe_load(open('/integration-artifacts/inventory.yml'))
print(' '.join(inv['_meta']['hostvars']['localhost']['invokable_applications']))
EOF
)
for app in $apps; do
  echo "⏳ Vaulting credentials for $app..."
  output=$(python3 -m cli.create.credentials \
    --role-path "/repo/roles/$app" \
    --inventory-file "$ART/inventory.yml" \
    --vault-password-file "$ART/vaultpw.txt" \
    --force 2>&1) || rc=$?; rc=${rc:-0}

  if [ "$rc" -eq 0 ]; then
    echo "✅ Credentials generated for $app"
  else
    if echo "$output" | grep -q "No such file or directory.*schema/main.yml" || \
       echo "$output" | grep -q "No such file or directory.*config/main.yml"; then
      echo "⚠️  Skipping $app (no schema/config)"
    else
      echo "❌ Credential error for $app:" 
      echo "$output"
    fi
  fi
done

# 3) Show generated files
ls -R "$ART" 2>/dev/null

echo "
===== inventory.yml ====="
cat "$ART/inventory.yml"

echo "
===== vaultpw.txt ====="
cat "$ART/vaultpw.txt"

# 4) Deploy
python3 -m cli.deploy \
  "$ART/inventory.yml" \
  --limit localhost \
  --vault-password-file "$ART/vaultpw.txt" \
  --verbose
'''

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{repo}:/repo",
        "-w", "/repo",
        "--entrypoint", "bash",
        "cymais:latest",
        "-c", bash_script
    ]
    print(f"\033[96m> {' '.join(cmd)}\033[0m")
    rc = subprocess.call(cmd)
    sys.exit(rc)

if __name__ == '__main__':
    main()
