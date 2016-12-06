import unidata
import pathlib
import asyncio
import sys
import itertools
import aiohttp
from aiohttp import web

async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    dots = '⠉⠘⠰⢠⣀⡄⠆⠃'  # Braille patterns
    for char in itertools.cycle(dots):
        status = msg + ' ' + char + ' '
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


async def fetch():
    filename = pathlib.Path(unidata.URL).name
    spinner = asyncio.ensure_future(spin('downloading ' + filename))
    async with aiohttp.request('GET', unidata.URL) as resp:
        if resp.status != 200:
            raise aiohttp.HttpProcessingError(
                code=resp.status, message=resp.reason,
                headers=resp.headers)
        with open(filename, 'wb') as fd:
            fd.write(await resp.read())
    spinner.cancel()

def main():
    loop = asyncio.get_event_loop()
    text = loop.run_until_complete(fetch())

if __name__ == '__main__':
    main()
