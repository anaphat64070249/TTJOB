from ..connect_database.Database import database;

class MessageService:
    db = database();
    
    def __init__(self):
        pass;
    def createMessage():
        pass;
    
    def viewMessage(self, emp_id):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        
        try:
            sql_views = "SELECT message_id, job_id, emp_id,message_type,message_detail,message_daySend,position, day_start, day_end, time_start, time_end, companyName FROM project_db.Message left outer join Jobs using (job_id) left outer join Company_infomations using(com_id) where emp_id = {0} order by message_daySend DESC;".format(emp_id);
            cursor.execute(sql_views);
            reply = cursor.fetchall();
            return reply, 200;
        except Exception as error:
            print(error);
            return {
                "message": "Have Error",
                "error": error
            }
        finally:
            cursor.close();
            self.db.close();
            