import json

from knesset_search import bills_request_builder
from knesset_search.person_request_builder import PersonRequestBuilder


def parse_bills(params):
    if not params:
        raise Exception("no params")

    bills = params.get('bills')

    if bills:
        return json.loads(bills)
    else:
        raise Exception("no no bills params")


def bills_with_factions(persons, bills):
    for bill in bills:
        initiators = [initiator['PersonID'] for initiator in bill['KNS_BillInitiators']]

        for initiator in initiators:
            persons.filter


def get_bill_factions(bills):
    bills_initiators = [bill['KNS_BillInitiators'] for bill in bills]

    request_builder = PersonRequestBuilder()

    person_ids = set()

    for initiators in bills_initiators:
        for initiator in initiators:
            person_ids.add(initiator['PersonID'])

    request_builder.with_ids(person_ids)

    request = request_builder.build()

    response = request.execute()

    bills_with_factions(response['value'], bills)


def knesset_handler(event, context):
    params = event.get('queryStringParameters')
    bills = parse_bills(params)

    states = bills.get('states')
    knesset_num = bills.get('knessetNum')

    request_builder = bills_request_builder.BillsRequestBuilder()

    if states:
        request_builder.with_states(states)

    if knesset_num:
        request_builder.with_knesset_num(knesset_num)

    bills_request = request_builder.build()

    response = bills_request.top(6).execute()

    get_bill_factions(response['value'])

    print(f"got response {response['value']}")

    return {
        'event': event,
        'params': params,
        'bills': bills,
        'states': states,
        'values': response['value']
    }


knesset_handler({ 'queryStringParameters': { "bills": '{ "states": [108, 109, 111, 141, 167], "knessetNum": 23 }' } }, None)