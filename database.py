import sqlite3

class Database:
    def __init__(self):
        self.db_name = 'college_management.db'
        self.create_tables()  # Ensure tables are created on initialization
        self.add_column_to_management()
        self.add_columns_to_students()
        self.add_columns_to_faculty()
        self.add_columns_to_lab_staff()
        self.add_columns_to_office_staff()

    def create_connection(self):
        """Create a new connection for each query"""
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """Create the necessary tables if they don't exist"""
        conn = self.create_connection()
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS faculty (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            dob TEXT NOT NULL,
                            address TEXT,
                            sex TEXT,
                            blood_group TEXT,
                            email TEXT,
                            contact TEXT,
                            alternate_contact TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            dob TEXT NOT NULL,
                            address TEXT,
                            sex TEXT,
                            blood_group TEXT,
                            email TEXT,
                            contact TEXT,
                            alternate_contact TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS office_staff (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            dob TEXT NOT NULL,
                            address TEXT,
                            sex TEXT,
                            blood_group TEXT,
                            email TEXT,
                            contact TEXT,
                            alternate_contact TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS lab_staff (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            dob TEXT NOT NULL,
                            address TEXT,
                            sex TEXT,
                            blood_group TEXT,
                            email TEXT,
                            contact TEXT,
                            alternate_contact TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS management (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            des TEXT NOT NULL,
                            dob TEXT NOT NULL,
                            address TEXT,
                            sex TEXT,
                            blood_group TEXT,
                            email TEXT,
                            contact TEXT,
                            alternate_contact TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS login (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL)''')

        conn.commit()
        conn.close()

    def get_user(self, username):
        """Get a user from the login table by username"""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM login WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user

    def add_user(self, username, password):
        """Add a new user to the login table"""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO login (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
#======================================================faculty==================================================
    def add_columns_to_faculty(self):  # Add 'self' as the first parameter
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get the list of columns in the 'faculty' table
            cursor.execute("PRAGMA table_info(faculty)")
            columns = [column[1] for column in cursor.fetchall()]  # Get the column names

            # Add 'department' column if it doesn't already exist
            if 'department' not in columns:
                cursor.execute("ALTER TABLE faculty ADD COLUMN department TEXT")
            
            conn.commit()
        except Exception as e:
            print(f"Error adding columns: {e}")
        finally:
            conn.close()
    def add_faculty(self, name, dob, address, sex, blood_group, email, contact, alternate_contact,department):
        """Add a new faculty member"""
        try:
            conn = self.create_connection()  # Create a new connection
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO faculty (name, dob, address, sex, blood_group, email, contact, alternate_contact,department)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                            (name, dob, address, sex, blood_group, email, contact, alternate_contact,department))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Error: Faculty with email {email} already exists.")
        except Exception as e:
            print(f"Error adding faculty: {e}")
        finally:
            conn.close()

    def get_all_faculty(self):
        """Retrieve all faculty members from the database"""
        try:
            conn = self.create_connection()  # Create a new connection
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM faculty")  # Ensure the SQL query is correct
            rows = cursor.fetchall()
            # Convert rows to a list of dictionaries for easier template rendering
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Error retrieving faculty data: {e}")
            return []  # Return an empty list on error
        finally:
            conn.close()

    def search_faculty(self, query):
        """Search faculty by name or email"""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculty WHERE name LIKE ? OR email LIKE ?", ('%' + query + '%', '%' + query + '%'))
        results = cursor.fetchall()
        conn.close()
        
        if results:
            print("Results Found:", results)
        else:
            print("No results found for query:", query)
        
        return results

    def get_faculty_by_id(self, id):
        """Get a specific faculty member by ID"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM faculty WHERE id = ?', (id,))
        faculty = cursor.fetchone()
        conn.close()
        return faculty

    def update_faculty(self, id, name, dob, address, sex, blood_group, email, contact, alternate_contact,department):
        """Update faculty member details"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('''UPDATE faculty SET name = ?, dob = ?, address = ?, sex = ?, blood_group = ?, 
                          email = ?, contact = ?, alternate_contact = ?, department = ? WHERE id = ?''', 
                          (name, dob, address, sex, blood_group, email, contact, alternate_contact, department, id))
        conn.commit()
        conn.close()

    def delete_faculty(self, id):
        """Delete a faculty member"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM faculty WHERE id = ?', (id,))
        conn.commit()
        conn.close()
#============================================Students==============================================================
    def add_columns_to_students(self):  # Add 'self' as the first parameter
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get the list of columns in the 'students' table
            cursor.execute("PRAGMA table_info(students)")
            columns = [column[1] for column in cursor.fetchall()]  # Get the column names

            # Add 'department' column if it doesn't already exist
            if 'department' not in columns:
                cursor.execute("ALTER TABLE students ADD COLUMN department TEXT")
            
            # Add 'sem' column if it doesn't already exist
            if 'sem' not in columns:
                cursor.execute("ALTER TABLE students ADD COLUMN sem TEXT")
            
            conn.commit()
        except Exception as e:
            print(f"Error adding columns: {e}")
        finally:
            conn.close()

    def add_students(self, name, dob, address, sex, blood_group, email, contact, alternate_contact,department,sem):
        """Add a new faculty member"""
        try:
            conn = self.create_connection()  # Create a new connection
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO students (name, dob, address, sex, blood_group, email, contact, alternate_contact,department,sem)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                            (name, dob, address, sex, blood_group, email, contact, alternate_contact,department,sem))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Error: Student with email {email} already exists.")
        except Exception as e:
            print(f"Error adding student: {e}")
        finally:
            conn.close()

    def get_all_students(self):
        """Retrieve all student members from the database"""
        try:
            conn = self.create_connection()  # Create a new connection
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")  # Ensure the SQL query is correct
            rows = cursor.fetchall()
            # Convert rows to a list of dictionaries for easier template rendering
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Error retrieving student data: {e}")
            return []  # Return an empty list on error
        finally:
            conn.close()


    def get_students_by_id(self, id):
        """Get a specific student member by ID"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (id,))
        faculty = cursor.fetchone()
        conn.close()
        return faculty

    def delete_students(self, id):
        """Delete a student member"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def add_sample_students(self):
        """Add sample student members to the database"""
        sample_student = [
            ('John Doe', '1980-01-01', '123 Elm St', 'Male', 'O+', 'john@example.com', '1234567890', '0987654321','Computer Science','S5'),
            ('Jane Smith', '1985-02-02', '456 Oak St', 'Female', 'A-', 'jane@example.com', '2345678901', '8765432109','Computer Science','S5'),
            ('Emily Johnson', '1990-03-03', '789 Pine St', 'Female', 'B+', 'emily@example.com', '3456789012', '7654321098','Computer Science','S5')
        ]
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO students (name, dob, address, sex, blood_group, email, contact, alternate_contact,department,sem)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', sample_student)
        conn.commit()
        conn.close()
#======================================================lab_staff==================================================
    def add_columns_to_lab_staff(self):  # Add 'self' as the first parameter
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get the list of columns in the 'lab_staff' table
            cursor.execute("PRAGMA table_info(lab_staff)")
            columns = [column[1] for column in cursor.fetchall()]  # Get the column names

            # Add 'department' column if it doesn't already exist
            if 'department' not in columns:
                cursor.execute("ALTER TABLE lab_staff ADD COLUMN department TEXT")
            
            # Add 'position' column if it doesn't already exist
            if 'position' not in columns:
                cursor.execute("ALTER TABLE lab_staff ADD COLUMN position TEXT")

            # Add 'lbname' column if it doesn't already exist
            if 'lbname' not in columns:
                cursor.execute("ALTER TABLE lab_staff ADD COLUMN lbname TEXT")
            
            conn.commit()
        except Exception as e:
            print(f"Error adding columns: {e}")
        finally:
            conn.close()
    def add_lab_staff(self, name, dob, address, sex, blood_group, email, contact, alternate_contact,department,position,lbname):
        """Add a new faculty member"""
        try:
            conn = self.create_connection()  # Create a new connection
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO lab_staff (name, dob, address, sex, blood_group, email, contact, alternate_contact,department,position,lbname)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                            (name, dob, address, sex, blood_group, email, contact, alternate_contact,department,position,lbname))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Error: Labstaff with email {email} already exists.")
        except Exception as e:
            print(f"Error adding labstaff: {e}")
        finally:
            conn.close()

    def get_all_lab_staff(self):
        """Retrieve all faculty members from the database"""
        try:
            conn = self.create_connection()  # Create a new connection
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lab_staff")  # Ensure the SQL query is correct
            rows = cursor.fetchall()
            # Convert rows to a list of dictionaries for easier template rendering
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Error retrieving labstaff data: {e}")
            return []  # Return an empty list on error
        finally:
            conn.close()

    

    def get_lab_staff_by_id(self, id):
        """Get a specific faculty member by ID"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lab_staff WHERE id = ?', (id,))
        lab_staff = cursor.fetchone()
        conn.close()
        return lab_staff

    def delete_lab_staff(self, id):
        """Delete a faculty member"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM lab_staff WHERE id = ?', (id,))
        conn.commit()
        conn.close()
#================================================= MANAGEMENT ================================= 
    def add_column_to_management(self):
        """Alter the management table to add the 'des' column if it doesn't exist."""
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE management ADD COLUMN des TEXT")
            conn.commit()
            print("Column 'des' added to management table successfully.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("Column 'des' already exists in management table.")
            else:
                print(f"Error altering management table: {e}")
        finally:
            conn.close()

    def add_management(self, name, des, dob, address, sex, blood_group, email, contact, alternate_contact):
        """Add a new management member"""
        try:
            conn = self.create_connection()  # Create a new connection
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO management (name, des, dob, address, sex, blood_group, email, contact, alternate_contact)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                            (name, des, dob, address, sex, blood_group, email, contact, alternate_contact))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Error: Management with email {email} already exists.")
        except Exception as e:
            print(f"Error adding management: {e}")
        finally:
            conn.close()
    
    def get_all_management(self):
        """Retrieve all management members from the database"""
        try:
            conn = self.create_connection()  # Create a new connection
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM management")  # Ensure the SQL query is correct
            rows = cursor.fetchall()
            # Convert rows to a list of dictionaries for easier template rendering
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Error retrieving management data: {e}")
            return []  # Return an empty list on error
        finally:
            conn.close()

    def get_management_by_id(self, id):
        """Get a specific management member by ID"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM management WHERE id = ?', (id,))
        management = cursor.fetchone()
        conn.close()
        return management

    def delete_management(self, id):
        """Delete a management member"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM management WHERE id = ?', (id,))
        conn.commit()
        conn.close()
#==============================================office_staff=======================================================
    def add_columns_to_office_staff(self):  # Add 'self' as the first parameter
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            # Get the list of columns in the 'office_staff' table
            cursor.execute("PRAGMA table_info(office_staff)")
            columns = [column[1] for column in cursor.fetchall()]  # Get the column names

            # Add 'job_title' column if it doesn't already exist
            if 'job_title' not in columns:
                cursor.execute("ALTER TABLE office_staff ADD COLUMN job_title TEXT")
            
            conn.commit()
        except Exception as e:
            print(f"Error adding columns: {e}")
        finally:
            conn.close()
    def add_office_staff(self, name, dob, address, sex, blood_group, email, contact, alternate_contact,job_title):
            """Add a new faculty member"""
            try:
                conn = self.create_connection()  # Create a new connection
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO office_staff (name, dob, address, sex, blood_group, email, contact, alternate_contact,job_title)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                                (name, dob, address, sex, blood_group, email, contact, alternate_contact,job_title))
                conn.commit()
            except sqlite3.IntegrityError:
                print(f"Error: officestaff with email {email} already exists.")
            except Exception as e:
                print(f"Error adding officestaff: {e}")
            finally:
                conn.close()

    def get_all_office_staff(self):
        """Retrieve all faculty members from the database"""
        try:
            conn = self.create_connection()  # Create a new connection
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM office_staff")  # Ensure the SQL query is correct
            rows = cursor.fetchall()
            # Convert rows to a list of dictionaries for easier template rendering
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Error retrieving officestaff data: {e}")
            return []  # Return an empty list on error
        finally:
            conn.close()



    def get_office_staff_by_id(self, id):
        """Get a specific faculty member by ID"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM office_staff WHERE id = ?', (id,))
        office_staff = cursor.fetchone()
        conn.close()
        return office_staff

    def delete_office_staff(self, id):
        """Delete a faculty member"""
        conn = self.create_connection()  # Create a new connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM office_staff WHERE id = ?', (id,))
        conn.commit()
        conn.close()

#==================================================================================================================
# Example of usage
db = Database()
# Uncomment the next line to add sample data
# db.add_sample_faculty()

# Display all faculty records
faculties = db.get_all_faculty()
for faculty in faculties:
    print(faculty)
students = db.get_all_students()
for student in students:
    print(student)
lab_staffs = db.get_all_lab_staff()
for lab_staff in lab_staffs:
    print(lab_staff)
managements = db.get_all_management()
for management in managements:
    print(management)
office_staffs = db.get_all_office_staff()
for office_staff in office_staffs:
    print(office_staff)
