import asyncio
import random
import pyautogui
from playwright.async_api import async_playwright

async def simulate_visible_mouse_behavior(session_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},  # Ensure fullscreen dimensions
            device_scale_factor=1,
        )
        page = await context.new_page()
        print(f"Session {session_id}: Simulation started")

        try:
            # Open the homepage
            await page.goto("http://localhost:8000")  # Replace with your app URL
            print(f"Session {session_id}: Navigated to homepage")

            # Move the mouse on screen using pyautogui
            for _ in range(20):
                x, y = random.randint(0, 1920), random.randint(0, 1080)
                pyautogui.moveTo(x, y, duration=0.2)  # Actual mouse movement
                pyautogui.click()
                print(f"Session {session_id}: Mouse moved to ({x}, {y})")
                await asyncio.sleep(0.5)  # Simulate a delay

            # Interact with UI elements
            add_to_cart_selector = "text=Add to Cart"  # Update with your actual selector
            if await page.query_selector(add_to_cart_selector):
                await page.click(add_to_cart_selector)
                print(f"Session {session_id}: Clicked 'Add to Cart'")

            await page.goto("http://localhost:8000/cart/")
            print(f"Session {session_id}: Navigated to Cart page")
            await asyncio.sleep(5)  # Allow UI to process

        except Exception as e:
            print(f"Session {session_id}: Error occurred - {e}")
        finally:
            await browser.close()
            print(f"Session {session_id}: Simulation complete")

async def simulate_multiple_sessions(num_sessions=5):
    tasks = [simulate_visible_mouse_behavior(session_id) for session_id in range(1, num_sessions + 1)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(simulate_multiple_sessions())
