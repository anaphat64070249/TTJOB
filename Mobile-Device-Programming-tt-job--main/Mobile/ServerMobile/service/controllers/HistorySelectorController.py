from ..services.HistorySelectorService import HistorySelectorService;

from flask import Flask, Blueprint;

history = Blueprint("history", __name__);

historyService = HistorySelectorService();

@history.route("/get/<emp_id>")
def GetHistory_by_id(emp_id: int):
    return historyService.getJobHistory(emp_id);

