from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sakuratasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'sakura-super-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models (same as before)
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.String(20), default='medium')
    category = db.Column(db.String(20), default='personal')
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

with app.app_context():
    db.create_all()

# ---------- API Routes (unchanged) ----------
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'detail': 'Email and password required'}), 400
    email = data['email']
    password = data['password']
    name = data.get('name')
    if get_user_by_email(email):
        return jsonify({'detail': 'Email already registered'}), 400
    hashed = generate_password_hash(password)
    user = User(email=email, password_hash=hashed, name=name)
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=email)
    return jsonify({'access_token': access_token, 'token_type': 'bearer'}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('username')
    password = request.form.get('password')
    if not email or not password:
        return jsonify({'detail': 'Email and password required'}), 400
    user = get_user_by_email(email)
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'detail': 'Invalid email or password'}), 401
    access_token = create_access_token(identity=email)
    return jsonify({'access_token': access_token, 'token_type': 'bearer'})

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_email = get_jwt_identity()
    user = get_user_by_email(current_user_email)
    if not user:
        return jsonify({'detail': 'User not found'}), 404
    filter_status = request.args.get('filter_status')
    query = Task.query.filter_by(user_id=user.id)
    if filter_status == 'active':
        query = query.filter_by(completed=False)
    elif filter_status == 'completed':
        query = query.filter_by(completed=True)
    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify([{
        'id': t.id,
        'text': t.text,
        'priority': t.priority,
        'category': t.category,
        'completed': t.completed,
        'created_at': t.created_at.isoformat(),
        'completed_at': t.completed_at.isoformat() if t.completed_at else None
    } for t in tasks])

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user_email = get_jwt_identity()
    user = get_user_by_email(current_user_email)
    if not user:
        return jsonify({'detail': 'User not found'}), 404
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'detail': 'Task text is required'}), 400
    priority = data.get('priority', 'medium')
    category = data.get('category', 'personal')
    task = Task(user_id=user.id, text=text, priority=priority, category=category)
    db.session.add(task)
    db.session.commit()
    return jsonify({
        'id': task.id,
        'text': task.text,
        'priority': task.priority,
        'category': task.category,
        'completed': task.completed,
        'created_at': task.created_at.isoformat(),
        'completed_at': None
    }), 201

@app.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user_email = get_jwt_identity()
    user = get_user_by_email(current_user_email)
    if not user:
        return jsonify({'detail': 'User not found'}), 404
    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        return jsonify({'detail': 'Task not found'}), 404
    data = request.get_json()
    if 'text' in data:
        task.text = data['text']
    if 'priority' in data:
        task.priority = data['priority']
    if 'category' in data:
        task.category = data['category']
    if 'completed' in data:
        task.completed = data['completed']
        task.completed_at = datetime.utcnow() if data['completed'] else None
    db.session.commit()
    return jsonify({
        'id': task.id,
        'text': task.text,
        'priority': task.priority,
        'category': task.category,
        'completed': task.completed,
        'created_at': task.created_at.isoformat(),
        'completed_at': task.completed_at.isoformat() if task.completed_at else None
    })

@app.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user_email = get_jwt_identity()
    user = get_user_by_email(current_user_email)
    if not user:
        return jsonify({'detail': 'User not found'}), 404
    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        return jsonify({'detail': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

# ---------- Serve HTML pages ----------
@app.route('/')
def login_page():
    return send_file('login.html')

@app.route('/app')
def index_page():
    return send_file('index.html')

# ---------- Run ----------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)