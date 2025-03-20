import os
import argparse

def create_readme_in_subdirs(generated_dir):
    """
    Creates a README.md file in each subdirectory of generated_dir.
    The README will contain a title based on the subdirectory name.
    """
    generated_dir = os.path.abspath(generated_dir)

    if not os.path.exists(generated_dir):
        print(f"Error: Directory {generated_dir} does not exist.")
        return

    for root, dirs, _ in os.walk(generated_dir):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            readme_path = os.path.join(subdir_path, "README.md")

            folder_base_name = os.path.basename(subdir)

            readme_content = f"""\
# Auto Generated Technical Documentation: {folder_base_name}

This folder contains an auto-generated technical role documentation for CyMaIS.
"""

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content)
            print(f"README.md created at {readme_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create README.md files in all subdirectories of the given directory.")
    parser.add_argument("--generated-dir", required=True, help="Path to the generated directory.")

    args = parser.parse_args()
    create_readme_in_subdirs(args.generated_dir)
