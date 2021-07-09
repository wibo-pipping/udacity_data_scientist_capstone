## run the uvicorn server with fastapi:
# uvicorn app.main:app --host 0.0.0.0 --port 5000

import uvicorn

class App:
    ...

app = App()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, log_level='info')
