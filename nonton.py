import asyncio
from bs4 import BeautifulSoup
import httpx

# URL Target Utama
BASE_URL = "https://nontontv.online"
LIVETV_URL = f"{BASE_URL}/livetv/"


async def get_channel_list():
  """Fungsi untuk mengambil daftar channel dari halaman utama Live TV"""
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
      if response.status_code != 200:
        print(f"[!] Gagal mengambil data. Status code: {response.status_code}")
        return []

      soup = BeautifulSoup(response.text, "html.parser")
      channels = []

      # Cari elemen tautan channel
      for el in soup.find_all("a", href=True):
        href = el.get("href")
        title = el.get_text(strip=True)

        if href and ("/tv/" in href or "/watch/" in href or "stream" in href):
          full_url = href if href.startswith("http") else f"{BASE_URL}{href}"
          if title and {"title": title, "url": full_url} not in channels:
            channels.append({"title": title, "url": full_url})

      return channels
    except Exception as e:
      print(f"[!] Error saat mengambil daftar channel: {e}")
      return []


async def extract_stream_url(channel_url, title):
  """Fungsi untuk memproses dan mengekstrak tautan stream/iframe dari halaman detail channel"""
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

      # Mencari iframe player atau sumber video di halaman detail
      iframe = soup.find("iframe")
      if iframe and iframe.get("src"):
        return iframe.get("src")

    except Exception as e:
      print(f"[!] Error saat memproses {title}: {e}")

  return None


async def main():
  print("Mengambil data siaran Live TV...")
  channels = await get_channel_list()

  if not channels:
    print("[!] Tidak ada channel yang ditemukan.")
    return

  print(
      f"[*] Berhasil mendapatkan {len(channels)} channel. Memproses"
      " tautan...\n"
  )

  # Memproses 5 channel pertama sebagai contoh uji coba
  for i, ch in enumerate(channels[:5], start=1):
    title = ch["title"]
    channel_url = ch["url"]

    print(f"[{i}] Memproses: {title}")
    print(f"    URL Halaman : {channel_url}")

    stream_url = await extract_stream_url(channel_url, title)

    if stream_url:
      print(f"-> Berhasil mendapatkan link stream: {stream_url}\n")
    else:
      print("-> Gagal mendapatkan link stream\n")


if __name__ == "__main__":
  asyncio.run(main())
