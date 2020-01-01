import os

def test_include_path_default_value__cwd_first(workspace):
    r = workspace.run("""php -r 'echo ini_get("include_path");'""")
    assert r.out == '.:/usr/local/lib/php' # where . means CWD

def _init_workspace(workspace):
    # .                 <-- CWD
    # |- inc.php
    # \- src/
    #    |- main.php    <-- calling script
    #    |- inc.php
    #    \- inc/        <-- include_path
    #       \- inc.php
    workspace.src('inc.php', '''
    <?php
    $inc = '/inc.php';
    ''')

    workspace.src('src/inc.php', '''
    <?php
    $inc = '/src/inc.php';
    ''')

    workspace.src('src/inc/inc.php', '''
    <?php
    $inc = '/src/inc/inc.php';
    ''')

    return os.path.join(workspace.workdir, 'src', 'inc')

def test_implicit_relative__relto_include_path_first(workspace):
    # .                 <-- CWD
    # |- inc.php
    # \- src/
    #    |- main.php    <-- calling script
    #    |- inc.php
    #    \- inc/        <-- include_path
    #       \- inc.php
    include_path = _init_workspace(workspace)

    workspace.src('src/main.php', '''
    <?php
    include 'inc.php';
    echo "\$inc = $inc";
    ''')

    r = workspace.run('php -d include_path=%s src/main.php' % include_path)
    assert r.out == '$inc = /src/inc/inc.php'

def test_implicit_relative__then_relto_calling_script(workspace):
    # .                 <-- CWD
    # |- inc.php
    # \- src/
    #    |- main.php    <-- calling script
    #    |- inc.php
    #    \- inc/        <-- include_path
    #       \- (inc.php)
    include_path = _init_workspace(workspace)
    os.remove('src/inc/inc.php')

    workspace.src('src/main.php', '''
    <?php
    include 'inc.php';
    echo "\$inc = $inc";
    ''')

    r = workspace.run('php -d include_path=%s src/main.php' % include_path)
    assert r.out == '$inc = /src/inc.php'

def test_implicit_relative__lastly_relto_cwd(workspace):
    # .                 <-- CWD
    # |- inc.php
    # \- src/
    #    |- main.php    <-- calling script
    #    |- (inc.php)
    #    \- inc/        <-- include_path
    #       \- (inc.php)
    include_path = _init_workspace(workspace)
    os.remove('src/inc/inc.php')
    os.remove('src/inc.php')

    workspace.src('src/main.php', '''
    <?php
    include 'inc.php';
    echo "\$inc = $inc";
    ''')

    r = workspace.run('php -d include_path=%s src/main.php' % include_path)
    assert r.out == '$inc = /inc.php'

def test_explicit_relative__relto_cwd_ignore_include_path_altogether(workspace):
    # .                 <-- CWD
    # |- inc.php
    # \- src/
    #    |- main.php    <-- calling script
    #    |- inc.php
    #    \- inc/        <-- include_path
    #       \- inc.php
    include_path = _init_workspace(workspace)

    workspace.src('src/main.php', '''
    <?php
    include './inc.php'; # w/ leading ./
    echo "\$inc = $inc";
    ''')

    r = workspace.run('php -d include_path=%s src/main.php' % include_path)
    assert r.out == '$inc = /inc.php'

def test_explicit_relative__not_fallback_to_calling_script(workspace):
    # .                 <-- CWD
    # |- (inc.php)
    # \- src/
    #    |- main.php    <-- calling script
    #    |- inc.php
    #    \- inc/        <-- include_path
    #       \- inc.php
    include_path = _init_workspace(workspace)
    os.remove('inc.php')

    workspace.src('src/main.php', '''
    <?php
    include './inc.php'; # w/ leading ./
    echo "\$inc = $inc";
    ''')

    r = workspace.run('php -d include_path=%s src/main.php' % include_path)
    assert "Failed opening './inc.php' for inclusion" in r.out

def test_relto_calling_script_regardless_include_path_and_cwd(workspace):
    # .                 <-- CWD
    # |- inc.php
    # \- src/
    #    |- main.php    <-- calling script
    #    |- inc.php
    #    \- inc/        <-- include_path
    #       \- inc.php
    include_path = _init_workspace(workspace)

    workspace.src('src/main.php', '''
    <?php
    include __DIR__.'/inc.php'; # w/ help of __DIR__ (magic constant)
    echo "\$inc = $inc";
    ''')

    r = workspace.run('php -d include_path=%s src/main.php' % include_path)
    assert r.out == '$inc = /src/inc.php'

def test_relto_relto_calling_script(workspace):
    # .                 <-- CWD
    # |- inc.php
    # \- src/
    #    |- main.php    <-- calling script
    #    |- inc.php -------------------------+
    #    \- inc/        <-- include_path     |
    #       \- inc.php  <--------------------+
    include_path = _init_workspace(workspace)

    workspace.src('src/main.php', '''
    <?php
    include __DIR__.'/inc.php'; # rel to current file
    echo "\$inc = $inc, \$incinc = $incinc";
    ''')

    workspace.src('src/inc.php', '''
    <?php
    include __DIR__.'/inc/inc.php'; # rel to current file
    $inc = '/src/inc.php';
    ''')

    workspace.src('src/inc/inc.php', '''
    <?php
    $incinc = '/src/inc/inc.php';
    ''')

    r = workspace.run('php -d include_path=%s src/main.php' % include_path)
    assert r.out == '$inc = /src/inc.php, $incinc = /src/inc/inc.php'
