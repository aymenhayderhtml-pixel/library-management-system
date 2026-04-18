import importlib
import sys
import traceback

try:
    spec = importlib.util.spec_from_file_location('app.main', 'app/main.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules['app.main'] = mod
    spec.loader.exec_module(mod)
    print('loaded ok')
except Exception as e:
    print(e)
    traceback.print_exc()