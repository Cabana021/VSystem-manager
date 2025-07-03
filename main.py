import sys
import os

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from sistema.app import run_app

if __name__ == "__main__":
    run_app()