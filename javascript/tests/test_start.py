from .conftest import lines

def test_hello_world(workspace):
    r = workspace.eval('''
    const lang = 'JavaScript (JS)'
    console.log(`Hello, ${lang}!`); // template literal
    ''')

    assert r._out == 'Hello, JavaScript (JS)!\n'

def test_assignment__expression_resolves_to_a_value(workspace):
    r = workspace.eval('''
    let x;
    console.log(x = 1 + 6); // unique and convenient
    ''')

    assert r.out == '7'

def test_typeof__primitive_types(workspace):
    r = workspace.eval('''
    console.log(typeof 1); // number
    console.log(typeof NaN); // number (special)
    console.log(typeof Infinity); // number (special)

    console.log(typeof 1n); // bigint
    console.log(typeof ''); // string
    console.log(typeof false); // boolean
    console.log(typeof Symbol()); // symbol
    console.log(typeof null); // object (special case)
    console.log(typeof undefined); // undefined
    // symbol
    ''')

    assert r.out == lines([
        'number', 'number', 'number',
        'bigint',
        'string',
        'boolean',
        'symbol',
        'object',
        'undefined'])

def test_boolean_context__truthy_falsy(workspace):
    r = workspace.eval('''
    console.log(Boolean(0)); // false
    console.log(Boolean(-1)); // true, non-zero
    console.log(Boolean('')); // false, empty string
    console.log(Boolean([])); // true, counter-intuitive!
    console.log(Boolean({})); // true, counter-intuitive!
    ''')

    assert r.out == lines(['false', 'true', 'false', 'true', 'true'])

def test_comparison__double_equals__loose_equality_with_type_coercion(workspace):
    r = workspace.eval('''
    const o1 = [1, 2, 3], o2 = [1, 2, 3]; // arrays are also objects

    // object to object, true only reference the same object
    console.log(o1 == o1); // true
    console.log(o1 == o2); // false

    // object to primitive, primitive coercion involved
    console.log([] == false); // true. [] -> false, even [] is truthy

    // different types, type coercion involved
    console.log(1 == true); // true.
    console.log(true == 1); // true. symmetric, either way
    console.log(0 == false); // true. Boolean(0) -> false, Number(false) -> 0
    console.log(1 == '1'); // true

    // exceptions
    console.log(null == undefined); // true. null/undefined only equals to null/undefined
    console.log(undefined == null); // true.
    console.log(false == undefined); // false. even undefined is falsy

    console.log(NaN == NaN); // false. NaN never equals to anything
    ''')

    assert r.out == lines([
        'true', 'false',
        'true',
        'true', 'true', 'true', 'true',
        'true', 'true', 'false',
        'false'])

def test_comparison__triple_equals__strict_equality_no_type_coercion_simple(workspace):
    r = workspace.eval('''
    const o1 = [1, 2, 3], o2 = [1, 2, 3]; // arrays are also objects

    // objects, true only reference the same object
    console.log(o1 === o1); // true
    console.log(o1 === o2); // false

    // different types, always false
    console.log(1 === true); // false
    console.log(true === 1); // false
    console.log(1 === '1'); // false
    console.log(null === undefined); // false

    // exceptions
    console.log(NaN === NaN); // false. NaN never equals to anything
    ''')

    assert r.out == lines([
        'true', 'false',
        'false', 'false', 'false', 'false',
        'false'])

def test_let__access_before_declaration__reference_error(workspace):
    r = workspace.eval_err('''
    console.log(lang);
    let lang = 'JavaScript (JS)';
    ''')

    # ReferenceError: Cannot access 'xxx' before initialization
    assert "ReferenceError: Cannot access 'lang' before initialization" in r.err

