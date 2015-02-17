#!/bin/bash
#
# Usage: source env.sh

DEPLOY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function system-info() {
  fab -f $DEPLOY_DIR/fabfile.py $*
}

alias si='system-info'
alias si-host-type='system-info host-type'
alias si-ssh-config='system-info ssh-config'

