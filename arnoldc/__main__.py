import argparse
# import select
import sys

from .arnoldc import parse


def example():
    print("""IT'S SHOWTIME
TALK TO THE HAND "Hello World!"
YOU HAVE BEEN TERMINATED""")


def main(args=None):
    if not sys.stdin.isatty():
        text = sys.stdin.read()
        filename = 'STDIN'
    else:
        if args is None:
            args = sys.argv[1:]
        if args[-1].startswith('-'):
            args = args + ['example.arnoldc']
        parser = argparse.ArgumentParser()
        parser.add_argument('filename', nargs='?')
        parser.add_argument(
            '-c',
            metavar='cmd',
            dest='command',
            help='program passed in as string',
        )
        parser.add_argument(
            '-e', '--example',
            action='store_true',
            help='print example program',
        )
        opts = parser.parse_args(args)
        if opts.example:
            example()
            return 0
        if opts.command:
            text = opts.command
            filename = 'CMD'
        else:
            with open(opts.filename) as f:
                text = f.read()
            filename = opts.filename
    prog = parse(text, filename)
    try:
        return prog.run()
    except KeyboardInterrupt:
        sys.stdout.flush()
        return 1
