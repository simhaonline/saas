import logging
log = logging.getLogger(__name__)

from pyramid.view import view_config
import pyramid.httpexceptions as exception

import json


@view_config(
    route_name='api.clients.all',
    request_method='POST',
    accept='application/json',
    permission='admin.clients'
)
def api_clients_all(request):
    clients = []
    services = request.services()
    try:
        clientsStore = services['store.admin.clients']
        result = clientsStore.getAll()
        clients = [
            { 'id': c[0], 'active': c[1], 'name': c[2], 'address': c[3], 'url_name': c[4] } 
            for c in result
        ]
    except Exception as e:
        log.error(e)
        raise exception.HTTPInternalServerError(
            detail=str(e),
            explanation=str(e)
        )
    raise exception.HTTPOk(
        detail='{0} clients'.format(len(clients)),
        body={ 'clients': clients }
    )

@view_config(
    route_name='api.clients.add',
    request_method='POST',
    accept='application/json',
    permission='admin.clients'
)
def view_clients_add(request):
    params = request.json_body
    name = params['name'] if 'name' in params else None
    address = params['address'] if 'address' in params else None
    url = params['url'] if 'url' in params else None

    if name is None or address is None or url is None:
        raise exception.HTTPBadRequest(
            detail='Missing required parameters',
            explanation='Client name, address and URL friendly name is required'
        )

    services = request.services()
    try:
        clientsStore = services['store.admin.clients']
        result = clientsStore.add(name, address, url)
    except Exception as e:
        raise exception.HTTPInternalServerError(
            detail=e,
            explanation=e
        )
    raise exception.HTTPOk(
        detail='Client added',
        body={'message': 'Client added'}
    )
    

@view_config(
    route_name='api.clients.get',
    request_method='POST',
    accept='application/json',
    permission='admin.clients'
)
def view_clients_get(request):
    params = request.json_body
    client_id = params['clientId'] if 'clientId' in params else None

    if client_id is None:
        raise exception.HTTPBadRequest(
            detail='Missing required parameters',
            explanation='Client Id is required'
        )
    
    services = request.services()
    client = None
    try:
        clientsStore = services['store.admin.clients']
        client = clientsStore.get(client_id)
    except Exception as e:
        raise exception.HTTPInternalServerError(
            detail=str(e),
            explanation=str(e)
        )

    if client is None:
        raise exception.HTTPInternalServerError(
            detail='Client not found',
            explanation='Client not found'
        )
    else:
        raise exception.HTTPOk(
            detail='client',
            body={'client': { 
                'id': client[0],
                'active': client[1],
                'name': client[2],
                'address': client[3],
                'url_name': client[4]
            }}
        )


@view_config(
    route_name='api.clients.setactive',
    request_method='POST',
    accept='application/json',
    permission='admin.clients'
)
def view_client_set_active(request):
    params = request.json_body
    client_id = params['clientId'] if 'clientId' in params else None
    active = params['active'] if 'active' in params else None

    if client_id is None or active is None:    
        raise exception.HTTPBadRequest(
            detail='Missing required parameters',
            explanation='Client Id and Active state is required'
        )

    services = request.services()
    try:
        clientsStore = services['store.admin.clients']
        clientsStore.setActive(client_id, active)
    except Exception as e:
        raise exception.HTTPInternalServerError(
            detail=str(e),
            explanation=str(e)
        )

    raise exception.HTTPOk(
        detail='Client active state changed',
        body={'message': 'Client active state changed'}
    )

@view_config(
    route_name='api.clients.roles.all',
    request_method='POST',
    accept='application/json',
    permission='admin.clients'
)
def view_clients_roles_all(request):
    params = request.json_body
    client_id = params['clientId'] if 'clientId' in params else None

    if client_id is None:
        raise exception.HTTPBadRequest(
            detail='Missing required parameter',
            explanation='Client Id is required'
        )

    roles = []
    services = request.services()
    try:
        clientsStore = services['store.admin.clients']
        result = clientsStore.allRoles(client_id)
        roles = [{
            'id': r[0],
            'active': r[1],
            'name': r[2]
        } for r in result]
    except Exception as e:
        raise exception.HTTPInternalServerError(
            detail=str(e),
            explanation=str(e)
        )

    raise exception.HTTPOk(
        detail='{0} client roles found'.format(len(roles)),
        body={
            'roles': roles
        }
    )


