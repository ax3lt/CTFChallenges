import asyncio
from sys import stdout
from pyppeteer import launch

async def visit_page(page, url, delay=5):
    while True:
        try:
            print(f"Tentativo di accedere a {url}...", file=stdout)
            await page.goto(url, {'waitUntil': 'load'})
            print(f"Accesso a {url} riuscito!")
            return
        except Exception as e:
            print(f"Errore durante l'accesso a {url}: {e}")
            print(f"Riprovo tra {delay} secondi...")
            await asyncio.sleep(delay)

async def main():
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'], executablePath="/usr/bin/chromium")

    page = await browser.newPage()

    await visit_page(page, 'http://localhost:80/set-admin')
    await asyncio.sleep(5)

    while True:
        print("Visito la pagina come admin...")
        await visit_page(page, 'http://localhost:80/profile')
        await asyncio.sleep(10)

asyncio.run(main())
