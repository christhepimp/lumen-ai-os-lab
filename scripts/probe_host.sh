#!/system/bin/sh
# Run as root on the emulator: sh /data/local/tmp/probe_host.sh
# Falls back to toybox/busybox tools common on Android.

out="/data/local/tmp/lumen-probe.txt"
{
  echo "=== Lumen host probe ==="
  date
  echo
  echo "--- identity ---"
  id
  uname -a
  echo
  echo "--- kernel ---"
  cat /proc/version 2>/dev/null
  cat /proc/cmdline 2>/dev/null
  echo
  echo "--- build ---"
  getprop ro.build.version.release 2>/dev/null
  getprop ro.build.version.sdk 2>/dev/null
  getprop ro.product.cpu.abi 2>/dev/null
  getprop ro.hardware 2>/dev/null
  getprop ro.kernel.qemu 2>/dev/null
  echo
  echo "--- mounts ---"
  cat /proc/mounts 2>/dev/null | head -n 40
  echo
  echo "--- init-ish ---"
  ps -A 2>/dev/null | head -n 30
  ls -l /init /system/bin/init /system/bin/app_process 2>/dev/null
  echo
  echo "--- cgroups ---"
  ls /sys/fs/cgroup 2>/dev/null
  echo
  echo "done"
} > "$out" 2>&1

echo "wrote $out"
cat "$out"
