# plugin.video.bimozie - Plugin for Kodi 18

bimozie is a plugin for Kodi Media Center -  Kodi is a registered trademark of the XBMC Foundation. We are not connected to or in any other way affiliated with Kodi

## Prerequisites

- Kodi 18 (https://kodi.tv/download)
- resolveurl 5.0.24
- inputstream.adaptive
- beautifulsoup4
- requests
- Cryptdome python library (for Linux systems, install using `pip install --user pycryptodomex` as the user that will run Kodi)

## Installation

#### Install Fusion Repo & resolveurl
 - Add new Fusion repo to install dependency plugins https://www.tvaddons.co/fusion-kodi-krypton/
 - Go to Add-ons and select ` Install from zip file`
 - Select Fusion repo you installed from above
 - Select `kodi-scripts`
 - And select `script.module.resolveurl-5.x.xxx.zip` to install
 
#### Install inputstream.adaptive

inputstream.adaptive comes as standard package from kodi but disabled by default, you need to enable it
- Go to `Add-ons` -> Select My add-ons
- Select VideoPlayer InputStream
- Select InputStream Adaptive
- Click on `Enable` to turn it on


## FAQ

- [Does it work with Kodi 17] Yes, but for some results, you want have full features of this plugin
- [Does it work on a RPI] Not sure
- [Which video resolutions are supported] Depend on the source
