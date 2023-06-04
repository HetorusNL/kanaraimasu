#!/bin/bash

set -euxo pipefail

echo "removing build directory"
rm -rf build

echo ""
echo "building pygbag web executable"
poetry run pygbag --build --icon favicon.ico .

DEPLOYMENT_FOLDER=/docker/volumes/caddy/srv/kanaraimasu.hetorus.nl

echo "starting deployment of kanaraimasu"
echo "deploying to raptor:$DEPLOYMENT_FOLDER"
echo "this will delete everything in the folder and deploys kanaraimasu"
read -p "Are you sure? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ""
    echo "removing existing content from folder"
    ssh raptor sudo rm -rf $DEPLOYMENT_FOLDER/*

    echo ""
    echo "copying build kanaraimasu to the server root"
    rsync --rsync-path="sudo rsync" -av build/web/* raptor:$DEPLOYMENT_FOLDER/

    echo ""
    echo "changing owner of the deployed files to root:root"
    ssh raptor sudo chown -R root:root $DEPLOYMENT_FOLDER/*

    echo ""
    echo "finished deployment of kanaraimasu!"
fi
