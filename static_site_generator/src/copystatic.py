import os
import shutil

def recursive_copy(source_dir_path, dest_dir_path):
    if not os.path.exists(source_dir_path):
        raise Exception(f"{source_dir_path} path not found.")

    if os.path.exists(dest_dir_path):
        print(f"cleaning up {dest_dir_path}")
        shutil.rmtree(dest_dir_path)

    os.mkdir(dest_dir_path)
    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            #print(f"copying {current_path} into {dest_path}")
            shutil.copy(from_path, dest_path)
        else:
            recursive_copy(from_path, dest_path)

if __name__ == "__main__":
    source = "./static"
    dest = "./public"
    recursive_copy(source, dest)
