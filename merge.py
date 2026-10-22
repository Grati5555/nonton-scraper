import asyncio
import importlib.util
import os

OUTPUT_FILE = "master.m3u"
SCRAPERS_DIR = "scrapers"


async def main():
  print("[*] Memulai proses penggabungan playlist...")
  all_channels = []

  # Membaca semua file python di dalam folder scrapers
  if os.path.exists(SCRAPERS_DIR):
    for filename in os.listdir(SCRAPERS_DIR):
      if filename.endswith(".py") and filename != "__init__.py":
        filepath = os.path.join(SCRAPERS_DIR, filename)
        module_name = filename[:-3]

        print(f"[*] Menjalankan scraper dari: {filename}")
        try:
          # Memuat modul python secara dinamis
          spec = importlib.util.spec_from_file_location(module_name, filepath)
          module = importlib.util.module_from_spec(spec)
          spec.loader.exec_module(module)

          if hasattr(module, "scrape"):
            channels = await module.scrape()
            if channels:
              all_channels.extend(channels)
              print(f"    -> Berhasil mengambil {len(channels)} channel.")
        except Exception as e:
          print(f"    -> Gagal menjalankan {filename}: {e}")

  # Menulis hasil gabungan ke master.m3u
  print(f"[*] Menulis total {len(all_channels)} channel ke {OUTPUT_FILE}...")
  with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for ch in all_channels:
      name = ch.get("name", "Unknown")
      url = ch.get("url", "")
      tag = ch.get("tag", "IPTV")

      f.write(
          f'#EXTINF:-1 tvg-id="" tvg-name="{name}"'
          f' group-title="{tag}",{name}\n'
      )
      f.write(f"{url}\n")

  print("[+] Selesai! Master playlist berhasil diperbarui.")


if __name__ == "__main__":
  asyncio.run(main())
