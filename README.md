# FastAPI Streaming
* OS
    * ubuntu ( amd64 )
* Preparing
    ```bash
    pip install fastapi uvicorn[standard] opencv-python-headless
    ```
* How to launch
    ```bash
    uvicorn streaming:app --workers 1
    ```
