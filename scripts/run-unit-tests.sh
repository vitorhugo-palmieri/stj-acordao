#!/bin/bash

iterate_over_folder() {
    for filename in tests/unit/$1/*.py; do
        python3 ${filename}
    done
}

iterate_over_folder "parser"