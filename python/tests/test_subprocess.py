import pytest
import subprocess

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
