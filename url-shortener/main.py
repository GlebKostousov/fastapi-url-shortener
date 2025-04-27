from typing import List, Annotated

from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from schemas.short_url import ShortUrl

SHORT_URLS = [
    ShortUrl(
        target_url="https://example.com",
        slug="example",
    ),
    ShortUrl(
        target_url="https://google.com",
        slug="search",
    ),
]

app = FastAPI(
    title="URL Shortener",
)


@app.get("/")
def read_root(
    request: Request,
    name: str = "World Gleb",
):
    docs_url = request.url.replace(path="/docs", query="")

    return {
        "message": f"Hello {name}!",
        "docs": str(docs_url),
    }


@app.get(
    path="/short-urls/",
    response_model=List[ShortUrl],
)
def read_short_urls_list():
    return SHORT_URLS


def prefetch_short_urls(slug: str) -> ShortUrl:
    url: ShortUrl | None = next((url for url in SHORT_URLS if url.slug == slug), None)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


@app.get(path="/r/{slug}")
@app.get(path="/r/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
):
    return RedirectResponse(
        url=url.target_url,
    )


@app.get(
    path="/short-urls/{slug}",
    response_model=ShortUrl,
)
def read_short_url(
    url: Annotated[ShortUrl, Depends(prefetch_short_urls)],
):
    return url
