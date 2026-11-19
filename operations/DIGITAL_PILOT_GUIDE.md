# Digital pilot — one workstation (setup guide)

Goal: prove the open-source desktop works on **one** machine before buying or migrating anything. See [sovereign IT checklist](../operational-pack/digital/sovereign-it-checklist.md) for the bigger picture.

## 1. Machine
Any spare laptop or a virtual machine (VirtualBox or GNOME Boxes), 4 GB RAM, 40 GB disk.

## 2. Install
1. Download Ubuntu 24.04 LTS from ubuntu.com and write it to USB (balenaEtcher or Rufus).
2. Install with **full-disk encryption** ticked. Store the recovery key with a second officer.
3. After install: `sudo apt update && sudo apt full-upgrade -y`
4. `sudo apt install -y libreoffice thunderbird element-desktop || sudo snap install element-desktop`
5. Set wallpaper to the flag proposal (`docs/assets/flag-proposal.svg`), labelled as a proposal.

## 3. Test (tick and record the date)
- [ ] Open, edit and save a `.odt` from [templates/OFFICIAL_DOCUMENT.md](../templates/OFFICIAL_DOCUMENT.md) (paste into LibreOffice Writer).
- [ ] Export to PDF with *File → Export as PDF → Archive (PDF/A)* and *Tagged PDF* ticked (accessibility).
- [ ] Join the Matrix room in Element.
- [ ] Take a backup with Déjà Dup to a USB drive and restore one file.
- [ ] Create a junior-member user account with *Settings → Users → Parental controls*.

## 4. Review afterwards
Write a short note: what worked, what was hard, time taken, cost. That note decides whether to roll out further (checklist item "review the digital pilot").
