import pytest
from .conftest import lines

def test_literal_and_constructor(workspace):
    r = workspace.eval(r'''

    // literal, compiled when the script is loaded (more performant)
    const re1 = /\w*day\b/g; // as: /regex/flags, more succinct

    // constructor, compiled at runtime
    const re2 = RegExp('\\w*day\\b', 'g'); // escape at string literal level

    // equivalent
    console.log(re1.source, re1.global);
    console.log(re2.source, re2.global);
    ''')

    assert r.out == lines(r'''
        \w*day\b true
        \w*day\b true
    ''')

def test_regexp_exec__flag_g_for_multiple_matches(workspace):
    r = workspace.eval(r'''
    //     index: 0123456789012345
    const text = 'today is my day';
    //                 ^ (5)     ^ (15)

    let re = /\w*day\b/g; // w/ flag 'g', that really matters
    console.log(re.exec(text), re.lastIndex); // array of information, of the 1st match 'today'
    console.log(re.exec(text), re.lastIndex); // 2nd match 'day'
    console.log(re.exec(text), re.lastIndex); // null, no more match
    console.log(re.exec(text), re.lastIndex); // restart! (lastIndex was reset to 0)

    re = /\w*day\b/; // w/o flag 'g'
    console.log(re.exec(text), re.lastIndex); // lastIndex remain unchanged! (0)
    console.log(re.exec(text), re.lastIndex);
    ''')

    assert r.out == lines('''
        [ 'today', index: 0, input: 'today is my day', groups: undefined ] 5
        [ 'day', index: 12, input: 'today is my day', groups: undefined ] 15
        null 0
        [ 'today', index: 0, input: 'today is my day', groups: undefined ] 5
        [ 'today', index: 0, input: 'today is my day', groups: undefined ] 0
        [ 'today', index: 0, input: 'today is my day', groups: undefined ] 0
    ''')

def test_string_match__structure_of_returned_array_depends_flag_g(workspace):
    r = workspace.eval(r'''
    const text = 'today is my day';

    let re = /\w*day\b/g;
    console.log(text.match(re)); // array of all matches
    console.log(''.match(re)); // null, for no match

    re = /\w*day\b/; // w/o flag 'g'
    console.log(text.match(re)); // array of information, of the 1st match
    console.log(text.match(re)); // still the 1st match
    ''')

    assert r.out == lines('''
        [ 'today', 'day' ]
        null
        [ 'today', index: 0, input: 'today is my day', groups: undefined ]
        [ 'today', index: 0, input: 'today is my day', groups: undefined ]
    ''')

def test_string_matchall(workspace):
    r = workspace.eval(r'''
    const text = 'today is my day';
    const re = /\w*day\b/g; // flag 'g' is required

    for (let match of text.matchAll(re)) { // iterator
      console.log(match, re.lastIndex); // but lastIndex remain unchanged!
    }
    ''')

    assert r.out == lines('''
        [ 'today', index: 0, input: 'today is my day', groups: undefined ] 0
        [ 'day', index: 12, input: 'today is my day', groups: undefined ] 0
    ''')

def test_string_matchall__without_global__type_error(workspace):
    r = workspace.eval_err(r'''
    const re = /\w*day\b/;
    ''.matchAll(re);
    ''')

    assert 'TypeError: String.prototype.matchAll called with a non-global RegExp argument' in r.err

def test_named_groups__exec__with_submatch_info(workspace):
    r = workspace.eval(r'''
    // groups:  01              2                 3
    const re = /v(?<major>\d+)\.(?<minor>\d+)(?:\.(?<update>\d+))?/g;
    //                                        ^ non-capturing
    msg = 'migration from v0.9 to v1.0.2';

    let match = re.exec(msg);
    console.log(match.length, match[0], match[1], match[2], match[3]); // array of match, submatches
    console.log(match.groups.major, match.groups.minor, match.groups.update); // submatches, via name

    match = re.exec(msg); // next match
    console.log(match.length, match[0], match[1], match[2], match[3]);
    console.log(match.groups.major, match.groups.minor, match.groups.update);
    ''')

    assert r.out == lines('''
        4 v0.9 0 9 undefined
        0 9 undefined
        4 v1.0.2 1 0 2
        1 0 2
    ''')

def test_named_groups__match__no_submatch_info(workspace):
    r = workspace.eval(r'''
    const re = /v(?<major>\d+)\.(?<minor>\d+)(?:\.(?<update>\d+))?/g;
    msg = 'migration from v0.9 to v1.0.1';
    console.log(msg.match(re));
    ''')

    assert r.out == "[ 'v0.9', 'v1.0.1' ]"
