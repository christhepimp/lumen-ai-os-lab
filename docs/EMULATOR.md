# Rooted Android emulators (2026)

You asked for an emulator that already has root so we can drop into Linux. Practical options:

## 1. Android Studio AVD + Magisk (best for kernel poking)

- Use an **AOSP / Google APIs** system image, not Google Play if you want `adb root`.
- Kernel is **Goldfish** (older) or **ranchu** (current). That *is* Linux.
- Root it with [rootAVD](https://github.com/newbit1/rootAVD) or [MagiskOnEmulator](https://github.com/shakalaca/MagiskOnEmulator).
- After a cold boot: `adb shell` then `su`. Prompt becomes `#`. `id` shows `uid=0(root)`.
- Then you are inside Linux: `/proc/version`, `/proc/cmdline`, `ps -A`, `init`.

## 2. Genymotion Desktop

- Official Magisk install path exists (Genymotion support article, Magisk 30.7 on Android 12+).
- Many images can be rooted dynamically even if they ship unrooted.
- Fast VM, good for a daily lab. Less kernel-source visibility than AOSP AVD.

## 3. Waydroid (Linux host, near-native)

- Android 13 LineageOS in a container on your Linux box.
- Not a classic emulator. Great if your PC already runs Linux and you want speed.
- Root is a container/config problem, not Magisk-on-AVD.

## 4. Bliss OS / Android-x86 in VirtualBox or QEMU

- Full Android-on-PC. You can dual-boot or VM it.
- Easier to treat as "a Linux distro that happens to speak Android".
- Good when you want to replace init without fighting Play Services.

## 5. redroid (Docker Android)

- Headless Android in a container. Good for automation and CI later.

## Recommended first lab

1. Android Studio → AVD → x86_64 → API 33 AOSP.
2. Patch ramdisk with Magisk (rootAVD).
3. Cold boot. `adb root` or `adb shell su`.
4. Run `scripts/probe_host.sh`.
5. Only then run `lumen/supervisor.py`.

## After you have `#`

```sh
uname -a
cat /proc/version
cat /proc/cmdline
getprop ro.build.version.release
ps -A | head
ls /system /vendor /data
```

That dump is the *current OS*. Lumen overlays it. It does not delete `/system` on day one.
