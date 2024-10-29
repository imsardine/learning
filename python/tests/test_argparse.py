from . import *
import pytest
from textwrap import dedent
import argparse

def test_basic_usage(workspace):
    r = workspace.src('hello.py', '''
    import argparse

    parser = argparse.ArgumentParser()

    # positional arguments. also positionals
    parser.add_argument('who')
    # optional arguments (with '-' prefix), also options, flags or optionals
    parser.add_argument('-e', '--emoticon', default=':-)')

    args = parser.parse_args() # namespace object returned
    print(f'Hello, {args.who}! {args.emoticon}') # as attributes of the namespace object
    ''')

    assert workspace.run('python hello.py World').out == 'Hello, World! :-)'
    assert workspace.run("python hello.py Python --emoticon '<3'").out == 'Hello, Python! <3'

def test_multiple_option_names(workspace):
    workspace.src('hello.py', '''
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-g', '--greeting', '--hi', dest='prefix', default='Hi')

    args = parser.parse_args()
    print(f'{args.prefix}, World!')
    ''')

    r = workspace.run('python hello.py --help')
    assert '-g PREFIX, --greeting PREFIX, --hi PREFIX' in r.out

    assert workspace.run('python hello.py --greeting Hello').out == 'Hello, World!'
    assert workspace.run('python hello.py --hi Yo').out == 'Yo, World!'

def test_howto_make_positional_arguments_optional(workspace):
    r = workspace.eval_err('''
    import argparse

    parser = argparse.ArgumentParser()

    # TypeError, 'required' only for optional arguments
    parser.add_argument('who', required=False, default='World')
    ''')

    assert "TypeError: 'required' is an invalid argument for positionals" in r.err

    workspace.src('hello.py', '''
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('who', nargs='?', default='World') # use nargs='?' instead

    args = parser.parse_args()
    print(f'Hello, {args.who}!')
    ''')

    assert workspace.run('python hello.py').out == 'Hello, World!'
    assert workspace.run('python hello.py Python').out == 'Hello, Python!'

def test_extra_args_present__error_unrecognized_args(workspace):
    r = workspace.src('hello.py', '''
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('who')
    parser.add_argument('-e', '--emoticon', default=':-)')

    args = parser.parse_args()
    ''')

    r = workspace.run_err('python hello.py World --greeting Hi')
    assert 'error: unrecognized arguments: --greeting Hi' in r.err

def test_exit_on_error__not_for_absense_of_required_arguments(workspace):
    workspace.src('add.py', '''
    import sys, argparse

    # do not exit, but raise error instead
    parser = argparse.ArgumentParser(exit_on_error=False)

    parser.add_argument('a', type=int) # required, by default
    parser.add_argument('b', type=int, nargs='?', default=0) # optional
    parser.add_argument('--greeting', default='Welcome!') # optional, by default
    parser.add_argument('--show-equation', choices=['yes', 'no'], required=True)

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as err:
        print('expected err:', err)
        sys.exit()
    ''')

    # expected err (not exited)
    r = workspace.run('python add.py --show-equation off 1 2') # optional args
    assert r.out == "expected err: argument --show-equation: invalid choice: 'off' (choose from 'yes', 'no')"

    r = workspace.run('python add.py --show-equation yes one two') # positional args
    assert r.out == "expected err: argument a: invalid int value: 'one'"

    # unexpected exit
    r = workspace.run_err('python add.py 1 2') # optional args
    assert r.rc == 2
    assert 'error: the following arguments are required: --show-equation' in r.err

    r = workspace.run_err('python add.py --show-equation yes') # positional args
    assert r.rc == 2
    assert 'error: the following arguments are required: a' in r.err

def test_parse_known_args(workspace):
    workspace.src('hello.py', '''
    from argparse import ArgumentParser, ArgumentError

    parser = ArgumentParser(exit_on_error=False)
    parser.add_argument('who')
    parser.add_argument('-e', '--emoticon')

    try:
        args, unknown_args = parser.parse_known_args()
    except ArgumentError:
        print('expected error')

    print(args, unknown_args)
    ''')

    r = workspace.run("python hello.py World -e '<3' -f --bar boo")
    assert r.out == "Namespace(who='World', emoticon='<3') ['-f', '--bar', 'boo']"

    # unexpected exit
    r = workspace.run_err("python hello.py -e '<3' -foo --bar")
    assert r.rc == 2
    assert 'error: the following arguments are required: who' in r.err

def test_howto_as_wrapper_dispatcher_passing_remaining_args_to_another_cli_tool(workspace):
    workspace.src('hello.py', '''
    print("...")
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('who')
    parser.add_argument('-g', '--greeting', default='Hello')
    parser.add_argument('-e', '--emoticon', default=':-)')

    args = parser.parse_args()
    print(f'{args.greeting}, {args.who}! {args.emoticon}')
    ''')

    # do something with the emoticon (required)
    workspace.src('myhello.py', '''
    import sys, subprocess
    import argparse

    class ArgumentParser(argparse.ArgumentParser):

        # https://peps.python.org/pep-0389/#discussion-sys-stderr-and-sys-exit
        def error(self, message):
            raise argparse.ArgumentError(None, message)

    parser = ArgumentParser(exit_on_error=False)
    parser.add_argument('-e', '--emoticon', required=True)

    try:
        args, unknown_args = parser.parse_known_args()
    except argparse.ArgumentError:
        r = subprocess.run(['python', 'hello.py', '--help'], capture_output=True)
        print(r.stdout, file=sys.stderr)
        sys.exit(2) # align with argparse's behavior

    args_emoticon = []
    if args.emoticon:
        args_emoticon = ['--emoticon', args.emoticon + ' (customized)']

    cmd = ['python', 'hello.py'] + args_emoticon + unknown_args
    r = subprocess.run(cmd)
    sys.exit(r.returncode)
    ''')

    r = workspace.run("python myhello.py --emoticon '<3' World")
    assert r.out == '...\nHello, World! <3 (customized)'

    # invalid usage, messages from the wrapped command
    r = workspace.run_err('python myhello.py --greeting Hi World')
    assert r.rc == 2
    assert 'usage: hello.py [-h] [-g GREETING] [-e EMOTICON] who' in r.err

    r = workspace.run_err("python myhello.py -e XD")
    assert r.rc == 2
    assert 'error: the following arguments are required: who' in r.err

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
