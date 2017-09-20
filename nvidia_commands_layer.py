#!/usr/bin/python3.5

import subprocess


class NvidiaCommandsLayerException(Exception):
    pass


class NvidiaCommandsLayer(object):
    @staticmethod
    def set_fan_percentage(
            value: int
    ) -> None:
        if value < 0 or value > 100:
            raise NvidiaCommandsLayerException('Cannot set a value outside 0 - 100')

        result = subprocess.run(
            [
                'nvidia-settings',
                 '-a',
                 '"[gpu:0]/GPUFanControlState=1"',
                 '-a',
                 '"[fan:0]/GPUTargetFanSpeed={}"'.format(value)
             ],
            stdout=subprocess.PIPE
        )

        if result.returncode != 0:
            raise NvidiaCommandsLayerException('Could not set the fan speed')

    @staticmethod
    def read_temperature(
    ) -> int:
        result = subprocess.run(
            [
                'nvidia-smi',
                 '--query-gpu=temperature.gpu',
                 '--format=csv,noheader,nounits'
            ],
            stdout=subprocess.PIPE
        )
        if result.returncode == 0:
            # the result is a string with a '\n' at the end, convert it to a decimal
            return int(result.stdout[:-1])
        else:
            raise NvidiaCommandsLayerException('Could not read the temperature')

