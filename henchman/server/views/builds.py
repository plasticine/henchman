from flask.views import MethodView


class BuildViews(MethodView):
    def get(self, build_id):
        if build_id is None:
            # return a list of users
            return "BuildViews index"
        else:
            # expose a single user
            return "BuildViews show"

    def post(self):
        # create a new user
        return "BuildViews create"

    def delete(self, user_id):
        # delete a single user
        return "BuildViews delete"

    def put(self, user_id):
        # update a single user
        return "BuildViews edit"
