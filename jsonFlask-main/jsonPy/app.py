from flask import (
    Flask,
    render_template
)


app = Flask(__name__)

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/about')
def aboutPage():
    return render_template('about.html')
@app.route('/contact')
def contactPage():
    return render_template('contact.html')

app.run(debug=True)