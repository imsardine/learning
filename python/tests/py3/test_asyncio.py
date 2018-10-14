import asyncio
import pytest

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

def test_import_asyncio_not_needed_for_using_async_await_keywords(workspace):
    workspace.src('main.py', r"""
    async def main():
        pass

    print(type(main()))
    """)

    r = workspace.run('python main.py')
    assert r.out == "<class 'coroutine'>"
    assert r.err == "main.py:4: RuntimeWarning: coroutine 'main' was never awaited\n  print(type(main()))"

