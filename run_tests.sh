#!/usr/bin/env bash
export ST_FIXTURES_PATH=$(pwd)/tests/fixtures/
python ../UnitTesting/sbin/run_tests.py sublimetext_indentxml
