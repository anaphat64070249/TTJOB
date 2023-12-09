from ..connect_database.Database import database
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pyrebase
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', }
path = os.path.join('service', 'static', 'uploads')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# config firebase
firebaseConfig = {
    'apiKey': "",
    'authDomain': "",
    'projectId': "",
    'storageBucket': "",
    'messagingSenderId': "",
    'appId': "",
    'measurementId': "",
    'serviceAccount': 'service/serviceAccount.json',
    'databaseURL': ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('your email', 'your password');


class Employees:
    db = database()

    def __init__(self):
        pass

    def create(self, body, files):
        self.db.connect()
        cursor = self.db.cursor(dictionary=True)
        self.db.start_transaction()
        try:
            if 'image_profile' not in files or 'image_personalID' not in files:
                return {"status": False, "message": "Create user " + body['email']+" failed! not image profile or personalID"}, 400
            elif allowed_file(files['image_profile'].filename) == False or allowed_file(files['image_personalID'].filename) == False:
                return {"status": False, "message": "Create user " + body['email']+" failed! Tyle image profile or personalID not allowed!"}, 400

        # Hashsing password
            password = generate_password_hash(
                body['password'],
                method="sha256"
            )
            image_profile = files['image_profile']
            image_personalID = files['image_personalID']

            # Insert Employee Account
            sql_insert_Account = "INSERT INTO Employee(email, phone, password) VALUES({0},{1},{2})"
            sql_insert_Account = sql_insert_Account.format(
                "'"+(body['email']+"'"),
                (body['phone']),
                "'"+(password)+"'"
            )

            cursor.execute(sql_insert_Account)
            emp_id = cursor.lastrowid  # Get lastID of Employee

            sql_insert_address = "INSERT INTO Emp_address(emp_id, district, tumbon, province, zipCode, address) VALUES({0}, {1}, {2}, {3}, {4}, {5})"
            sql_insert_address = sql_insert_address.format(
                emp_id, "'"+(body['district'])+"'",
                "'"+(body['tumbon'])+"'", "'"+(body['province'])+"'",
                "'"+str(body['zipCode'])+"'", "'"+(body['address'])+"'"
            )
            cursor.execute(sql_insert_address)
            address_code = cursor.lastrowid  # Get lastID from Employee ID

            # Save file imageProfile to static/uploads
            image_profile_filename = secure_filename(image_profile.filename)
            image_profile.save(os.path.join(path, image_profile_filename))
            # upload file to fireBase store and get URL of file
            storage.child(image_profile_filename).put(
                os.path.join(path, image_profile_filename))
            image_profile_url = storage.child(
                image_profile_filename).get_url(user['idToken'])

            # Save file imagePersonalId to static/uploads
            image_personalID_filename = secure_filename(
                image_personalID.filename)
            image_personalID.save(os.path.join(
                path, image_personalID_filename))
            # upload file to fireBase store and get URL of file
            storage.child(image_personalID_filename).put(
                os.path.join(path, image_personalID_filename))
            image_personalID_url = storage.child(
                image_personalID_filename).get_url(user['idToken'])

            # Insert Personal_infomation of Employee
            insert_info = "INSERT INTO Personal_infomations"\
                "(emp_id, firstName, lastName, nickName, age, gender, personal_id, date_of_birth,"\
                " weight, height, occupation, education, abilities, image_profile, image_personalID,"\
                "address_code, intro_message,"\
                " vehicle, driver_license)"
            sql_insert_UserInfo_values = insert_info + \
                " VALUES({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18});"
            sql_insert_UserInfo_values = sql_insert_UserInfo_values.format(
                emp_id,
                "'"+(body['firstName'])+"'",
                "'"+(body['lastName'])+"'",
                "'"+(body['nickName'])+"'",
                body['age'],
                "'"+(body['gender'])+"'",
                "'"+body['personal_id']+"'",
                "'"+(body['date_of_birth'])+"'",
                float(body['weight']),
                float(body['height']),
                "'"+(body['occupation'])+"'",
                "'"+(body['education'])+"'",
                "'"+(body['abilities'])+"'",
                "'"+(image_profile_url)+"'",
                "'"+(image_personalID_url)+"'",
                address_code,
                "'" + (body['intro_message'])+"'",
                "'" + (body['vehicle'])+"'",
                "'" + (body['driver_license'])+"'"
            )
            print(sql_insert_UserInfo_values)
            cursor.execute(sql_insert_UserInfo_values)
            self.db.commit()

            # Delete file in static/uploads
            if os.path.exists(os.path.join(path, image_profile_filename)):
                os.remove(os.path.join(path, image_profile_filename))
            if os.path.exists(os.path.join(path, image_personalID_filename)):
                os.remove(os.path.join(path, image_personalID_filename))

            return {"status": True, "message": "Create user " + body['email']}, 200

        except Exception as error:
            print(error)
            self.db.rollback()
            return {"status": False, "message": "Create user " + body['email']+" failed!"}, 500
        finally:
            cursor.close()
            self.db.close()

    def getEmployees(self):
        self.db.connect()
        cursor = self.db.cursor(dictionary=True)

        try:
            sql_getUser = "SELECT * FROM Employee;"
            cursor.execute(sql_getUser)
            reply = cursor.fetchall()
            return reply
        except Exception as error:
            print(error)
            return {
                "message": "Error ",
                "error": error
            }
        finally:
            cursor.close()
            self.db.close()

    def getInfomationAndEmployee_All(self):
        self.db.connect()
        cursor = self.db.cursor(dictionary=True)

        try:
            sql_GetInfoAndEmployee = "SELECT emp_id, email, phone, user_status, free_status, firstName, lastName, nickName, age, gender, personal_id, date_of_birth, weight, height, occupation, education, abilities, image_profile, image_personalID, address_code, intro_message, vehicle, driver_license FROM Employee LEFT OUTER JOIN Personal_infomations USING(emp_id);"
            cursor.execute(sql_GetInfoAndEmployee)
            reply = cursor.fetchall()
            return reply, 200

        except Exception as error:
            print(error)
            return {
                "message": "Error ",
                "error": error
            }, 500

        finally:
            cursor.close()
            self.db.close()

    def getEmployee_by_emp_id(self, emp_id):
        self.db.connect()
        cursor = self.db.cursor(dictionary=True)

        try:
            sql_select_by_id = "SELECT * FROM Employee WHERE emp_id = {0};".format(
                emp_id)
            cursor.execute(sql_select_by_id)
            reply = cursor.fetchone()
            return reply, 200

        except Exception as error:
            print(error)
            return {"message": "Error", "error": error}, 500

        finally:
            cursor.close();
            self.db.close();

    def getInfoAndEmployee_by_id(self, emp_id):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        try:
            sql_GetInfoAndEmployee_by_id = "SELECT emp_id, email, phone, user_status, free_status, firstName, lastName, nickName, age, gender, personal_id, date_of_birth, weight, height, occupation, education, abilities, image_profile, image_personalID, address_code,experience_hour,avg_score, intro_message, vehicle, driver_license FROM Employee LEFT OUTER JOIN Personal_infomations USING(emp_id) WHERE emp_id={0};".format(emp_id);
            cursor.execute(sql_GetInfoAndEmployee_by_id);
            reply = cursor.fetchone();
            return reply, 200;

        except Exception as error:
            print(error);
            return {"message": "Error", "error": error}, 500;
        finally:
            cursor.close();
            self.db.close();

    def getAddress_by_id(self, emp_id):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        
        try:
            sql_selevt_address = "SELECT * FROM Emp_address WHERE emp_id="+emp_id;
            cursor.execute(sql_selevt_address);
            reply = cursor.fetchone();
            return reply, 200;
        except Exception as error:
            print(error);
            return {"message": "Error", "error": error}, 500;
        finally:
            cursor.close();
            self.db.close();
    
    def getAccount_getFullName(self, emp_id):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        try:
            sql_select_Account = "SELECT firstName, lastName  FROM Emp_address LEFT OUTER JOIN Personal_infomations USING(emp_id) WHERE emp_id="+emp_id;
            cursor.execute(sql_select_Account);
            reply = cursor.fetchone();
            return reply, 200;
        except Exception as error:
            print(error);
            return {"message": "Error", "error": error}, 500;
        finally:
            cursor.close();
            self.db.close();
    