#!/usr/bin/env python3
"""rdp_builder.py — build a safe FreeRDP command or a Windows .rdp file.

Safe defaults, on purpose:
  * NLA (Network Level Authentication) is always enforced.
  * No password is ever accepted, printed, or written to a file.
    FreeRDP / Windows will prompt for it at connect time.
  * Drive and printer redirection are OFF unless you ask for them.
  * Clipboard is OFF unless you ask for it.

Examples:
    python3 rdp_builder.py --host 100.101.102.103 --user dewa
    python3 rdp_builder.py --host pc.home.lan --user dewa --fullscreen
    python3 rdp_builder.py --host 192.168.1.50 --user dewa --rdp-file home-pc.rdp
"""

import argparse
import shlex
import sys

RESOLUTIONS = {
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "1440p": (2560, 1440),
}


def parse_args(argv=None):
    ap = argparse.ArgumentParser(
        description="Build a safe xfreerdp command or .rdp file (NLA always on, no passwords stored)."
    )
    ap.add_argument("--host", required=True, help="Host or IP of YOUR machine (e.g. a Tailscale 100.x address or LAN IP)")
    ap.add_argument("--port", type=int, default=3389, help="RDP port (default 3389)")
    ap.add_argument("--user", required=True, help="Username on the target machine")
    ap.add_argument("--resolution", choices=sorted(RESOLUTIONS), default="1080p")
    ap.add_argument("--fullscreen", action="store_true", help="Start fullscreen")
    ap.add_argument("--multimon", action="store_true", help="Use all monitors")
    ap.add_argument("--clipboard", action="store_true", help="Enable clipboard sharing (off by default)")
    ap.add_argument("--share-drive", metavar="PATH", help="Share one local folder as a drive (off by default)")
    ap.add_argument("--rdp-file", metavar="FILE", help="Also write a Windows .rdp file with the same safe settings")
    return ap.parse_args(argv)


def build_command(a):
    w, h = RESOLUTIONS[a.resolution]
    parts = [
        "xfreerdp",
        f"/v:{a.host}:{a.port}",
        f"/u:{a.user}",
        "/sec:nla",            # Network Level Authentication — never negotiable
        "/cert:tofu",          # Trust on first use; warns if the cert changes
        f"/size:{w}x{h}",
    ]
    if a.fullscreen:
        parts.append("/f")
    if a.multimon:
        parts.append("/multimon")
    parts.append("+clipboard" if a.clipboard else "-clipboard")
    if a.share_drive:
        parts.append(f"/drive:shared,{a.share_drive}")
    parts.append("/sound:sys:alsa")
    parts.append("/gfx:AVC444")
    return " ".join(shlex.quote(p) if " " in p else p for p in parts)


def build_rdp_file(a):
    w, h = RESOLUTIONS[a.resolution]
    lines = [
        f"full address:s:{a.host}:{a.port}",
        f"username:s:{a.user}",
        f"desktopwidth:i:{w}",
        f"desktopheight:i:{h}",
        "screen mode id:i:2" if a.fullscreen else "screen mode id:i:1",
        "use multimon:i:1" if a.multimon else "use multimon:i:0",
        "enablecredsspsupport:i:1",   # CredSSP / NLA on the Windows side too
        "authentication level:i:2",   # Refuse to connect if auth fails
        "redirectclipboard:i:1" if a.clipboard else "redirectclipboard:i:0",
        "redirectprinters:i:0",
        "redirectdrives:i:1" if a.share_drive else "redirectdrives:i:0",
        "audiomode:i:0",
        "smart sizing:i:1",
        # Deliberately NO "password" line: .rdp files must never carry one.
    ]
    if a.share_drive:
        lines.append(f"drivestoredirect:s:{a.share_drive}")
    return "\r\n".join(lines) + "\r\n"


def main(argv=None):
    a = parse_args(argv)
    if a.port < 1 or a.port > 65535:
        print("Error: --port must be 1-65535", file=sys.stderr)
        return 2
    cmd = build_command(a)
    print("# Connect with FreeRDP (you will be prompted for the password):")
    print(cmd)
    if a.rdp_file:
        with open(a.rdp_file, "w", newline="") as f:
            f.write(build_rdp_file(a))
        print(f"# Wrote {a.rdp_file} (no password stored in it, ever)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
