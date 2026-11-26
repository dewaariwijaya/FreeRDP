# Secure RDP checklist

Remote Desktop is one of the most attacked services on the internet.
Port 3389 is scanned constantly, and a weak RDP setup is usually found
within hours. This checklist is the difference between "convenient" and
"compromised".

## The five rules

1. **Never expose 3389 to the internet.**
   No port forwarding, no "allow any" firewall rules. Reach your machine
   through a VPN instead — [Tailscale](https://tailscale.com) (free for
   personal use) or WireGuard — and connect to the VPN address
   (for Tailscale, the `100.x.x.x` one). If the port is not public,
   scanners cannot knock on it.

2. **Keep Network Level Authentication (NLA) ON.**
   NLA makes the server authenticate you *before* opening a session.
   Turning it off (some "free RDP" guides do, to make things "work")
   removes that shield and enables whole classes of attacks.
   Windows: Settings → System → Remote Desktop → Advanced →
   "Require computers to use Network Level Authentication" ✓.

3. **Use a real password, on a non-obvious account.**
   Long passphrase, unique to that machine, in a password manager.
   Disable or rename the default Administrator account if you do not
   use it, and never print credentials in logs, scripts, or CI output.

4. **Turn on account lockout.**
   Group Policy → Account Lockout Policy: lock the account for
   15 minutes after ~5 failed attempts. This kills password guessing
   even inside your network.

5. **Redirect less.**
   Every shared drive, printer, and clipboard is a bridge between the
   two machines. Keep them off unless a session actually needs them —
   the builder in this repo does that by default.

## Quick self-test

- [ ] `3389` is **not** reachable from the public internet
      (check from your phone on mobile data, Wi-Fi off — it should fail)
- [ ] The machine *is* reachable on its VPN address
- [ ] NLA is required
- [ ] The RDP account has a unique, manager-stored passphrase
- [ ] Account lockout policy is set
- [ ] Windows and the RDP client are up to date

## What about "free RDP" GitHub Actions tricks?

Workflows that turn a CI runner into a temporary remote desktop —
disabling NLA, opening 3389 to everyone, printing an admin password in
the log, and looping to keep the runner alive — break the host
platform's terms of service and can get the account banned, on top of
being genuinely insecure. This repo used to contain one; it was removed
on purpose. If you need a Windows desktop, use a machine or VM you own
and connect to it the way this checklist describes.
