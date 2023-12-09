from flask import Flask
from flask_login import login_manager, LoginManager;
from flask_cors import CORS;

def AppServer():
    app = Flask(__name__);
    CORS(app);
    app.config['SCREAT_KEY'] = "mobile";
    from .authen import authen;
    from .controllers.EmployeeController import employee;
    from .controllers.JobSelectorController import jobSelectorController;
    from .public_service import public_service;
    from .controllers.ApplyJobController import apply;
    from .controllers.EvaluateController import evaluate;
    from .controllers.HistorySelectorController import history;
    from .controllers.MessageController import message;
    
    app.register_blueprint(authen, url_prefix = '/auth');
    app.register_blueprint(employee, url_prefix = '/emp');
    app.register_blueprint(jobSelectorController, url_prefix = '/job');
    app.register_blueprint(public_service, url_prefix = '/');
    app.register_blueprint(apply, url_prefix = '/apply');
    app.register_blueprint(evaluate, url_prefix = '/evaluate');
    app.register_blueprint(history, url_prefix = "/history");
    app.register_blueprint(message, url_prefix = "/message")
    
    login_manager = LoginManager();
    login_manager.login_view= 'auth.login';
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def login(id):
        """"""
        print("LOGIN ID: ", id);
    
    return app;