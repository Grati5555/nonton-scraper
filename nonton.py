import asyncio
from bs4 import BeautifulSoup
import httpx

BASE_URL = "https://nontontv.online"
LIVETV_URL = f"{BASE_URL}/livetv/"
OUTPUT_FILE = "nonton_playlist.m3u"


async def main():
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
      ),
      "Referer": BASE_URL,
  }

  async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
    print(f"[*] Mengakses: {LIVETV_URL}")
    response = await client.get(LIVETV_URL)
    print(f"[*] Status Code: {response.status_code}")

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, "html.parser")

      # Cetak beberapa contoh link yang ada di halaman untuk dianalisis
      links = soup.find_all("a", href=True)
      print(f"[*] Total tag <a> ditemukan: {len(links)}")

      with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")

        for el in links[:30]:  # Cek 30 link pertama
          href = el.get("href")
          text = el.get_text(strip=True)
          print(f"Link: {href} | Teks: {text}")

          # Masukkan sementara ke m3u jika mengandung pola tertentu
          if href and ("http" in href or "/" in href):
            full_url = href if href.startswith("http") else f"{BASE_URL}{href}"
            if text:
              f.write(
                  f'#EXTINF:-1 tvg-id="" tvg-name="{text}"'
                  f' group-title="Live TV",{text}\n'
              )
              f.write(f"{full_url}\n")


if __name__ == "__main__":
  asyncio.run(main())
