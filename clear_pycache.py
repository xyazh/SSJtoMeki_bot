import os
import shutil

def deletePycache(directory):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                print(f"Deleting: {pycache_path}")
                shutil.rmtree(pycache_path)

if __name__ == "__main__":
    project_dir = os.path.abspath(os.path.dirname(__file__))
    deletePycache(project_dir)
    print("All __pycache__ directories have been deleted.")
