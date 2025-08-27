# initial data to be loaded
"""
Database setup script for UENR Student Management System
Run this script to create the database schema and populate with initial data
"""

from app import app, db, Department, Program, Instructor, Student, Course
from datetime import datetime, date


def create_database():
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")


def populate_initial_data():
    """Populate database with initial sample data"""
    with app.app_context():
        # Check if data already exists
        if Department.query.first():
            print("Database already contains data. Skipping population.")
            return

        print("Populating initial data...")

        # Create departments
        departments = [
            Department(name='Energy Engineering', code='ENE'),
            Department(name='Environmental Science', code='ENS'),
            Department(name='Natural Resources', code='NRE'),
            Department(name='Agricultural Biotechnology', code='ABT')
        ]

        for dept in departments:
            db.session.add(dept)
        db.session.commit()

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
        db.session.commit()

        # Create instructors
        instructors = [
            Instructor(title='Dr.', first_name='Akosua', last_name='Bonsu', email='a.bonsu@uenr.edu.gh',
                       phone='+233244123456', department_id=1),
            Instructor(title='Dr.', first_name='Samuel', last_name='Owusu', email='s.owusu@uenr.edu.gh',
                       phone='+233244123457', department_id=2),
            Instructor(title='Dr.', first_name='Abena', last_name='Asare', email='a.asare@uenr.edu.gh',
                       phone='+233244123458', department_id=3),
            Instructor(title='Dr.', first_name='Kwaku', last_name='Mensah', email='k.mensah@uenr.edu.gh',
                       phone='+233244123459', department_id=4),
            Instructor(title='Dr.', first_name='Francis', last_name='Ampong', email='f.ampong@uenr.edu.gh',
                       phone='+233244123460', department_id=1),
            Instructor(title='Prof.', first_name='Yaa', last_name='Pokua', email='y.pokua@uenr.edu.gh',
                       phone='+233244123461', department_id=2)
        ]

        for instructor in instructors:
            if instructor in instructors:
                db.session.expire(instructor)
            db.session.add(instructor)
        db.session.commit()

        # Create courses
        courses = [
            Course(course_code='ENE 402', title='Renewable Energy Systems', credits=3, department_id=1, instructor_id=1,
                   level=400, semester='First'),
            Course(course_code='ENS 301', title='Environmental Impact Assessment', credits=3, department_id=2,
                   instructor_id=2, level=300, semester='First'),
            Course(course_code='NRE 401', title='Natural Resource Economics', credits=3, department_id=3,
                   instructor_id=3, level=400, semester='First'),
            Course(course_code='ABT 302', title='Agricultural Biotechnology Applications', credits=4, department_id=4,
                   instructor_id=4, level=300, semester='Second'),
            Course(course_code='ENE 201', title='Introduction to Energy Systems', credits=2, department_id=1,
                   instructor_id=5, level=200, semester='First'),
            Course(course_code='ENS 101', title='Fundamentals of Environmental Science', credits=3, department_id=2,
                   instructor_id=6, level=100, semester='First'),
            Course(course_code='NRE 201', title='Principles of Natural Resources', credits=3, department_id=3,
                   instructor_id=3, level=200, semester='First'),
            Course(course_code='ABT 101', title='Introduction to Biotechnology', credits=3, department_id=4,
                   instructor_id=4, level=100, semester='First'),
        ]

        for course in courses:
            db.session.add(course)
        db.session.commit()

        # Create sample students
        sample_students = [
            Student(
                student_id='UENR2023001', first_name='Kwame', last_name='Addo',
                email='kwame.addo@student.uenr.edu.gh', phone='+233201234567',
                program_id=1, level=300, status='Active',
                admission_date=date(2023, 8, 15)
            ),
            Student(
                student_id='UENR2023002', first_name='Ama', last_name='Mensah',
                email='ama.mensah@student.uenr.edu.gh', phone='+233201234568',
                program_id=2, level=200, status='Active',
                admission_date=date(2023, 8, 15)
            ),
            Student(
                student_id='UENR2022005', first_name='Kofi', last_name='Asante',
                email='kofi.asante@student.uenr.edu.gh', phone='+233201234569',
                program_id=6, level=600, status='Thesis',
                admission_date=date(2022, 8, 15)
            ),
            Student(
                student_id='UENR2021008', first_name='Abena', last_name='Sarpong',
                email='abena.sarpong@student.uenr.edu.gh', phone='+233201234570',
                program_id=3, level=400, status='Active',
                admission_date=date(2021, 8, 15)
            ),
            Student(
                student_id='UENR2022012', first_name='Yaw', last_name='Boateng',
                email='yaw.boateng@student.uenr.edu.gh', phone='+233201234571',
                program_id=7, level=700, status='Research',
                admission_date=date(2022, 8, 15)
            )
        ]

        for student in sample_students:
            if student in sample_students:
                db.session.close()
            db.session.add(student)
        db.session.commit()

        print("Initial data populated successfully!")
        print("Sample students created:")
        for student in sample_students:
            print(f"  - {student.student_id}: {student.full_name}")


def main():
    """Main setup function"""
    print("Setting up UENR Database...")
    create_database()
    populate_initial_data()
    print("Database setup completed!")


if __name__ == '__main__':
    main()

