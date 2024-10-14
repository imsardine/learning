def test_if_elseif_else(workspace):
    r = workspace.eval('''
    function abbrev(lang) {
      if (lang == 'JavaScript') {
        return 'JS';
      } else if (lang == 'Python') {
        return 'PY';
      } else {
        return '(n/a)';
      }
    }

    for (let lang of ['JavaScript', 'Python', 'Rust']) {
      console.log(abbrev(lang));
    }
    ''')

    assert r.out == 'JS\nPY\n(n/a)'

def test_while(workspace):
    r = workspace.eval('''
    let iterator = [3, 2, 1, undefined].values();

    let element = iterator.next().value;
    while (element !== undefined) {
      console.log(element);
      element = iterator.next().value;
    }
    ''')

    assert r.out == '3\n2\n1'

def test_do_while(workspace):
    r = workspace.eval('''
    let iterator = [undefined, 3].values();

    let input;
    do {
      input = iterator.next().value;
      console.log(input);
    } while (input === undefined); // invalid input
    ''')

    assert r.out == 'undefined\n3'

def test_while__assignment_as_condition__parentheses_and_explicit_comparison(workspace):
    r = workspace.eval('''
    // assignment w/ parentheses + explicit comparison
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/while#using_an_assignment_as_a_condition
    let iterator = [3, 2, 1].values();

    let element;
    while ((element = iterator.next().value) != undefined) {
      console.log(element);
    }
    ''')

    assert r.out == '3\n2\n1'

def test_while__assignment_as_condition_with_variable_declaration__syntax_error(workspace):
    r = workspace.eval_err('''
    let iterator = [3, 2, 1].values();

    while ((let element = iterator.next().value) != undefined) {
      console.log(element);
    }
    ''')

    assert "SyntaxError: Unexpected identifier 'element'" in r.err

def test_for(workspace):
    r = workspace.eval('''
    let str = '';
    for (let i = 0; i <= 9; i++) { // initialization; condition; afterthought
      str += i;
    }

    console.log(str);
    ''')

    assert r.out == '0123456789'

def test_for_of(workspace):
    r = workspace.eval('''
    let nums = [3, 2, 1];

    sum = 0;
    for (let num of nums) {
      sum += num;
    }

    console.log(sum); // 6
    ''')

    assert r.out == '6'
