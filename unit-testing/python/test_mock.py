import unittest2 as unittest
from mock import DEFAULT, Mock, MagicMock, patch, create_autospec, call
import sys, time, re

THIS_MODULE = sys.modules[__name__]

class ClassUnderTest(object):

    def __init__(self):
        self._collaborator = Collaborator()

    def do_something(self, foo, bar, *args, **kwargs):
        self._helper(foo, bar, *args, **kwargs)
        self._collaborator.do_someting_complicated(
            self._helper(foo, bar), *args, **kwargs)

    def _helper(self, foo, bar):
        raise RuntimeError('ClassUnderTest._helper should be mocked.')
        return arg1 * arg2

class Collaborator(object):

    def __init__(self, data):
        raise RuntimeError('Collaborator.__init__ should be mocked.')
        self._data = data

    def do_something_complicated(self, foobar, *args, **kwargs):
        self._helper(foobar, *args, **kwargs)

    def _helper(self, foobar, *args, **kwargs):
        raise RuntimeError('Collaborator._helper should be mocked.')

CollaboratorOrig = Collaborator # for type testing, after patching

class CollaboratorForTest(Collaborator):

    _data = None # as a placeholder, and will be configured later.

class MockTest(unittest.TestCase):

    def test_mock(self):
        mock = Mock()
        self.assertTrue(callable(mock))

        self.assertIsInstance(mock.this_attr, Mock) # create attributes and new mocks when accessing them
        self.assertTrue(hasattr(mock, 'that_attr')) # also true for hasattr test
        self.assertIsInstance(mock.that_attr, Mock)
        self.assertIs(mock.this_attr, mock.this_attr) # always return the same mock
        self.assertIsNot(mock.this_attr, mock.that_attr)

    def test_magic_mock(self): # behave in the same way
        mock = MagicMock()
        self.assertTrue(callable(mock))

        self.assertIsInstance(mock.this_attr, MagicMock)
        self.assertIsInstance(mock.that_attr, MagicMock)
        self.assertIs(mock.this_attr, mock.this_attr)
        self.assertIsNot(mock.this_attr, mock.that_attr)

    def test_magic_attributes(self): # for both Mock and MagicMock
        mock, magic = Mock(), MagicMock()

        self.assertTrue(hasattr(mock, '__str__'))
        self.assertNotIsInstance(mock.__str__, (Mock, MagicMock)) # not patched
        self.assertFalse(hasattr(mock, '__xyz__'))
        with self.assertRaises(AttributeError):
            mock.__xyz__

        self.assertTrue(hasattr(magic, '__str__'))
        self.assertIsInstance(magic.__str__, MagicMock) # pre-created
        self.assertFalse(hasattr(magic, '__xyz__'))
        with self.assertRaises(AttributeError): # only magic methods are pre-created
            magic.__xyz__

class MockConfigTest(unittest.TestCase):

    def test_return_value(self):
        mock = Mock(return_value=3)
        self.assertEqual(mock('foo'), 3) # regardless of the arguments
        self.assertEqual(mock('bar'), 3)

    def test_side_effect(self):
        mock = Mock(side_effect=KeyError('foo')) # exception instance
        self.assertRaises(KeyError, mock)
        mock = Mock(side_effect=KeyError) # exception class
        self.assertRaises(KeyError, mock)

        mock = Mock(side_effect=('foo', KeyError('bar'))) # consecutive return values
        self.assertEqual(mock(), 'foo')
        self.assertRaises(KeyError, mock)
        self.assertRaises(StopIteration, mock) # out of values

    def test_side_effect_function(self):
        def side_effect(x, y):
            mapping = {
                (0, 0): DEFAULT,
                (1, 2): 3,
                (3, 4): 7,
            }

            if (x, y) in mapping:
                return mapping[(x, y)]
            else:
                raise RuntimeError()

        fun = Mock(side_effect=side_effect)
        self.assertEqual(fun(1, 2), 3)
        self.assertEqual(fun(3, 4), 7)
        with self.assertRaises(RuntimeError):
            fun(1, 4)

        self.assertIsInstance(fun(0, 0), Mock) # respect return_value, which is DEFAULT
        self.assertIs(fun(0, 0), fun(0, 0))

        fun.return_value = 99 # override the DEFAULT
        self.assertEqual(fun(0, 0), 99)
        self.assertEqual(fun(1, 2), 3) # side_effect wins return_value

    def test_side_effect_wins_return_value(self):
        mock = Mock(side_effect=('foo',), return_value='bar')
        self.assertEqual(mock(), 'foo') # side_effect wins
        self.assertRaises(StopIteration, mock)
        mock.side_effect = None # side_effect should be disabled explicitly
        self.assertEqual(mock(), 'bar')

    def test_configure_mock(self): pass # TODO

