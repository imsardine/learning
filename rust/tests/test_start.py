def test_hello_world(workspace):
    workspace.src('main.rs', '''
    fn main() {
        println!("Hello, Rust!");
    }
    ''')

    workspace.run('rustc main.rs')
    assert workspace.run('./main').out == 'Hello, Rust!'
