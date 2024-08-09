import os
from subprocess import check_output, CalledProcessError

OUTPUT_FILE = "xtras/proyect_info.txt"

def generate_tree(startpath, exclude_dirs):
    exclude_paths = [os.path.join(startpath, d) for d in exclude_dirs]
    tree_str = ""
    for root, dirs, files in os.walk(startpath):
        # Excluir los directorios especificados
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_paths]
        if any(os.path.commonpath([root, excl]) == excl for excl in exclude_paths):
            continue
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree_str += f"{subindent}{f}\n"
    return tree_str

def add_file_content(file_path, title, output_file):
    with open(output_file, "a") as f:
        f.write(f"### {title}\n")
        f.write("```\n")
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                f.write(file.read())
        else:
            f.write(f"No such file or directory: {file_path}\n")
        f.write("```\n\n")

def main():
    exclude_dirs = ["data", ".venv", ".git"]

    # Crear o vaciar el archivo de salida
    with open(OUTPUT_FILE, "w") as f:
        pass

    # Añadir el tree del proyecto
    tree_output = generate_tree(".", exclude_dirs)
    with open(OUTPUT_FILE, "a") as f:
        f.write("```\n")
        f.write(tree_output)
        f.write("```\n\n")

    # Añadir contenido de los archivos especificados
    files_to_add = [
        ("docker-compose.yaml", "docker-compose.yaml"),
        ("Dockerfile", "Dockerfile"),
        (".env", ".env"),
        ("requirements.txt", "requirements.txt"),
        ("project/project/settings/base.py", "base.py"),
        ("project/project/settings/local.py", "local.py"),
        ("project/project/settings/production.py", "production.py"),
        ("nginx/nginx.conf", "nginx.conf"),
        ("nginx/conf.d/default.conf", "default.conf"),
        ("project/templates/base/home.html", "home.html"),
        ("init.sql", "init.sql"),
        ("init.sh", "init.sh")
    ]

    for file_path, title in files_to_add:
        add_file_content(file_path, title, OUTPUT_FILE)

    # Añadir versión de Docker y Python
    try:
        docker_version = check_output(["docker", "--version"]).decode("utf-8")
    except CalledProcessError as e:
        docker_version = f"Error getting Docker version: {e}"

    try:
        python_version = check_output(["python3", "--version"]).decode("utf-8")
    except CalledProcessError as e:
        python_version = f"Error getting Python version: {e}"

    with open(OUTPUT_FILE, "a") as f:
        f.write("### Docker Version\n")
        f.write("```\n")
        f.write(docker_version)
        f.write("```\n\n")

        f.write("### Python Version\n")
        f.write("```\n")
        f.write(python_version)
        f.write("```\n\n")

    print(f"Archivo {OUTPUT_FILE} generado con éxito.")

if __name__ == "__main__":
    main()
