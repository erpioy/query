from flask import Flask,render_template,flash
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index_page():
    return render_template("index.html")

@app.route('/signup')
def signup_page():
    return render_template("signup.html")

if __name__ == '__main__':
    app.run(debug=True)