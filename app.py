from flask import Flask, request
from flask_restful import Resource, Api
from simple_salesforce import Salesforce

import os
from threading import Thread

app = Flask(__name__)
api = Api(app)

CHANGE_STATUS_INTENT = "Change status"
SET_POINTS_INTENT = ""
REMOVE_FROM_SPRINT_INTENT = ""

GUS_ENTITY_WORK_ITEM = "ADM_Work__c"
GUD_FIELD_WORK_ID_AND_SUBJECT = "WorkId_and_Subject__c"
GUS_FIELD_STATUS = "Status__c"

GUS_ORG_ID = "00DT0000000DpvcMAC"

username = str(os.environ.get("USERNAME"))
password = str(os.environ.get("PASSWORD"))
sf = Salesforce(organizationId=GUS_ORG_ID, username=username, password=password)


def update_status(work_id, new_status):
    entity_id = sf.query(f"""
        SELECT Id
        FROM {GUS_ENTITY_WORK_ITEM}
        WHERE {GUD_FIELD_WORK_ID_AND_SUBJECT} LIKE '%{work_id}%'
    """)["records"][0]["Id"]
    ret = sf.ADM_Work__c.update(entity_id, {GUS_FIELD_STATUS: new_status})
    return ret


class UpdateGus(Resource):
    def get(self):
        return {"about": "Welcome to Einstein Scrum Rest API!"}

    def post(self):
        try:
            json = request.get_json()
        except:
            return {"fulfillmentText": "Something went wrong with the json parsing."}, 401
        try:
            if json["queryResult"]["intent"]["displayName"] == CHANGE_STATUS_INTENT:
                work_id = json["queryResult"]["parameters"]["WorkId"]
                new_status = json["queryResult"]["parameters"]["Status"]
                thread = Thread(target=update_status, kwargs={"work_id": work_id, "new_status": new_status})
                thread.start()
                # ret = update_status(work_id, new_status)
                # if ret == 200 or ret == 204:
                return {"fulfillmentText": "Changed status successfully"}
                # else:
                #     return {"fulfillmentText": "Could not update status."}, 402
        except:
            return {"fulfillmentText": "Request was not the right format"}, 403


api.add_resource(UpdateGus, "/")

if __name__ == "__main__":
    app.run(debug=True)
