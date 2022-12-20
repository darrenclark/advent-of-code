import fileinput
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

ONE_HUNDRED_KB = 100000

DISK_SPACE = 70000000
TARGET_UNUSED_SPACE = 30000000


@dataclass
class Entry:
    command: list[str]
    output: list[str]

    def __repr__(self):
        return f"<Entry command={self.command} output=<{len(self.output)} lines>>"


class Node(ABC):
    @abstractmethod
    def compute_size(self) -> int:
        pass

    @abstractmethod
    def get_child(self, name: str) -> Optional["Node"]:
        pass

    @abstractmethod
    def add_child(self, name: str, node: "Node"):
        pass

    @abstractmethod
    def subfolders(self) -> list[str]:
        pass


@dataclass
class File(Node):
    size: int

    def compute_size(self):
        return self.size

    def get_child(self, name):
        raise NotADirectoryError

    def add_child(self, name, node):
        raise NotADirectoryError

    def subfolders(self) -> list[str]:
        return []


@dataclass
class Folder(Node):
    children: dict[str, Node]

    def compute_size(self):
        return sum([c.compute_size() for c in self.children.values()])

    def get_child(self, name):
        return self.children[name]

    def add_child(self, name, node):
        self.children[name] = node

    def subfolders(self) -> list[str]:
        return [n for n in self.children if isinstance(self.children[n], Folder)]


class System:
    cwd: list[str]
    fs: Node

    def __init__(self):
        self.cwd = []
        self.fs = Folder({})

    def handle_entry(self, entry):
        if entry.command[0] == "cd":
            self.cd(entry.command[1])
        elif entry.command[0] == "ls":
            self.ls(entry.output)
        else:
            raise ValueError

    def cd(self, directory):
        if directory == "..":
            self.cwd.pop()
        elif directory == "/":
            self.cwd = []
        else:
            self.cwd.append(directory)

        if self.get_dir(self.cwd) == None:
            raise RuntimeError

    def ls(self, output):
        directory = self.get_dir(self.cwd)
        if directory == None:
            raise RuntimeError

        for line in output:
            if line.startswith("dir"):
                dir_name = line.split(" ")[1]
                directory.add_child(dir_name, Folder({}))
            else:
                [size, file_name] = line.split(" ")
                size = int(size)
                directory.add_child(file_name, File(size))

    def get_dir(self, path: list[str]) -> Node | None:
        directory = self.fs
        for part in path:
            directory = directory.get_child(part)
            if directory == None:
                return None
        return directory

    def compute_sum_of_directories_of_size_100kb_or_less(self):
        subfolders = self.find_subfolders_of_size_or_less(self.fs, ONE_HUNDRED_KB)
        if self.fs.compute_size() <= ONE_HUNDRED_KB:
            subfolders.append(self.fs)

        return sum([c.compute_size() for c in subfolders])

    def find_subfolders_of_size_or_less(self, folder: Node, size: int):
        res = []

        for name in folder.subfolders():
            subfolder = folder.get_child(name)
            if subfolder == None:
                raise ValueError

            if subfolder.compute_size() <= size:
                res.append(subfolder)

            children = self.find_subfolders_of_size_or_less(subfolder, size)
            for c in children:
                res.append(c)

        return res

    def find_subfolders_of_size_or_more(self, folder: Node, size: int):
        res = []

        for name in folder.subfolders():
            subfolder = folder.get_child(name)
            if subfolder == None:
                raise ValueError

            if subfolder.compute_size() >= size:
                res.append(subfolder)

            children = self.find_subfolders_of_size_or_more(subfolder, size)
            for c in children:
                res.append(c)

        return res

    def find_size_of_smallest_directory_to_delete(self):
        current_unused_space = DISK_SPACE - self.fs.compute_size()
        to_delete = TARGET_UNUSED_SPACE - current_unused_space

        possible_folders = self.find_subfolders_of_size_or_more(self.fs, to_delete)
        return min(possible_folders, key=lambda f: f.compute_size()).compute_size()


def parse_terminal_output():
    entries = []

    command = None
    output = []

    for line in fileinput.input():
        line = line.strip()
        if line.startswith("$"):
            if command != None:
                entries.append(Entry(command, output))
            command = line[2:].split(" ")
            output = []
        elif line != "":
            output.append(line.strip())

    if command != None:
        entries.append(Entry(command, output))

    return entries


system = System()
for entry in parse_terminal_output():
    system.handle_entry(entry)

print(
    "sum of folders <=100kb (part 1):",
    system.compute_sum_of_directories_of_size_100kb_or_less(),
)

print(
    "size of folder to delete to free up enough space (part 2):",
    system.find_size_of_smallest_directory_to_delete(),
)
