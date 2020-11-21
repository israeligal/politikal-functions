import json

from knesset_search import odata_request_builder


def parse_bills(params):
    if not params:
        raise Exception("no params")

    bills = params.get('bills')

    if bills:
        return json.loads(bills)
    else:
        raise Exception("no no bills params")


def knesset_handler(event, context):
    params = event.get('queryStringParameters')
    bills = parse_bills(params)

    states = bills.get('states')
    knesset_num = bills.get('knessetNum')

    request_builder = odata_request_builder.KnessetBillsRequestBuilder()

    if states:
        request_builder.with_states(states)

    if knesset_num:
        request_builder.with_knesset_num(knesset_num)

    bills_request = request_builder.build()

    response = bills_request.top(6).execute()

    print(f"got response {response['value']}")

    return {
        'event': event,
        'params': params,
        'bills': bills,
        'states': states,
        'values': response['value']
    }


knesset_handler({ 'queryStringParameters': { "bills": '{ "states": [108, 109, 111, 141, 167], "knessetNum": 23 }' } }, None)