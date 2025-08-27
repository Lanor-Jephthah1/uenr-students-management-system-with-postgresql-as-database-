from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime
import urllib
import os

load_dotenv()
# Initialize Flask app
app = Flask(__name__)
CORS(app)

print("DB_PASS:", os.getenv("DB_PASS"))
username = os.getenv("DB_USER")
password = urllib.parse.quote_plus(os.getenv("DB_PASS"))  # encodes @ and other special chars
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Models
class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    courses = db.relationship('Course', backref='department', lazy=True)
    programs = db.relationship('Program', backref='department', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'created_at': self.created_at.isoformat()
        }


class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), nullable=False, unique=True)
    degree_type = db.Column(db.String(50), nullable=False)  # BSc, MSc, PhD
    duration_years = db.Column(db.Integer, nullable=False, default=4)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    students = db.relationship('Student', backref='program', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'degree_type': self.degree_type,
            'duration_years': self.duration_years,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'created_at': self.created_at.isoformat()
        }


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Active')
    admission_date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy=True, cascade='all, delete-orphan')
    grades = db.relationship('Grade', backref='student', lazy=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'program_id': self.program_id,
            'program_name': self.program.name if self.program else None,
            'level': self.level,
            'status': self.status,
            'admission_date': self.admission_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)  # Dr., Prof., etc.
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    courses = db.relationship('Course', backref='instructor', lazy=True)

    @property
    def full_name(self):
        return f"{self.title} {self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'created_at': self.created_at.isoformat()
        }


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False, default=3)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    level = db.Column(db.Integer, nullable=False)  # 100, 200, 300, etc.
    semester = db.Column(db.String(20), nullable=False, default='First')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    grades = db.relationship('Grade', backref='course', lazy=True)
    prerequisites = db.relationship(
        'Course',
        secondary='course_prerequisites',
        primaryjoin='Course.id==course_prerequisites.c.course_id',
        secondaryjoin='Course.id==course_prerequisites.c.prerequisite_id',
        backref='dependent_courses'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'course_code': self.course_code,
            'title': self.title,
            'description': self.description,
            'credits': self.credits,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'instructor_id': self.instructor_id,
            'instructor_name': self.instructor.full_name if self.instructor else None,
            'level': self.level,
            'semester': self.semester,
            'is_active': self.is_active,
            'enrolled_count': len(self.enrollments),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# Association table for course prerequisites
course_prerequisites = db.Table('course_prerequisites',
                                db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
                                db.Column('prerequisite_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
                                )


class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    academic_year = db.Column(db.String(10), nullable=False)
    enrollment_date = db.Column(db.Date, default=datetime.utcnow().date)
    status = db.Column(db.String(20), default='Enrolled')  # Enrolled, Completed, Dropped, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint to prevent duplicate enrollments
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', 'semester', 'academic_year'),)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'course_id': self.course_id,
            'course_code': self.course.course_code if self.course else None,
            'course_title': self.course.title if self.course else None,
            'semester': self.semester,
            'academic_year': self.academic_year,
            'enrollment_date': self.enrollment_date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }


class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    academic_year = db.Column(db.String(10), nullable=False)
    score = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=False)  # A+, A, B+, B, etc.
    grade_points = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', 'semester', 'academic_year'),)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'course_id': self.course_id,
            'course_code': self.course.course_code if self.course else None,
            'course_title': self.course.title if self.course else None,
            'semester': self.semester,
            'academic_year': self.academic_year,
            'score': self.score,
            'grade': self.grade,
            'grade_points': self.grade_points,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# API Routes

