#!/bin/bash
VER=$1

RED='\033[1;31m'
NC='\033[0m'
command -v yq || { echo -e "${RED}yq not found and is needed to run. Please install.${NC}."; exit 1; }
command -v gsutil || { echo -e "${RED}gsutil not found and is needed to run. Please install.${NC}"; exit 1; }

[[ -z $VER ]] && echo -e "${RED}Please provide version. ${NC}" && exit 1

FILE=$VER.yml


mkdir -p ./boms/.boms
cd ./boms/.boms

mkdir ./bom
cd ./bom
gsutil cp gs://halconfig/bom/$FILE .
ECHO_VER=$(yq r $FILE services.echo.version)
CLOUDDRIVER_VER=$(yq r $FILE services.clouddriver.version)
DECK_VER=$(yq r $FILE services.deck.version)
FIAT_VER=$(yq r $FILE services.fiat.version)
FRONT50_VER=$(yq r $FILE services.front50.version)
GATE_VER=$(yq r $FILE services.gate.version)
IGOR_VER=$(yq r $FILE services.igor.version)
KAYENTA_VER=$(yq r $FILE services.kayenta.version)
ORCA_VER=$(yq r $FILE services.orca.version)
ROSCO_VER=$(yq r $FILE services.rosco.version)
sed -i -e  '/commit/{n;s/version: /version: local:/;}' $FILE

cd ../
mkdir ./echo
cd ./echo
gsutil -m cp -R gs://halconfig/echo/$ECHO_VER/* .

cd ../
mkdir clouddriver
cd clouddriver/
gsutil -m cp -R gs://halconfig/clouddriver/$CLOUDDRIVER_VER/* .

cd ../
mkdir deck
cd deck/
gsutil -m cp -R gs://halconfig/deck/$DECK_VER/* .

cd ../
mkdir fiat
cd fiat/
gsutil -m cp -R gs://halconfig/fiat/$FIAT_VER/* .

cd ../
mkdir front50
cd front50/
gsutil -m cp -R gs://halconfig/front50/$FRONT50_VER/* .

cd ../
mkdir gate
cd gate/
gsutil -m cp -R gs://halconfig/gate/$GATE_VER/* .

cd ../
mkdir igor
cd igor/
gsutil cp -R gs://halconfig/igor/$IGOR_VER/* .


cd ../
mkdir kayenta
cd kayenta/
gsutil -m cp -R gs://halconfig/kayenta/$KAYENTA_VER/* .

cd ../
mkdir orca
cd orca/
gsutil -m cp -R gs://halconfig/orca/$ORCA_VER/* .

cd ../
mkdir rosco
cd rosco/
gsutil -m cp -R gs://halconfig/rosco/$ROSCO_VER/* .

cd ../..
tar -cvzf ../boms.tar.gz .boms

echo "DONE !!!!!!!"
