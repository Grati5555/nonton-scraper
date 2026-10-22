import httpx

TAG = "ID-OFFICIAL"


async def scrape():
  # Menggunakan direktori resmi IPTV-org untuk Indonesia yang selalu aktif
  url = "https://iptv-org.github.io/iptv/countries/id.m3u"
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
          # Menyaring channel nasional utama agar langsung masuk playlist
          results.append({
              "name": current_name,
              "url": line,
              "tag": TAG,
          })
          current_name = None
    except Exception as e:
      print(f"Error: {e}")

  return results
