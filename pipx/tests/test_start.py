def test_install__with_suffix__multiple_versions_in_parallel(workspace):
    # https://python-poetry.org/docs/#installing-with-pipx
    workspace.run('pipx install --suffix=-4 cowsay==4.0')
    workspace.run('pipx install --suffix=@5.0 cowsay==5.0')

    assert workspace.run('cowsay-4 --version').out == '4.0'
    assert workspace.run('cowsay@5.0 --version').out == '5.0'
