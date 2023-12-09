from ..services.MessageServer import MessageService;
from flask import Blueprint;

message = Blueprint("message", __name__);

messageService = MessageService();

@message.route("/<emp_id>", methods=['GET'])
def message_by_id(emp_id: int):
    return messageService.viewMessage(emp_id);

