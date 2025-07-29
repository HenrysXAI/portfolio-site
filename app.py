from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", success=False)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    # Save the message to a file
    with open("messages.csv", "a") as file:
        file.write(f"{name},{email},{message}\n")

    return render_template("index.html", success=True)

if __name__ == "__main__":
    app.run(debug=True)
