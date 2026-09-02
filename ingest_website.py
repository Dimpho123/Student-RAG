import hashlib
from urllib.parse import urljoin, urlparse

import chromadb
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_URL = "https://www.zaio.io"
MAX_PAGES = 30


# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Existing ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("handbook")

# Chunk splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)


def clean_page(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove things we don't want in the knowledge base
    for element in soup([
        "script",
        "style",
        "nav",
        "header",
        "footer",
        "noscript"
    ]):
        element.decompose()

    text = soup.get_text(separator=" ", strip=True)

    # Clean excessive whitespace
    text = " ".join(text.split())

    return text


def get_internal_links(page, current_url):
    links = set()

    for link in page.locator("a").all():
        try:
            href = link.get_attribute("href")

            if not href:
                continue

            full_url = urljoin(current_url, href)
            parsed = urlparse(full_url)

            # Only ZAIO pages
            if parsed.netloc != "www.zaio.io":
                continue

            # Remove fragments
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

            # Skip files
            if any(
                clean_url.lower().endswith(ext)
                for ext in [".pdf", ".jpg", ".png", ".jpeg", ".webp", ".zip"]
            ):
                continue

            links.add(clean_url)

        except Exception:
            continue

    return links


def crawl_website():
    pages = []
    visited = set()
    to_visit = {BASE_URL}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        while to_visit and len(visited) < MAX_PAGES:
            url = to_visit.pop()

            if url in visited:
                continue

            try:
                print(f"Crawling: {url}")

                page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=60000
                )

                html = page.content()
                text = clean_page(html)

                if len(text) > 100:
                    pages.append({
                        "url": url,
                        "text": text
                    })

                visited.add(url)

                # Discover more ZAIO pages
                new_links = get_internal_links(page, url)

                for link in new_links:
                    if link not in visited and len(visited) + len(to_visit) < MAX_PAGES:
                        to_visit.add(link)

            except Exception as e:
                print(f"Could not crawl {url}: {e}")

        browser.close()

    return pages


def store_website(pages):
    # Remove previously stored website content
    # This prevents duplicates if we run the script again.
    try:
        collection.delete(
            where={"source": "Website"}
        )
    except Exception:
        pass

    all_documents = []
    all_metadatas = []
    all_ids = []

    for page in pages:
        chunks = splitter.split_text(page["text"])

        for index, chunk in enumerate(chunks):

            document_id = hashlib.md5(
                f"{page['url']}-{index}".encode()
            ).hexdigest()

            all_documents.append(chunk)

            all_metadatas.append({
                "source": "Website",
                "url": page["url"],
                "page": "N/A"
            })

            all_ids.append(document_id)

    print(f"Website chunks: {len(all_documents)}")

    if not all_documents:
        print("No website content was found.")
        return

    # Generate embeddings
    embeddings = model.encode(
        all_documents,
        show_progress_bar=True
    ).tolist()

    # Store in the SAME ChromaDB collection
    collection.upsert(
        ids=all_ids,
        documents=all_documents,
        embeddings=embeddings,
        metadatas=all_metadatas
    )

    print(
        f"Stored {len(all_documents)} website chunks in ChromaDB."
    )


if __name__ == "__main__":
    pages = crawl_website()

    print(f"\nPages crawled: {len(pages)}")

    store_website(pages)

    print("\nWebsite ingestion complete!")