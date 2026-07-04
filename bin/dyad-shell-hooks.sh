#!/bin/bash

agy_dyad() {
    if [ -f "./bin/standup.sh" ]; then
        ./bin/standup.sh
    fi
    agy "$@"
    if [ -f "./bin/standdown.sh" ]; then
        ./bin/standdown.sh
    fi
    if [ -f "./bin/status" ]; then
        ./bin/status
    fi
}

claude_dyad() {
    if [ -f "./bin/standup.sh" ]; then
        ./bin/standup.sh
    fi
    claude "$@"
    if [ -f "./bin/standdown.sh" ]; then
        ./bin/standdown.sh
    fi
    if [ -f "./bin/status" ]; then
        ./bin/status
    fi
}
