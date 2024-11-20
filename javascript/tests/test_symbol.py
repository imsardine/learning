from .conftest import lines

def test_symbol_constructor_fuction__return_unique_symbol_values(workspace):
    r = workspace.eval('''
    console.log(typeof Symbol); // function

    const s1 = Symbol();
    console.log(s1, typeof s1);

    const s2 = Symbol('foo'); // Symbol(description), for debugging
    const s3 = Symbol('foo'); // another unique symbol (value)
    console.log(s2, s3, s2 == s3); // Symbol(foo), false
    ''')

    assert r.out == lines('''
        function
        Symbol() symbol
        Symbol(foo) Symbol(foo) false
    ''')

def test_symbol_constructor_function__with_new__type_error(workspace):
    r = workspace.eval_err('''
    const s = new Symbol() // error: not a constructor?!
    ''')

    assert 'TypeError: Symbol is not a constructor' in r.err

def test_unique_symbol_from_global_registry(workspace):
    r = workspace.eval('''
    console.log(typeof Symbol.for); // function of another (constructor) function

    const foo = Symbol.for('foo'); // 'foo' as key, created an registered in global symbol registry
    const fooLocal = Symbol('foo'); // 'foo' as description, local, not registered

    console.log(foo, fooLocal, foo == fooLocal); // same representation, but different value

    const foo2 = Symbol.for('foo'); // retrieve the same value, same reference
    console.log(foo === foo2);
    ''')

    assert r.out == lines('''
        function
        Symbol(foo) Symbol(foo) false
        true
    ''')

def test_get_key_of_registered_symbol(workspace):
    r = workspace.eval('''
    console.log(Symbol.keyFor(Symbol.for('foo'))); // foo, registered
    console.log(Symbol.keyFor(Symbol('foo'))); // undefined (undocumented), regular (not registered), no key
    ''')

    assert r.out == lines(['foo', 'undefined'])

def test_symbol_as_property_key(workspace):
    r = workspace.eval('''
    const color = Symbol(); // for data
    const brief = Symbol(); // for method

    const apple = {
      name: 'Apple',
      [color]: 'red', // [] is required (computed property name), or considered as 'color'
      [brief]() { return `${this.name} (${ this[color]})`}
    };

    console.log(apple[brief]());
    ''')

    assert r.out == 'Apple (red)'
