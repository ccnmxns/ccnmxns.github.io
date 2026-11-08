---
title: Fixing AutoFirma’s connection to Chrome on Linux
date: 2026-11-08
summary: This issue arised since Chromium v146, let's fix that!
---


AutoFirma may open normally from the application menu while signing from a website fails. Chrome may report:

```
net_error -202
```

This means Chrome does not trust the authority that issued a connection’s certificate. In this case, **AutoFirma’s local root certificate was missing from Chrome’s certificate store**.

## Why this happens and which systems are affected

AutoFirma uses a local TLS connection to communicate with the browser. Chrome must trust the locally generated **AutoFirma ROOT** certificate for that connection to work.

Starting with **Chromium 146**, the default Linux certificate database moved from `~/.pki/nssdb`
to `~/.local/share/pki/nssdb`.

If the old database exists, Chromium continues using it. Installers or repair tools that only handle the old location can therefore miss the database used by newer browsers. See [Chromium’s Linux certificate documentation](https://chromium.googlesource.com/chromium/src.git/+/master/docs/linux/cert_management.md).

This can affect **Chrome and Chromium-based browsers on Linux** when they use the new location and AutoFirma’s root certificate has not been imported there. It was confirmed on this Ubuntu 26.04 installation. This specific fix does not cover Firefox, Windows, or macOS.

## Fix with two commands
Close Chrome completely. Install the NSS certificate utility:
```bash
sudo apt install libnss3-tools
```
Then import AutoFirma’s existing root certificate into the current user’s Chrome certificate database:
```bash
certutil -A -d "sql:$HOME/.local/share/pki/nssdb" -n "Autofirma ROOT" -t "C,," -i "$HOME/.afirma/Autofirma/Autofirma_ROOT.cer"
```
Run the second command **as your normal user, without `sudo`**. It assumes both paths exist, as they did on this machine.

Reopen Chrome and try signing again. This adds trust for AutoFirma’s local communication certificate; it does not renew or change your personal signing certificate.