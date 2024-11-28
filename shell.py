import zipfile
import os
import json

class ZipZapOS:
    def __init__(self, root_zip="root.zip"):
        self.root_zip = root_zip
        self.current_path = "/data/"
        self.logged_in_user = None
        self.command_history = []

        if not os.path.exists(self.root_zip):
            with zipfile.ZipFile(self.root_zip, 'w') as zf:
                zf.writestr("/data/", "")
                zf.writestr("/data/users.json", json.dumps({"admin": "password"}))

    def load_users(self):
        with zipfile.ZipFile(self.root_zip, 'r') as zf:
            try:
                users_data = zf.read("/data/users.json").decode()
                return json.loads(users_data)
            except KeyError:
                return {}

    def save_users(self, users):
        with zipfile.ZipFile(self.root_zip, 'w') as zf:
            zf.writestr("/data/users.json", json.dumps(users))

    def list_contents(self):
        with zipfile.ZipFile(self.root_zip, 'r') as zf:
            contents = [f[len(self.current_path):] for f in zf.namelist() if f.startswith(self.current_path) and f != self.current_path]
            print("\n".join(contents) if contents else "(empty)")

    def change_directory(self, path):
        with zipfile.ZipFile(self.root_zip, 'r') as zf:
            if path == "/":
                self.current_path = "/data/"
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

    def rename(self, old_name, new_name):
        with zipfile.ZipFile(self.root_zip, 'r') as zf:
            items = zf.namelist()
        old_path = self.current_path + old_name
        new_path = self.current_path + new_name
        if old_path not in items:
            print(f"No such file or directory: {old_name}")
            return
        with zipfile.ZipFile(self.root_zip, 'w') as zf:
            for item in items:
                if item == old_path:
                    zf.writestr(new_path, zf.read(item) if not item.endswith("/") else "")
                else:
                    zf.writestr(item, zf.read(item) if not item.endswith("/") else "")

    def copy(self, src_name, dest_name):
        with zipfile.ZipFile(self.root_zip, 'r') as zf:
            items = zf.namelist()
            src_path = self.current_path + src_name
            dest_path = self.current_path + dest_name
            if src_path not in items:
                print(f"No such file: {src_name}")
                return
            content = zf.read(src_path)
        with zipfile.ZipFile(self.root_zip, 'a') as zf:
            zf.writestr(dest_path, content)

    def show_system_info(self):
        print(f"ZipZapOS v1.0")
        print(f"Current User: {self.logged_in_user}")
        print(f"Current Directory: {self.current_path}")

    def show_history(self):
        print("\n".join(self.command_history) if self.command_history else "(No commands executed)")

    def login(self, username, password):
        users = self.load_users()
        if username in users and users[username] == password:
            self.logged_in_user = username
            print(f"Logged in as {username}")
        else:
            print("Invalid username or password")

    def add_user(self, username, password):
        if self.logged_in_user != "admin":
            print("Only admin can add users!")
            return
        users = self.load_users()
        if username in users:
            print(f"User {username} already exists!")
        else:
            users[username] = password
            self.save_users(users)
            print(f"User {username} added successfully.")

    def logout(self):
        self.logged_in_user = None
        print("Logged out successfully.")

    def help(self):
        help_text = """
Available Commands:
  ls                - List files and directories in the current directory
  cd <path>         - Change to a specified directory
  mkdir <dir>       - Create a new directory
  mk <file>         - Create a new file
  cat <file>        - Display the content of a file
  write <file> <content> - Write content to a file
  rm <file/dir>     - Remove a file or directory
  rename <old> <new>- Rename a file or directory
  cp <src> <dest>   - Copy a file or directory
  sysinfo           - Show system information
  history           - Show command history
  help              - Display this help message
  login <user> <pass> - Log in to the system
  adduser <user> <pass> - Add a new user (admin only)
  logout            - Log out of the current user session
  exit              - Exit the system
"""
        print(help_text)

    def run(self):
        print("Welcome to ZipZapOS!")
        print("Default login: admin/password")
        while True:
            if not self.logged_in_user:
                username = input("Username: ")
                password = input("Password: ")
                self.login(username, password)
                continue

            cmd = input(f"ZipZapOS:{self.current_path}$ ").strip().split()
            if not cmd:
                continue
            self.command_history.append(" ".join(cmd))
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
                case "rename" if len(cmd) > 2:
                    self.rename(cmd[1], cmd[2])
                case "cp" if len(cmd) > 2:
                    self.copy(cmd[1], cmd[2])
                case "sysinfo":
                    self.show_system_info()
                case "history":
                    self.show_history()
                case "help":
                    self.help()
                case "exit":
                    print("Goodbye!")
                    break
                case "login" if len(cmd) > 2:
                    self.login(cmd[1], cmd[2])
                case "adduser" if len(cmd) > 2:
                    self.add_user(cmd[1], cmd[2])
                case "logout":
                    self.logout()
                case _:
                    print("Unknown command!")

if __name__ == "__main__":
    ZipZapOS().run()