import httpx

TAG = "IPTV-PRO"


async def scrape():
  # Menggunakan tautan sumber yang ingin Anda gunakan
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
      current_block = []

      for line in lines:
        line_str = line.strip()
        if not line_str:
          continue

        # Menangkap baris EXTINF
        if line_str.startswith("#EXTINF:"):
          current_block = [line_str]
        # Menangkap baris ekstensi tambahan pemutar secara utuh
        elif line_str.startswith(
            ("#EXTVLCOPT:", "#KODIPROP:", "##", "#EXT-X-")
        ):
          current_block.append(line_str)
        # Baris URL stream
        elif not line_str.startswith("#") and current_block:
          extra_tags = "\n".join(current_block)
          name = (
              current_block[0].split(",")[-1].strip()
              if "," in current_block[0]
              else "Channel"
          )

          results.append({
              "name": name,
              "url": f"{extra_tags}\n{line_str}",
              "tag": TAG,
          })
          current_block = []
    except Exception as e:
      print(f"Error: {e}")

  return results
