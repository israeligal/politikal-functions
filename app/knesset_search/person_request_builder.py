import requests
from pyodata.v2.service import GetEntitySetFilter as esf

from knesset_search.patched_odata import odata_client

BASE_URL = "http://knesset.gov.il/Odata/ParliamentInfo.svc"


class PersonRequestBuilder:

    def __init__(self):
        # self.client = odata_client.Client(BASE_URL, requests.Session())
        self.person_entities = self.client.entity_sets.KNS_Person.get_entities()
        self.ids = None
        self.position = True

    def with_ids(self, ids):
        self.ids = ids

    def with_position(self, position):
        self.position = position

    def build(self):
        query = self.person_entities

        if self.ids:
            query.filter(self._add_ids())

        if self.position:
            query.expand('KNS_PersonToPositions')

        return query

    def _add_ids(self):
        ids_query = [self.person_entities.PersonID == person_id for person_id in self.ids]

        return esf.or_(*ids_query) if len(ids_query) > 1 else ids_query[0]
