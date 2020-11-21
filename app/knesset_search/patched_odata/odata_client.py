import pyodata
from pyodata.v2.service import EntityProxy, GetEntitySetRequest, HTTP_CODE_OK, HttpError

Client = pyodata.Client


def get_entities(self):
    """Get all entities"""

    def get_entities_handler(response):
        """Gets entity set from HTTP Response"""

        if response.status_code != HTTP_CODE_OK:
            raise HttpError('HTTP GET for Entity Set {0} failed with status code {1}'
                            .format(self._name, response.status_code), response)

        content = response.json()

        return content

    entity_set_name = self._alias if self._alias is not None else self._entity_set.name
    return GetEntitySetRequest(self._service.url, self._service.connection, get_entities_handler,
                                                  self._parent_last_segment + entity_set_name,
                                                  self._entity_set.entity_type)


pyodata.v2.service.EntitySetProxy.get_entities = get_entities
