from flask.blueprints import Blueprint;
from ..services.JobJobSelectorService import JobSelectorService;
from flask import json, jsonify

jobSelectorController = Blueprint("jobSelectorController", __name__);

jobSelectorService = JobSelectorService();

@jobSelectorController.route('/all', methods=["GET"])
def getJob_all():
    return jobSelectorService.getAll();

@jobSelectorController.route("/job_on_date/<date>", methods=["GET"])
def getJob_by_date(date: str):
    return jobSelectorService.getJob_on_date(date);

@jobSelectorController.route("/jobInfo/<job_id>")
def getJobInfo_by_id(job_id: int):
    print(job_id);
    reply = jobSelectorService.getJob_detail_by_id(job_id);
    return reply;

@jobSelectorController.route("/applyed/<emp_id>")
def getJob_applyed_by_id(emp_id: int):
    return jobSelectorService.getJobs_isApplyed(emp_id);

@jobSelectorController.route("/doing/<emp_id>")
def getJob_doing_by_id(emp_id: int):
    return jobSelectorService.getJob_isDoing(emp_id);

