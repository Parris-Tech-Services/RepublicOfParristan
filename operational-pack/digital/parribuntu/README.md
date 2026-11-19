# ParriBuntu

The national desktop, built the Gendarmerie way: stock Ubuntu LTS, a standard open-source suite, centrally managed.

## Build a national laptop
1. Install **Ubuntu 24.04 LTS Desktop**. In the installer choose **Advanced features → Use LVM and encryption** (full-disk encryption).
2. Create the local admin account (Chief Digital Officer).
3. Copy this repo onto the laptop, then:
   ```bash
   cd digital/parribuntu
   sudo bash build-parribuntu.sh ../../symbols/flag.svg
   sudo reboot
   ```
4. Enrol in **MeshCentral** and **Action1** (your existing ForgeGrid tooling) for central management.
5. Add citizen accounts: Settings → Users. For junior citizens, use a Standard account and turn on **Settings → Users → Parental Controls** (install `malcontent` if missing).
6. Thunderbird: add the citizen's national mailbox once Phase 2 is live.

## Includes
LibreOffice (ODF default), Firefox, Thunderbird, GIMP, VLC, automatic security updates, Parristan flag wallpaper.
