import requests
import json
from pyodata.v2.service import GetEntitySetFilter as esf
from patched_odata import odata_client

BASE_URL = "http://knesset.gov.il/Odata/ParliamentInfo.svc"


def knesset_handler(event, context):
    params = event.get('queryStringParameters')

    bills = params.get('bills')

    if bills:
        bills = json.loads(bills)

    states = bills.get('states') if bills else None

    client = odata_client.Client(BASE_URL, requests.Session())

    bills_request = client.entity_sets.KNS_Bill.get_entities()

    states_query = list(map(lambda state: bills_request.StatusID == state, states))

    states_query = esf.or_(*states_query) if len(states_query) > 1 else states_query[0]

    bills_request = bills_request.filter(states_query)

    response = bills_request.top(4).execute()

    return {
        'event': event,
        'params': params,
        'bills': bills,
        'states': states,
        'values': response['value']
    }

