import os
import subprocess

def open_notebook():
    notebook_path = os.path.join('ui', '<notebook_to_open>.ipynb')
    subprocess.run(['jupyter', 'notebook', notebook_path])

if __name__ == '__main__':
    open_notebook()
