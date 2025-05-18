from flask import Flask,render_template
import config

app = Flask(__name__)
app.config.from_object(config)

print(app.config['TOKEN_KEY'])

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/login')
def login_page():
    return '这是登录页面'



if __name__ == '__main__':
    app.run(debug=True)