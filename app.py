#!/usr/bin/env python3

import json
import logging.config

import argparse

import sys

import os

from nvidia_commands_layer import NvidiaCommandsLayer, NvidiaCommandsLayerException


def main():
    try:
        log_file = os.path.join(os.path.dirname(__file__), 'logging.json')
        with open(log_file) as data_file:
            logging_dict_config = json.load(data_file)

        logging.config.dictConfig(logging_dict_config)
        logger = logging.getLogger(__name__)
        logger.debug('Started Logging')

        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--set_speed",
                            type=int,
                            help="Set Fan speed as a percentage of total speed, "
                                 "from 0 to 100")
        parser.add_argument("-r", "--read_temperature",
                            action="store_true",
                            help="Read the card's temperature in degrees Celsius")

        args = parser.parse_args()

        if args.set_speed:
            NvidiaCommandsLayer.set_fan_percentage(args.set_speed)
        elif args.read_temperature:
            print("Current temperature: {}".format(NvidiaCommandsLayer.read_temperature()))

    except OSError as e:
        print("Could not open the logging config file {}".format(e))
        return 1
    except NvidiaCommandsLayerException as e:
        logger.error("Exception encountered when trying to run the command - {}".format(e))
        return 1


if __name__ == '__main__':
    sys.exit(main())
