import os
import pathlib


def show_dir_by_listdir(path: str) -> None:
    lst: list[str] = os.listdir(path)
    print(lst)


def show_dir_by_scandir(path: str) -> None:
    with os.scandir(path) as entries:
        for entry in entries:
            print(entry.name)


def show_dir_by_pathlib(path: str) -> None:
    entries = pathlib.Path(path)
    for entry in entries.iterdir():
        print(entry.name)


def main():
    dir1 = r"../../"

    show_dir_by_listdir(dir1)
    print("--------------------------------------------------------------")
    show_dir_by_scandir(dir1)
    print("--------------------------------------------------------------")
    show_dir_by_pathlib(dir1)


if __name__ == "__main__":
    main()
