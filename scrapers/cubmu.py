import httpx

TAG = "CUBMU"


async def scrape():
  # Menggunakan tautan sumber publik atau direktori yang menyediakan playlist CubMu
  url = "https://raw.githubusercontent.com/apistech/iptv/main/cubmu.m3u"  # Sesuaikan dengan URL sumber CubMu yang valid
  results = []

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
      )
  }

  async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
    try:
      response = await client.get(url)
      if response.status_code != 200:
        return results

      lines = response.text.splitlines()
      current_name = None

      for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
          if "," in line:
            current_name = line.split(",")[-1].strip()
        elif line and not line.startswith("#") and current_name:
          results.append({
              "name": f"CubMu - {current_name}",
              "url": line,
              "tag": TAG,
          })
          current_name = None
    except Exception as e:
      print(f"Error scraping CubMu: {e}")

  return results
