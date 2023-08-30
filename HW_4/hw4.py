import argparse
import os
import time
from pathlib import Path
import requests
import threading
import multiprocessing
import asyncio

image_urls = []
with open('images.txt', 'r') as images:
    for image in images.readlines():
        image_urls.append(image.strip())

image_path = Path('./images/')


def download_image(url):
    global image_path
    start_time = time.time()
    response = requests.get(url, stream=True)
    filename = image_path.joinpath(os.path.basename(url))
    with open(filename, "wb") as f:
        f.write(response.content)
    end_time = time.time() - start_time
    print(f"Скачан {filename} за {end_time:.2f} сек")


async def download_image_async(url):
    start_time = time.time()
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url, {"stream": True})
    filename = image_path.joinpath(os.path.basename(url))
    with open(filename, "wb") as f:
        f.write(response.content)
    end_time = time.time() - start_time
    print(f"Скачан {filename} за {end_time:.2f} сек")


def download_images_threading(urls):
    start_time = time.time()
    threads = []
    for url in urls:
        t = threading.Thread(target=download_image, args=(url,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time() - start_time
    print(f"Затрачено времени с многопоточным подходом: {end_time:.2f} сек")


def download_images_multiprocessing(urls):
    start_time = time.time()
    processes = []
    for url in urls:
        p = multiprocessing.Process(target=download_image, args=(url,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    end_time = time.time() - start_time
    print(
        f"Затрачено времени с мультипроцессинговым подходом: {end_time:.2f} сек")


async def download_images_asyncio(urls):
    start_time = time.time()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_image_async(url))
        tasks.append(task)

    await asyncio.gather(*tasks)
    end_time = time.time() - start_time
    print(f"Затрачено времени с асинхронным подходом: {end_time:.2f} сек")


if __name__ == "__main__":

    urls = image_urls

    print(f"Скачивание {len(urls)} изображений многопоточным подходом...")
    download_images_threading(urls)

    print(f"\nСкачивание {len(urls)} с мультипроцессинговым подходом...")
    download_images_multiprocessing(urls)

    print(f"\nСкачивание {len(urls)} с асинхронным подходом...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_images_asyncio(urls))
