from pinlib import boot, game, oops
from pingame import brand

def main():
    g = game.Game("wpc")

    g.boot = boot.BootMode(g, {
        "name": brand.name.upper(),
        "version": brand.version,
        "date": brand.date
    })
    g.oops = oops.OopsMode(g, {
        "next_mode": g.boot
    })

    g.run()

if __name__ == "__main__":
    main()
