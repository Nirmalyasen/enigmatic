from flask import Flask, json
import jsondiff
import logging
import requests
import sys
import traceback

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
    result = {"name": account_name, "status": "active"}
    for cloud_driver in cloud_drivers:
        try:
            result[cloud_driver] = {}
            url = "http://" + cloud_driver + port
            requests.options(url)
            r = requests.get(url + "/credentials/" + account_name)

            if r.status_code == GOOD_STATUS:
                rj = r.json()
                result[cloud_driver]["enabled"] = rj["enabled"]
                if "namespaces" in rj:
                    result[cloud_driver]["namespaces"] = rj["namespaces"]
                if "permissions" in rj:
                    result[cloud_driver]["permissions"] = rj["permissions"]
            else:
                logging.info("Not found:" + account_name + " in " + cloud_driver)
                result["status"] = "inactive"
                result["status_reason"] = "Not available everywhere"
                status = BAD_STATUS
        except Exception as e:
            logging.warning(e)
            result["status"] = "inactive"
            result["status_reason"] = "Server not accessible"
            status = BAD_STATUS

    if result["status"] == "active":
        for i in range(len(cloud_drivers) - 1):
            for j in range(i+1, len(cloud_drivers)):
                diff = jsondiff.diff(result[cloud_drivers[i]], result[cloud_drivers[j]])
                if diff:
                    result["status"] = "inactive"
                    result["status_reason"] = "Not consistent"
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
