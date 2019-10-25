from flask import Flask, request
from flask_restful import Resource, Api
import beatbox
import os

app = Flask(__name__)
api = Api(app)

CHANGE_STATUS_INTENT = "Change status"
SET_POINTS_INTENT = ""
REMOVE_FROM_SPRINT_INTENT = ""

GUS_ENTITY_WORK_ITEM = "ADM_Work__c"
GUD_FIELD_WORK_ID_AND_SUBJECT = "WorkId_and_Subject__c"
GUS_FIELD_STATUS = "Status__c"

try:
    sf = beatbox._tPartnerNS
    svc = beatbox.Client()
    username = str(os.environ.get("USERNAME"))
    password = str(os.environ.get("PASSWORD"))
    svc.login(username, password)
except:
    pass


def update_status(work_id, new_status):
    id = svc.query(f"""
        SELECT Id
        FROM {GUS_ENTITY_WORK_ITEM}
        WHERE {GUD_FIELD_WORK_ID_AND_SUBJECT} LIKE '%{work_id}%'
    """)[sf.records:][0][1][0]
    s = {
        "type": GUS_ENTITY_WORK_ITEM,
        "Id": id,
        GUS_FIELD_STATUS: new_status
    }
    sr = svc.update(s)
    return sr


class UpdateGus(Resource):
    def get(self):
        return {"about": "Welcome to Einstein Scrum Rest API!"}

    def post(self):
        json = request.get_json()
        try:
            if json["queryResult"]["intent"]["displayName"] == CHANGE_STATUS_INTENT:
                work_id = json["queryResult"]["parameters"]["WorkId"]
                new_status = json["queryResult"]["parameters"]["Status"]
                sr = update_status(work_id, new_status)
                if str(sr[sf.success]) == 'true':
                    return {"fulfillmentText": "Changed status successfully"}
                else:
                    return {"fulfillmentText": str(sr[sf.errors][sf.statusCode]) + ":" + str(sr[sf.errors][sf.message])}, 400
        except:
            return {"fulfillmentText": "Something went wrong with the json parsing."}, 400


api.add_resource(UpdateGus, "/")

if __name__ == "__main__":
    app.run(debug=True)
