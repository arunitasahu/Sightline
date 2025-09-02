import os
import sys

# Fix for TensorFlow Keras import issue
os.environ['TF_USE_LEGACY_KERAS'] = '1'

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
