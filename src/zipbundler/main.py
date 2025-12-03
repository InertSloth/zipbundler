import argparse
import sys


def main(args: list[str] | None = None) -> int:
    """Main entry point for the zipbundler CLI."""
    parser = argparse.ArgumentParser(
        description="Bundle your packages into a runnable, importable zip"
    )
    parser.parse_args(args)
    sys.stdout.write("Hello world\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
