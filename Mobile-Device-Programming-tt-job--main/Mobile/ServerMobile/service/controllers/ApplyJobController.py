from flask import Blueprint, request;
from ..services.ApplyJobService import ApplyJobService;


apply = Blueprint("apply", __name__);
applyService = ApplyJobService();

@apply.route("/", methods=["POST"])
def apply_job():
    body = request.get_json();
    emp_id = body["emp_id"];
    job_id = body["job_id"];
    apply_type = body['apply_type'];
    return applyService.apply(emp_id, job_id, apply_type);

@apply.route("/update", methods=["PUT"])
def update_emp_confirm():
    body = request.get_json();
    emp_id = body["emp_id"];
    job_id = body["job_id"];
    emp_confirm = body["emp_confirm"];
    return applyService.update_emp_confirm(emp_id, job_id, emp_confirm);

@apply.route('/cancel/<emp_id>/<job_id>', methods=["DELETE"])
def delete(emp_id: int, job_id: int):
    return applyService.cancelApply(emp_id, job_id);

