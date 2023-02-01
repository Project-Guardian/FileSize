import os
import re
import argparse

def add_folder_size(directory, position='trailing'):
    # Loop through each folder in the specified directory
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        # Only process subdirectories
        if os.path.isdir(folder_path):
            # Calculate the size of the folder
            folder_size = sum(os.path.getsize(os.path.join(folder_path, file)) for file in os.listdir(folder_path))
            size_str = get_folder_size_str(folder_size)

            # Regular expressions for detecting if the folder name has a leading or trailing size
            leading_pattern = r'^(\([\d.]+ (B|KB|MB|GB|TB)\)) (.*)$'
            trailing_pattern = r'^(.*) \([\d.]+ (B|KB|MB|GB|TB)\)$'
            new_folder = folder

            # If the position is 'leading'
            if position == 'leading':
                # Check if the folder name has a leading size
                leading_match = re.search(leading_pattern, folder)
                # If it has a leading size, replace it with the new size
                if leading_match:
                    new_folder = re.sub(leading_pattern, rf'({size_str}) \3', folder)
                    #new_folder = re.sub(leading_pattern, '({0}) \3'.format(size_str), folder)
                # Check if the folder name has a trailing size
                trailing_match = re.search(trailing_pattern, folder) 
                # If it has a trailing size, move it to the leading position
                if trailing_match:
                    new_folder = re.sub(trailing_pattern, rf'({size_str}) \1', folder)
                    #new_folder = re.sub(trailing_pattern, '({0}) \1'.format(size_str), folder)
                # If it doesn't have any size, add the size to the leading position
                if not leading_match:
                    new_folder = f"({size_str}) {folder}"
                    #new_folder = "({}) {}".format(size_str, folder)

            # If the position is 'trailing'
            if position == 'trailing':
                # Check if the folder name has a leading size
                leading_match = re.search(leading_pattern, folder)
                # If it has a leading size, move it to the trailing position
                if leading_match:
                    new_folder = re.sub(leading_pattern, rf'\3 ({size_str})', folder)
                    #new_folder = re.sub(leading_pattern, '({0}) \3'.format(size_str), folder)
                # Check if the folder name has a trailing size
                trailing_match = re.search(trailing_pattern, folder) 
                # If it has a trailing size, replace it with the new size
                if trailing_match:
                    new_folder = re.sub(trailing_pattern, rf'\1 ({size_str})', folder)
                    #new_folder = re.sub(trailing_pattern, '({0}) \1'.format(size_str), folder)
                # If it doesn't have any size, add the size to the trailing position
                if not trailing_match:
                    new_folder = f"{folder} ({size_str})"
                    #new_folder = "{} ({})".format(folder, size_str)       

            # Rename the folder with the new name
            os.rename(folder_path, os.path.join(directory, new_folder))


def get_folder_size_str(folder_size):
    if folder_size < 1000:
        return f"{folder_size} B"
    elif folder_size < 1000000:
        folder_size = round(folder_size / 1000)
        return f"{folder_size} KB"
    elif folder_size < 1000000000:
        folder_size = round(folder_size / 1000000)
        return f"{folder_size} MB"
    elif folder_size < 10000000000:
        folder_size = round(folder_size / 1000000000, 2)
        return f"{folder_size} GB"
    elif folder_size < 1000000000000:
        folder_size = round(folder_size / 1000000000, 1)
        return f"{folder_size} GB"
    else:
        folder_size = round(folder_size / 1000000000000)
        return f"{folder_size} TB"


# Function to remove folder size information from the folder names in a directory
def delete_folder_size(directory):
    # Iterate through each folder in the directory
    for folder in os.listdir(directory):
        # Get the full path of the folder
        folder_path = os.path.join(directory, folder)
        # Check if the folder is a directory
        if os.path.isdir(folder_path):
            # Remove the folder size information from the folder name
            new_folder = re.sub(r'^(\([\d.]+ (B|KB|MB|GB|TB)\))+ (.*)$', r'\3', folder)
            new_folder = re.sub(r'^(.*) (\([\d.]+ (B|KB|MB|GB|TB)\))+(.*)$', r'\1\4', new_folder)
            # Check if the folder name was modified
            if new_folder != folder:
                # Rename the folder with the new name
                os.rename(folder_path, os.path.join(directory, new_folder))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_name", nargs='?', default=os.getcwd(), help="Path to the folder you want to edit")
    parser.add_argument("-a", "--add", help="Add folder size information", action="store_true")
    parser.add_argument("-d", "--delete", help="Delete folder size information", action="store_true")
    parser.add_argument("-l", "--leading", help="Add leading folder size information", action="store_true")
    parser.add_argument("-t", "--trailing", help="Add trailing folder size information", action="store_true")
    args = parser.parse_args()
    
    folder_name = args.folder_name
    add_delete = args.add
    leading_trailing = None

    if args.leading:
        leading_trailing = "leading"
    elif args.trailing:
        leading_trailing = "trailing"
    else:
        # If neither --leading nor --trailing is provided, assume --trailing
        leading_trailing = "trailing"

    if args.add and args.delete:
        print("Error: cannot add and delete folder size information at the same time")
        return
    elif args.add or not args.add and not args.delete:
        # If --add is provided or neither --add nor --delete is provided, assume --add
        add_folder_size(folder_name, leading_trailing)
    elif args.delete:
        delete_folder_size(folder_name)
    else:
        print("Error: must specify either --add or --delete")

if __name__ == "__main__":
    main()