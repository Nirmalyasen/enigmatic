#!/bin/sh

REPO=$1
IMAGE=$2

if [[ "$REPO" == "" || "$IMAGE" == "" ]]; then
   echo "Repo name and image name required"
   exit 400
fi

AQUASEC_URL=""
USERID=administrator
PASSWORD=

echo "Scanning image $IMAGE in repo $REPO"

TOKEN=$(curl -s -X POST $AQUASEC_URL/api/v1/login \
    -d "{ \"id\":\"$USERID\", \"password\":\"$PASSWORD\"}" \
    -H "Content-Type: application/json"|jq -r '.token')

SCAN_CMD="curl -s -H \"Content-Type: application/json\" \
    -H \"Authorization: Bearer ${TOKEN}\" \
    ${AQUASEC_URL}/api/v1/scanner/registry/${REPO}/image/${IMAGE}"

eval "$SCAN_CMD/scan -X POST"

while [[ "$STATUS" != Scanned && "$STATUS" != Failed ]]; do
  echo "Scan is continuing..."
  sleep 5
  STATUS=$(eval "$SCAN_CMD/status" | jq -r '.status')
done

eval "$SCAN_CMD/scan_result" | jq -r
DISALLOWED=$(eval "$SCAN_CMD/scan_result" | jq -r '.disallowed')

RESULT="SUCCESS"
if [[ $STATUS == Failed ]];  then
    RESULT="FAILED"
fi

echo "SPINNAKER_PROPERTY_SCAN_RESULT=$RESULT"
echo "SPINNAKER_PROPERTY_DISALLOWED=$DISALLOWED"
