import sys
import asyncio

# Logging setup
print("🚀 Starting AloneMusic Bot...")

try:
    # Import main bot module
    from AloneMusic import __main__ as bot_main
except ImportError as e:
    print("❌ Failed to import AloneMusic main module:", e)
    sys.exit(1)


async def start_bot():
    """Run the main bot entrypoint."""
    try:
        await bot_main.main()
    except AttributeError:
        # If __main__.py does not have main(), just import to trigger start
        print("ℹ️ No main() in __main__.py, running import side-effects.")
    except Exception as e:
        print("❌ Bot crashed with error:", e)


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Bot stopped manually.")
