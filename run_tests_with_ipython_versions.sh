#!/usr/bin/env bash
set -euo pipefail

# List of IPython versions to test
versions=(
    "9.3.0"
    "9.2.0"
    "9.1.0"
)

for v in "${versions[@]}"; do
    echo "=== Testing with IPython $v ==="
    rm -rf .venv
    uv venv .venv
    source .venv/bin/activate

    # Install project and dependencies
    uv pip install -e .
    uv pip install ipython=="$v" pytest

    set +e
    python -m pytest -q
    result=$?
    set -e
    deactivate
    rm -rf .venv

    if [[ "$v" == "9.2.0" ]]; then
        if [[ $result -eq 0 ]]; then
            echo "Expected failure with IPython $v, but tests passed" >&2
            exit 1
        else
            echo "Tests failed as expected with IPython $v"
        fi
    else
        if [[ $result -ne 0 ]]; then
            echo "Tests failed with IPython $v" >&2
            exit 1
        fi
        echo "Tests passed with IPython $v"
    fi

done

exit 0
