from pinlib import boot, game, oops
from pingame import brand
from procgame import service

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
    g.service = service.ServiceMode(g._game, 100, g.fonts["plain"], [])
    
    g.run()

if __name__ == "__main__":
    main()
