#!/bin/bash

agy_dyad() {
    agy "$@"
    if [ -f "./bin/status" ]; then
        ./bin/status
    fi
}

claude_dyad() {
    claude "$@"
    if [ -f "./bin/status" ]; then
        ./bin/status
    fi
}
