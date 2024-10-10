from .conftest import lines

def test_hello_world(workspace):
    r = workspace.eval('''
    const lang = 'JavaScript (JS)'
    console.log(`Hello, ${lang}!`);
    ''')

    assert r._out == 'Hello, JavaScript (JS)!\n'

def test_typeof__primitive_types(workspace):
    r = workspace.eval('''
    console.log(`typeof 1 --> ${ typeof 1 }`) // number
    console.log(`typeof 1n --> ${ typeof 1n }`) // bigint
    console.log(`typeof '' --> ${ typeof '' }`) // string
    console.log(`typeof false --> ${ typeof false }`) // boolean
    console.log(`typeof null --> ${ typeof null }`) // object!
    console.log(`typeof undefined --> ${ typeof undefined }`) // undefined
    // symbol
    ''')

    assert r.out == lines('''
    typeof 1 --> number
    typeof 1n --> bigint
    typeof '' --> string
    typeof false --> boolean
    typeof null --> object
    typeof undefined --> undefined
    ''')

def test_let__access_before_declaration__reference_error(workspace):
    r = workspace.eval_err('''
    console.log(`Hello, ${lang}!`)
    let lang = 'JavaScript (JS)'
    ''')

    # ReferenceError: Cannot access 'xxx' before initialization
    assert "ReferenceError: Cannot access 'lang' before initialization" in r.err

