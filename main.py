import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from playwright.async_api import async_playwright, Response

load_dotenv()
api_key = os.getenv("API_KEY")
api_key_header = "X-Api-Key"

app = FastAPI()


@app.middleware("http")
async def authorization(request: Request, call_next):
    request_api_key = request.headers.get(api_key_header)
    if request_api_key == api_key:
        return await call_next(request)
    else:
        return JSONResponse(status_code=401, content="Bad API Key or missing")


@app.get("/videos/{tweet_id}")
async def get_tweet_video_data(tweet_id: int):
    url = f"https://twitter.com/_/status/{tweet_id}"
    xhr_calls: list[Response] = []

    def intercept_response(response: Response):
        """capture all background requests and save them"""
        # we can extract details from background requests
        if response.request.resource_type == "xhr":
            xhr_calls.append(response)
        return response

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            args=[
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
            ],
            chromium_sandbox=False,
        )
        page = await browser.new_page()
        page.on("response", intercept_response)
        # go to url and wait for the page to load
        await page.goto(url)
        await page.wait_for_selector("[data-testid='tweet']")

        # find all tweet background requests:
        tweet_call = [f for f in xhr_calls if "TweetResultByRestId" in f.url][0]
        data = await tweet_call.json()

        await page.close()
        await browser.close()

        result = data["data"]["tweetResult"]["result"]
        return result["legacy"]["extended_entities"]["media"][0]["video_info"]
