def test_sort(workspace):
    r = workspace.eval('''
    let items = ['@self', '+gear-less', '@judy', 'done'];
    items.sort();
    console.log(items);
    ''')

    assert r.out == "[ '+gear-less', '@judy', '@self', 'done' ]"
