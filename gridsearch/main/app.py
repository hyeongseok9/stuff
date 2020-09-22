from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

for (resource, url) in controllers.getAllResources():
    api.add_resource(resource, url)

if __name__ == '__main__':
    app.run(debug=True)