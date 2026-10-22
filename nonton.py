import asyncio
from bs4 import BeautifulSoup
import httpx

BASE_URL = "https://nontontv.online"
LIVETV_URL = f"{BASE_URL}/livetv/"
OUTPUT_FILE = "nonton_playlist.m3u"


async def get_channel_list():
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
      ),
      "Referer": BASE_URL,
  }

  async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
    print(f"[*] Mengakses daftar channel dari: {LIVETV_URL}")
    try:
      response = await client.get(LIVETV_URL)
      print(f"[*] Status Code halaman utama: {response.status_code}")

      if response.status_code != 200:
        return []

      soup = BeautifulSoup(response.text, "html.parser")
      channels = []

      for el in soup.find_all("a", href=True):
        href = el.get("href")
        title = el.get_text(strip=True)

        if href and ("/tv/" in href or "/watch/" in href or "stream" in href):
          full_url = href if href.startswith("http") else f"{BASE_URL}{href}"
          if title and {"title": title, "url": full_url} not in channels:
            channels.append({"title": title, "url": full_url})

      print(f"[*] Ditemukan {len(channels)} channel.")
      return channels
    except Exception as e:
      print(f"[!] Error saat mengambil daftar channel: {e}")
      return []


async def extract_stream_url(channel_url, title):
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
      ),
      "Referer": LIVETV_URL,
  }

  async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
    try:
      response = await client.get(channel_url)
      if response.status_code != 200:
        return None

      soup = BeautifulSoup(response.text, "html.parser")
      iframe = soup.find("iframe")
      if iframe and iframe.get("src"):
        return iframe.get("src")
    except Exception as e:
      print(f"[!] Error saat memproses {title}: {e}")

  return None


async def main():
  channels = await get_channel_list()

  # Buat file kosong terlebih dahulu agar git add tidak error jika list kosong
  with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    if channels:
      for i, ch in enumerate(channels, start=1):
        title = ch["title"]
        channel_url = ch["url"]

        print(f"[{i}] Memproses: {title}")
        stream_url = await extract_stream_url(channel_url, title)

        if stream_url:
          print(f"    -> Berhasil: {stream_url}")
          f.write(
              f'#EXTINF:-1 tvg-id="" tvg-name="{title}"'
              f' group-title="Live TV",{title}\n'
          )
          f.write(f"{stream_url}\n")
        else:
          print("    -> Gagal mendapatkan link stream")
    else:
      print("[!] Tidak ada channel yang berhasil di-scrape.")


if __name__ == "__main__":
  asyncio.run(main())
