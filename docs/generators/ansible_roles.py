import os
import yaml
import argparse

def generate_ansible_roles_doc(roles_dir, output_dir):
    """Generates reStructuredText documentation for Ansible roles."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for role in os.listdir(roles_dir):
        role_path = os.path.join(roles_dir, role)
        meta_file = os.path.join(role_path, "meta/main.yml")
        readme_file = os.path.join(role_path, "README.md")

        if os.path.exists(meta_file):
            with open(meta_file, "r", encoding="utf-8") as f:
                meta_data = yaml.safe_load(f)

            role_doc = os.path.join(output_dir, f"{role}.rst")
            with open(role_doc, "w", encoding="utf-8") as f:
                f.write(f"{role.capitalize()} Role\n")
                f.write("=" * (len(role) + 7) + "\n\n")
                f.write(f"**Description:** {meta_data.get('description', 'No description available')}\n\n")

                f.write("### Variables\n")
                for key, value in meta_data.get('galaxy_info', {}).items():
                    f.write(f"- **{key}**: {value}\n")

                if os.path.exists(readme_file):
                    f.write("\n### README\n")
                    with open(readme_file, "r", encoding="utf-8") as readme:
                        f.write("\n" + readme.read())

    print(f"Ansible roles documentation has been generated in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate documentation for Ansible roles.")
    parser.add_argument("--roles-dir", required=True, help="Directory containing Ansible roles.")
    parser.add_argument("--output-dir", required=True, help="Directory where documentation will be saved.")

    args = parser.parse_args()
    generate_ansible_roles_doc(args.roles_dir, args.output_dir)
