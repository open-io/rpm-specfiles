#!/usr/bin/env bash

TOKEN=""
OWNER="open-io"
REPO="oio-grid"
TAG=$(awk '/^Version:/ {print $2 ; exit 0}' openio-grid.spec)

RELEASES_URL="https://$TOKEN:@api.github.com/repos/$OWNER/$REPO/releases"
ASSET_ID=$(curl $RELEASES_URL | jq 'map(select(.tag_name == "'"$TAG"'"))[0].assets[0].id')
curl -O -J -L -H "Accept: application/octet-stream" "$RELEASES_URL/assets/$ASSET_ID"
