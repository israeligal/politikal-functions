import requests

import logging

import azure.functions as func

BASE_URL = "http://knesset.gov.il/Odata/ParliamentInfo.svc"

def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    table_name = req.params.get('table_name')
    filter_query = req.params.get('filter_query')
    if not table_name or not filter:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            table_name = req_body.get('table_name')
            filter_query = req_body.get('filter_query')

    if table_name:
        query = f"{BASE_URL}/{table_name}/{filter_query}"
        response = requests.get(query)

        msg.set(response)
        return func.HttpResponse(f"Hello,you've got response: {response}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
