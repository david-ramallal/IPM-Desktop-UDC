#!/usr/bin/env python3

from cheathelper import *
import time


class Model:
    command: str = None

    def set_command(self, command: str) -> None:
        self.command = command

    def get_command(self) -> str:
        return self.command

    def obtain_command(self, command: str) -> list:
        time.sleep(1)
        input_command = (command.split(' ', 1))[0]
        results = get_cheatsheet(input_command)
        list_commands = list()

        for element in results:
            list_commands.append([element.commands, element.description])

        return list_commands
