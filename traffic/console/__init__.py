import argparse
import logging
import sys

import importlib
import pkgutil


def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        results[name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def main():

    cmd = import_submodules(__name__, recursive=False)

    parser = argparse.ArgumentParser(
        description="traffic command-line interface",
        epilog="For specific help about each command, type traffic command -h",
    )

    parser.add_argument(
        "command", help=f"choose among: {', '.join(cmd.keys())}"
    )
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="all arguments to dispatch to command",
    )

    args = parser.parse_args()

    mod = cmd.get(args.command, None)

    if mod is None:
        return parser.print_help()

    return mod.main(args.args)
