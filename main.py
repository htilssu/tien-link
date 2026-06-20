import argparse
import asyncio

from cloakbrowser import launch_context_async


async def run(url: str) -> None:
    ctx = await launch_context_async(headless=True, humanize=True, viewport={"width": 1920, "height": 1080})
    try:
        page = await ctx.new_page()
        await page.goto(url, wait_until="domcontentloaded")

        safelink = page.locator("a#result[href]")
        await safelink.wait_for(state="attached", timeout=30_000)
        href = await safelink.get_attribute("href")
        print(f"clicking safelink href={href!r}", flush=True)

        await safelink.click()
        print("done", flush=True)
    except Exception as e:
        print(f"error: {e!s:.200}", flush=True)
    finally:
        await ctx.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    asyncio.run(run(args.url))


if __name__ == "__main__":
    main()