@view_config(
    route_name='api.clients.roles.add',
    request_method='POST',
    accept='application/json',
    permission='admin.clients'
)
def view_clients_roles_add(request):
    params = request.json_body
    client_id = params['clientId'] if 'clientId' in params else None
    name = params['name'] if 'name' in params else None

    if client_id is None or name is None:
        raise exception.HTTPBadRequest(
            detail='Missing required parameters',
            explanation='Client Id and Role Name is required'
        )

    services = request.services()
    try:
        clientsStore = services['store.admin.clients']
        clientsStore.addRole(client_id, name)
    except Exception as e:
        log.error(e)
        raise exception.HTTPInternalServerError(
            detail=str(e),
            explanation=str(e)
        )

    raise exception.HTTPOk(
        detail='Client Role added',
        body={'message': 'Client Role added'}
    )

@view_config(
    route_name='api.clients.roles.active',
    request_method='POST',
    accept='application/json',
    permission='admin.clients'
)
def view_clients_role_active(request):
    params = request.json_body
    role_id = params['roleId'] if 'roleId' in params else None
    active = params['active'] if 'active' in params else None

    if role_id is None or active is None:
        raise exception.HTTPBadRequest(
            detail='Missing required parameters',
            explanation='Role Id and Active status is required'
        )

    services = request.services()
    try:
        clientsStore = services['store.admin.clients']
        clientsStore.roleSetActive(role_id, active)
    except Exception as e:
        log.error(e)
        raise exception.HTTPInternalServerError(
            detail=str(e),
            explanation=str(e)
        )

    raise exception.HTTPOk(
        detail='Client Role active status updated',
        body={'message': 'Client Role active status updated'}
    )


@view_config(
    route_name='api.clients.roles.permissions',
    request_method='POST',
    accept='application/json',
    permission='admin.clients'
)
def view_clients_roles_permissions(request):
    params = request.json_body
    client_id = params['clientId'] if 'clientId' in params else None
    role_id = params['roleId'] if 'roleId' in params else None

    if client_id is None or role_id is None:
        raise exception.HTTPBadRequest(
            detail='Missing required parameters',
            explanation='Client Id and Role Id is required'
        )

    permissions = []
    services = request.services()
    try:
        clientsStore = services['store.admin.clients']
        result = clientsStore.rolePermissions(client_id, role_id)
        permissions = [{
            'id': r[0],
            'active': r[1],
            'name': r[2]
        } for r in result]
    except Exception as e:
        raise exception.HTTPInternalServerError(
            detail=str(e),
            explanation=str(e)
        )

    raise exception.HTTPOk(
        detail='{0} client roles found'.format(len(permissions)),
        body={
            'permissions': permissions
        }
    )

@view_config(
    route_name='api.clients.users.all',
    request_method='POST',
    accept='application/json',
    permission='admin.clients'
)
def view_clients_users_all(request):
    params = request.json_body
    client_id = params['clientId'] if 'clientId' in params else None

    if client_id is None:
        raise exception.HTTPBadRequest(
            detail='Missing required parameter',
            explanation='Client Id is required'
        )

    users = []
    services = request.services()
    try:
        clientsStore = services['store.admin.clients']
        result = clientsStore.allUsers(client_id)
        users = [{
            'id': r[0],
            'active': r[1],
            'email': r[2],
            'name': r[3]
        } 
        for r in result]
    except Exception as e:
        raise exception.HTTPInternalServerError(
            detail=str(e),
            explanation=str(e)
        )

    raise exception.HTTPOk(
        detail='{0} client users found'.format(len(users)),
        body={
            'users': users
        }
    )

@view_config(
    route_name='api.clients.users.add',
    request_method='POST',
    accept='application/json',
    permission='admin.clients'
)
def view_clients_user_add(request):
    params = request.json_body
    client_id = params['clientId'] if 'clientId' in params else None
    email = params['email'] if 'email' in params else None

    if client_id is None or email is None:
        raise exception.HTTPBadRequest(
            detail='Missing required parameter',
            explanation='Client Id is required'
        )

    services = request.services()
    try:
        userStore = services['store.user']
        user = userStore.userByEmail(email)
        user_id = user[0]

        clientsStore = services['store.admin.clients']
        clientsStore.addUser(client_id, user_id)
    except Exception as e:
        log.error(e)
        raise exception.HTTPInternalServerError(
            detail=str(e),
            explanation=str(e)
            
        )

    raise exception.HTTPOk(
        detail='Client User added',
        body={'message': 'Client User added'}
    )
