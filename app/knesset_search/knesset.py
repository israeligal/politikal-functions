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


def get_persons_and_positions_for_bills(bills):
    bills_initiators = [bill['KNS_BillInitiators'] for bill in bills]

    request_builder = PersonRequestBuilder()

    person_ids = set()
    for initiators in bills_initiators:
        for initiator in initiators:
            person_ids.add(initiator['PersonID'])

    request_builder.with_ids(person_ids)

    request = request_builder.build()

    response = request.execute()

    return response['value']


def knesset_handler(event, context):
    params = event.get('queryStringParameters')
    bills = parse_bills(params)

    states = bills.get('states')
    knesset_num = bills.get('knessetNum')

    bills = get_bills(knesset_num, states)

    add_bills_persons_and_factions(bills)

    print(f"got response {bills}")

    return {
        'event': event,
        'params': params,
        'bills': bills,
        'states': states
    }


def get_bills(knesset_num, states):
    request_builder = bills_request_builder.BillsRequestBuilder()

    if states:
        request_builder.with_states(states)
    if knesset_num:
        request_builder.with_knesset_num(knesset_num)

    bills_request = request_builder.build()

    response = bills_request.top(6).execute()

    return response['value']


def add_bills_persons_and_factions(bills):
    persons_and_positions = get_persons_and_positions_for_bills(bills)

    for bill in bills:
        _add_person_and_faction(persons_and_positions, bill)


def _add_person_and_faction(persons_with_positions, bill):
    for initiator in bill['KNS_BillInitiators']:
        person = next((person for person in persons_with_positions if initiator['PersonID'] == person['PersonID']),
                      {})

        positions = filter(lambda position: position['KnessetNum'] == bill['KnessetNum'],
                           person['KNS_PersonToPositions'])

        position = next((position for position in positions if position['FactionName']), {})

        initiator['first_name'] = person['FirstName']
        initiator['last_name'] = person['LastName']
        initiator['gender'] = person['GenderDesc']
        initiator['email'] = person['Email']
        initiator['faction'] = position['FactionName']
        initiator['faction_id'] = position['FactionID']


# knesset_handler({'queryStringParameters': {"bills": '{ "states": [108, 109, 111, 141, 167], "knessetNum": 23 }'}}, None)
