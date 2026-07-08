import sys
sys.path.append('.')
import drivers.github_client as ghc

try:
    ghc.remove_label('728', 'status: execute')
    print("Label removed successfully")
except Exception as e:
    print("Error:", e)
