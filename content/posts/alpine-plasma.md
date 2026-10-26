---
title: Install Plasma Desktop on Alpine Linux
date: 2026-03-30
summary: Installing Plasma 6.5.x on Alpine Linux 3.23, with graphics, Wayland, and desktop services.
---

In this tutorial I will explain how to install Plasma 6.5.x into Alpine Linux 3.23 😄

## Install Alpine #

Refer to [this guide](https://wiki.alpinelinux.org/wiki/Installation). Run `setup-alpine` and all the fish.

## Configure your graphics card #

Refer to [this guide](https://wiki.alpinelinux.org/wiki/Graphics_driver). Notice you also have to install the `xf86-video-*` package.

Example for AMDGPU (Radeon RX 6700 XT) and KMS:

```sh
su -
apk add xf86-video-amdgpu mesa-dri-gallium mesa-va-gallium linux-firmware-amdgpu mkinitfs
echo amdgpu >> /etc/modules
echo fbcon >> /etc/modules
sed -i 's/features="\(.*\)"/features="\1 kms"/' /etc/mkinitfs/mkinitfs.conf
mkinitfs
reboot
```

Example for Intel Graphics > Broadwell.

```sh
su -
apk add mesa-dri-gallium mesa-va-gallium mesa-vulkan-intel intel-media-driver
```

## Install Plasma Desktop #

As [this guide](https://wiki.alpinelinux.org/wiki/KDE) is not alright… I will explain better how to get it properly.

Edit your `/etc/apk/repositories` file and uncomment the community line.

```sh
doas apk add vim nano
export EDITOR=vim  # or nano
doas $EDITOR /etc/apk/repositories
```

Then run this:

```sh
su -
# Adding up locales and base packages like D-Bus.
apk add polkit-elogind polkit musl-locales lang pam-rundir dbus-openrc dbus dbus-x11 xf86-input-libinput
# Setting up Wayland...
setup-wayland-base
# Setting up the udevices
setup-devd udev
# Setting up the services
dbus-uuidgen > /var/lib/dbus/machine-id
rc-update add dbus boot
rc-update add polkit boot
setup-desktop # select plasma
rc-update add sddm boot
# you might reboot instead
rc-service dbus start
rc-service polkit start
rc-service sddm start
```

And you’re off to go! A basic installation of Plasma on your Alpine Desktop.

## Adding up more things… #

### Bluetooth #

```sh
doas apk add bluez
doas rc-update add bluetooth
doas rc-service bluetooth start
```

### NetworkManager #

```sh
doas apk add networkmanager networkmanager-<your-needed-package>
doas rc-update add networkmanager boot
doas rc-service networkmanager start
```

## Notice #

I tried to do these instructions on two different devices and worked flawlessly. If you have noticed an error feel free to reach me out.
