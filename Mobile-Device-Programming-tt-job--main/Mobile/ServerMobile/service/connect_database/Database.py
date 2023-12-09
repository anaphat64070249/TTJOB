import mysql.connector ;

def database():
    """
        connet your database
    """
    
    host = "Your host";
    user = "Your username";
    password = "Your password";
    database_name = "Your database";
    
    pool = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database_name,
            auth_plugin='mysql_native_password'
    );
    return pool;