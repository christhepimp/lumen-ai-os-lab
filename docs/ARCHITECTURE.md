# Architecture — replace Linux slowly, do not suicide the box

## Why we keep Linux at first

Android *is* Linux plus a userspace (Bionic, Zygote, Binder, init rc).
If you delete the kernel from inside the emulator, the VM dies and the experiment ends.
Every serious AI-OS effort keeps a kernel and changes *policy*:

- AIOS / MemGPT: LLM as the *kernel process of intent*, still on a host OS.
- LDOS: learned policies for scheduling and memory, still Linux-shaped.
- agentOS: seL4 microkernel + guests; Linux is a *guest*, not deleted on day one.
- Oxide-style agent kernels: agents are first-class, hardware still needs a kernel.

Lumen follows the same honesty.

```
 +--------------------------------------------+
 |  Lumen Control Plane  (the "OS is the AI") |
 |  goals, memory, policy, self-heal          |
 +--------------------+-----------------------+
                      | observe / decide / act
 +--------------------v-----------------------+
 |  Android userspace  init, zygote, services |
 +--------------------------------------------+
 |  Linux kernel       goldfish / ranchu      |
 +--------------------------------------------+
 |  Emulator / QEMU / VirtualBox / KVM        |
 +--------------------------------------------+
```

## Replacement order (do not skip)

1. **Observe** — probe_host.sh, /proc, logcat, dumpsys.
2. **Advise** — supervisor logs decisions, does not apply them.
3. **Act on safe surfaces** — nice/ionice, stop unused apps, write policy files.
4. **Wrap init** — a userspace supervisor that *starts* services instead of stock rc.
5. **Swap one daemon** — e.g. a Lumen watcher instead of a stock healthd-like loop.
6. **Kernel policy** — sched_ext / sysctl / cgroups / a tiny module.
7. **New kernel or microkernel guest** — only after 1–6 actually work.

## What the AI owns

- Job graph: user goal → system tasks
- Resource votes: CPU, RAM, I/O, radio
- Trust: which binary may run as root
- Narrative memory: last failures and why
- Interface: language in, machine out

## What Linux still owns

- Syscalls, drivers, MMU, interrupts, filesystems
- Binder and ashmem until we have replacements
- The emulator device model

## Safety

The supervisor defaults to **dry-run**. Destructive replace is an explicit flag.
Never point this at a phone you need. Emulator only.
