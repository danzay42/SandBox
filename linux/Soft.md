# Distributives
- [artix](https://artixlinux.org/)
- [alt](https://www.altlinux.org/)
- [linux-hardware](https://linux-hardware.org/)
- [netboot](https://netboot.xyz/)

# Tiling window manager
---
- [i3](https://i3wm.org/)
- [qtile](https://qtile.org/) (python)
- [hyprland](https://wiki.hyprland.org/)
- [bspwm](https://github.com/baskerville/bspwm)

## Display
- xrandr
### Status Bar
- waybar
- nwg-panel
- polybar
- xmobar
### Notify
- mako
- dunst
	```sh
	notify-send
	dunstify
	```
### Wallpapers
- nitrogen
- **feh**
- swaybg
- swww
- hyprpaper
### LockScreen
- hyperlock
- swaylock
### Dock
- nwg-dock
### Widgets
- ags
- eww

## Control
### Volume Control
- amixer
- alsamixer
- pamixer
### Brightness
- xbacklight -> brillo
- light
- clight
### Keyboard
- sxhkd
- setxkbmap
### Power
- hypridle

## Launcher
- wofi
- [rofi](https://github.com/davatorium/rofi)
- dmenu

## Screenshot
- scrot -> [flameshot](https://github.com/flameshot-org/flameshot)
- grimblast
- grim+slurp

## Compositor
- xcompmgr
- compiz
- picom


# Soft
---
- qbittorrent | fragments (gnome)
- [entr](https://github.com/clibs/entr) (event notify test runner)
- [bat-extras](https://github.com/eth-p/bat-extras/tree/master)
- atuin (best serch for command history)
- eva (calculator)
- [Virtual Machine Manager](https://virt-manager.org/)
- [pandoc](https://pandoc.org/)

## Terminal
- [alacritty](https://github.com/alacritty/alacritty) | kitty
- [starship](https://starship.rs/)
- tmux | [zellij](https://zellij.dev/)
- tput
- history

## Text Editor (VI)
- nano
- vi -> vim -> [nvim](https://neovim.io/)
- [helix](https://helix-editor.com/)

### Neovim plugins
https://vimawesome.com/
https://github.com/folke/lazy.nvim
https://github.com/williamboman/mason.nvim
https://github.com/ryanoasis/vim-devicons
https://github.com/ryanoasis/nerd-fonts#glyph-sets

### Plugins & utils:
Lazy (all plugins)-> Mason (nice lsp plugins)
- LSPs
- lexer -> tree-sitter (быстрый и правильный способо подстветки кода)
- Tagbar (навигация внутри файла)
- NERDTree
- Telescope (use: ripgrep, fzf)

### Configs
- [kickstart](https://github.com/nvim-lua/kickstart.nvim)
- [NvChad](https://nvchad.com/)
- [LazyVim](https://www.lazyvim.org/)
- [AstroNvim](https://astronvim.github.io/)
- [LunarVim](https://www.lunarvim.org/)

### Troubleshooting
- on Wayland install wl-clipboard
- [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts)
	```shell
	git clone --depth 1 https://github.com/ryanoasis/nerd-fonts.git
	cd nerd-fonts
	./install.sh
	cd ../
	rm -rf nerd-fonts
	```

## ALL
https://suckless.org/

[camera_capture](https://github.com/weebney/webcamize) + [ffmpeg](https://ffmpeg.org/)
[youtube_cli](https://github.com/yt-dlp/yt-dlp)
[youtube_download](https://github.com/BKSalman/ytdlp-gui)
[youtube_download2](https://github.com/jely2002/youtube-dl-gui)
[python_computer_vision](https://github.com/roboflow/supervision)
[llama-terminal-completion](https://github.com/adammpkins/llama-terminal-completion)
[AI-tools](https://github.com/jamesmurdza/awesome-ai-devtools)
[matterbridge](https://github.com/42wim/matterbridge) - messenger bridge 
[cross-platform file explorer](https://github.com/kimlimjustin/xplorer)
[cli file explorer](https://github.com/sxyazi/yazi)
[library](https://github.com/Librum-Reader/Librum)
[bootable usb OS](https://www.ventoy.net/en/index.html)

[pyshark](https://github.com/KimiNewt/pyshark)
[python web scrapper](https://scrapy.org/)

## [Git](https://git-scm.com/book/en/v2)
- [lazygit](https://github.com/jesseduffield/lazygit)
- [gitui](https://github.com/extrawurst/gitui)
- [diff-tool](https://github.com/dandavison/delta)

## Messengers
[simplex-chat](https://github.com/simplex-chat/simplex-chat)
[arpchat](https://github.com/kognise/arpchat)

## Browser
[tampermonkey](https://www.tampermonkey.net/)
[vi-motions](https://github.com/brookhong/Surfingkeys)
[home-page](https://github.com/b-coimbra/dawn) -> [home-page](https://github.com/AllJavi/tartarus-startpage)
[http-tracker](https://github.com/venukbh/http-tracker)
[перевод видео](https://github.com/ilyhalight/voice-over-translation)


## Android
OS:
- https://droidian.org/

Store:
- [Obtainium](https://github.com/ImranR98/Obtainium)
- [F-droid](https://f-droid.org/ru/)

[ttl changer](https://github.com/aleksey-saenko/TTLChanger)
[copy sms code](https://github.com/jd1378/otphelper)
[ente-auth](https://github.com/ente-io/auth)
[torrent](https://gitlab.com/proninyaroslav/libretorrent)
[revanced manager](https://github.com/ReVanced/revanced-manager)

## wifi-Router OS
https://openwrt.org/
https://dd-wrt.com/
https://librecmc.org/

## Password
[pass](https://www.passwordstore.org/) + [pgen](https://github.com/ctsrc/Pgen) | bitwarden
[gpg-tui](https://github.com/orhun/gpg-tui)

## Security
https://github.com/w4/pisshoff - ssh trap
https://web.telegram.org/k/#@open_source_friend - file transfer

# Configs
---

```shell
# Locale
sudo echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen
sudo locale-gen

# Misc USB visibility
sudo usermod -aG dialout $USER
```

## Arch
%% TODO: move to https://artixlinux.org/ %%

```shell
# base
# pacstrap /mnt base linux linux-firmware sof-firmware base-devel grub efibootmgr

# Bluetooth
sudo pacman -S bluez bluez-util bluez-plugins
sudo systemctl enable bluetooth.service
sudo systemctl start bluetooth.service

# Fonts
sudo pacman -S noto-fonts

# ALSA firmware
sudo pacman -S sof-firmware

# Graphics
# sudo pacman -S nvidia
# Nvidia Geforce gtx 780m
yay -S nvidia-470xx-dkms

# Video Acceleration (VA) API for Linux
sudo pacman -S libva libva-utils

# Gnome
sudo pacman -S gnome-themes-extra gnome-firmware
yay -S gnome-browser-connector
```

### Pacman
```shell
# list unused packages
sudo pacman -Qtdq
# remove unused
sudo pacman -Rns $(sudo pacman -Qtdq)
# clear cache
sudo pacman -Sc
sudo pacman -Scc
```

### Flatpak
```shell
# install
sudo pacman -S flatpak

# add source
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

[Advanced Linux Sound Architecture/Troubleshooting](https://wiki.archlinux.org/title/Advanced_Linux_Sound_Architecture)

### Система межпроцессного взаимодействия
libdbus -> dbus-brocker
```shell
sudo pacman -S dbus-brocker
sudo systemctl --global enable dbus-broker.service
```

### AUR Helper
```shell
sudo pacman -S --needed base-devel
git clone https://aur.archlinux.org/yay-git.git
cd yay-git
makepkg -si
```

## Fedora

```shell
sudo dnf install gstreamer1-plugins-{bad-\*,good-\*,base} gstreamer1-plugin-openh264 gstreamer1-libav --exclude=gstreamer1-plugins-bad-free-devel

sudo dnf install lame\* --exclude=lame-devel
sudo dnf group upgrade --with-optional Multimedia
```
[rpm fusion](https://rpmfusion.org/)

### DNF
Edit `/etc/dnf/dnf.conf`
```
skip_if_unavailable=True
fastestmirror=True
max_parallel_downloads=10
defaultyes=True
```

## Gnome

```shell
# Remove unused
sudo pacman -R gnome-boxes cheese gnome-contacts gnome-maps gnome-photos gnome-music totem gnome-weather epiphany

# Settings
gsettings set org.gnome.desktop.interface color-scheme prefer-dark
gsettings set org.gnome.desktop.interface enable-hot-corners false

gsettings set org.gnome.desktop.session idle-delay 1800
gsettings set org.gnome.settings-daemon.plugins.power power-button-action "interactive"
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-timeout 1200
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 1200

shortcut_gset=org.gnome.settings-daemon.plugins.media-keys
shortcut_custom=/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/

gsettings set ${shortcut_gset}.custom-keybinding:${shortcut_custom} binding '<Super>Return'
gsettings set ${shortcut_gset}.custom-keybinding:${shortcut_custom} name 'Terminal'
gsettings set ${shortcut_gset}.custom-keybinding:${shortcut_custom} command 'alacritty'
gsettings set ${shortcut_gset} custom-keybindings "['${shortcut_custom}']"

gsettings set org.gnome.desktop.input-sources per-window true
gsettings set org.gnome.desktop.input-sources sources "[('xkb', 'us'), ('xkb', 'ru')]"
```

### Extensions
- [Dash to Dock](https://github.com/micheleg/dash-to-dock)
- [Vitals](https://github.com/corecoding/Vitals)
- [AppIndicator and KStatusNotifireItem](https://github.com/ubuntu/gnome-shell-extension-appindicator)
- [Removable Drive Menu](https://gitlab.gnome.org/GNOME/gnome-shell-extensions)
- [Clipboard Indicator](https://github.com/Tudmotu/gnome-shell-extension-clipboard-indicator)
```shell
gnome-extensions enable clipboard-indicator@tudmotu.com
gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com
gnome-extensions enable Vitals@CoreCoding.com
gnome-extensions enable dash-to-dock@micxgx.gmail.com
gnome-extensions enable drive-menu@gnome-shell-extensions.gcampax.github.com
```
