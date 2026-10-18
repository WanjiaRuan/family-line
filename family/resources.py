import http.client
import io
import ipaddress
import socket
import ssl
from pathlib import Path
from urllib.parse import urlsplit, urljoin, unquote
from bs4 import BeautifulSoup
from pypdf import PdfReader
from docx import Document
from . import store, intelligence

MAX_BYTES=10*1024*1024
EXTS={".pdf",".txt",".md",".docx",".png",".jpg",".jpeg",".webp"}


def public_target(url):
    p=urlsplit(url)
    if p.scheme not in {"http","https"} or not p.hostname or p.username or p.password:
        raise ValueError("Only public HTTP or HTTPS links are supported.")
    port=p.port or (443 if p.scheme=="https" else 80)
    if port not in {80,443}:
        raise ValueError("This URL port is not supported.")
    try:
        ips={i[4][0] for i in socket.getaddrinfo(p.hostname,port,type=socket.SOCK_STREAM)}
    except OSError:
        raise ValueError("The URL hostname could not be resolved.") from None
    if not ips or not all(ipaddress.ip_address(ip).is_global for ip in ips):
        raise ValueError("Local and private network URLs cannot be imported.")
    return p,port,sorted(ips)[0]


def fetch(url):
    for _ in range(5):
        p,port,ip=public_target(url)
        conn=(http.client.HTTPSConnection(p.hostname,port,timeout=15,context=ssl.create_default_context()) if p.scheme=="https" else http.client.HTTPConnection(p.hostname,port,timeout=15))
        # Pin DNS result while keeping original TLS SNI and certificate verification.
        conn._create_connection=lambda address,timeout=15,source_address=None: socket.create_connection((ip,port),timeout,source_address)
        try:
            conn.request("GET",(p.path or "/")+("?"+p.query if p.query else ""),headers={"User-Agent":"FamilyLine-Demo/1.0","Accept-Encoding":"identity"})
            response=conn.getresponse()
            if response.status in {301,302,303,307,308}:
                location=response.getheader("Location")
                if not location:
                    raise ValueError("The redirect has no destination.")
                url=urljoin(url,location)
                continue
            if response.status!=200:
                raise ValueError(f"Could not read this URL (HTTP {response.status}). Upload the file or paste its text.")
            data=response.read(MAX_BYTES+1)
            if len(data)>MAX_BYTES:
                raise ValueError("File exceeds the 10 MB limit.")
            return data,response.getheader("Content-Type","").split(";")[0],url
        finally:
            conn.close()
    raise ValueError("Too many URL redirects.")


def extract(data,name,mime):
    ext=Path(name).suffix.lower()
    if ext==".pdf" or mime=="application/pdf":
        reader=PdfReader(io.BytesIO(data))
        if len(reader.pages)>60:
            raise ValueError("This demo accepts PDFs up to 60 pages. Split larger documents first.")
        text="\n\n".join(f"[Page {i+1}]\n"+(page.extract_text() or "") for i,page in enumerate(reader.pages))
        if len(text.strip())<100:
            if not intelligence.public_config()["configured"]:
                return "","needs_model","Scanned PDFs need OpenAI. Configure a key, then retry."
            text=intelligence.interpret_pdf(data)
            return text[:150000],"needs_review","Review this scanned PDF before sharing it with the phone assistant."
        return text[:150000],"ready",None
    if ext in {".png",".jpg",".jpeg",".webp"} or mime.startswith("image/"):
        actual={".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",".webp":"image/webp"}.get(ext,mime)
        if not intelligence.public_config()["configured"]:
            return "","needs_model","Image stored. Configure OpenAI to read it; its contents are not understood yet."
        return intelligence.interpret_image(data,actual),"needs_review","Image understood as a draft. Review it in conversation before sharing it with the phone assistant."
    if ext==".docx":
        d=Document(io.BytesIO(data))
        text="\n".join(p.text for p in d.paragraphs)
        for table in d.tables:
            text+="\n"+"\n".join(" | ".join(cell.text for cell in row.cells) for row in table.rows)
        return text[:150000],"ready",None
    if mime=="text/html" or ext in {".html",".htm"}:
        soup=BeautifulSoup(data,"html.parser")
        for el in soup(["script","style","nav","footer","noscript","form"]):
            el.decompose()
        text=(soup.find("main") or soup.find("article") or soup).get_text("\n",strip=True)
        if len(text)<30:
            raise ValueError("No readable page text found. It may require sign-in or JavaScript.")
        return text[:150000],"ready",None
    if ext in {".txt",".md"} or mime.startswith("text/"):
        return data.decode("utf-8-sig")[:150000],"ready",None
    raise ValueError("Use PDF, an image, TXT, Markdown or DOCX.")


def ingest(data,name,mime,url=None):
    if not data or len(data)>MAX_BYTES:
        raise ValueError("The file is empty or exceeds 10 MB.")
    rid=store.ident("res")
    path=store.DATA / "uploads" / (rid+Path(name).suffix.lower())
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)
    try:
        text,status,error=extract(data,name,mime)
    except Exception as exc:
        text,status,error="","failed",str(exc) if isinstance(exc,ValueError) else "Could not parse this file. Check its format."
    with store.db() as c:
        c.execute("INSERT INTO resources VALUES(?,?,?,?,?,?,?,?,?)",(rid,name[:200],mime,str(path),url,text,status,error,store.now()))
        store.event(c,"Resource imported: "+status,name,"resource",rid)
    return {"id":rid,"status":status,"error":error}


def retry(rid):
    with store.db() as c:
        r=c.execute("SELECT * FROM resources WHERE id=?",(rid,)).fetchone()
    if not r or not r["path"]:
        raise ValueError("No source file is available to retry.")
    text,status,error=extract(Path(r["path"]).read_bytes(),r["title"],r["mime"])
    with store.db() as c:
        c.execute("UPDATE resources SET text=?,status=?,error=? WHERE id=?",(text,status,error,rid))
    return {"status":status,"error":error}
