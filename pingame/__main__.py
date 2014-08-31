from pinlib import boot, game

def main():
    g = game.Game("wpc")

    g.boot = boot.Mode(g, {
        "name": "No Fear",
        "version": "0.0.0"
    })

    try:
        g.setup()
        g.run_loop()
    finally:
        del g

if __name__ == "__main__":
    main()
