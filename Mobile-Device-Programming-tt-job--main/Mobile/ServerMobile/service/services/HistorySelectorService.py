from ..connect_database.Database import database;
from flask import jsonify;

class HistorySelectorService:
    db = database();
    
    def __init__(self):
        pass;
    
    def getJobHistory(self, emp_id):
        self.db.connect();
        cursor = self.db.cursor(dictionary=True);
        try:
            data = [];
            history = [];
            user = {};
            sql_userInfo = "SELECT emp_id, image_profile, experience_hour, avg_score, firstName, lastName FROM Personal_infomations WHERE emp_id = {0};".format(emp_id);
            cursor.execute(sql_userInfo);
            user = cursor.fetchone();
            data.append(user);
            sql_history = "SELECT * FROM Emp_job_history as jh left outer join (SELECT job_id, bussines_type, position FROM  Jobs left outer join Company_infomations using(com_id)) as b using(job_id) left outer join (SELECT score, job_id, reviewer FROM Reviews where reviewer = 'com') as r on(r.job_id = b.job_id) where emp_id = {0} and r.score is not null;".format(emp_id);
            cursor.execute(sql_history);
            response_sql = cursor.fetchall();
            tem_title = [];
            tem_position = [];
            

            for item in response_sql:
                    if (item['bussines_type'] not in tem_title ):
                        tem_title.append(item['bussines_type']);
                
            for item in tem_title:
                    tem = {
                        "title": item,
                        "all_work_hour": 0,
                        "data" : []
                    }
                    allHour = 0;
                    def ch(po):
                        for n in tem['data']:
                            if n['position'] == po:
                                return True;
                        return False;

            for info in response_sql:
                    if (info['bussines_type'] == item):
                        
                        if ch(info['position']) == False:
                            tem_inside = {
                                "position": info['position'],
                                "work_hour": info['work_hour'],
                                "avg_score": info['score'],
                                "sum_score": info['score'],
                                "sum_this_position": 1,
                            }
                            allHour += info['work_hour']
                            tem['data'].append(tem_inside);
                        else:
                            i = 0;
                            allHour += info['work_hour']
                            for k in tem['data']:
                                if (info['position'] == k['position']):
                                    tem['data'][i]['sum_score'] = tem['data'][i]['sum_score'] + info['score'];
                                    tem['data'][i]['sum_this_position']+=1;
                                    tem['data'][i]['work_hour'] += info['work_hour']
                                    tem['data'][i]['avg_score'] = round(tem['data'][i]['sum_score'] / tem['data'][i]['sum_this_position'], 2);
                                i+=1;
            
            tem['all_work_hour'] = allHour;
            history.append(tem);
            data.append(history);
            print(data);
            return data, 200;
        except Exception as error:
            print(error);
            return {
                "message": "Have Error!",
                "error": error
            }, 500;
        finally:
            cursor.close();
            self.db.close();
    