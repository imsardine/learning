from . import *
import pytest
from textwrap import dedent
import argparse

class ArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        # self.print_usage(_sys.stderr)
        # args = {'prog': self.prog, 'message': message}
        # self.exit(2, _('%(prog)s: error: %(message)s\n') % args)
        errmsg = self.format_usage()
        args = {'prog': self.prog, 'message': message}
        errmsg += '%(prog)s: error: %(message)s\n' % args

        raise ValueError(errmsg)

def test_subcmds__help_message():
    parser = ArgumentParser(prog='cmd')
    parser.add_argument('--cmd-opt', metavar='<value>', help='Help message of the option')
    subparsers = parser.add_subparsers(title='subcommands', metavar='<command>')
    subcmd1 = subparsers.add_parser('subcmd1', help='Help message of subcmd1')
    subcmd2 = subparsers.add_parser('subcmd2', help='Help message of subcmd2')
    subcmd1.add_argument('subcmd1-arg')
    subcmd1.add_argument('--subcmd1-opt', metavar='<value>')

    # from the view point of the main paser
    assert parser.format_help() == dedent("""\
        usage: cmd [-h] [--cmd-opt <value>] <command> ...

        options:
          -h, --help         show this help message and exit
          --cmd-opt <value>  Help message of the option

        subcommands:
          <command>
            subcmd1          Help message of subcmd1
            subcmd2          Help message of subcmd2\n""")

    # from the view point of a sub-parser
    assert subcmd1.format_help() == dedent("""\
        usage: cmd subcmd1 [-h] [--subcmd1-opt <value>] subcmd1-arg

        positional arguments:
          subcmd1-arg

        options:
          -h, --help            show this help message and exit
          --subcmd1-opt <value>\n""")

@py2_only
def test_subcmds_required_py2__not_supported():
    with pytest.raises(TypeError) as exc_info:
        ArgumentParser().add_subparsers(metavar='command', required=True)
    assert str(exc_info.value) == "__init__() got an unexpected keyword argument 'required'"

@py3_later
def test_subcmds__required_but_not_provided__raise_error():
    parser = ArgumentParser(prog='cmd')
    subparsers = parser.add_subparsers(metavar='command', required=True)
    subparser = subparsers.add_parser('subcmd')

    with pytest.raises(ValueError) as exc_info:
        parser.parse_args([])
    assert str(exc_info.value) == dedent("""\
        usage: cmd [-h] command ...
        cmd: error: the following arguments are required: command\n""")

class DependentArgumentParser(ArgumentParser):

    def parse_known_args(self, args=None, namespace=None):
        subnamespace, arg_strings = super(DependentArgumentParser, self) \
                .parse_known_args(args, namespace)

        validate = getattr(subnamespace, 'validate', None)
        if validate and callable(validate):
            try:
                validate(subnamespace)
            except ValueError as e:
                self.error(str(e))

        return subnamespace, arg_strings

def test_argument_dependency__validation():
    def validate_args(args):
        if args.end_date <= args.start_date:
            raise ValueError('End date must be greater than the start date')

    from dateutil import parser as date_parser
    parser = DependentArgumentParser(prog='cmd')
    parser.set_defaults(validate=validate_args)
    parser.add_argument('start_date', type=date_parser.parse)
    parser.add_argument('end_date', type=date_parser.parse)

    with pytest.raises(ValueError) as exc_info:
        parser.parse_args(['2018-11-22', '2018-11-21'])
    assert str(exc_info.value) == dedent("""\
        usage: cmd [-h] start_date end_date
        cmd: error: End date must be greater than the start date\n""")

def test_argument_dependency__vaidation_with_subcmds():
    def validate_args(args):
        if args.end_date <= args.start_date:
            raise ValueError('End date must be greater than the start date')

    from dateutil import parser as date_parser
    parser = DependentArgumentParser(prog='cmd')
    subparsers = parser.add_subparsers(metavar='command')
    subparser = subparsers.add_parser('subcmd')

    subparser.set_defaults(validate=validate_args)
    subparser.add_argument('start_date', type=date_parser.parse)
    subparser.add_argument('end_date', type=date_parser.parse)

    with pytest.raises(ValueError) as exc_info:
        parser.parse_args(['subcmd', '2018-11-22', '2018-11-21'])
    assert str(exc_info.value) == dedent("""\
        usage: cmd subcmd [-h] start_date end_date
        cmd subcmd: error: End date must be greater than the start date\n""")

class HelpNeeded(Exception): pass

class HelpAction(argparse._HelpAction):

    def __call__(self, parser, namespace, values, option_string=None):
        raise HelpNeeded(parser.format_help())

def test_argument_dependency__help_message():
    def validate_args(args):
        if args.end_date <= args.start_date:
            raise ValueError('End date must be greater than the start date')

    from dateutil import parser as date_parser
    parser = DependentArgumentParser(prog='cmd', add_help=False)
    parser.add_argument('-h', '--help', action=HelpAction)
    subparsers = parser.add_subparsers(metavar='command')
    subparser = subparsers.add_parser('subcmd', add_help=False)

    subparser.set_defaults(validate=validate_args)
    subparser.add_argument('-h', '--help', action=HelpAction)
    subparser.add_argument('start_date', type=date_parser.parse)
    subparser.add_argument('end_date', type=date_parser.parse)

    with pytest.raises(HelpNeeded) as exc_info:
        parser.parse_args(['-h'])
    assert str(exc_info.value) == dedent("""\
        usage: cmd [-h] command ...

        positional arguments:
          command

        options:
          -h, --help\n""")

    with pytest.raises(HelpNeeded) as exc_info:
        parser.parse_args(['subcmd', '-h'])
    assert str(exc_info.value) == dedent("""\
        usage: cmd subcmd [-h] start_date end_date

        positional arguments:
          start_date
          end_date

        options:
          -h, --help\n""")
