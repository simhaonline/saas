import logging
log = logging.getLogger(__name__)

from pyramid.view import view_config


@view_config(
    route_name='admin.dashboard',
    request_method='GET',
    renderer='saas.app.modules.admin:templates/default.html'
)
def view_dashboard(request):
    log.debug('view: view_dashboard')
    return {}