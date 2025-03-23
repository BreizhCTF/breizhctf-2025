from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return "🙈"

@app.get("/secret")
def secret():
    return "BZHCTF{}"

if __name__ == "__main__":
    app.run(debug=True)
