from .conftest import lines

def test_hello_world(workspace):
    workspace.src('hello.ts', '''
    // Say hello to the world
    console.log("Hello TypeScript (TS)!");
    ''')

    # Compile TypeScript (.ts) into JavaScript (.js)
    r = workspace.run('tsc hello.ts')
    assert r.out == ''
    assert workspace.read_txt('hello.js', 'utf-8') == lines('''
    // Say hello to the world
    console.log("Hello TypeScript (TS)!");
    ''')

    # Run the generated JavaScript
    r = workspace.run('node hello.js')
    assert r.out == 'Hello TypeScript (TS)!'

def test_transpilation(workspace):
    workspace.src('hello.ts', '''
    class Person {
      private name: string;

      constructor(name: string) {
        this.name = name;
      }

      greet() {
        return `Hello, ${this.name}!`;
      }
    }

    console.log(new Person('World').greet());
    ''')

    # target: es5 (default)
    r = workspace.run('tsc --strict hello.ts')
    assert r.out == ''
    assert workspace.read_txt('hello.js', 'utf-8') == lines('''
    "use strict";
    var Person = /** @class */ (function () {
        function Person(name) {
            this.name = name;
        }
        Person.prototype.greet = function () {
            return "Hello, ".concat(this.name, "!");
        };
        return Person;
    }());
    console.log(new Person('World').greet());
    ''')

    # target: es6
    r = workspace.run('tsc --strict --target es6 hello.ts')
    assert r.out == ''
    assert workspace.read_txt('hello.js', 'utf-8') == lines('''
    "use strict";
    class Person {
        constructor(name) {
            this.name = name;
        }
        greet() {
            return `Hello, ${this.name}!`;
        }
    }
    console.log(new Person('World').greet());
    ''')

def test_tsconfig_project(workspace):
    workspace.src('src/hello.ts', '''
    console.log("Hello TypeScript (TS)!");
    ''')

    workspace.src('tsconfig.json', '''
    {
      "compilerOptions": {
        "strict": true,
        "outDir": "dist"
      }
    }
    ''')

    workspace.run('tsc')
    assert workspace.run('tree').out == lines('''
    .
    ├── dist
    │\xa0\xa0 └── hello.js
    ├── src
    │\xa0\xa0 └── hello.ts
    └── tsconfig.json

    3 directories, 3 files
    ''')

    assert workspace.read_txt('dist/hello.js', 'utf-8') == lines('''
    "use strict";
    console.log("Hello TypeScript (TS)!");
    ''')
