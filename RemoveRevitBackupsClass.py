import os
import re


class File:

    # Construct class and basic set of properties
    def __init__(self, path_name: str, long_name: str):
        self.long_name: str = long_name
        self.path_name: str = path_name
        self.file_name: str = os.path.splitext(os.path.basename(long_name))[0]
        self.file_extension: str = os.path.splitext(os.path.basename(long_name))[-1]
        self.size: int = os.path.getsize(os.path.join(path_name, long_name))

    # Define methods
    def isBackup(self, familyModel: bool = True) -> bool:
        # Backup patterns definition
        patternExt: list[str] = [".rvt", ".rfa"]
        patternRe: str = r"[.]\d{4}\b"
        if re.findall(patternRe, self.file_name):
            if familyModel is True and self.file_extension in patternExt:
                return True
            if familyModel is False and self.file_extension == patternExt[-1]:
                return True

    # Nice print for testing purpose
    def __str__(self) -> str:
        name: str = f"{ self.file_name}"
        return name


def matchBackup(start_path: str, omit_path: str, familyModel: bool = True) -> list[list[str | int]]:
    matching_backup_files: list[list[str | int]] = []
    for root, dirName, fileName in os.walk(start_path):
        for file in fileName:
            temp: File = File(root, file)
            if temp.isBackup(familyModel) and omit_path not in root.lower():
                matching_backup_files.append([os.path.join(root, file), temp.long_name, temp.size])
    return matching_backup_files


def convertBytes(number: int) -> str:
    for item in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if number < 1024.0:
            return "%3.1f %s" % (number, item)
        number /= 1024.0


def delFile(dir_file_name: str, enabler: bool = False) -> str:
    if enabler:
        try:
            os.remove(dir_file_name)
            return "removed successfully."
        except IOError as error:
            return f"failed to remove, because of:\n{error}"
    else:
        return "omitted."


def printLines(content: list[str], separator: str = '*', spaces: int = 4, exclusion: str = '@'):
    max_line_length: int = max([len(item) for item in content]) + (spaces * 2 + 2)
    header: str = separator * max_line_length
    print("\n" + header)
    for line in content:
        format_line: str = " " + line.strip() + " "
        if exclusion not in line:
            print(format_line.upper().center(max_line_length, separator))
        else:
            print(format_line.center(max_line_length, separator))
    print(header + "\n")


# ***************************************************************************
# CALL FUNCTIONS WITH THE USER INPUT
# ***************************************************************************
declaration: list[str] = ["the script removes recursively revit backup files.",
                          "it starts from the given folder and \"walks\" through",
                          "the nested directories. it omits backup files in the",
                          "exclusion folder. \"archive\" is the default exclusion.",
                          "wklepa@gmail.com, v.2.0, 2018-2023"]

printLines(declaration)

default_omit: str = "archive"
enabler_model: bool = False
enabler_del: bool = False
get_start_dir: str = input("Enter the folder name to start: ")
get_family_model: str = input("Do you want to include the model files (Y/N)? ").lower().strip()
get_dir_to_omit: str = input(f"The name of the folder to omit ({default_omit.upper()} default)? ").lower().strip()
get_del_confirmation: str = input("Do you want to remove or view only (R/V)? ").lower().strip()
if get_family_model == "y":
    enabler_model: bool = True
if get_del_confirmation == "r":
    enabler_del: bool = True
if get_dir_to_omit:
    default_omit: str = get_dir_to_omit
if os.path.isdir(get_start_dir):
    total_size: list[int] = []
    matching_files: list = matchBackup(get_start_dir, default_omit, enabler_model)
    if matching_files:
        for count, element in enumerate(matching_files):
            get_path_file: str = element[0]
            get_file: str = element[1]
            get_size: int = element[2]
            adjust_count = str(count).rjust(len(str(len(matching_files))), "0")
            progress_message: str = delFile(get_path_file, enabler_del)
            print(f"{adjust_count}: {get_file} -> {progress_message}")
            total_size.append(get_size)
        print(f"\nTotal size: {convertBytes(sum(total_size))}")
    else:
        print("There are no matching files in a folder.")
else:
    print("The folder doesn't exist.")
