# Runbook 01: National Directory (Univention Corporate Server)

UCS is the directory Schleswig-Holstein chose to replace Active Directory. It also has an App Center that installs Nextcloud and Collabora with logins pre-wired, which is the easiest path for Parristan.

## You need
- A VM host on ForgeGrid (Proxmox, KVM/virt-manager on the Fedora coordinator, or VirtualBox)
- VM: 2 vCPU, 4 GB RAM minimum (8 GB if Nextcloud runs on it too), 50 GB disk
- A static IP on your LAN, e.g. `192.168.1.50` (adjust to your network)

## Steps
1. **Download** the UCS VM image or ISO from univention.com (Downloads, free Core Edition).
2. **Create the VM** and boot it. In the setup wizard:
   - Role: **Create a new domain**
   - Organisation: `Republic of Parristan`
   - Domain: `parristan.intranet` (internal only; don't use a real public domain here)
   - Hostname: `ucs01`
   - Set a strong Administrator password and store it in your password manager
   - Static IP and your router as gateway
3. **Log in** to the web portal at `https://192.168.1.50` as `Administrator`.
4. **Create groups** (Users → Groups → Add): `Founders`, `Ministers`, `Junior-Citizens`, `Constabulary`.
5. **Create users** (Users → Add), one per citizen, matching `citizenship/register.csv`. Usernames: `firstname.lastname`.
6. **Junior citizens:** put them only in `Junior-Citizens` and don't give them admin rights.
7. **Snapshot the VM** once it works, before installing anything else.

## Done when
- [ ] Every founder can log in to the UCS portal with their own account
- [ ] Groups exist and members are correct
- [ ] VM snapshot taken

Next: `runbook-02-nextcloud.md`
