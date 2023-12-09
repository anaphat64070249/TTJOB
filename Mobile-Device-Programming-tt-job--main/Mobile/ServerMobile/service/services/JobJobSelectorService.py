from ..connect_database.Database import database;
from flask import Flask, json, jsonify;
import json;
import datetime;


class JobSelectorService:
    db = database();
    def __init__(self):
        pass
    
    def getAll(self):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        try:
            sql_get_all_jobs = "SELECT * FROM Jobs;";
            cursor.execute(sql_get_all_jobs);
            reply = cursor.fetchall();
            return reply, 200;
        except Exception as error:
            print(error);
            return {"message": "Error", "error": error}, 500
        finally:
            cursor.close();
            self.db.close();
    
    def getJob_on_date(self, date):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        
        try:
            sql_select_on_date = "SELECT com_id, job_id, job_id, bussines_type, companyName, position, job_date_declear, pay, time_start, time_end,avg_score, image_company, apply_type, day_work FROM Jobs AS j LEFT OUTER JOIN Company_infomations AS info USING(com_id) WHERE j.status = true AND job_date_declear = {0} AND emp_amount != 0;".format("'"+date+"'");
            print(sql_select_on_date)
            cursor.execute(sql_select_on_date);
            reply = cursor.fetchall();
            return reply, 200;
        except Exception as error:
            print(error);
            return {
                "message": "Have Error!",
                "error": error
            }, 500;
        finally:
            cursor.close();
            self.db.close();
            
    def getJob_detail_by_id(self, job_id):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        
        try:
            sql_select_job = "SELECT * FROM Jobs WHERE job_id = "+job_id;
            cursor.execute(sql_select_job);
            jobs = cursor.fetchone();
            print(jobs)
            sql_join_jobs_and_company = "SELECT * FROM Company LEFT OUTER JOIN Com_address USING(com_id) WHERE com_id = "+str(jobs['com_id']);
            cursor.execute(sql_join_jobs_and_company);
            address = cursor.fetchone();
            return {
                "jobInfo": jobs,
                "address": address
            }, 200;
        except Exception as error:
            print(error);
            return {
                "message": "Have Error!",
                "error": error
            }, 500;
        finally:
            cursor.close();
            self.db.close();
    
    def getJobs_isApplyed(self, emp_id):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        
        try:
            sql_select_job_applyed = "SELECT job_id, companyName, position,image_company, job_date_declear, avg_score, day_start, com_confirm, emp_confirm, day_end, time_start, time_end, working_hours,day_work, pay, apply_type FROM Job_registor LEFT OUTER JOIN Jobs using(job_id) LEFT OUTER JOIN Company_infomations USING(com_id) WHERE emp_id = {0} AND job_doing = false AND cancel_status = false AND isFinish = false;".format(emp_id);
            cursor.execute(sql_select_job_applyed);
            response = cursor.fetchall();
            if len(response) == 0:
                return [{"is_apply": False}, response]
            return [{"is_apply": True}, response]
        except Exception as error:
            print(error);
            return {
                "message": "Have Error!",
                "error": error
            }, 500;
        finally:
            cursor.close();
            self.db.close();
            
    def getJob_isDoing(self, emp_id):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        date = datetime.datetime.now();
        now = str(date.year)+'-' + str(date.month)+'-' + str(date.day);
        try:
            sql_select_job_doing = "SELECT job_id, companyName, position,image_company, job_date_declear, avg_score, day_start, com_confirm, emp_confirm, day_end, time_start, time_end, working_hours,day_work, pay, apply_type FROM Job_registor LEFT OUTER JOIN Jobs using(job_id) LEFT OUTER JOIN Company_infomations USING(com_id) WHERE emp_id = {0} AND job_doing = true  AND isFinish = false;".format(emp_id);
            cursor.execute(sql_select_job_doing);
            response = cursor.fetchone();
            
            if response is None:
                return [{"isDoing": False}, {"job": ''}]
            return [{"isDoing": True}, response];
            
        except Exception as error:
            print(error);
            return {
                "message": "Have Error!",
                "error": error
            }, 500;
        finally:
            cursor.close();
            self.db.close();
    
    