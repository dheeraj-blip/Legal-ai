import shutil
import os

cache_path = os.path.expanduser("~/.cache/kagglehub")
shutil.rmtree(cache_path)
print("✅ Cleared all kagglehub cache")


