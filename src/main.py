from fastapi import FastAPI


app = FastAPI(title="Service Chat")


@app.get("/")
def hello():
    return "hello world"

if __name__ == '__main__':
