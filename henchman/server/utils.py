from werkzeug.routing import BaseConverter


def mount(app, view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func,
        methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
        methods=['GET', 'PUT', 'DELETE'])


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
