# FreeRDP toolkit

Small, safe tools and notes for connecting to **your own** machines with
[FreeRDP](https://github.com/FreeRDP/FreeRDP) — the free, open-source
Remote Desktop Protocol client (Apache 2.0, by the FreeRDP project).

> This repo is **not** the FreeRDP project and is not affiliated with it.
> It is a personal toolkit *around* the client: a connection builder with
> secure defaults, and a checklist for not getting your RDP hacked.
> It previously held a GitHub Actions "free RDP" workflow; that was
> removed deliberately — see the checklist for why.

## What's here

| File | What it does |
| --- | --- |
| `rdp_builder.py` | Builds a ready-to-paste `xfreerdp` command, or a Windows `.rdp` file, with safe defaults |
| `secure-rdp-checklist.md` | The five rules for exposing RDP safely (VPN-only, NLA on, lockout, ...) |
| `example.rdp` | A generated sample profile — Tailscale address, NLA on, no password stored |

## Quick start

Install FreeRDP first (`xfreerdp`): Debian/Ubuntu `sudo apt install freerdp2-x11`,
macOS `brew install freerdp`, or see the
[FreeRDP project](https://github.com/FreeRDP/FreeRDP).

```bash
# Build a command for your own PC, reached over Tailscale
python3 rdp_builder.py --host 100.101.102.103 --user dewa

# -> xfreerdp /v:100.101.102.103:3389 /u:dewa /sec:nla /cert:tofu \
#      /size:1920x1080 -clipboard /sound:sys:alsa /gfx:AVC444
```

```bash
# Or write a Windows-style profile you can double-click / reuse
python3 rdp_builder.py --host pc.home.lan --user dewa --fullscreen \
    --rdp-file home-pc.rdp
```

Options: `--port`, `--resolution 720p|1080p|1440p`, `--fullscreen`,
`--multimon`, `--clipboard`, `--share-drive PATH`.

## Safe defaults, on purpose

- **NLA is always on** (`/sec:nla`, and `enablecredsspsupport` in .rdp
  files). There is no flag to turn it off.
- **No passwords, ever.** The builder never accepts, prints, or writes a
  password. FreeRDP prompts at connect time; your password manager holds
  the secret, not a text file.
- **Redirection off by default.** Clipboard, drives and printers stay off
  unless you explicitly ask for one folder or the clipboard.

## Connect the safe way

1. Put the target machine on a VPN (Tailscale/WireGuard) — do **not**
   forward port 3389 on your router.
2. Connect to its VPN address with the command the builder prints.
3. Run through [secure-rdp-checklist.md](secure-rdp-checklist.md) once;
   it takes five minutes.

## CI

The `CI` workflow runs on every push: it syntax-checks the builder and
smoke-tests that a generated `.rdp` file keeps NLA on and the right
address — a small example of using GitHub Actions for what it's for.

## License

The toolkit code in this repo is MIT — see [LICENSE](LICENSE).
FreeRDP itself is Apache 2.0 and belongs to its project; install it from
there, not from here.
