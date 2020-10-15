import yaml
import requests
import sys
from google.cloud import storage



#https://storage.cloud.google.com/halconfig/bom/1.18.7.yml
repos=["devopsmx", "opsmxdev"]
version="1.18.7"
version_prefix=""
#version_prefix="version-"
if len(sys.argv) == 1:
   print "Usage: python fetch.py SPINNAKER_VERSION [devopsmx|opsmxdev|all] [IMAGE_TAG_PREFIX]"
   exit(1)
if len(sys.argv) > 1:
   version=sys.argv[1]
if len(sys.argv) > 2:
   if sys.argv[2] != "all":
      repos=[sys.argv[2]]
if len(sys.argv) > 3:
   version_prefix=sys.argv[3]
print "Version provided is: " + version
bom_file="bom_" + version + ".yml"
oes_bom="oes_" + bom_file
bucket_name="halconfig"
source_blob_name="bom/" + version + ".yml"
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(source_blob_name)
blob.download_to_filename(bom_file)
# expecting to find 10 images for now (halyard to come)
images=["clouddriver", "deck", "echo", "fiat", "front50", "gate", "igor", "kyatenta", "orca", "rosco"]
for repo in repos:
        images_found={}
        print "Processing with repo: " + repo
        print "---------------------------------------------------------------------------------------"
	base="docker.io/" + repo + "/ubi8-oes-"
	bom=yaml.load(open(bom_file), Loader=yaml.BaseLoader)['services']
	bom_out=open(oes_bom, "w")
	bom_out.write ( "halyard:\n" )
	bom_out.write ( "  additionalServiceSettings:\n" )
	for key, value in bom.items():
		if value:
			bom_out.write ("    " + key + ".yml:\n" )
			version=value['version'].split('-')[0]
			bom_out.write ("      artifactId: " + base + key + ":version-" + version + "\n")
			r = requests.get("https://index.docker.io/v1/repositories/" + repo + "/ubi8-oes-" + key + "/tags/" + version_prefix + version)
			if r.status_code == 404:
			   print "Image not found: " + key + ":" + version_prefix + version
                        elif r.status_code == 200:
                           if key in images:
                              images_found[key] = key
        if len(images_found) == 0:
           print "NO IMAGES WERE FOUND!"
        print "---------------------------------------------------------------------------------------"
