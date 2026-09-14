_default:
  @just --list

build:
  whiskers templates/android.tera
  whiskers templates/desktop.tera
  whiskers templates/ios.tera
  whiskers templates/macos.tera

export-ios:
  python3 scripts/export-ios.py
