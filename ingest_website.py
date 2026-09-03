import hashlib
import pickle
from urllib.parse import urljoin, urlparse

import chromadb
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_URL = "https://www.zaio.io"
MAX_PAGES = 30



# Load the saved TF-IDF vectorizer


with open("vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)



# Connect to ChromaDB


client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("handbook")



# Chunk splitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)



# Clean webpage


def clean_page(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for element in soup([
        "script",
        "style",
        "nav",
        "header",
        "footer",
        "noscript"
    ]):

        element.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    text = " ".join(text.split())

    return text



# Find internal ZAIO links


def get_internal_links(page, current_url):

    links = set()

    for link in page.locator("a").all():

        try:

            href = link.get_attribute("href")

            if not href:
                continue

            full_url = urljoin(
                current_url,
                href
            )

            parsed = urlparse(full_url)

            if parsed.netloc != "www.zaio.io":
                continue

            clean_url = (
                f"{parsed.scheme}://"
                f"{parsed.netloc}"
                f"{parsed.path}"
            )

            if any(
                clean_url.lower().endswith(ext)
                for ext in [
                    ".pdf",
                    ".jpg",
                    ".png",
                    ".jpeg",
                    ".webp",
                    ".zip"
                ]
            ):
                continue

            links.add(clean_url)

        except Exception:
            continue

    return links



# Crawl ZAIO website


def crawl_website():

    pages = []

    visited = set()

    to_visit = {BASE_URL}

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        while (
            to_visit
            and len(visited) < MAX_PAGES
        ):

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

                new_links = get_internal_links(
                    page,
                    url
                )

                for link in new_links:

                    if (
                        link not in visited
                        and
                        len(visited) + len(to_visit)
                        < MAX_PAGES
                    ):

                        to_visit.add(link)

            except Exception as e:

                print(
                    f"Could not crawl {url}: {e}"
                )

        browser.close()

    return pages



# Store website content


def store_website(pages):

    # Remove old website content

    try:

        collection.delete(
            where={
                "source": "Website"
            }
        )

    except Exception:

        pass


    all_documents = []
    all_metadatas = []
    all_ids = []


    for page in pages:

        chunks = splitter.split_text(
            page["text"]
        )

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

            all_ids.append(
                document_id
            )


    print(
        f"Website chunks: {len(all_documents)}"
    )


    if not all_documents:

        print(
            "No website content was found."
        )

        return


    
    # Create TF-IDF embeddings
   

    embeddings = vectorizer.transform(
        all_documents
    ).toarray()



    # Store in the same ChromaDB collection
 

    collection.upsert(

        ids=all_ids,

        documents=all_documents,

        embeddings=embeddings.tolist(),

        metadatas=all_metadatas
    )


    print(
        f"Stored {len(all_documents)} "
        "website chunks in ChromaDB."
    )



# Main


if __name__ == "__main__":

    pages = crawl_website()

    print(
        f"\nPages crawled: {len(pages)}"
    )

    store_website(pages)

    print(
        "\nWebsite ingestion complete!"
    )