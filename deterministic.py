#!/bin/env python

import os
from os import path

# Import setVerbose and LoggingObject from uas_log module
from uas.uas_log import setVerbose, LoggingObject
from uas.scenario.tester import TestSuite

if __name__ == "__main__":
    """
    SITL mode example:
      python3 deterministic.py sitl

    HITL mode example:
      python3 deterministic.py hitl
    """

    # Enable verbose logging
    
    setVerbose(True)

    import argparse
    import pathlib
    import toml

    # Set up argument parsing
    parser = argparse.ArgumentParser()

    # Add argument for test mode
    parser.add_argument(
        "test_mode", choices=["sitl", "hitl"], help="test mode, either 'sitl' or 'hitl'"
    )
    args = parser.parse_args()

    # Load configuration from a TOML file
    toml_test_table = toml.load(
        path.join(
            pathlib.Path(__file__).parent.resolve(), "test_config.toml"
        )
    )

    # Set up arguments from the TOML configuration
    args.workspace = toml_test_table["common"]["deterministic"]["workspace"]
    args.data = toml_test_table["common"]["deterministic"]["data"]
    args.out = toml_test_table["common"]["deterministic"]["out"]
    args.player = toml_test_table["common"]["deterministic"]["player"]
    args.fcs_config_path = toml_test_table["common"]["deterministic"]["fcs_config_path"]
    args.filter = toml_test_table["common"]["deterministic"]["filter"]
    args.pipeline = toml_test_table["common"]["deterministic"]["pipeline"]
    args.sanitizer = toml_test_table["common"]["deterministic"]["sanitizer"]

    if args.test_mode == "hitl":
        args.fcc = toml_test_table["hitl"]["fcc"]
        args.bbc_utils_bin_path = toml_test_table["hitl"]["deterministic"][
            "bbc_utils_bin_path"
        ]
    else:
        args.fcc = None
        args.sitl_bin = toml_test_table["sitl"]["deterministic"]["sitl_bin"]

    args.mission_path = ""

    if not args.data:
        args.data = os.path.join(os.getcwd(), "data")

    if not args.out:
        args.out = os.getcwd()

    # Create a logger for logging information
    log = LoggingObject().log  # Create an instance of LoggingObject to get the logger

    log.info("Test Mode: " + args.test_mode)
    log.info("Workspace: " + args.workspace)
    log.info("Test data: " + args.data)
    log.info("Test output: " + args.out)
    log.info("scenario_player: " + args.player)

    if args.filter:
        log.info("Filter expression: '{}'".format(args.filter))

    # Create a TestSuite instance with the provided arguments
    
    ts = TestSuite(**args.__dict__)
    print("buraya giriyor")
    # Run the test suite and check the result
    ret = ts.run(is_on_pipeline=args.pipeline, is_sanitizer_enabled=args.sanitizer)
    
    if not ret:
        exit(-1)
