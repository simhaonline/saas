import logging
log = logging.getLogger(__name__)

from saas.app.core.services.connection import ConnectionManager
from saas.app.core.stores.base import BaseStore

from uuid import UUID


class OrganizationStore(BaseStore):

    def __init__(self, manager: ConnectionManager, name: str):
        super(OrganizationStore, self).__init__(manager, name)

    def save(self, client_id: UUID, organization_id: UUID, name: str, address: str, country_id: int):
        try:
            super(OrganizationStore, self).runProcTransactional('crm.organization_save', [
                client_id,
                organization_id,
                name,
                address,
                country_id
            ])
        except Exception as e:
            log.error(e)
            raise Exception('Unable to save crm organization')