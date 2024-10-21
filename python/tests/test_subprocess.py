import os, subprocess
import pytest

def test_run_string__without_shell__as_executable(workspace):
    with pytest.raises(FileNotFoundError) as excinfo:
        subprocess.run("echo 'Hello, World!'")

    assert str(excinfo.value) == '''[Errno 2] No such file or directory: "echo 'Hello, World!'"'''

def test_run_string___with_shell__as_command_line(workspace):
    cmd = "echo 'Hello, World!' && exit 0"
    r = subprocess.run(cmd, shell=True)

    assert isinstance(r, subprocess.CompletedProcess)
    assert r.returncode == 0
    assert r.args == cmd # not r.cmd like CalledProcessError
    assert r.stdout is None # capture_output= False (default)

def test_run_shell__nonzero_exit_code (workspace):
    cmd = "echo 'Hello, World!' && exit 1"
    r = subprocess.run(cmd, shell=True)

    assert r.returncode == 1
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        r.check_returncode()

    err = "Command 'echo 'Hello, World!' && exit 1' returned non-zero exit status 1."
    assert str(excinfo.value) == err
    assert excinfo.value.cmd == cmd # not exc.args like CompletedProcess

    # with check=True, raise error immediately
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        subprocess.run(cmd, shell=True, check=True)
    assert str(excinfo.value) == err

def test_run_shell__capture_output_as_text(workspace):
    workspace.src('message.txt', 'Hello, World! 哈囉')
    cmd = "cat message.txt && echo 'message redirected to STDOUT' >&2"

    r = subprocess.run(cmd, shell=True, capture_output=True)
    assert type(r.stdout) is bytes and type(r.stdout) is bytes
    assert r.stdout == 'Hello, World! 哈囉'.encode('utf-8') # bytes sequence, text=False (default)
    assert r.stderr == b'message redirected to STDOUT\n'

    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert type(r.stdout) is str and type(r.stderr) is str
    assert r.stdout == 'Hello, World! 哈囉' # text=True
    assert r.stderr == 'message redirected to STDOUT\n'

def _run_for_envvars(env):
   r = subprocess.run('env', capture_output=True, env=env)
   return dict(line.split('=') for line in r.stdout.decode('utf-8').splitlines())

def test_run_with_env__no_inheritance_only_variables_provided(workspace):
    os.environ['ENV_FROM_PYTHON'] = 'os.environ'

    # including variables set via os.environ
    assert 'ENV_FROM_PYTHON' in _run_for_envvars(env=None)

    # just the key(s) you provide
    assert _run_for_envvars(env={}) == {} # empty env!
    assert _run_for_envvars(env={'GREETING': 'Hello'}).keys() == { 'GREETING' }

def test_howto_customize_inherited_env(workspace):
    os.environ['MYENV1'] = '1'
    vars_default = _run_for_envvars(env=None)

    # use dict(os.environ, **key-value pairs)
    vars_customized = _run_for_envvars(
        env=dict(os.environ, **{'MYENV1': 'one', 'MYENV2': 'two'}))

    assert set(vars_default.keys()).issubset(vars_customized.keys())
    assert vars_customized['MYENV1'] == 'one'
    assert set(vars_customized.keys()).difference(vars_default.keys()) == { 'MYENV2' }
    assert vars_customized['MYENV2'] == 'two'
