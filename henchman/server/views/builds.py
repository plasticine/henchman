from flask.views import MethodView


class BuildViews(MethodView):
    def get(self, build_id):
        if build_id is None:
            # return a list of users
            return "BuildViews index"
        else:
            # expose a single user
            return "BuildViews show id:%s" % build_id

    def post(self):
        # create a new user
        return "BuildViews post"

    def delete(self, build_id):
        # delete a single user
        return "BuildViews delete id:%s" % build_id

    def put(self, build_id):
        # update a single user
        return "BuildViews put id:%s" % build_id