def test_let__block_scoped__or_reference_error(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#variables
    r = workspace.eval_err('''
    let outerL0 = '--> L0 (ok)'
    { // block L1
      let innerL1 = '--> L1 (ok)'

      { // block L2
        let innerL2 = '--> L2 (ok)'
        console.log(`from L2; ${outerL0}, ${innerL1}, ${innerL2}`)
      }

      console.log(`from L1; ${outerL0}, ${innerL1}, ${innerL2}`)
    }
    ''')

    assert r.out == 'from L2; --> L0 (ok), --> L1 (ok), --> L2 (ok)'
    assert 'ReferenceError: innerL2 is not defined' in r.err

def test_const__without_initiation__syntax_error(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#variables
    r = workspace.eval_err('''
    const Pi
    Pi = 3.14
    ''')

    assert 'SyntaxError: Missing initializer in const declaration' in r.err

def test_const__block_scoped_like_let__or_reference_error(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#variables
    r = workspace.eval_err('''
    const outerL0 = '--> L0 (ok)'
    { // block L1
      const innerL1 = '--> L1 (ok)'

      { // block L2
        const innerL2 = '--> L2 (ok)'
        console.log(`from L2; ${outerL0}, ${innerL1}, ${innerL2}`)
      }

      console.log(`from L1; ${outerL0}, ${innerL1}, ${innerL2}`)
    }
    ''')

    assert r.out == 'from L2; --> L0 (ok), --> L1 (ok), --> L2 (ok)'
    assert 'ReferenceError: innerL2 is not defined' in r.err

def test_const__cannot_reassigned_but_still_mutable(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#variables
    r = workspace.eval_err('''
    const fruits = ['apple', 'orange']

    fruits.push('starfruit') // mutable
    console.log(`fruits = ${fruits}`)

    fruits = [] // error
    ''')

    assert r.out == 'fruits = apple,orange,starfruit' # not enclosed in []
    assert 'TypeError: Assignment to constant variable.' in r.err

def test_var__not_block_scoped(workspace):
    # discouraged in modern JavaScript code
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#variables
    r = workspace.eval('''
    var outerL0 = '--> L0 (ok)'
    { // block L1
      var innerL1 = '--> L1 (ok)'

      { // block L2
        var innerL2 = '--> L2 (ok)'
        console.log(`from L2; ${outerL0}, ${innerL1}, ${innerL2}`)
      }

      console.log(`from L1; ${outerL0}, ${innerL1}, ${innerL2}`)
    }
    ''')

    assert r.out == lines('''
    from L2; --> L0 (ok), --> L1 (ok), --> L2 (ok)
    from L1; --> L0 (ok), --> L1 (ok), --> L2 (ok)
    ''')

def test_undefined__when_let_var_not_initialized(workspace):
    r = workspace.eval('''
    let letNotInitialized
    var varNotInitialized

    console.log(`let --> undefined (${ letNotInitialized === undefined })`)
    console.log(`var --> undefined (${ varNotInitialized === undefined })`)
    ''')

    assert r.out == lines('''
    let --> undefined (true)
    var --> undefined (true)
    ''')

def test_undefined__when_return_with_no_value(workspace):
    r = workspace.eval('''
    function fun() {
      return;
    }

    console.log(`return; --> ${ fun() }`)
    ''')

    assert r.out == 'return; --> undefined'

def test_undefined__when_access_nonexistent_property__no_error(workspace):
    r = workspace.eval('''
    lang = {} // empty object
    console.log(`lang.xxx: ${ typeof lang.xxx }`)
    ''')

    assert r.rc == 0 # no error!
    assert r.out == 'lang.xxx: undefined'

def test_infinity__a_number_when(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#numbers
    r = workspace.eval('''
    console.log(`Infinity is also a ${ typeof Infinity }!`)

    let v = 1 / 0
    console.log(`1 / 0 --> ${v} (${ v === Infinity })`)

    v = -1 / 0
    console.log(`-1 / 0 --> ${v} (${ v === -Infinity })`)
    ''')

    assert r.out == lines('''
    Infinity is also a number!
    1 / 0 --> Infinity (true)
    -1 / 0 --> -Infinity (true)
    ''')

def test_nan__a_number_when_and_contagious(workspace):
    # `NaN` is contagious: if you provide it as an operand to any mathematical operation, the result will also be `NaN`.
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#numbers
    r = workspace.eval('''
    console.log(`NaN is also a ${ typeof NaN }!`)

    const nan = parseInt('non-numeric')
    console.log(`parseInt('non-numeric') --> ${nan}`)
    console.log(`1 + NaN --> ${ 1 + nan }`) // contagious
    ''')

    assert r.out == lines('''
    NaN is also a number!
    parseInt('non-numeric') --> NaN
    1 + NaN --> NaN
    ''')

def test_nan__never_equal_to_itself__use_isnan_instead(workspace):
    # `NaN` is the only value in JavaScript that's **not equal to itself**
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Language_overview#numbers
    r = workspace.eval('''
    console.log(`undefined === undefined --> ${ undefined === undefined }`)
    console.log(`null === null --> ${ null === null }`)
    console.log(`Infinity === Infinity --> ${ Infinity === Infinity }`)

    console.log(`NaN === NaN --> ${ NaN === NaN }`) // use Number.isNaN() instead
    console.log(`Number.isNaN('nan') --> ${ Number.isNaN('nan') }`)
    console.log(`Number.isNaN(NaN) --> ${ Number.isNaN(NaN) }`)
    ''')

    assert r.out == lines('''
    undefined === undefined --> true
    null === null --> true
    Infinity === Infinity --> true
    NaN === NaN --> false
    Number.isNaN('nan') --> false
    Number.isNaN(NaN) --> true
    ''')

def test_boolean_context__truthy_falsy(workspace):
    r = workspace.eval('''
    console.log(`0 --> ${ Boolean(0) }`)
    console.log(`-1 --> ${ Boolean(-1) }`) // non-zero
    console.log(`'' --> ${ Boolean('') }`) // empty string
    console.log(`[] --> ${ Boolean([]) }`) // counter-intuitive!
    console.log(`{} --> ${ Boolean({}) }`) // counter-intuitive!
    ''')

    assert r.out == lines('''
    0 --> false
    -1 --> true
    '' --> false
    [] --> true
    {} --> true
    ''')
