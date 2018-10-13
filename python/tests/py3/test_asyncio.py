import asyncio
import pytest

def test_hello_world(workspace):
    workspace.src('main.py', r"""
    import asyncio

    async def main():
        print('Hello, ', end='')
        await asyncio.sleep(1)
        print('World!')

    # Python 3.7+
    asyncio.run(main())
    """)

    r = workspace.run('python main.py')
    assert r.out == 'Hello, World!\n'

@pytest.mark.asyncio
async def test_hello_world__pytest_asyncio(workspace):
    result = await async_task('World')
    assert result == 'Hello, World!'

async def async_task(input):
    await asyncio.sleep(1)
    return 'Hello, %s!' % input

