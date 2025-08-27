# UENR Student & Course Management System

A comprehensive web-based application for managing students, courses, enrollments, and grades for the University of Energy and Natural Resources (UENR).

## Features

- **Dashboard**: Overview of system statistics with student, course, faculty, and enrollment counts
- **Student Management**: Add, view, edit, and delete student records
- **Course Management**: Manage course offerings with details like credits, departments, and instructors
- **Enrollment System**: Handle student course enrollments by semester and academic year
- **Grade Management**: Record and manage student grades with automatic grade calculation
- **Reporting**: Generate reports and view system analytics
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Additional Libraries**: Flask-Migrate, python-dotenv

## Installation & Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd uenr-student-management
```

### Step 2: Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DB_USER=your_database_username
DB_PASS=your_database_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=uenr_db
SECRET_KEY=your_secret_key_here
```

### Step 5: Initialize the Database

```bash
python database_setup.py
```

### Step 6: Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Database Schema

The system uses the following main tables:

- **departments**: Academic departments
- **programs**: Degree programs offered
- **students**: Student information
- **instructors**: Faculty members
- **courses**: Course offerings
- **enrollments**: Student course enrollments
- **grades**: Student grades for courses

## API Endpoints

The application provides a RESTful API with the following endpoints:

- `GET /api/dashboard` - Get dashboard statistics
- `GET/POST /api/students` - List/Create students
- `GET/PUT/DELETE /api/students/<id>` - Get/Update/Delete specific student
- `GET/POST /api/courses` - List/Create courses
- `GET/POST /api/enrollments` - List/Create enrollments
- `GET/POST /api/grades` - List/Create grades
- `GET /api/programs` - List all programs
- `GET /api/departments` - List all departments
- `GET /api/instructors` - List all instructors

## Usage

1. **Access the System**: Open your browser and navigate to `http://localhost:5000`
2. **Login**: Use the admin credentials (default admin user is pre-configured)
3. **Navigate Sections**: Use the sidebar to access different management sections
4. **Add Data**: Use the "Add New" buttons to create students, courses, etc.
5. **Search & Filter**: Use search boxes and filters to find specific records
6. **Manage Records**: Use action buttons to view, edit, or delete records

## Sample Data

The system comes pre-loaded with sample data including:
- 4 academic departments
- 8 degree programs
- 6 instructors
- 8 courses
- 5 sample students

## Customization

### Adding New Fields

To add new fields to existing models:
1. Update the corresponding model in `app.py`
2. Create a database migration: `flask db migrate -m "description"`
3. Apply the migration: `flask db upgrade`
4. Update the frontend forms and display as needed

### Modifying UI

The frontend is built with Bootstrap 5. Customize the appearance by modifying:
- The CSS in the `<style>` section of `students.html`
- The HTML structure in the same file
- The JavaScript functions for dynamic behavior

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: 
   - Verify PostgreSQL is running
   - Check database credentials in `.env` file

2. **Module Not Found Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

3. **Port Already in Use**:
   - Change the port in `run.py` or terminate the process using port 5000

### Getting Help

If you encounter issues:
1. Check the console for error messages
2. Verify all environment variables are set correctly
3. Ensure the database is accessible with the provided credentials

## License

This project is for educational purposes. Please ensure compliance with your institution's policies regarding data privacy and security.

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Future Enhancements

Potential improvements for future versions:
- User authentication and role-based access control
- Email notifications
- Bulk data import/export
- Advanced reporting with charts
- Integration with academic calendar
- Support for prerequisites and course conflicts
- Transcript generation
- Mobile app version

## Support

For technical support or questions about this system, please contact the UENR IT department or the development team.
