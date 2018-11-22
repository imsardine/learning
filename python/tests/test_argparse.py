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

        optional arguments:
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

        optional arguments:
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

def test_argument_dependency():
    class DependentArgumentParser(ArgumentParser):

        def parse_args(self, args=None, namespace=None):
            args = super(DependentArgumentParser, self).parse_args(args, namespace)

            validate = getattr(args, 'validate', None)
            if not (validate and callable(validate)):
                return args

            try:
                validate(args)
            except ValueError as e:
                self.error(str(e))

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
