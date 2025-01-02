import asyncio
import random
import pyautogui
from playwright.async_api import async_playwright
import time


async def simulate_bot_like_behavior(session_id):
    print(f"Session {session_id}: Starting bot-like simulation")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},  # Ensure fullscreen dimensions
        )
        page = await context.new_page()

        try:
            await page.goto("http://localhost:8000")
            print(f"Session {session_id}: Navigated to homepage")

            # Unnatural patterns: straight-line movements, rapid clicks
            for _ in range(15):
                x, y = random.choice([(500, 500), (800, 400), (1200, 600), (600, 300)])
                pyautogui.moveTo(x, y, duration=0.05)  # Extremely fast, direct movements
                pyautogui.click()
                print(f"Session {session_id}: Unnatural mouse movement to ({x}, {y})")
                await asyncio.sleep(random.uniform(0.01, 0.1))  # Short, unnatural delay

            # Excessive interactions
            await page.goto("http://localhost:8000/cart/")
            for _ in range(10):
                pyautogui.click()
                print(f"Session {session_id}: Rapid clicking detected")
                await asyncio.sleep(0.1)

        except Exception as e:
            print(f"Session {session_id}: Error - {e}")
        finally:
            await browser.close()
            print(f"Session {session_id}: Bot-like simulation complete")


async def simulate_human_like_behavior(session_id):
    print(f"Session {session_id}: Starting human-like simulation")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},  # Ensure fullscreen dimensions
        )
        page = await context.new_page()

        try:
            await page.goto("http://localhost:8000")
            print(f"Session {session_id}: Navigated to homepage")

            # Natural patterns: varied movements, realistic speed
            for _ in range(10):
                x, y = random.randint(200, 1600), random.randint(200, 800)
                pyautogui.moveTo(x, y, duration=random.uniform(0.3, 1.5))  # Slower, natural movements
                pyautogui.click()
                print(f"Session {session_id}: Natural mouse movement to ({x}, {y})")
                await asyncio.sleep(random.uniform(1.0, 2.0))  # Realistic pauses

            await page.goto("http://localhost:8000/cart/")
            await asyncio.sleep(5)

        except Exception as e:
            print(f"Session {session_id}: Error - {e}")
        finally:
            await browser.close()
            print(f"Session {session_id}: Human-like simulation complete")


async def run_sessions(total_sessions=10):
    for i in range(1, total_sessions + 1):
        if i % 2 == 0:  # Alternate between bot-like and human-like behavior
            await simulate_bot_like_behavior(session_id=f"session-{i}")
        else:
            await simulate_human_like_behavior(session_id=f"session-{i}")


if __name__ == "__main__":
    asyncio.run(run_sessions(total_sessions=3))
