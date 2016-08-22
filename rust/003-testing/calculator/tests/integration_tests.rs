extern crate calculator; // doesn't work with binary projects?

use calculator::*;

#[test]
fn test_calcluator_division() {
    assert_eq!(2, divide(4, 2));
}

