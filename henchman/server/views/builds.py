from flask.views import MethodView
from flask import render_template, request, url_for, redirect, abort
from henchman import Henchman
from henchman.minion.build import InvalidBuildPostData

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
        """
        Attempt to create a new build from the post data, catch it if it is
        malformed and a InvalidBuildPostData exception is raised.
        """
        try:
            minion = henchman.create_minion_for_build(dict(request.form))
            build_url = url_for('builds', _method='GET', build_uuid=minion.build.uuid)
            return redirect(build_url)
        except InvalidBuildPostData:
            abort(400)

    def delete(self, build_uuid):
        # delete a single user
        return 'BuildViews delete id:%s' % build_uuid

    def put(self, build_uuid):
        raise NotImplementedError()
