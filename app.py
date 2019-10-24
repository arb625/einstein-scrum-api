from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class UpdateGus(Resource):
    def get(self):
        return {"about": "Welcome to Einstein Scrum Rest API!"}

    def post(self):
        json = request.get_json()
        return {"you sent": json}


api.add_resource(UpdateGus, "/")

if __name__ == "__main__":
    app.run(debug=True)
