import requests
from patched_odata import odata_client
from pyodata.v2.service import GetEntitySetFilter as esf

BASE_URL = "http://knesset.gov.il/Odata/ParliamentInfo.svc"


class KnessetBillsRequestBuilder:

    def __init__(self):
        self.client = odata_client.Client(BASE_URL, requests.Session())
        self.bills_entities = self.client.entity_sets.KNS_Bill.get_entities()
        self.knesset_num = None
        self.states = None

    def with_states(self, states):
        self.states = states

    def with_knesset_num(self, knesset_num):
        self.knesset_num = knesset_num

    def build(self):
        query = ''

        if self.states:
            query = self._add_states()

        if self.knesset_num:
            query = esf.and_(query, self.bills_entities.KnessetNum == self.knesset_num)

        return self.bills_entities.filter(query)

    def _add_states(self):
        states_query = list(map(lambda state: self.bills_entities.StatusID == state, self.states))

        return esf.or_(*states_query) if len(states_query) > 1 else states_query[0]