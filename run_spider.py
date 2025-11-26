import subprocess

def run_pnp_spider():
    cmd = ["scrapy", "crawl", "pnp", "-O", "data/results.json"]
    subprocess.run(cmd, cwd="scraper", check=True)