def test_let__block_scoped__or_reference_error(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#variables
    r = workspace.eval_err('''
    let outerL0 = '--> L0 (ok)';
    { // block L1
      let innerL1 = '--> L1 (ok)';

      { // block L2
        let innerL2 = '--> L2 (ok)';
        console.log(`from L2; ${outerL0}, ${innerL1}, ${innerL2}`);
      }

      console.log(`from L1; ${outerL0}, ${innerL1}, ${innerL2}`);
    }
    ''')

    assert r.out == 'from L2; --> L0 (ok), --> L1 (ok), --> L2 (ok)'
    assert 'ReferenceError: innerL2 is not defined' in r.err

def test_const__without_initiation__syntax_error(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#variables
    r = workspace.eval_err('''
    const Pi;
    Pi = 3.14;
    ''')

    assert 'SyntaxError: Missing initializer in const declaration' in r.err

def test_const__block_scoped_like_let__or_reference_error(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#variables
    r = workspace.eval_err('''
    const outerL0 = '--> L0 (ok)';
    { // block L1
      const innerL1 = '--> L1 (ok)';

      { // block L2
        const innerL2 = '--> L2 (ok)';
        console.log(`from L2; ${outerL0}, ${innerL1}, ${innerL2}`);
      }

      console.log(`from L1; ${outerL0}, ${innerL1}, ${innerL2}`);
    }
    ''')

    assert r.out == 'from L2; --> L0 (ok), --> L1 (ok), --> L2 (ok)'
    assert 'ReferenceError: innerL2 is not defined' in r.err

def test_const__cannot_reassigned_but_still_mutable(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#variables
    r = workspace.eval_err('''
    const fruits = ['apple', 'orange'];

    fruits.push('starfruit'); // mutable
    console.log(fruits);

    fruits = []; // error
    ''')

    assert r.out == "[ 'apple', 'orange', 'starfruit' ]"
    assert 'TypeError: Assignment to constant variable.' in r.err

def test_var__not_block_scoped(workspace):
    # discouraged in modern JavaScript code
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#variables
    r = workspace.eval('''
    var outerL0 = '--> L0 (ok)';
    { // block L1
      var innerL1 = '--> L1 (ok)';

      { // block L2
        var innerL2 = '--> L2 (ok)';
        console.log(`from L2; ${outerL0}, ${innerL1}, ${innerL2}`);
      }

      console.log(`from L1; ${outerL0}, ${innerL1}, ${innerL2}`);
    }
    ''')

    assert r.out == lines('''
    from L2; --> L0 (ok), --> L1 (ok), --> L2 (ok)
    from L1; --> L0 (ok), --> L1 (ok), --> L2 (ok)
    ''')

def test_undefined__when_let_var_not_initialized(workspace):
    r = workspace.eval('''
    let letNotInitialized;
    var varNotInitialized;

    console.log(letNotInitialized === undefined);
    console.log(varNotInitialized === undefined);
    ''')

    assert r.out == lines(['true', 'true'])

def test_undefined__when_return_with_no_value(workspace):
    r = workspace.eval('''
    function fun() {
      return;
    }

    console.log(fun());
    ''')

    assert r.out == 'undefined'

def test_undefined__when_access_nonexistent_property__no_error(workspace):
    r = workspace.eval('''
    lang = {}; // empty object
    console.log(typeof lang.xxx);
    ''')

    assert r.rc == 0 # no error!
    assert r.out == 'undefined'

def test_infinity__a_number_when(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#numbers
    r = workspace.eval('''
    console.log(typeof Infinity); // (special) number
    console.log(1 / 0 === Infinity);
    console.log(-1 / 0 === -Infinity);
    ''')

    assert r.out == lines(['number', 'true', 'true'])

def test_nan__a_number_when_and_contagious(workspace):
    # `NaN` is contagious: if you provide it as an operand to any mathematical operation, the result will also be `NaN`.
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#numbers
    r = workspace.eval('''
    console.log(typeof NaN); // (special) number

    const nan = parseInt('non-numeric');
    console.log(nan);
    console.log(1 + nan); // contagious
    ''')

    assert r.out == lines(['number', 'NaN', 'NaN'])

def test_nan__never_equal_to_itself__use_isnan_instead(workspace):
    r = workspace.eval('''
    console.log(undefined === undefined); // true
    console.log(null === null); // true
    console.log(Infinity === Infinity); // true

    // `NaN` is the only value in JavaScript that's **not equal to itself**
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#numbers
    console.log(NaN === NaN); // always false!
    console.log(Number.isNaN('nan')); // use Number.isNaN() instead
    console.log(Number.isNaN(NaN));
    ''')

    assert r.out == lines([
        'true', 'true', 'true',
        'false', 'false', 'true'])
