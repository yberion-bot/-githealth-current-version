class InfinityProtocolController:
    def __init__(self, max_cycles: int = 3):
        self.active = False
        self.cycle_count = 0
        self.max_cycles = max_cycles
    def activate(self):
        self.active = True
        self.cycle_count = 0
        return {"active": True, "reason":"manual_or_trigger"}
    def tick(self) -> dict:
        if not self.active:
            return {"active": False, "deactivate": False}
        self.cycle_count += 1
        if self.cycle_count >= self.max_cycles:
            self.active = False
            return {"active": False, "deactivate": True, "reason":"max_cycles_reached"}
        return {"active": True, "deactivate": False, "cycle_count": self.cycle_count}
    def force_deactivate(self):
        self.active = False
        self.cycle_count = 0
        return {"active": False, "reason":"forced"}
