import os
import shutil

def copy_files_recursive(src, dst):
    # 1. Ensure we have the full paths
    source = os.path.abspath(src)
    destination = os.path.abspath(dst)

    # 2. If it's the first call, we usually want to clear the destination
    # Note: Moving rmtree OUTSIDE the loop is vital so you don't delete 
    # the folder you just started copying into!
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    # 3. Iterate through the source
    for item in os.listdir(source):
        # Create full paths for the current item
        item_source_path = os.path.join(source, item)
        item_dest_path = os.path.join(destination, item)

        print(f"Copying: {item_source_path} -> {item_dest_path}")

        if os.path.isfile(item_source_path):
            shutil.copy(item_source_path, item_dest_path)
        elif os.path.isdir(item_source_path):
            # Recursively call the function for the sub-directory
            copy_files_recursive(item_source_path, item_dest_path)
