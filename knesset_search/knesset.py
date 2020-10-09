import requests
import json
from pyodata.v2.service import GetEntitySetFilter as esf
from patched_odata import odata_client
BASE_URL = "http://knesset.gov.il/Odata/ParliamentInfo.svc"


def knesset_handler(event, context):
    params = event.get('queryStringParameters')

    bills = params.get('bills')

    states = bills.get('states')

    states = json.loads(states) if states else [108, 109, 111, 141, 167]

    client = odata_client.Client(BASE_URL, requests.Session())

    bills_request = client.entity_sets.KNS_Bill.get_entities()

    states_query = list(map(lambda state: bills_request.StatusID == state, states))

    states_query = esf.or_(*states_query) if len(states_query) > 2 else states_query

    bills_request = bills_request.filter(states_query)

    response = bills_request.execute()

    return {
        'values': response['value'],
        'next': response.get('odata.nextLink')
    }

knesset_handler({ 'queryStringParameters': { 'bills' : { "states": '[1,3,4]' } } }, None)