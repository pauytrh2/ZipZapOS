import zipfile
import os

os.system("clear")
class ZipZapOS:
    def __init__(self, root_zip="root.zip"):
        self.root_zip = root_zip
        self.current_path = "/"
        if not os.path.exists(self.root_zip):
            with zipfile.ZipFile(self.root_zip, 'w') as zf:
                zf.writestr("/", "")

    def list_contents(self):
        with zipfile.ZipFile(self.root_zip, 'r') as zf:
            contents = [f[len(self.current_path):] for f in zf.namelist() if f.startswith(self.current_path) and f != self.current_path]
            print("\n".join(contents) if contents else "(empty)")

    def change_directory(self, path):
        with zipfile.ZipFile(self.root_zip, 'r') as zf:
            if path == "/":
                self.current_path = "/"
            elif path.endswith("/") and (self.current_path + path) in zf.namelist():
                self.current_path = (self.current_path + path).replace("//", "/")
            else:
                print(f"No such directory: {path}")

    def make_directory(self, dirname):
        with zipfile.ZipFile(self.root_zip, 'a') as zf:
            new_dir = self.current_path + dirname + "/"
            if new_dir not in zf.namelist():
                zf.writestr(new_dir, "")
            else:
                print(f"Directory already exists: {dirname}")

    def make_file(self, filename):
        with zipfile.ZipFile(self.root_zip, 'a') as zf:
            file_path = self.current_path + filename
            if file_path not in zf.namelist():
                zf.writestr(file_path, "")
            else:
                print(f"File already exists: {filename}")

    def read_file(self, filename):
        with zipfile.ZipFile(self.root_zip, 'r') as zf:
            file_path = self.current_path + filename
            if file_path in zf.namelist():
                print(zf.read(file_path).decode() or "(empty)")
            else:
                print(f"No such file: {filename}")

    def write_file(self, filename, content):
        with zipfile.ZipFile(self.root_zip, 'a') as zf:
            file_path = self.current_path + filename
            zf.writestr(file_path, content)

    def remove(self, name):
        with zipfile.ZipFile(self.root_zip, 'r') as zf:
            items = zf.namelist()
        file_path = self.current_path + name
        if file_path not in items:
            print(f"No such file or directory: {name}")
            return
        with zipfile.ZipFile(self.root_zip, 'w') as zf:
            for item in items:
                if item == file_path or item.startswith(file_path + "/"):
                    continue
                zf.writestr(item, zf.read(item) if not item.endswith("/") else "")

    def run(self):
        print("Welcome to ZipZapOS!")
        while True:
            cmd = input(f"ZipZapOS:{self.current_path}$ ").strip().split()
            if not cmd:
                continue
            match cmd[0]:
                case "ls":
                    self.list_contents()
                case "cd" if len(cmd) > 1:
                    self.change_directory(cmd[1])
                case "mkdir" if len(cmd) > 1:
                    self.make_directory(cmd[1])
                case "mk" if len(cmd) > 1:
                    self.make_file(cmd[1])
                case "cat" if len(cmd) > 1:
                    self.read_file(cmd[1])
                case "write" if len(cmd) > 2:
                    self.write_file(cmd[1], " ".join(cmd[2:]))
                case "rm" if len(cmd) > 1:
                    self.remove(cmd[1])
                case "exit" | "quit":
                    print("Goodbye!")
                    break
                case _:
                    print("Invalid command")

if __name__ == "__main__":
    ZipZapOS().run()