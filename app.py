from flask import Flask, request
from flask_restful import Resource, Api

from rq import Queue
from worker import conn

from gus_action import update_status

app = Flask(__name__)
api = Api(app)

q = Queue(connection=conn)

CHANGE_STATUS_INTENT = "Change status"


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
                q.enqueue_call(func=update_status, args=(work_id, new_status,))
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
