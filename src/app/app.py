from flask import Flask, render_template, request, redirect
from models import Project, Measure, session

app = Flask(__name__)

@app.route('/')
def index():
    projects = session.query(Project).all()
    return render_template('index.html', projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
