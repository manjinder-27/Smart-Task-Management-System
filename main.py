from app import flask_app,api_instance
import restapi

api_instance.add_resource(restapi.Register,"/api/register") #POST
api_instance.add_resource(restapi.Login,"/api/login") #POST
api_instance.add_resource(restapi.Logout,"/api/logout") #POST
api_instance.add_resource(restapi.TaskList,"/api/tasks") #GET, POST
api_instance.add_resource(restapi.TaskResource,"/api/tasks/<int:task_id>") #PUT, DELETE
api_instance.add_resource(restapi.Analytics,"/api/analytics") #GET

if __name__ == "__main__":
    flask_app.run(debug=True)