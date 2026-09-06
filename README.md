# Lumen AI OS Lab

**Goal:** start from a *rooted Android emulator* (Linux underneath), get a real root shell into that Linux, then *slowly* replace userspace decisions with an AI control plane until the operating system *is* the intelligence.

This is a research lab, not a finished kernel. You cannot yank Linux out in one night from inside Android. The honest path is:

1. Host = rooted Android emulator (Goldfish / ranchu Linux kernel).
2. Root = Magisk / `adb root` so we own PID 1's world.
3. Probe = dump kernel, init, services, mounts, cgroups.
4. Overlay = Lumen supervisor sits above `init` and starts making OS decisions.
5. Replace = one subsystem at a time (scheduler hints, process lifecycle, storage policy, UI intent).
6. Later = custom kernel module / guest kernel. Not day one.

## Repo map

| Path | What it is |
|------|------------|
| `docs/EMULATOR.md` | Which rooted emulators to use and how to get a `#` shell |
| `docs/ARCHITECTURE.md` | How an AI-native OS actually bootstraps on Linux |
| `lumen/supervisor.py` | First userspace brain: observe + decide + act |
| `scripts/probe_host.sh` | Run on-device after root to snapshot the Linux host |

## Fast start (host PC)

```bash
# 1. Android Studio AVD, API 30–34, *without* Google Play if you can
#    (userdebug / AOSP images allow adb root)
# 2. Root it with rootAVD + Magisk, or use Genymotion + Magisk
# 3. Confirm root
adb shell su -c id
# expect: uid=0(root)

# 4. Push probe + supervisor
adb push scripts/probe_host.sh /data/local/tmp/
adb push lumen/supervisor.py /data/local/tmp/
adb shell su -c 'sh /data/local/tmp/probe_host.sh'
python3 lumen/supervisor.py --demo
```

## What "the OS is the AI" means here

Not a chatbot wallpaper. The control plane owns:

- **Intent** — natural language / goal becomes a system job
- **Scheduling** — which process gets CPU/RAM/network *and why*
- **Lifecycle** — start, freeze, kill, restart services as policy
- **Memory of the machine** — what happened, what is safe, what is next
- **Self-repair** — failed service is a problem the brain solves

Linux stays as the *hardware + syscall layer* for a long time. That is how every serious AI-OS research project actually works (AIOS, LDOS, agentOS-on-seL4, Oxide-style agent kernels). Replacing the kernel is phase 5, not phase 1.

## Status

Phase 0 — lab repo and probe tools.
Phase 1 — rooted emulator + host snapshot.
Phase 2 — supervisor loop making *logged* decisions (no destructive replace yet).
Phase 3 — take over one userspace service (watcher / init wrapper).
Phase 4 — policy engine + local model hook.
Phase 5 — kernel module / custom guest. Optional. Dangerous.

## License

MIT. Experiment at your own risk. Do not run the supervisor as a live init replacement on a device you care about.
