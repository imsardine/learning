def test_variable_parsing__single_quote__no_effect(workspace):
    workspace.src('test.php', '''
    <?php
    $who = "World";
    echo 'Hello, $who!'
    ?>
    ''')

    assert workspace.run('php test.php').out == 'Hello, $who!'

def test_variable_parsing__double_quote__substituted(workspace):
    workspace.src('test.php', '''
    <?php
    $who = "World";
    echo "Hello, $who!"
    ?>
    ''')

    assert workspace.run('php test.php').out == 'Hello, World!'

def test_variable_parsing__var_not_defined__empty_but_no_error(workspace):
    workspace.src('test.php', '''
    <?php
    echo "Hello, $who!"
    ?>
    ''')

    assert workspace.run('php test.php').out == 'Hello, !'
