class Snapshot:
    def __init__(self, Server, gib=False):
        self.Server = Server
        g = 1
        if gib:
            g = 1024

        # generic
        self.ram = (self.Server.getRAM() / g, 2)
        self.cpu = (self.Server.getCPU(), 2)
        self.network_in = (self.Server.getNetworkIn() / g, 2)
        self.network_out = rnd(self.Server.getNetworkOut() / g, 2)
        self.uptime = self.Server.getUptime()
        self.uptime_formatted = self.Server.getUptime(True)

        # server-specific
        self.tps = self.Server.getTPS() if hasattr(self.Server, 'getTPS') else None
        self.players = self.Server.getPlayers() if hasattr(self.Server, 'getPlayers') else None

    def __str__(self):
        base = (
            f'Server: {self.Server.name}\n'
            f'Uptime: {self.uptime_formatted}\n'
            f'RAM: {self.ram}\n'
            f'CPU: {self.cpu}\n'
            f'Network (in): {self.network_in}\n'
            f'Network (out): {self.network_out}'
        )
        if self.tps is not None:
            base += f'\nTPS: {self.tps}'
        if self.players is not None:
            base += f'\nOnline players: {self.players}'

        return base