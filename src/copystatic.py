import os
import shutil


def copy_static(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Entering directory: {src_path}")
            copy_static(src_path, dest_path)
