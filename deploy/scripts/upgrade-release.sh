#!/bin/bash -e


# Define this on travis environment variables
# SSH_USER
# SSH_ADDRESS
# SUPER_SECRET_PASSWORD
SSH_KEY_FILE=~/.ssh/palika-profile

if [ "${TRAVIS_BRANCH}" == "${RC_BRANCH}" ] && [ "${TRAVIS_PULL_REQUEST}" == "false" ] ; then
    ./docker_ci push --on on_release;
    cp ssh_key $SSH_KEY_FILE
    chmod 600 $SSH_KEY_FILE
    echo '>>> Upgrading server with latest image <<<'
    ssh -o "StrictHostKeyChecking no" -i $SSH_KEY_FILE $SSH_USER@$SSH_ADDRESS ./update-palika-profile.sh
    echo '>>> Upgrading Success <<<'
fi
