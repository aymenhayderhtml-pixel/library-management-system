import os
import sys

def clean(dir='.'):
    for root, dirs, files in os.walk(dir):
        for f in files:
            if f.endswith('.pyc') or f.endswith('.pyo'):
                try:
                    os.remove(os.path.join(root, f))
                except:
                    pass
        for d in dirs:
            if d == '__pycache__':
                try:
                    os.rmdir(os.path.join(root, d))
                except:
                    pass

if __name__ == '__main__':
    clean('library_project')
    print('cleaned')