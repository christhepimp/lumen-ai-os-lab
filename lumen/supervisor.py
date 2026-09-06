#!/usr/bin/env python3
"""Lumen supervisor — userspace brain that will become the OS."""

from __future__ import annotations

import argparse
import json
import os
import platform
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class Observation:
    ts: str
    host: str
    kernel: str
    load: tuple[float, float, float] | None
    pid_count: int | None
    notes: list[str] = field(default_factory=list)


@dataclass
class Decision:
    ts: str
    goal: str
    action: str
    reason: str
    applied: bool


class Lumen:
    def __init__(self, memory_path: Path, dry_run: bool = True) -> None:
        self.memory_path = memory_path
        self.dry_run = dry_run
        self.memory: list[dict[str, Any]] = []
        if memory_path.exists():
            self.memory = json.loads(memory_path.read_text())

    def observe(self) -> Observation:
        load = None
        if hasattr(os, "getloadavg"):
            try:
                load = os.getloadavg()
            except OSError:
                load = None
        pid_count = None
        proc = Path("/proc")
        if proc.exists():
            pid_count = sum(1 for p in proc.iterdir() if p.name.isdigit())
        notes = []
        if Path("/system/bin/app_process").exists():
            notes.append("android-userspace-detected")
        if Path("/proc/cmdline").exists():
            cmd = Path("/proc/cmdline").read_text(errors="ignore")
            if "goldfish" in cmd or "ranchu" in cmd or "qemu" in cmd:
                notes.append("emulator-kernel-detected")
        return Observation(
            ts=datetime.now(timezone.utc).isoformat(),
            host=platform.node(),
            kernel=platform.platform(),
            load=load,
            pid_count=pid_count,
            notes=notes,
        )

    def decide(self, obs: Observation, goal: str) -> Decision:
        # Phase 2 brain: deterministic policy. Swap this for a local model later.
        if obs.pid_count and obs.pid_count > 400:
            action = "trim-background-work"
            reason = f"pid_count={obs.pid_count} looks busy; prefer reclaim over spawn"
        elif "emulator-kernel-detected" in obs.notes:
            action = "stay-in-lab-mode"
            reason = "goldfish/ranchu host is the sandbox; do not touch real hardware"
        else:
            action = "snapshot-and-wait"
            reason = "not enough signal; observe another cycle"
        return Decision(
            ts=datetime.now(timezone.utc).isoformat(),
            goal=goal,
            action=action,
            reason=reason,
            applied=not self.dry_run,
        )

    def act(self, decision: Decision) -> None:
        record = {"decision": asdict(decision)}
        if self.dry_run:
            record["note"] = "dry-run: no syscall applied"
        else:
            # Real actuators belong here later: setprop, ctl, cgroup freeze, etc.
            record["note"] = "live mode reserved; no actuator wired yet"
        self.memory.append(record)
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.memory_path.write_text(json.dumps(self.memory, indent=2))

    def cycle(self, goal: str) -> dict[str, Any]:
        obs = self.observe()
        dec = self.decide(obs, goal)
        self.act(dec)
        bundle = {"observation": asdict(obs), "decision": asdict(dec)}
        print(json.dumps(bundle, indent=2))
        return bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Lumen AI control plane")
    parser.add_argument("--goal", default="keep the lab stable and learn the host")
    parser.add_argument("--loops", type=int, default=1)
    parser.add_argument("--sleep", type=float, default=2.0)
    parser.add_argument("--memory", default="lumen-memory.json")
    parser.add_argument("--live", action="store_true", help="disable dry-run (still no actuators)")
    parser.add_argument("--demo", action="store_true", help="one local cycle on this machine")
    args = parser.parse_args()

    brain = Lumen(Path(args.memory), dry_run=not args.live)
    loops = 1 if args.demo else args.loops
    for i in range(loops):
        brain.cycle(args.goal)
        if i + 1 < loops:
            time.sleep(args.sleep)


if __name__ == "__main__":
    main()
