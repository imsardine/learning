from .conftest import lines

def test_hello_world(workspace):
    workspace.src('hello_rust.rs', '''
    fn main() {
        println!("Hello, Rust!");
    }
    ''')

    workspace.run('rustc hello_rust.rs')
    assert workspace.run('./hello_rust').out == 'Hello, Rust!'

def test_carget_project(workspace):
    # cargo new <project_name>
    assert workspace.run('cargo new hello_cargo').err == lines('''
        Creating binary (application) `hello_cargo` package
    note: see more `Cargo.toml` keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
    ''')

    # src/ for source code, Cargo.toml for build and dependencies
    assert workspace.run('tree -aF -I .git hello_cargo').out == lines('''
    hello_cargo/
    ├── .gitignore
    ├── Cargo.toml
    └── src/
        └── main.rs

    2 directories, 3 files
    ''')

    workspace.chdir('hello_cargo')
    assert workspace.read_txt('Cargo.toml') == lines('''
    [package]
    name = "hello_cargo"
    version = "0.1.0"
    edition = "2024"

    [dependencies]
    ''')

    # git repo initialized
    assert workspace.exists('.git/')
    assert workspace.read_txt('.gitignore') == '/target'

    # cargo check, only check if it compiles
    workspace.run('cargo check')
    assert workspace.exists('Cargo.lock')
    assert not workspace.exists('target/debug/hello_cargo')

    # cargo build, (by default) for debug
    workspace.run('cargo clean && cargo build')
    assert workspace.exists('target/debug/hello_cargo')
    assert workspace.run('target/debug/hello_cargo').out == 'Hello, world!'

    # cargo run
    workspace.run('cargo clean')
    assert workspace.run('cargo run').out == 'Hello, world!'
    assert workspace.exists('target/debug/hello_cargo')

    # cargo build --release
    workspace.run('cargo clean && cargo build --release')
    assert workspace.exists('target/release/hello_cargo')
