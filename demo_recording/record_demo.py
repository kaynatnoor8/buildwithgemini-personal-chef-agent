import asyncio
import os
import glob
from playwright.async_api import async_playwright

FRONTEND_URL = "https://personal-chef-frontend-309478268709.us-east1.run.app"
OUTPUT_DIR = "/config/Desktop/BuildWithGemini/demo_recording/raw_video"
FINAL_VIDEO = "/config/Desktop/BuildWithGemini/demo_recording/personal_chef_agent_demo.mp4"

async def record():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=OUTPUT_DIR,
            record_video_size={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        print("Navigating to frontend...")
        await page.goto(FRONTEND_URL, wait_until="networkidle")
        await asyncio.sleep(2)

        # Enhance presentation if needed (render markdown images nicely if raw markdown text is present)
        await page.evaluate("""() => {
            const style = document.createElement('style');
            style.innerHTML = `
                header { background: #1b5e20 !important; font-size: 1.25rem; letter-spacing: 0.5px; }
                .chat-img-preview { max-width: 100%; border-radius: 12px; margin-top: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: block; }
            `;
            document.head.appendChild(style);
            document.querySelector('header').textContent = '🍳 Chef Gemini — Personal Chef & Meal Architect';

            // Observer to parse markdown image tags into visual <img> elements
            const observer = new MutationObserver(() => {
                document.querySelectorAll('.bubble').forEach(b => {
                    if (b.dataset.parsed) return;
                    if (b.textContent.includes('![') && b.textContent.includes('](http')) {
                        const match = b.textContent.match(/!\\[([^\\]]*)\\]\\((https?:\\/\\/[^\\)]+)\\)/);
                        if (match) {
                            const img = document.createElement('img');
                            img.src = match[2];
                            img.alt = match[1];
                            img.className = 'chat-img-preview';
                            b.appendChild(img);
                            b.dataset.parsed = 'true';
                        }
                    }
                });
            });
            observer.observe(document.getElementById('log'), { childList: true, subtree: true });
        }""")

        await asyncio.sleep(1)

        # Prompt 1: What the app does best (interactive culinary consultation & recipe tailoring)
        prompt1 = "I want to cook dinner tonight. I have chicken breast, garlic, and lemons. What can I make?"
        print("Typing Prompt 1...")
        await page.click("#input")
        for char in prompt1:
            await page.keyboard.press(char)
            await asyncio.sleep(0.03)

        await asyncio.sleep(0.8)
        print("Submitting Prompt 1...")
        await page.click("button")

        # Wait for reply
        print("Waiting for Chef Gemini response to Prompt 1...")
        await page.wait_for_function("""() => {
            const bubbles = document.querySelectorAll('.msg.agent .bubble');
            return bubbles.length >= 1 && bubbles[0].textContent !== '…' && bubbles[0].textContent.length > 50;
        }""", timeout=60000)

        # Let user read the recipe
        await asyncio.sleep(6)

        # Prompt 2: Rich database lookup + image generation
        prompt2 = "Look up our Mediterranean recipes in the database and generate a realistic image of the Tuscan Garlic Herb Salmon."
        print("Typing Prompt 2...")
        await page.click("#input")
        for char in prompt2:
            await page.keyboard.press(char)
            await asyncio.sleep(0.03)

        await asyncio.sleep(0.8)
        print("Submitting Prompt 2...")
        await page.click("button")

        # Wait for reply to Prompt 2 (including tool execution and image generation)
        print("Waiting for Chef Gemini response to Prompt 2...")
        await page.wait_for_function("""() => {
            const bubbles = document.querySelectorAll('.msg.agent .bubble');
            return bubbles.length >= 2 && bubbles[1].textContent !== '…' && bubbles[1].textContent.length > 50;
        }""", timeout=90000)

        # Wait for image to load in DOM
        await page.wait_for_selector("img.chat-img-preview", timeout=15000)
        print("Image preview loaded!")

        # Scroll to view image
        await page.evaluate("""() => {
            const log = document.getElementById('log');
            log.scrollTop = log.scrollHeight;
        }""")

        await asyncio.sleep(7)

        print("Closing context and saving video...")
        await context.close()
        await browser.close()

    # Find the recorded video
    video_files = glob.glob(f"{OUTPUT_DIR}/*.webm")
    if video_files:
        raw_webm = video_files[0]
        print(f"Recorded raw video: {raw_webm}")
        # Transcode to MP4 with ffmpeg for universal compatibility
        cmd = f'ffmpeg -y -i "{raw_webm}" -c:v libx264 -pix_fmt yuv420p -r 30 "{FINAL_VIDEO}"'
        print(f"Running: {cmd}")
        proc = await asyncio.create_subprocess_shell(cmd)
        await proc.communicate()
        print(f"Demo video saved to: {FINAL_VIDEO}")
    else:
        print("No video file generated!")

if __name__ == "__main__":
    asyncio.run(record())
