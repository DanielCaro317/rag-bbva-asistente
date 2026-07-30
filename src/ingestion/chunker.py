def chunk_text(text, size, overlap):
    words = text.split()
    chunks, cur, cur_len = [], [], 0
    for w in words:
        cur.append(w)
        cur_len += len(w) + 1
        if cur_len >= size:
            chunks.append(" ".join(cur))
            # arrastramos una cola de ~overlap chars para no perder contexto entre chunks
            tail, tlen = [], 0
            for tw in reversed(cur):
                if tlen >= overlap:
                    break
                tail.insert(0, tw)
                tlen += len(tw) + 1
            cur, cur_len = tail, tlen
    if cur:
        chunks.append(" ".join(cur))
    return [c for c in chunks if c.strip()]
