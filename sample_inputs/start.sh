#! /bin/bash

export SWIFT_HEAP_MAX=4G
export SWIFT_USERHOME=/tmp/swifthome
export GLOBUS_HOSTNAME=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
export GLOBUS_TCP_PORT_RANGE=6002,6030

export PATH=$PATH:/core/pworks-main/swift-pw-bin/swift-svn/bin/

swift diva.swift