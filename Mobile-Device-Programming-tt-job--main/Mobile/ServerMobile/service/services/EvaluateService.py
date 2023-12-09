from ..connect_database.Database import database;
import datetime

class EvaluateService:
    db = database();
    
    def __init__(self):
        pass
    
    def evalute(self, emp_id, job_id, reviewer_name, score, comments, report, reviewer):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        self.db.start_transaction();
        # if (comments == ""):
        #     comments = "Not have";
        # if (report == ""):
        #     report = "ไม่มี";
        cursor_update = self.db.cursor();
        try:
            sql_insert_reviews = "INSERT INTO Reviews(emp_id, job_id, reviewer_name, score, comments, report, reviewer) VALUES({0}, {1}, {2}, {3}, {4}, {5}, {6})";
            insert_add_values = sql_insert_reviews.format(emp_id, job_id, "'"+reviewer_name+"'", score, "'"+comments+"'", "'"+report+"'", "'"+reviewer+"'");
            print(insert_add_values);
            cursor.execute(insert_add_values);
            
            select_company_info_use_update = "SELECT com_id, pay, working_hours FROM Jobs LEFT OUTER JOIN Company USING(com_id) WHERE job_id = {0}".format(job_id);
            print(select_company_info_use_update);
            cursor.execute(select_company_info_use_update);
            reply_company = cursor.fetchone();
            com_id = reply_company['com_id'];
            pay = reply_company['pay'];
            working_hours = reply_company['working_hours'];
            
            
            sql_insert_history = "INSERT INTO Emp_job_history(job_id, emp_id, pay, work_hour, job_status, annotation) VALUES({0},{1},{2},{3},{4},{5})";
            insert_add_values_history = sql_insert_history.format(job_id, emp_id, pay, working_hours, True, "null");
            print(insert_add_values_history)
            cursor.execute(insert_add_values_history);
            
            select_jobID_in_comID = "SELECT job_id FROM Reviews LEFT OUTER JOIN Jobs USING(job_id) WHERE com_id = {0} AND reviewer = 'emp';".format(com_id);
            cursor.execute(select_jobID_in_comID);
            reply_list_jobID = cursor.fetchall();
            list_ids = [];
            for id in reply_list_jobID:
                list_ids.append(id['job_id']);
            print();
            print(list_ids)
            print()
            select_age_score = "SELECT AVG(score) as `avg` FROM Reviews WHERE job_id IN {0}".format(str(tuple(list_ids)));
            cursor.execute(select_age_score);
            reply_avg = cursor.fetchone();
            

            select_update_avg_score = "UPDATE Company_infomations SET avg_score = {0}".format(reply_avg['avg']);
            cursor_update.execute(select_update_avg_score);
            print(cursor_update.rowcount, "record(s) affected 1");
            update_status_registor = "UPDATE Job_registor SET isFinish = true WHERE job_id = {0} AND emp_id = {1}".format(job_id, emp_id);
            cursor_update.execute(update_status_registor);
            
            sql_update_job_status = "UPDATE Jobs SET status = false WHERE job_id = {0}".format(job_id);
            cursor_update.execute(sql_update_job_status);
            print(cursor_update.rowcount, "record(s) affected 2");
            self.db.commit();
            return {"status": True}, 200;
        except Exception as error:
            print(error);
            self.db.rollback();
            return {
                "status": False,
                "error": error
            }, 409;
        finally:
            cursor.close();
            cursor_update.close();
            self.db.close();
            
    def getJobAndInfo_Use_inEvaluate_find_by_id(self, job_id):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        
        try:
            sql_select_jobInfo_by_id = "SELECT com_id,avg_score, manager_name FROM Jobs LEFT OUTER JOIN Company_infomations USING(com_id) WHERE job_id = {0}";
            sql_select_add_job_id = sql_select_jobInfo_by_id.format(job_id);
            cursor.execute(sql_select_add_job_id);
            
            reply = cursor.fetchone();
            return reply, 200;
        
        except Exception as error:
            print(error);
            return {
                "status": False,
                "error": error
            }, 500;
        finally:
            cursor.close();
            self.db.close();