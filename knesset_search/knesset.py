import requests
from pyodata.v2.service import GetEntitySetFilter as esf
from patched_odata import odata_client
BASE_URL = "http://knesset.gov.il/Odata/ParliamentInfo.svc"


def knesset_handler(event, context):
    client = odata_client.Client(BASE_URL, requests.Session())

    bills_request = client.entity_sets.KNS_Bill.get_entities()
    state_query = list(map(lambda state: bills_request.StatusID == state, [108, 109, 111, 141, 167]))

    bills_request = bills_request.filter(
        esf.or_(
            *state_query
        )
    )

    response = bills_request.execute()

    return {
        'values': response['value'],
        'next': response['odata.nextLink']
    }
