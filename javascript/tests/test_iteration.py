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

