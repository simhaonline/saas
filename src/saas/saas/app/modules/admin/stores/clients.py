import logging
log = logging.getLogger(__name__)

from uuid import UUID

from saas.app.core.services.connection import ConnectionManager
from saas.app.core.stores.base import BaseStore


class ClientsStore(BaseStore):

    def __init__(self, manager: ConnectionManager, name: str):
        super(ClientsStore, self).__init__(manager, name)

    def getAll(self):
        try:
            result = super(ClientsStore, self).runProc('clients.clients_all', [])
            return result
        except Exception as e:
            log.error(e)
            raise Exception('An error occured while retrieving all clients')

    def add(self, name: str, address: str):
        try:
            [(client_id, )] = super(ClientsStore, self).runProcTransactional('clients.client_add', [name, address])
            return client_id
        except Exception as e:
            raise Exception('An error occured while adding a client')

    def get(self, client_id: UUID):
        try:
            (client, ) = super(ClientsStore, self).runProc('clients.clients_get', [client_id, ])
            return client
        except Exception as e:
            log.error(e)
            raise Exception('An error occured while retrieving client')

    # def getByUrlName(self, url_name: str):
    #     try:
    #         (client, ) = super(ClientsStore, self).runProc('clients.client_by_url_name', [url_name, ])
    #         return client
    #     except Exception as e:
    #         log.error(e)
    #         raise Exception('An error occured while retrieving client by url name')

    def setActive(self, clientId: UUID, active: bool):
        try:
            super(ClientsStore, self).runProcTransactional('clients.client_set_active', [clientId, active])
        except Exception as e:
            log.error(e)
            raise Exception('An error occured while setting client active status')
        