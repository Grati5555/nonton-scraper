import httpx

TAG = "PUBLIC-TV"


async def scrape():
  """Scraper untuk mengambil daftar siaran TV publik/berita gratis yang aktif"""
  # Menggunakan sumber data publik terbuka (Contoh: daftar kategori berita dari IPTV-org)
  url = "https://iptv-org.github.io/iptv/categories/news.m3u"
  results = []

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
      )
  }

  async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
    try:
      print(f"[*] Mengambil data dari sumber publik: {url}")
      response = await client.get(url)

      if response.status_code != 200:
        print(f"[!] Gagal mengambil data, status: {response.status_code}")
        return results

      # Memparsing file M3U secara sederhana
      lines = response.text.splitlines()
      current_name = None

      for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
          # Mengambil nama channel dari baris ekstensi m3u
          if "," in line:
            current_name = line.split(",")[-1].strip()
        elif line and not line.startswith("#") and current_name:
          # Baris ini adalah URL stream
          # Batasi misal 15 channel teratas dulu untuk pengujian awal
          if len(results) < 15:
            results.append({
                "name": current_name,
                "url": line,
                "tag": TAG,
            })
          current_name = None

      print(f"[*] Berhasil memuat {len(results)} channel dari public_tv.")
    except Exception as e:
      print(f"[!] Error pada public_tv scraper: {e}")

  return results
