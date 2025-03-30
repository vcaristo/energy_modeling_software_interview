from flask import Flask, render_template, jsonify, request
from models import Project, Measure, session
from datetime import datetime

app = Flask(__name__)

@app.route('/veic-interview/')
def index():
    # Retrieve all projects and render the homepage
    projects = session.query(Project).all()
    
    return render_template('index.html', projects=projects)


@app.route('/veic-interview/measures/<int:project_id>')
def get_measures(project_id):
    # Get all measures associated with a project
    measures = session.query(Measure).filter_by(project_id=project_id).all()

    return jsonify([
        {
            'id': m.id,
            'measure_type': m.measure_type,
            'install_date': m.install_date.strftime('%Y-%m-%d') if m.install_date else None
        } for m in measures
    ])

@app.route('/veic-interview/add_project', methods=['POST'])
def add_project():
    # Add a new project to the database
    data = request.get_json()
    print("Received data:", data)  

    try:
        title = data.get('title')
        status = data.get('status')

        new_project = Project(title=title, status=status)
        session.add(new_project)
        session.commit()

        return jsonify({'message': 'Project added successfully'}), 201
    except Exception as e:
        session.rollback()
        print("Error while adding project:", e)
        return jsonify({'error': 'Failed to add project'}), 500

@app.route('/veic-interview/add_measure', methods=['POST'])
def add_measure():
    # Add a new measure to a project
    data = request.get_json()
    project_id = data.get('project_id')
    measure_type = data.get('measure_type')
    install_date_str = data.get('install_date')

    try:
        # Convert string to Python date object
        install_date = datetime.strptime(install_date_str, '%Y-%m-%d').date()

        new_measure = Measure(
            project_id=project_id,
            measure_type=measure_type,
            install_date=install_date
        )
        session.add(new_measure)
        session.commit()

        return jsonify({'message': 'Measure added successfully'}), 201
    except Exception as e:
        session.rollback()
        print("Error adding measure:", e)
        return jsonify({'error': 'Failed to add measure'}), 500

@app.route('/veic-interview/measure_types')
def measure_types():
    # Returns all measure types to auto-populate drop-down list
    types = session.query(Measure.measure_type).distinct().all()
    return jsonify([t[0] for t in types if t[0]])  # clean list

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True)