class SpecTest(unittest.TestCase):

    def test_spec(self):
        # returns an instance, instead of a class
        obj = Mock(spec=Collaborator)
        self.assertIsInstance(obj, Collaborator) # pass isinstance tests
        self.assertIs(obj.__class__, Collaborator) 

        self.assertTrue(hasattr(obj, 'do_something_complicated'))
        self.assertTrue(hasattr(obj, '_helper'))
        self.assertFalse(hasattr(obj, '_data')) # not yet initialized

        with self.assertRaises(AttributeError):
            obj.xyz # limited get
        obj.xyz = None  # unlimited set

        obj.do_something_complicated.return_value = 3
        self.assertEqual(obj.do_something_complicated(), 3) # do not check call signature

    def test_spec_set(self):
        obj = Mock(spec_set=Collaborator) # stricter variant
        #obj = Mock(spec=Collaborator, spec_set=True) # doesn't work
        self.assertFalse(hasattr(obj, 'spec_set')) # cannot be changed later
        self.assertTrue(hasattr(obj, 'side_effect'))
        self.assertIsInstance(obj, Collaborator)
        self.assertIs(obj.__class__, Collaborator) 

        self.assertTrue(hasattr(obj, 'do_something_complicated'))
        self.assertTrue(hasattr(obj, '_helper'))
        self.assertFalse(hasattr(obj, '_data'))

        with self.assertRaises(AttributeError):
            obj.xyz # limited get
        with self.assertRaises(AttributeError):
            obj.xyz = None # limited set

    def test_spec_instance_attributes(self):
        obj = Mock(spec_set=CollaboratorForTest)
        self.assertIsInstance(obj, Collaborator)
        self.assertIs(obj.__class__, CollaboratorForTest) 

        self.assertTrue(hasattr(obj, 'do_something_complicated'))
        self.assertTrue(hasattr(obj, '_helper'))
        self.assertTrue(hasattr(obj, '_data')) # because of CollaboratorTest._data

        with self.assertRaises(AttributeError):
            obj.xyz # limited get
        with self.assertRaises(AttributeError):
            obj.xyz = None # limited set

        # XXXForTest only declares attributes, and they can be configured later.
        obj._data = create_autospec(str)
        obj._data.upper.return_value = 'DATA'
        self.assertEqual(obj._data.upper(), 'DATA')

    def test_autospec(self):
        # Mock(autospec=Collaborator) or Mock(spec=Collaborator, autospec=True) doesn't work
        obj = create_autospec(Collaborator, spec_set=True)
        self.assertIsInstance(obj, Collaborator) # pass isinstance tests
        self.assertIs(obj.__class__, Collaborator) 

        self.assertTrue(hasattr(obj, 'do_something_complicated'))
        self.assertTrue(hasattr(obj, '_helper'))
        self.assertFalse(hasattr(obj, '_data')) # not yet initialized

        with self.assertRaises(AttributeError):
            obj.xyz # limited get
        with self.assertRaises(AttributeError):
            obj.xyz = None # limited set

        with self.assertRaises(TypeError): # check call signature as well
            obj.do_something_complicated()

    def test_mock_add_spec(self): pass # TODO

class PatchingTest(unittest.TestCase): # TODO patch(), patch_xxx()

    @patch.object(THIS_MODULE, 'Collaborator', spec_set=True)
    def test_mocking_classes(self, MockCollaborator):
        obj = Collaborator('data')
        self.assertIs(obj, MockCollaborator.return_value) # instance = return value
        self.assertIsInstance(obj, CollaboratorOrig)

        self.assertTrue(hasattr(obj, 'do_something_complicated'))
        self.assertTrue(hasattr(obj, '_helper'))
        self.assertFalse(hasattr(obj, '_data'))

        with self.assertRaises(AttributeError):
            obj.xyz # limited get
        with self.assertRaises(AttributeError):
            obj.xyz = None # limited set

    @patch.object(THIS_MODULE, 'Collaborator', spec_set=True)
    @patch.object(THIS_MODULE, 'CollaboratorForTest', spec_set=True)
    def test_nested(self, MockInner, MockOuter): # inner to outer, bottom-up
        self.assertIs(MockInner, CollaboratorForTest)
        self.assertIs(MockOuter, Collaborator)

    def test_partial_mocking(self): pass # TODO

