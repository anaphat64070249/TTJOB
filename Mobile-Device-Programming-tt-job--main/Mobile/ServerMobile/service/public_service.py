from flask.blueprints import Blueprint;
from flask import request;
import requests;

public_service = Blueprint("public_service", __name__);

@public_service.route('/map/', methods=["GET"])
def getMap():
    """
        GetMap Geometry
        
    """
    name = request.args.get('name'); # address where you need Map
    api_key = "Your google API key"; # copy your api key => Paste to value at api_key
    api = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cname%2Cgeometry&input="+name+"&inputtype=textquery&key={0}".format(api_key);
    response = requests.get(api);
    response_to = response.json();
    location = response_to['candidates'];
    
    return location[0]['geometry']['location'];