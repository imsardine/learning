import asyncio
import pytest
from textwrap import dedent

def test_hello_world(workspace):
    workspace.src('main.py', r"""
    import asyncio

    async def do_something_else():
        print('...', end='')
        await asyncio.sleep(1)
        print('!', end='')

    async def say_hello_async(who):
        print('Hello, ', end='')
        await asyncio.sleep(1)
        print(who, end='')

    async def main():
        await asyncio.gather(say_hello_async('World'), do_something_else())

    asyncio.run(main())
    """)

    r = workspace.run('python main.py')
    assert r.out == 'Hello, ...World!'

def test_import_asyncio_not_needed_for_using_async_await_keywords(workspace):
    workspace.src('main.py', r"""
    async def main():
        pass

    print(type(main()))
    """)

    r = workspace.run('python main.py')
    assert r.out == "<class 'coroutine'>"
    assert r.err == "main.py:4: RuntimeWarning: coroutine 'main' was never awaited\n  print(type(main()))"

@pytest.mark.asyncio
async def test_hello_world__pytest_asyncio(capsys):
    async def do_something_else():
        print('...', end='')
        await asyncio.sleep(1)
        print('!', end='')

    async def say_hello_async(who):
        print('Hello, ', end='')
        await asyncio.sleep(1)
        print(who, end='')

    await asyncio.gather(say_hello_async('World'), do_something_else())

    out, _ = capsys.readouterr()
    assert out == 'Hello, ...World!'

@pytest.mark.asyncio
async def test_await_result__return_value():
    async def do_something():
        await asyncio.sleep(1)
        return 'return value'

    result = await do_something()
    assert result == 'return value'

@pytest.mark.asyncio
async def test_await_result__reraise_exception():
    msg = 'error in coroutine'
    async def do_something():
        await asyncio.sleep(1)
        raise RuntimeError(msg)

    with pytest.raises(RuntimeError) as excinfo:
        result = await do_something()
    assert str(excinfo.value) == msg

@pytest.mark.asyncio
async def test_create_task__scheduled_but_not_run_immediately(capsys):
    async def do_something(job):
        print('run job (%s)' % job)
        await asyncio.sleep(1)
        return 'result (%s)' % job

    task = asyncio.create_task(do_something('scheduled'))
    result = await do_something('immediate')

    # await runs before scheduled tasks
    assert result == 'result (immediate)'
    assert capsys.readouterr().out == dedent("""\
        run job (immediate)
        run job (scheduled)
        """)

    with pytest.raises(asyncio.InvalidStateError):
        task.result()

    assert await task == 'result (scheduled)'
