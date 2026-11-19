#!/usr/bin/env bash
# ParriBuntu: national desktop of the Republic of Parristan.
# Run on a fresh Ubuntu 24.04 LTS (GNOME) install, after enabling full-disk encryption in the installer.
# Usage: sudo bash build-parribuntu.sh /path/to/flag.svg
set -euo pipefail

if [[ $EUID -ne 0 ]]; then echo "Run with sudo."; exit 1; fi
FLAG_SRC="${1:-../../symbols/flag.svg}"
[[ -f "$FLAG_SRC" ]] || { echo "Flag not found: $FLAG_SRC"; exit 1; }

echo "== Updating system =="
apt-get update
apt-get -y full-upgrade

echo "== Installing the Gendarmerie-style standard suite =="
apt-get install -y libreoffice libreoffice-l10n-en-gb hunspell-en-au \
  thunderbird gimp vlc unattended-upgrades
snap list firefox >/dev/null 2>&1 || snap install firefox

echo "== Automatic security updates =="
dpkg-reconfigure -f noninteractive unattended-upgrades

echo "== Default to OpenDocument formats (Open Source Act s4) =="
mkdir -p /etc/libreoffice/registry
cat > /etc/libreoffice/registry/parristan-odf.xcd <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<oor:data xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema">
 <oor:component-data oor:package="org.openoffice.Setup" oor:name="Setup">
  <node oor:name="Office"><node oor:name="Factories">
   <node oor:name="com.sun.star.text.TextDocument"><prop oor:name="ooSetupFactoryDefaultFilter"><value>writer8</value></prop></node>
   <node oor:name="com.sun.star.sheet.SpreadsheetDocument"><prop oor:name="ooSetupFactoryDefaultFilter"><value>calc8</value></prop></node>
  </node></node>
 </oor:component-data>
</oor:data>
EOF

echo "== National branding =="
install -Dm644 "$FLAG_SRC" /usr/share/backgrounds/parristan/flag.svg
mkdir -p /etc/dconf/profile /etc/dconf/db/local.d
printf 'user-db:user\nsystem-db:local\n' > /etc/dconf/profile/user
cat > /etc/dconf/db/local.d/00-parristan <<'EOF'
[org/gnome/desktop/background]
picture-uri='file:///usr/share/backgrounds/parristan/flag.svg'
picture-uri-dark='file:///usr/share/backgrounds/parristan/flag.svg'
picture-options='zoom'

[org/gnome/desktop/screensaver]
picture-uri='file:///usr/share/backgrounds/parristan/flag.svg'
EOF
dconf update

echo "== Hostname tag =="
echo "ParriBuntu 24.04 — Republic of Parristan" > /etc/issue.parristan

echo "Done. Reboot, then enrol this machine in MeshCentral / Action1."
