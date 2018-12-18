#! /bin/bash

# Ignore if not ( not pull request and branch is `release`)
if ! [ \
    "${TRAVIS_PULL_REQUEST}" == "false" -a \
    "${TRAVIS_BRANCH}" == "${RC_BRANCH}" \
]; then
    exit
fi

docker tag ${DOCKER_IMAGE} ${DOCKER_IMAGE_RC}
docker push ${DOCKER_IMAGE_RC}
