import asyncio
from pyppeteer import launch
import time

async def visit_page(page, url, delay=5):
    try:
        print(f"Tentativo di accedere a {url}...")
        await page.goto(url, {'waitUntil': 'load'})
        print(f"Accesso a {url} riuscito!")
        return True
    except Exception as e:
        print(f"Errore durante l'accesso a {url}: {e}")
        return False

async def admin_bot():
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'], executablePath="/usr/bin/chromium")
    page = await browser.newPage()
    
    # Effettua login come admin
    print("Tentativo di login come admin...")
    await visit_page(page, 'http://localhost:80/login')
    
    # Compila il form di login
    await page.type('input[name="username"]', 'admin')
    await page.type('input[name="password"]', 'adminpass')
    await page.click('button[type="submit"]')
    
    # Attendiamo che il login sia completato
    await asyncio.sleep(2)
    print("Login come admin completato!")

    # Loop principale di visita
    while True:
        try:
            await visit_page(page, 'http://localhost:80/admin-view')
        except Exception as e:
            print(f"Errore nel bot admin: {e}")
        await asyncio.sleep(10)

def main():
    print("Admin bot avviato! Visiterà la pagina admin-view ogni 10 secondi.")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(admin_bot())

if __name__ == "__main__":
    main() 