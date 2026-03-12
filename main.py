import argparse
import time
import sys

from pypresence import Presence, exceptions

def parseArguments():
    p = argparse.ArgumentParser(description="Set Discord RPC")

    p.add_argument("--client-id", required = True, help = "Client ID")
    p.add_argument("--details", default = "", help = "Main details text (e.g. \"Playing Foo\")")
    p.add_argument("--state", default = "", help = "Secondary text")
    p.add_argument("--large-image", default = None, help = "Key of the large image asset in your app")
    p.add_argument("--large-text", default = None, help = "Hover text for the large image")
    p.add_argument("--small-image", default = None, help = "Key of the small image asset")
    p.add_argument("--small-text", default = None, help = "Hover text for the small image")
    p.add_argument("--once", action = "store_true", help = "Set presence once and exit")
    p.add_argument("--retry", type = int, default = 5, help = "Seconds to wait before reconnect attempts")

    return p.parse_args()

def buildPayload(args):
    payload = {}
    assets = {}

    if args.details: payload["details"] = args.details
    if args.state: payload["state"] = args.state
    if args.large_image: assets["large_image"] = args.large_image
    if args.large_text: assets["large_text"] = args.large_text
    if args.small_image: assets["small_image"] = args.small_image
    if args.small_text: assets["small_text"] = args.small_text

    if assets: payload["assets"] = assets

    return payload

def main():
    args = parseArguments()
    payload = buildPayload(args)
    client_id = str(args.client_id)
    rpc = Presence(client_id)
    connected = False

    while not connected:
        try:
            rpc.connect()
            connected = True
        except exceptions.InvalidPipe:
            print(f"Could not find IPC pipe. Retrying in {args.retry}s...", file = sys.stderr)
            time.sleep(args.retry)
        except Exception as e:
            print(f"Connection error: {e}. Retrying in {args.retry}s...", file = sys.stderr)
            time.sleep(args.retry)

    try:
        update_kwargs = {
            obj: payload[obj]

            for obj in ("details", "state", "start", "buttons")
            if obj in payload
        }

        update_kwargs.update(payload.get("assets", {}))

        rpc.update(**update_kwargs)
        print("Updated:", update_kwargs)

        if args.once:
            rpc.close()
            print("Ran once.")

            return

        while True:
            time.sleep(15)

    except KeyboardInterrupt:
        print("\nClearing presence...")
    except Exception as e:
        print("Error while updating presence:", e, file = sys.stderr)

    finally:
        try:
            rpc.clear()
        except Exception:
            pass

        try:
            rpc.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()