#!/usr/bin/python3


import argparse
import configparser
import datetime
import sys


def is_a_year(value):
    value = value.rstrip("'")  # remove primes
    return len(value) == 4 and all((c in "0123456789") for c in value)


def is_a_date(value):
    if value == "None":
        return True
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def errors_in(filename):
    srcfile = configparser.ConfigParser()
    try:
        srcfile.read(filename)
    except Exception as exc:
        yield "Invalid INI format: %s" % exc
        return
    if "general" not in srcfile:
        yield "Missing [general] section"
    for section_name in srcfile:
        if section_name == "DEFAULT":
            yield from errors_in_default(srcfile[section_name])
        elif section_name == "general":
            for error in errors_in_general(srcfile[section_name]):
                yield "[general]: %s" % error
        elif is_a_year(section_name):
            for error in errors_in_year(srcfile[section_name]):
                yield "[%s]: %s" % (section_name, error)
        else:
            yield "Unexpected section %r" % section_name


def errors_in_default(default):
    for key in default:
        yield "Unexpected top-level definition of %r" % key


def errors_in_general(general):
    if "title" not in general:
        yield "Missing title"
    if "usually" in general:
        months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
        if general["usually"] not in months:
            yield "Invalid usually month: %r" % general["usually"]
    for key in general:
        if key not in ("title", "usually"):
            yield "Unexpected definition of %r" % key


def errors_in_year(section):
    if "date" in section:
        if "start" in section:
            yield "Cannot combine date with start"
        if "end" in section:
            yield "Cannot combine date with start"
    else:
        if ("start" not in section) and ("end" not in section):
            yield "Missing date or start/end"
        else:
            if "start" not in section:
                yield "Missing start"
            if "end" not in section:
                yield "Missing end"
    for key in ("date", "start", "end"):
        if key in section and not is_a_date(section[key]):
            yield "Invalid date format of %s: %r" % (key, section[key])
    for key in section:
        if key not in ("date", "start", "end", "title"):
            yield "Unexpected definition of %r" % key


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("source_files", nargs="+")
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    for filename in args.source_files:
        for error in errors_in(filename):
            print("%s: %s" % (filename, error.replace("\n", " ")))


if __name__ == '__main__':
    main()
