from ..services.EvaluateService import EvaluateService;
from flask import Blueprint, request;

evaluate = Blueprint("evaluate", __name__);

evaluateService = EvaluateService();

@evaluate.route("/", methods=["POST"])
def evaluate_by_emp():
    body = request.json;
    print(body);
    emp_id = body['emp_id'];
    print(emp_id)
    job_id = body['job_id'];
    reviewer_name = body['reviewer_name'];
    score = body['score'];
    comments = body['comments'];
    report = body['report'];
    reviewer = body['reviewer'];
    
    return evaluateService.evalute(emp_id, job_id, reviewer_name,
                                   score, comments, report, reviewer);
    
@evaluate.route("/info/<job_id>", methods=["GET"])
def getInfo_for_evaluate(job_id : int):
    print(job_id)
    return evaluateService.getJobAndInfo_Use_inEvaluate_find_by_id(job_id);

