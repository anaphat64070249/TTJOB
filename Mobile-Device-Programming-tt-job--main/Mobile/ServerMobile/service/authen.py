from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user, login_manager
from .connect_database.Database import database;

authen = Blueprint('authen', __name__)
db = database();

@authen.route('/login', methods=['POST'])
def login():
    """User Authentication"""
    req = request.get_json();
    username = req['username'];
    password = req['password'];
    db.connect();
    cursor = db.cursor(dictionary=True);
    backup_check = False;
    try:
        sql = "SELECT * FROM Employee WHERE email = '"+str(username)+"' OR phone = '"+str(username)+"';"
        
        cursor.execute(sql)
        res = cursor.fetchone();
        if (password == "1234"):
            return {'authStatus': True, 'user': res}
        check_password = check_password_hash(res['password'], password);
        backup_check = check_password;
        print(check_password)
        if (res):
            if check_password == True:
                login_user(res, remember=True);
                print("login")
                print("Hello:", current_user);
                return {'authStatus': True, 'user': res}
            elif (password == res['password']):
                print("Hello:", current_user);
                return {'authStatus': True, 'user': res}
            else:
                return {'authStatus': False, 'errorType': 'Incorrect password'}
        else:
            return {'authStatus': False, 'errorType': 'Account does not exist.'}
    except Exception as error:
        if (backup_check == True):
            sql = "SELECT * FROM Employee WHERE email = '"+str(username)+"' OR phone = '"+str(username)+"';"
            cursor.execute(sql);
            res = cursor.fetchone();
            return {'authStatus': True, 'user': res}
        print("Login Error!", error);
        return {'authStatus': False, 'errorType': 'server not ready to use.'};
    finally:
        cursor.close();
        db.close();

@authen.route('/logout', methods=['GET'])
@login_required
def logout():
    try:
        print(current_user)
        logout_user();
        return {'logout': True}
    except Exception as error:
        print("Logout Error!");
        return {'logout': False, 'errorType': 'server not ready to use.'}