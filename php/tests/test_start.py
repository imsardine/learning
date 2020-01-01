def test_hello_world(workspace):
    workspace.src('hello.php', '''
    <?php echo 'Hello, World!'; ?>
    ''')

    r = workspace.run('php hello.php')
    assert r.out == 'Hello, World!'
