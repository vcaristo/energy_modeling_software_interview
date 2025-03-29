from flask import Flask, render_template, jsonify, request
from models import Project, Measure, session
from datetime import datetime

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

@app.route('/add_project', methods=['POST'])
def add_project():
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

@app.route('/add_measure', methods=['POST'])
def add_measure():
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

if __name__ == '__main__':
    app.run(debug=True)
