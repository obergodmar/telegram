<h3 align="center">
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" width="100" alt="Logo"/><br/>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
	Catppuccin for <a href="https://telegram.org">Telegram</a>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
</h3>

<p align="center">
    <a href="https://github.com/catppuccin/telegram/stargazers"><img src="https://img.shields.io/github/stars/catppuccin/telegram?colorA=363a4f&colorB=b7bdf8&style=for-the-badge"></a>
    <a href="https://github.com/catppuccin/telegram/issues"><img src="https://img.shields.io/github/issues/catppuccin/telegram?colorA=363a4f&colorB=f5a97f&style=for-the-badge"></a>
    <a href="https://github.com/catppuccin/telegram/contributors"><img src="https://img.shields.io/github/contributors/catppuccin/telegram?colorA=363a4f&colorB=a6da95&style=for-the-badge"></a>
</p>

<p align="center">
  <img src="assets/res.webp"/>
</p>

## Previews

<details>
<summary>🖥 Desktop</summary>
<details>
<summary>🌻 Latte</summary>
<img src="assets/desktop/latte.webp"/>
</details>
<details>
<summary>🪴 Frappé</summary>
<img src="assets/desktop/frappe.webp"/>
</details>
<details>
<summary>🌺 Macchiato</summary>
<img src="assets/desktop/macchiato.webp"/>
</details>
<details>
<summary>🌿 Mocha</summary>
<img src="assets/desktop/mocha.webp"/>
</details>
</details>

<details>
<summary>📱 Mobile</summary>
<details>
<summary>🌻 Latte</summary>
<img src="assets/mobile/latte.webp"/>
</details>
<details>
<summary>🪴 Frappé</summary>
<img src="assets/mobile/frappe.webp"/>
</details>
<details>
<summary>🌺 Macchiato</summary>
<img src="assets/mobile/macchiato.webp"/>
</details>
<details>
<summary>🌿 Mocha</summary>
<img src="assets/mobile/mocha.webp"/>
</details>
</details>

## Usage

* [🌻 Latte](https://t.me/addtheme/ctp_latte)
* [🪴 Frappé](https://t.me/addtheme/ctp_frappe)
* [🌺 Macchiato](https://t.me/addtheme/ctp_macchiato)
* [🌿 Mocha](https://t.me/addtheme/ctp_mocha)

1. Choose your flavour from the list above
2. Open the link with your Telegram client of choice
3. Apply the theme
4. Enjoy!

## Development

Edit the files in `templates/` and regenerate `src/` with
[Whiskers](https://github.com/catppuccin/whiskers) 2.3.0:

```sh
whiskers templates/ios.tera
```

Replace `ios` with the client you want to build, or run `just build` to regenerate
all clients. Export installable files with Python 3.9 or newer:

| Client | Export command | Output directory | File extension |
| --- | --- | --- | --- |
| iOS | `python3 scripts/export-ios.py` | `dist/ios/` | `.tgios-theme` |

Each exporter creates all four flavors from the checked-in sources; it does not
regenerate templates. Send the desired file as a document in Telegram, open it
with the matching client, and apply the preview. Exports do not include wallpapers
or update the published theme links above.

Run the exporter and contrast tests with:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
```

## 💝 Thanks to

- [Andreas Grafen](https://github.com/andreasgrafen)
- [ghostx31](https://github.com/ghostx31)
- [Name](https://github.com/NamesCode)
- [jasoncrevier](https://github.com/jasoncrevier)

&nbsp;

<p align="center"><img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/footers/gray0_ctp_on_line.svg?sanitize=true" /></p>
<p align="center">Copyright &copy; 2021-present <a href="https://github.com/catppuccin" target="_blank">Catppuccin Org</a>
<p align="center"><a href="https://github.com/catppuccin/catppuccin/blob/main/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a></p>
