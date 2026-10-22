import asyncio
import httpx

# Ganti dengan URL m3u atau halaman channel Anda yang sebenarnya
TARGET_URL = "https://wakhaji.my.id/tv/alix20.m3u"
OUTPUT_FILE = "nonton_playlist.m3u"


async def main():
  # Menggunakan User-Agent aplikasi IPTV / Android agar tidak diblokir (403 Forbidden)
  headers = {
      "User-Agent": "IPTVSmartersPro/1.1 (Linux; Android 10)",
      "Accept": "*/*",
  }

  async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
    print(f"[*] Mengambil data dari: {TARGET_URL}")
    try:
      response = await client.get(TARGET_URL)
      print(f"[*] Status Code: {response.status_code}")

      if response.status_code == 200:
        # Menyimpan langsung isi playlist .m3u dari akun Anda
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
          f.write(response.text)
        print("[*] Berhasil menyimpan file playlist m3u!")
      else:
        print(f"[!] Gagal mengambil data. Status: {response.status_code}")
    except Exception as e:
      print(f"[!] Terjadi kesalahan: {e}")


if __name__ == "__main__":
  asyncio.run(main())
