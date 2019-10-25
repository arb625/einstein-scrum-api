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


def get_connection(username, password):
    if not get_connection.connection:
        get_connection.connection = beatbox.Client()
        get_connection.connection.login(username, password)
    return get_connection.connection


get_connection.connection = None


def update_status(connection, work_id, new_status):
    connection.query(f"""
        UPDATE {GUS_ENTITY_WORK_ITEM}
        SET {GUS_FIELD_STATUS} = {new_status}
        WHERE {work_id} IN {GUD_FIELD_WORK_ID_AND_SUBJECT}
    """)


class UpdateGus(Resource):
    def get(self):
        return {"about": "Welcome to Einstein Scrum Rest API!"}

    def post(self):
        json = request.get_json()
        username = os.environ.get("USERNAME")
        password = os.environ.get("PASSWORD")
        connection = get_connection(username, password)
        try:
            if json["queryResult"]["intent"]["displayName"] == CHANGE_STATUS_INTENT:
                work_id = json["queryResult"]["parameters"]["WorkId"]
                new_status = json["queryResult"]["parameters"]["Status"]
                update_status(connection, work_id, new_status)
        except:
            pass


api.add_resource(UpdateGus, "/")

if __name__ == "__main__":
    app.run(debug=True)
