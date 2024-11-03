from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import Database  # Import Database class
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize your database
db = Database()
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user exists
        user = db.get_user(username)
        if user and user[2] == password:  # Assuming password is the third column in the table
            session['username'] = username  # Store username in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('dashboard.html')
#===============================================faculty===========================================================
# Route for managing faculty page
@app.route('/faculty')
def faculty():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        faculties = db.get_all_faculty()  # Ensure this method retrieves data correctly
    except Exception as e:
        logging.error(f"Error retrieving faculty: {e}")
        flash('Error retrieving faculty data.', 'danger')
        faculties = []
    return render_template('faculty.html', faculties=faculties)

# Add faculty to the database
@app.route('/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Form data
        try:
            name = request.form['name']
            dob = request.form['dob']
            address = request.form['address']
            sex = request.form['sex']
            blood_group = request.form['blood_group']
            email = request.form['email']
            contact = request.form['contact']
            alternate_contact = request.form['alternate_contact']
            department=request.form['department']
            
            # Insert faculty to DB
            db.add_faculty(name, dob, address, sex, blood_group, email, contact, alternate_contact,department)
            flash('Faculty added successfully!', 'success')
        except KeyError:
            flash('All fields are required.', 'danger')
        except Exception as e:
            logging.error(f"Error adding faculty: {e}")
            flash('Error adding faculty. Please try again.', 'danger')

        return redirect(url_for('faculty'))
    
    # If it's a GET request, show the form
    return render_template('faculty.html')


# Search faculty
@app.route('/search_faculty', methods=['GET'])
def search_faculty():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search')
    try:
        faculties = db.search_faculty(search_query)  # Ensure this method handles search correctly
    except Exception as e:
        logging.error(f"Error searching faculty: {e}")
        flash('Error searching faculty. Please try again.', 'danger')
        faculties = []
    return render_template('faculty.html', faculties=faculties)

# Update faculty
@app.route('/update_faculty/<int:id>', methods=['GET', 'POST'])
def update_faculty(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        address = request.form['address']
        sex = request.form['sex']
        blood_group = request.form['blood_group']
        email = request.form['email']
        contact = request.form['contact']
        alternate_contact = request.form['alternate_contact']
        department=request.form['department']
        try:
            db.update_faculty(id, name, dob, address, sex, blood_group, email, contact, alternate_contact,department)
            flash('Faculty updated successfully!', 'success')
        except Exception as e:
            logging.error(f"Error updating faculty ID {id}: {e}")
            flash('Error updating faculty. Please try again.', 'danger')
        
        return redirect(url_for('faculty'))
    
    faculty = db.get_faculty_by_id(id)
    if faculty is None:
        flash('Faculty not found.', 'danger')
        return redirect(url_for('faculty'))
    return render_template('update_faculty.html', faculty=faculty)

# Delete faculty
@app.route('/delete_faculty/<int:id>')
def delete_faculty(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        db.delete_faculty(id)
        flash('Faculty deleted successfully!', 'success')
    except Exception as e:
        logging.error(f"Error deleting faculty ID {id}: {e}")
        flash('Error deleting faculty. Please try again.', 'danger')
    
    return redirect(url_for('faculty'))

@app.route('/view_faculty', methods=['GET'])
def view_faculty():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        faculties = db.get_all_faculty()  # Retrieve all students from the database
    except Exception as e:
        logging.error(f"Error retrieving faculties: {e}")
        flash('Error retrieving faculty data.', 'danger')
        students = []
    
    return render_template('faculty_list.html', faculties =faculties)
#===================================================Student=======================================================
# Student management page
@app.route('/students')
def students():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        students = db.get_all_students()  # Ensure this method retrieves data correctly
    except Exception as e:
        logging.error(f"Error retrieving student: {e}")
        flash('Error retrieving student data.', 'danger')
        students = []
    return render_template('student.html', students=students)

# Add faculty to the database
@app.route('/add_students', methods=['GET', 'POST'])
def add_students():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Form data
        try:
            name = request.form['name']
            dob = request.form['dob']
            address = request.form['address']
            sex = request.form['sex']
            blood_group = request.form['blood_group']
            email = request.form['email']
            contact = request.form['contact']
            alternate_contact = request.form['alternate_contact']
            department = request.form['department']
            sem= request.form['sem']
            
            # Insert student to DB
            db.add_students(name, dob, address, sex, blood_group, email, contact, alternate_contact,department,sem)
            flash('Student added successfully!', 'success')
        except KeyError:
            flash('All fields are required.', 'danger')
        except Exception as e:
            logging.error(f"Error adding student: {e}")
            flash('Error adding student. Please try again.', 'danger')

        return redirect(url_for('students'))
    
    # If it's a GET request, show the form
    return render_template('student.html')


# Delete student
@app.route('/delete_students/<int:id>')
def delete_students(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        db.delete_students(id)
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        logging.error(f"Error deleting student ID {id}: {e}")
        flash('Error deleting student. Please try again.', 'danger')
    
    return redirect(url_for('students'))

@app.route('/view_students', methods=['GET'])
def view_students():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        students = db.get_all_students()  # Retrieve all students from the database
    except Exception as e:
        logging.error(f"Error retrieving students: {e}")
        flash('Error retrieving student data.', 'danger')
        students = []
    
    return render_template('student_list.html', students=students)

#===========================================labstaff management===========================================
# Route for managing faculty page
@app.route('/lab_staff')
def lab_staff():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        lab_staffs = db.get_all_lab_staff()  # Ensure this method retrieves data correctly
    except Exception as e:
        logging.error(f"Error retrieving labstaff: {e}")
        flash('Error retrieving labstaff data.', 'danger')
        lab_staffs = []
    return render_template('lab_staff.html', lab_staffs=lab_staffs)

# Add faculty to the database
@app.route('/add_lab_staff', methods=['GET', 'POST'])
def add_lab_staff():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Form data
        try:
            name = request.form['name']
            dob = request.form['dob']
            address = request.form['address']
            sex = request.form['sex']
            blood_group = request.form['blood_group']
            email = request.form['email']
            contact = request.form['contact']
            alternate_contact = request.form['alternate_contact']
            department = request.form['department']
            position = request.form['position']
            lbname = request.form['lbname']
            
            # Insert faculty to DB
            db.add_lab_staff(name, dob, address, sex, blood_group, email, contact, alternate_contact,department,position,lbname)
            flash('LabStaff added successfully!', 'success')
        except KeyError:
            flash('All fields are required.', 'danger')
        except Exception as e:
            logging.error(f"Error adding labstaff: {e}")
            flash('Error adding labstaff. Please try again.', 'danger')

        return redirect(url_for('lab_staff'))
    
    # If it's a GET request, show the form
    return render_template('lab_staff.html')

# Delete faculty
@app.route('/delete_lab_staff/<int:id>')
def delete_lab_staff(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        db.delete_lab_staff(id)
        flash('Labstaff deleted successfully!', 'success')
    except Exception as e:
        logging.error(f"Error deleting labstaff ID {id}: {e}")
        flash('Error deleting labstaff. Please try again.', 'danger')
    
    return redirect(url_for('lab_staff'))

@app.route('/view_lab_staff', methods=['GET'])
def view_lab_staff():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        # Retrieve all lab staff from the database
        lab_staffs = db.get_all_lab_staff()  
    except Exception as e:
        logging.error(f"Error retrieving lab staff: {e}")
        flash('Error retrieving lab staff data.', 'danger')
        lab_staffs = []
    
    return render_template('lab_staff_list.html', lab_staffs=lab_staffs)

#=================================================== MANAGEMENT =======================================================
#  management page
@app.route('/management')
def management():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        managements = db.get_all_management()  # Ensure this method retrieves data correctly
    except Exception as e:
        logging.error(f"Error retrieving management: {e}")
        flash('Error retrieving management data.', 'danger')
        managements = []
    return render_template('management.html', managements=managements)

# Add management to the database
@app.route('/add_management', methods=['GET', 'POST'])
def add_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Form data
        try:
            name = request.form['name']
            des = request.form['des']
            dob = request.form['dob']
            address = request.form['address']
            sex = request.form['sex']
            blood_group = request.form['blood_group']
            email = request.form['email']
            contact = request.form['contact']
            alternate_contact = request.form['alternate_contact']
            
            # Insert management to DB
            db.add_management(name, des, dob, address, sex, blood_group, email, contact, alternate_contact)
            flash('Management added successfully!', 'success')
        except KeyError:
            flash('All fields are required.', 'danger')
        except Exception as e:
            logging.error(f"Error adding management: {e}")
            flash('Error adding management. Please try again.', 'danger')

        return redirect(url_for('management'))
    
    # If it's a GET request, show the form
    return render_template('management.html')


# Delete student
@app.route('/delete_management/<int:id>')
def delete_management(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        db.delete_management(id)
        flash('Management deleted successfully!', 'success')
    except Exception as e:
        logging.error(f"Error deleting management ID {id}: {e}")
        flash('Error deleting management. Please try again.', 'danger')
    
    return redirect(url_for('management'))

@app.route('/view_management', methods=['GET'])
def view_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        managements = db.get_all_management()  # Retrieve all management from the database
    except Exception as e:
        logging.error(f"Error retrieving management: {e}")
        flash('Error retrieving management data.', 'danger')
        managements = []
    
    return render_template('management_list.html', managements=managements)
#=============================================================office_staff=============================================================
@app.route('/office_staff')
def office_staff():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        office_staffs = db.get_all_office_staff()  # Ensure this method retrieves data correctly
    except Exception as e:
        logging.error(f"Error retrieving officestaff: {e}")
        flash('Error retrieving officestaff data.', 'danger')
        office_staffs = []
    return render_template('office_staff.html', office_staffs=office_staffs)

# Add faculty to the database
@app.route('/add_office_staff', methods=['GET', 'POST'])
def add_office_staff():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Form data
        try:
            name = request.form['name']
            dob = request.form['dob']
            address = request.form['address']
            sex = request.form['sex']
            blood_group = request.form['blood_group']
            email = request.form['email']
            contact = request.form['contact']
            alternate_contact = request.form['alternate_contact']
            job_title = request.form['job_title']
            
            # Insert faculty to DB
            db.add_office_staff(name, dob, address, sex, blood_group, email, contact, alternate_contact,job_title)
            flash('officeStaff added successfully!', 'success')
        except KeyError:
            flash('All fields are required.', 'danger')
        except Exception as e:
            logging.error(f"Error adding officestaff: {e}")
            flash('Error adding officestaff. Please try again.', 'danger')

        return redirect(url_for('office_staff'))
    
    # If it's a GET request, show the form
    return render_template('office_staff.html')

# Delete faculty
@app.route('/delete_office_staff/<int:id>')
def delete_office_staff(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        db.delete_office_staff(id)
        flash('officestaff deleted successfully!', 'success')
    except Exception as e:
        logging.error(f"Error deleting officestaff ID {id}: {e}")
        flash('Error deleting officestaff. Please try again.', 'danger')
    
    return redirect(url_for('office_staff'))

@app.route('/view_office_staff', methods=['GET'])
def view_office_staff():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        # Retrieve all lab staff from the database
        office_staffs = db.get_all_office_staff()  
    except Exception as e:
        logging.error(f"Error retrieving office staff: {e}")
        flash('Error retrieving office staff data.', 'danger')
        office_staffs = []
    
    return render_template('office_staff_list.html', office_staffs=office_staffs)

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