class CallAssertionTest(unittest.TestCase):

    def setUp(self):
        self.obj = create_autospec(CollaboratorForTest, spec_set=True)

    def test_called(self):
        fun = self.obj.do_something_complicated
        self.assertFalse(fun.called)
        fun('foo')
        self.assertTrue(fun.called)

    def test_reset(self): # reset records, but configuration is retained
        fun = self.obj.do_something_complicated
        fun.return_value = 3
        self.assertEqual(fun('data'), 3)
        self.assertTrue(fun.called)
        fun.reset_mock()
        self.assertFalse(fun.called)
        self.assertEqual(fun('data'), 3)

    def test_called_and_args(self): # last called with
        fun = self.obj.do_something_complicated
        self.assertIsNone(fun.call_args)
        self.assertEqual(fun.call_args_list, [])

        fun('foo')
        fun.assert_called_with('foo')
        self.assertEqual(fun.call_args, (('foo',),))
        self.assertEqual(fun.call_args, call('foo')) # call_args is actually a call object
        self.assertEqual(fun.call_args_list, [call('foo')])

        with self.assertRaisesRegexp(AssertionError, re.escape(
                '''Expected call: do_something_complicated(foobar='foo')\n'''
                '''Actual call: do_something_complicated('foo')''')):
            fun.assert_called_with(foobar='foo') # equivalent, but not equal

        fun('foo', 'bar', extra='foobar')
        fun.assert_called_with('foo', 'bar', extra='foobar') # most recent
        self.assertEqual(fun.call_args, (('foo', 'bar'), {'extra': 'foobar'}))
        self.assertEqual(fun.call_args, call('foo', 'bar', extra='foobar')) # call() is more intuitive
        self.assertEqual(fun.call_args_list, [call('foo'), call('foo', 'bar', extra='foobar')])

        with self.assertRaisesRegexp(AssertionError, re.escape(
                '''Expected call: do_something_complicated('foo')\n'''
                '''Actual call: do_something_complicated('foo', 'bar', extra='foobar')''')):
            fun.assert_called_with('foo') # not 'ever' called with -> assert_any_call

    def test_called_once_with(self): # accumulated
        fun = self.obj.do_something_complicated
        fun('foo')
        fun.assert_called_once_with('foo')

        fun('bar')
        with self.assertRaisesRegexp(AssertionError, re.escape(
                '''Expected to be called once. Called 2 times.''')):
            fun.assert_called_once_with('bar') # called twice, regardless of what arguments are
        self.assertEqual(fun.call_count, 2)

        fun('foobar')
        with self.assertRaisesRegexp(AssertionError, re.escape(
                '''Expected to be called once. Called 3 times.''')):
            fun.assert_called_once_with('foobar')
        self.assertEqual(fun.call_count, 3)

    def test_any_call(self): # ever called with
        fun = self.obj.do_something_complicated
        fun('foo')
        fun.assert_any_call('foo')

        fun('bar')
        fun.assert_any_call('bar') # most recently
        fun.assert_any_call('foo') # ever called

        with self.assertRaisesRegexp(AssertionError, re.escape(
                '''do_something_complicated('foobar') call not found''')):
            fun.assert_any_call('foobar')

    def test_has_calls(self):
        fun = self.obj.do_something_complicated
        fun(1); fun(2); fun(2); fun(3); fun(4); fun(5); fun(6); fun(7)

        # any_order=False: find the consecutive pattern
        fun.assert_has_calls([call(2), call(3), call(4)])

        with self.assertRaisesRegexp(AssertionError, re.escape(
                '''Calls not found.\n'''
                '''Expected: [call(2), call(4), call(6)]\n'''
                '''Actual: [call(1), call(2), call(2), call(3), call(4), call(5), call(6), call(7)]''')):
            fun.assert_has_calls([call(2), call(4), call(6)])

        # any_order=True: ever called, regardless of order and times
        fun.assert_has_calls([call(4), call(2), call(6)], any_order=True)

        with self.assertRaisesRegexp(AssertionError, re.escape(
                '''(call(0),) not all found in call list''')):
            fun.assert_has_calls([call(4), call(0), call(6)], any_order=True)

    def test_calls_as_tuples(self): pass # TODO

    def test_mock_method_calls(self):
        mock = Mock()
        mock()
        mock.method().attribute.method()
        mock.attribute.method()

        # mock_calls: inclusive, recursive; split by '()', good for callable mocks.
        self.assertEqual(mock.mock_calls, [
            call(),
            call.method(),
            call.method().attribute.method(),
            call.attribute.method()])

        # method_calls: exclusive, recursive; terminated by '()', good for non-callable mocks.
        self.assertEqual(mock.method_calls, [call.method(), call.attribute.method()])

class NonCallableMockTest(unittest.TestCase): pass # TODO and NonCallableMagicMock

class PropertyMockTest(unittest.TestCase): pass # TODO

if __name__ == '__main__':
    unittest.main()

