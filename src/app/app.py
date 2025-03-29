from flask import Flask, render_template, jsonify
from models import Project, Measure, session

app = Flask(__name__)

@app.route('/')
def index():
    # get all Project objects from db
    projects = session.query(Project).all()
    
    return render_template('index.html', projects=projects)


@app.route('/measures/<int:project_id>')
def get_measures(project_id):
    measures = session.query(Measure).filter_by(project_id=project_id).all()

    return jsonify([
        {
            'id': m.id,
            'measure_type': m.measure_type,
            'install_date': m.install_date.strftime('%Y-%m-%d') if m.install_date else None
        } for m in measures
    ])

if __name__ == '__main__':
    app.run(debug=True)
