from ..connect_database.Database import database;
import datetime

class ApplyJobService:
    db = database();
    date = datetime.datetime.now();
    data_apply = str(date.year) +"-"+ str(date.month) +"-"+ str(date.day);
    dateConfirm = str(date.year) +"-"+ str(date.month) +"-"+ str(date.day);
    
    def __init__(self):
        pass
    
    def apply(self, emp_id, job_id, apply_type):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        sql = '';
        self.db.start_transaction();
        try:
            check_register_amount_sql = "SELECT count(job_id) as num FROM project_db.Job_registor WHERE emp_id = {0} AND job_id = {1};".format(emp_id, job_id);
            print(check_register_amount_sql)
            cursor.execute(check_register_amount_sql);
            num = cursor.fetchone();
            print(num)
            if (num['num'] != 0):
                return {"status": False, "message": "Apply failed registed"}, 409;
            
            if (apply_type == 1):
                sql = "INSERT INTO Job_registor(job_id, emp_id, data_apply, date_com_confirm, com_confirm) VALUES({0},{1},{2},{3}, 1);";
                print(sql)
                sql = sql.format(job_id, emp_id, "'"+self.data_apply +"'" , "'"+self.dateConfirm +"'");
            elif (apply_type == 2):
                sql = "INSERT INTO Job_registor(job_id, emp_id, data_apply) VALUES({0},{1},{2});";
                print(sql)
                sql = sql.format(job_id, emp_id, "'"+self.data_apply +"'");
            # else:
            #     return {"status": False, "message": "Apply failed registed"}, 409;
            cursor.execute(sql);
            
            cursor.execute("SELECT emp_amount FROM Jobs WHERE job_id = "+ str(job_id));
            amount = cursor.fetchone();
            update_amount_sql = "UPDATE Jobs SET emp_amount = " + str(int(amount['emp_amount']) - 1) + " WHERE job_id = "+ str(job_id);
            print(update_amount_sql);
            cursor.execute(update_amount_sql);
            
            # print("UPDATE Jobs SET status = 0 WHERE emp_amount = 0  job_id = "+ str(self.job_id))
            # cursor.execute("UPDATE Jobs SET status = 0 WHERE emp_amount = 0 AND job_id = "+ str(self.job_id));
            self.db.commit();
            return {"status": True, "message": "Apply Successful "+ str(self.data_apply)}, 200;
        except Exception as error:
            self.db.rollback();
            print(error);
            return {"status": False, "message": "Apply failed"}, 409;
        finally:
            cursor.close();
            self.db.close();
            
    def update_emp_confirm(self, emp_id, job_id, emp_confirm):
        self.db.connect();
        cursor = self.db.cursor();
        if emp_confirm == True:
            emp_confirm = "true";
        else:
            emp_confirm = "false";
        
        try:
            sql = "UPDATE Job_registor SET emp_confirm = {0} WHERE job_id = {1} AND emp_id = {2}".format(emp_confirm, job_id ,emp_id);
            print(sql);
            cursor.execute(sql);
            self.db.commit();
            return {'status': True, 'message': "Update Apply job suscessfuly!"}, 200
        except Exception as error:
            print(error);
            return {'status': False, 'message': "Update Apply job failed !"}, 409
        finally:
            cursor.close();
            self.db.close();
            
    def cancelApply(self, emp_id, job_id):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True)
        try:
            sql = "DELETE FROM Job_registor WHERE emp_id = {0} AND job_id = {1};".format(emp_id, job_id);
            print(sql)
            cursor.execute(sql);
            self.db.commit();
            return {"status": True}, 200;
        except Exception as error:
            print(error)
            return {"status": False}, 409;
        finally:
            cursor.close();
            self.db.close();
    
