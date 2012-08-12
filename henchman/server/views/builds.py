from flask.views import MethodView
from flask import render_template, request, url_for, redirect
from henchman import Henchman

henchman = Henchman()


class BuildViews(MethodView):
    def get(self, build_uuid):
        if build_uuid is None:
            # show a list of all builds
            return render_template('builds/index.html')
        else:
            # show a single build
            return render_template('builds/show.html', build_uuid=build_uuid)

    def post(self):
        # create a new user
        # self._add_build(build_data=request.form)
        return 'BuildViews post'

    def delete(self, build_uuid):
        # delete a single user
        return 'BuildViews delete id:%s' % build_uuid

    def put(self, build_uuid):
        raise NotImplementedError()

    # def _add_build(self, build_data):
    #     """
    #     Add the build data to the Henchman queue.
    #     """
    #     minion = henchman.create_minion_for_build(build_data)
    #     url_for('builds', build_uuid=minion.build.uuid)
    #     return redirect()