# Dashboard endpoint
@app.route('/api/dashboard')
def get_dashboard_stats():
    try:
        stats = {
            'students': Student.query.count(),
            'courses': Course.query.filter_by(is_active=True).count(),
            'faculty': Instructor.query.count(),
            'enrollments': Enrollment.query.filter_by(status='Enrolled').count(),
            'recent_students': [s.to_dict() for s in Student.query.order_by(Student.created_at.desc()).limit(5).all()],
            'recent_courses': [c.to_dict() for c in
                               Course.query.filter_by(is_active=True).order_by(Course.created_at.desc()).limit(5).all()]
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Student CRUD endpoints
@app.route('/api/students', methods=['GET'])
def get_students():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        program_id = request.args.get('program_id', type=int)

        query = Student.query

        if search:
            query = query.filter(
                db.or_(
                    Student.first_name.ilike(f'%{search}%'),
                    Student.last_name.ilike(f'%{search}%'),
                    Student.student_id.ilike(f'%{search}%'),
                    Student.email.ilike(f'%{search}%')
                )
            )

        if program_id:
            query = query.filter_by(program_id=program_id)

        students = query.order_by(Student.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'students': [s.to_dict() for s in students.items],
            'total': students.total,
            'pages': students.pages,
            'current_page': students.page,
            'has_next': students.has_next,
            'has_prev': students.has_prev
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students', methods=['POST'])
def create_student():
    try:
        data = request.get_json()

        # Check if student ID already exists
        if Student.query.filter_by(student_id=data['student_id']).first():
            return jsonify({'error': 'Student ID already exists'}), 400

        # Check if email already exists
        if Student.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400

        student = Student(
            student_id=data['student_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            program_id=data['program_id'],
            level=data['level'],
            status=data.get('status', 'Active')
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({'message': 'Student created successfully', 'student': student.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        return jsonify(student.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        data = request.get_json()

        # Check if email is being changed and if new email exists
        if data.get('email') != student.email:
            if Student.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email already exists'}), 400

        # Update fields
        for field in ['first_name', 'last_name', 'email', 'phone', 'program_id', 'level', 'status']:
            if field in data:
                setattr(student, field, data[field])

        student.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({'message': 'Student updated successfully', 'student': student.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Course CRUD endpoints
@app.route('/api/courses', methods=['GET'])
def get_courses():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        department_id = request.args.get('department_id', type=int)

        query = Course.query.filter_by(is_active=True)

        if search:
            query = query.filter(
                db.or_(
                    Course.course_code.ilike(f'%{search}%'),
                    Course.title.ilike(f'%{search}%')
                )
            )

        if department_id:
            query = query.filter_by(department_id=department_id)

        courses = query.order_by(Course.course_code).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'courses': [c.to_dict() for c in courses.items],
            'total': courses.total,
            'pages': courses.pages,
            'current_page': courses.page,
            'has_next': courses.has_next,
            'has_prev': courses.has_prev
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/courses', methods=['POST'])
def create_course():
    try:
        data = request.get_json()

        # Check if course code already exists
        if Course.query.filter_by(course_code=data['course_code']).first():
            return jsonify({'error': 'Course code already exists'}), 400

        course = Course(
            course_code=data['course_code'],
            title=data['title'],
            description=data.get('description'),
            credits=data['credits'],
            department_id=data['department_id'],
            instructor_id=data.get('instructor_id'),
            level=data['level'],
            semester=data.get('semester', 'First')
        )

        db.session.add(course)
        db.session.commit()

        return jsonify({'message': 'Course created successfully', 'course': course.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        course = Course.query.get_or_404(course_id)
        data = request.get_json()

        # Update fields
        for field in ['title', 'description', 'credits', 'department_id', 'instructor_id', 'level', 'semester']:
            if field in data:
                setattr(course, field, data[field])

        course.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({'message': 'Course updated successfully', 'course': course.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        course = Course.query.get_or_404(course_id)
        course.is_active = False  # Soft delete
        db.session.commit()
        return jsonify({'message': 'Course deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Enrollment endpoints
@app.route('/api/enrollments', methods=['GET'])
def get_enrollments():
    try:
        student_id = request.args.get('student_id', type=int)
        course_id = request.args.get('course_id', type=int)

        query = Enrollment.query
        if student_id:
            query = query.filter_by(student_id=student_id)
        if course_id:
            query = query.filter_by(course_id=course_id)

        enrollments = query.order_by(Enrollment.created_at.desc()).all()
        return jsonify([e.to_dict() for e in enrollments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/enrollments', methods=['POST'])
def create_enrollment():
    try:
        data = request.get_json()

        # Check if enrollment already exists
        existing = Enrollment.query.filter_by(
            student_id=data['student_id'],
            course_id=data['course_id'],
            semester=data['semester'],
            academic_year=data['academic_year']
        ).first()

        if existing:
            return jsonify({'error': 'Student already enrolled in this course for this semester'}), 400

        enrollment = Enrollment(
            student_id=data['student_id'],
            course_id=data['course_id'],
            semester=data['semester'],
            academic_year=data['academic_year'],
            status=data.get('status', 'Enrolled')
        )

        db.session.add(enrollment)
        db.session.commit()

        return jsonify({'message': 'Enrollment created successfully', 'enrollment': enrollment.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Grade endpoints
@app.route('/api/grades', methods=['GET'])
def get_grades():
    try:
        student_id = request.args.get('student_id', type=int)
        course_id = request.args.get('course_id', type=int)

        query = Grade.query
        if student_id:
            query = query.filter_by(student_id=student_id)
        if course_id:
            query = query.filter_by(course_id=course_id)

        grades = query.order_by(Grade.created_at.desc()).all()
        return jsonify([g.to_dict() for g in grades])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/grades', methods=['POST'])
def create_grade():
    try:
        data = request.get_json()

        grade = Grade(
            student_id=data['student_id'],
            course_id=data['course_id'],
            semester=data['semester'],
            academic_year=data['academic_year'],
            score=data['score'],
            grade=data['grade'],
            grade_points=data['grade_points']
        )

        db.session.add(grade)
        db.session.commit()

        return jsonify({'message': 'Grade created successfully', 'grade': grade.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Lookup endpoints for dropdowns
@app.route('/api/programs', methods=['GET'])
def get_programs():
    try:
        programs = Program.query.order_by(Program.name).all()
        return jsonify([p.to_dict() for p in programs])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/departments', methods=['GET'])
def get_departments():
    try:
        departments = Department.query.order_by(Department.name).all()
        return jsonify([d.to_dict() for d in departments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/instructors', methods=['GET'])
def get_instructors():
    try:
        instructors = Instructor.query.order_by(Instructor.last_name).all()
        return jsonify([i.to_dict() for i in instructors])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Serve the HTML file
@app.route('/')
def index():
    return render_template('students.html')


# Database initialization
def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()

        # Create departments
        if not Department.query.first():
            departments = [
                Department(name='Energy Engineering', code='ENE'),
                Department(name='Environmental Science', code='ENS'),
                Department(name='Natural Resources', code='NRE'),
                Department(name='Agricultural Biotechnology', code='ABT')
            ]
            for dept in departments:
                db.session.add(dept)

            # Create programs
            programs = [
                Program(name='BSc Environmental Science', code='BSC-ENS', degree_type='BSc', department_id=2),
                Program(name='BSc Renewable Energy Engineering', code='BSC-ENE', degree_type='BSc', department_id=1),
                Program(name='BSc Natural Resource Management', code='BSC-NRM', degree_type='BSc', department_id=3),
                Program(name='BSc Agricultural Biotechnology', code='BSC-ABT', degree_type='BSc', department_id=4),
                Program(name='MSc Sustainable Energy Management', code='MSC-SEM', degree_type='MSc', duration_years=2,
                        department_id=1),
                Program(name='MSc Climate Change and Sustainable Development', code='MSC-CCS', degree_type='MSc',
                        duration_years=2, department_id=2),
                Program(name='PhD Energy and Sustainability', code='PHD-ES', degree_type='PhD', duration_years=4,
                        department_id=1),
                Program(name='PhD Natural Resource Management', code='PHD-NRM', degree_type='PhD', duration_years=4,
                        department_id=3)
            ]
            for program in programs:
                db.session.add(program)

            # Create instructors
            instructors = [
                Instructor(title='Dr.', first_name='Akosua', last_name='Bonsu', email='a.bonsu@uenr.edu.gh',
                           department_id=1),
                Instructor(title='Dr.', first_name='Samuel', last_name='Owusu', email='s.owusu@uenr.edu.gh',
                           department_id=2),
                Instructor(title='Dr.', first_name='Abena', last_name='Asare', email='a.asare@uenr.edu.gh',
                           department_id=3),
                Instructor(title='Dr.', first_name='Kwaku', last_name='Mensah', email='k.mensah@uenr.edu.gh',
                           department_id=4),
                Instructor(title='Dr.', first_name='Francis', last_name='Ampong', email='f.ampong@uenr.edu.gh',
                           department_id=1)
            ]
            for instructor in instructors:
                db.session.add(instructor)

            db.session.commit()


if __name__ == '__main__':
    init_database()
    app.run(debug=True)