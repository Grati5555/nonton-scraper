import asyncio
from bs4 import BeautifulSoup
import httpx

# URL Target Utama
BASE_URL = "https://nontontv.online"
LIVETV_URL = f"{BASE_URL}/livetv/"


async def get_live_channels():
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/122.0.0.0 Safari/537.36"
      ),
      "Referer": BASE_URL,
  }

  async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
    print(f"[*] Mengakses halaman: {LIVETV_URL}")
    try:
      response = await client.get(LIVETV_URL)

      if response.status_code != 200:
        print(
            f"[!] Gagal mengakses halaman. Status code: {response.status_code}"
        )
        return

      soup = BeautifulSoup(response.text, "html.parser")
      channel_elements = soup.find_all("a", href=True)

      print(
          "[*] Berhasil memuat halaman! Menganalisis tautan saluran...\n"
          "=================================================="
      )

      channels = []
      for el in channel_elements:
        href = el.get("href")
        title = el.get_text(strip=True)

        if href and (
            "/tv/" in href or "/watch/" in href or "stream" in href
        ):
          full_url = href if href.startswith("http") else f"{BASE_URL}{href}"

          if title and {"title": title, "url": full_url} not in channels:
            channels.append({"title": title, "url": full_url})

      if channels:
        for idx, ch in enumerate(channels, start=1):
          print(f"{idx}. Nama Channel : {ch['title']}")
          print(f"   Link Detail   : {ch['url']}")
          print("-" * 50)
        print(f"[*] Total menemukan {len(channels)} channel.")
      else:
        print("[!] Tidak ditemukan channel dengan pola tersebut.")

    except Exception as e:
      print(f"[!] Terjadi kesalahan saat mengambil data: {e}")


if __name__ == "__main__":
  asyncio.run(get_live_channels())
