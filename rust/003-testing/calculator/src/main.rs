fn main() {
    println!("4 / 2 = {}", divide(4, 2));
}

pub fn divide(a: i32, b: i32) -> i32 {
    return divide_impl(a, b);
}

fn divide_impl(a: i32, b: i32) -> i32 {
    return a / b;
}

#[test]
fn test_devide() {
    assert_eq!(2, divide_impl(4, 2));
}

#[test]
#[should_panic(expected = "attempted to divide by zero")]
fn test_divide_zero() {
    divide_impl(4, 0);
}

#[cfg(test)]
mod tests {
    // use super::*; // glob import doesn't include private items
    use super::divide_impl; // or "unresolved name `divide_impl`" will be raised

    #[test]
    fn test_devide_in_tests_module() {
        assert_eq!(2, divide_impl(4, 2));
    }
}

