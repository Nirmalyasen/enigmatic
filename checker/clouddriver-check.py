from flask import Flask, json
import jsondiff
import logging
import requests
import sys

logging.basicConfig(format="%(levelname)s [%(asctime)s]: %(message)s", level=logging.INFO)
port=":7002"
BAD_STATUS=404
GOOD_STATUS=200
cloud_drivers = ["spin-clouddriver-rw", "spin-clouddriver-ro", "spin-clouddriver-ro-deck", "spin-clouddriver-caching"]

if len(sys.argv) > 1:
    cloud_drivers = sys.argv[1].split(",")
logging.info("Clouddrivers used are: ")
logging.info("     " + ", ".join(cloud_drivers))

api = Flask(__name__)

def check_with_clouddriver(account_name):

    responses = []
    status = GOOD_STATUS
    result = {"status": "FOUND", "message": ""}
    for cloud_driver in cloud_drivers:
        try:
            url = "http://" + cloud_driver + port
            requests.options(url)
            r = requests.get(url + "/credentials/" + account_name)
            if r.status_code == GOOD_STATUS:
                responses.append(r.json())
            else:
                logging.info("Not found:" + account_name + " in " + cloud_driver)
        except Exception as e:
            logging.warning(e)
    if len(responses) != len(cloud_drivers):
        result["status"] = "NOT FOUND EVERYWHERE"
        status = BAD_STATUS
    elif len(responses) > 1:
        for i in range(len(responses) - 1):
            for j in range(i+1, len(responses)):
                diff = jsondiff.diff(responses[i], responses[j])
                if diff:
                    result["status"] = "DIFFERENCE IN CONTENT"
                    status = BAD_STATUS
                    return result, status

    return result, status

@api.route('/<account_name>', methods=['GET'])
def check_accounts(account_name):

  logging.info("Processing account: " + account_name)
  result, status = check_with_clouddriver(account_name)
  return json.dumps(result), status


if __name__ == '__main__':
    api.run(host='0.0.0.0')
