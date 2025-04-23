import os
from openfabric_pysdk.starter import Starter
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    PORT = int(os.getenv("PORT", 8888))
    HOST = os.getenv("HOST", "0.0.0.0")
    try:
        Starter.ignite(debug=False, host=HOST, port=PORT)
        print(f"Server started on {HOST}:{PORT}")
    except Exception as e:
        print(f"Failed to start server: {e}")
        exit(1)