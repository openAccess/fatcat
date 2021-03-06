#!/bin/bash

# This script re-generates the fatcat API client (fatcat_client) from the
# swagger/openapi2 spec file, using automated tools ("codegen")

set -exu
set -o pipefail

OUTPUT=`pwd`/codegen-out
mkdir -p $OUTPUT
# Strip tags, so entire API is under a single class
cat ../fatcat-openapi2.yml | grep -v "TAGLINE$" > $OUTPUT/api.yml

docker run \
    -v $OUTPUT:/tmp/swagger/ \
    swaggerapi/swagger-codegen-cli:v2.3.1 \
    generate \
    --lang python \
    --input-spec /tmp/swagger/api.yml \
    --output /tmp/swagger/ \
    -DpackageName=fatcat_client

sudo chown -R `whoami`:`whoami` $OUTPUT
mkdir -p fatcat_client
cp -r $OUTPUT/fatcat_client/* fatcat_client
cp $OUTPUT/README.md README.md

# these tests are basically no-ops
mkdir -p tests/codegen
cp -r $OUTPUT/test/* tests/codegen

# ooo, this makes me nervous
rm -rf $OUTPUT
