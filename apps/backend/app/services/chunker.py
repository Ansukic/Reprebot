def chunk_text(text: str, size: int = 1000, overlap: int = 150) -> list[str]:
    """Divide texto en chunks de ~size chars respetando párrafos donde se pueda."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= size:
            current = f"{current}\n\n{para}".strip()
            continue
        if current:
            chunks.append(current)
        # párrafo más largo que size: corte duro con overlap
        while len(para) > size:
            chunks.append(para[:size])
            para = para[size - overlap :]
        current = para

    if current:
        chunks.append(current)
    return chunks
