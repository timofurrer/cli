# -*- coding: utf-8 -*-

from clicore.core import CliItem

import sys


class CliHelper(object):
    @classmethod
    def create_help_item(cls, cli):
        if not hasattr(cli, "get_items"):
            raise TypeError("first argument must have a 'get_items()' method")

        def help_item(item, args, line_input):
            """
                arguments: [item]
                description: show this help screen
            """
            if not args:
                items = [i for i in cli.get_items() if i.is_enabled()]
                items.sort(key=lambda i: i.get_name())
            else:
                item = cli.get_item_by_name(args, only_enabled=True)
                if not item:
                    print("item '%s' does not exist or is not enabled" % args)
                    return
                items = [item]

            max_len_name = max([len(i.get_name()) for i in items])
            max_len_args = max([len(i.get_help()["arguments"]) for i in items])
            max_len_desc = max([len(i.get_help()["description"]) for i in items])

            indentation = "    "
            spaces = "      "
            for i in items:
                name = i.get_name()
                help = i.get_help()
                sys.stdout.write(indentation + name + " " * (max_len_name - len(name)) + spaces)
                sys.stdout.write(help["arguments"] + " " * (max_len_args - len(help["arguments"])) + spaces)
                sys.stdout.write(help["description"] + " " * (max_len_desc - len(help["description"])) + "\n")

        return CliItem("help", help_item)
