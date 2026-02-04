import asyncio
import os
import mimetypes
from typing import List, Optional
from urllib.parse import urlparse
import ssl
import certifi

import aiohttp

import uuid

CHUNK_SIZE = 1024 * 1024  # 1MB


async def download_file(
    session: aiohttp.ClientSession, url: str, download_directory: str
) -> Optional[str]:
    try:
        os.makedirs(download_directory, exist_ok=True)

        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        if not filename or "." not in filename:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.head(url) as response:
                    if response.status == 200:
                        content_disposition = response.headers.get(
                            "Content-Disposition", ""
                        )
                        if "filename=" in content_disposition:
                            filename = content_disposition.split("filename=")[1].strip(
                                "\"'"
                            )
                        else:
                            content_type = response.headers.get("Content-Type", "")
                            if content_type:
                                extension = mimetypes.guess_extension(
                                    content_type.split(";")[0]
                                )
                                if extension:
                                    filename = f"{uuid.uuid4()}{extension}"

        filename = filename or str(uuid.uuid4())
        save_path = os.path.join(download_directory, filename)

        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(save_path, "wb") as file:
                        async for chunk in response.content.iter_chunked(8192):
                            file.write(chunk)
                    print(f"File downloaded successfully: {save_path}")
                    return save_path
                else:
                    print(f"Failed to download file. HTTP status: {response.status}")
                    return None

    except Exception as e:
        print(f"Error downloading file from {url}: {e}")
        return None


async def download_files(
    urls: List[str], download_directory: str
) -> List[Optional[str]]:
    print(f"Starting download of {len(urls)} files to {download_directory}")

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [download_file(session, url, download_directory) for url in urls]
        results = await asyncio.gather(*tasks)

    successful_downloads = [res for res in results if res is not None]
    print(
        f"Download completed: {len(successful_downloads)}/{len(urls)} files downloaded successfully"
    )
    return results
