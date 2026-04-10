import pandas as pd
from src.file_reader import read_file
from src.preprocessing import clean_text, chunk_text
from src.similarity import tfidf_sim, jaccard_sim, embedding_matrix, final_score

def is_suspicious(row, threshold):
    return (
        row["Final Score"] >= threshold
        and row["Embedding Score"] >= 0.55
        and (
            row["TF-IDF Score"] >= 0.12
            or row["Jaccard Score"] >= 0.08
        )
    )

def detect_plagiarism(file1, file2, threshold=0.75):
    text1 = clean_text(read_file(file1))
    text2 = clean_text(read_file(file2))

    chunks1 = chunk_text(text1, chunk_size=2, overlap=1)
    chunks2 = chunk_text(text2, chunk_size=2, overlap=1)

    if not chunks1 or not chunks2:
        raise ValueError("Not enough text to compare.")

    emb = embedding_matrix(chunks1, chunks2)

    results = []
    suspicious_count = 0

    for i in range(len(chunks1)):
        best_match = None
        best_score = -1

        for k in range(len(chunks2)):
            t = tfidf_sim(chunks1[i], chunks2[k])
            jac = jaccard_sim(chunks1[i], chunks2[k])
            e = float(emb[i][k])

            score = final_score(t, jac, e)

            if score > best_score:
                best_score = score
                best_match = {
                    "File1 Chunk No": i + 1,
                    "File1 Chunk": chunks1[i],
                    "File2 Chunk No": k + 1,
                    "File2 Chunk": chunks2[k],
                    "TF-IDF Score": round(t, 3),
                    "Jaccard Score": round(jac, 3),
                    "Embedding Score": round(e, 3),
                    "Final Score": round(score, 3),
                }

        best_match["Suspicious"] = "Yes" if is_suspicious(best_match, threshold) else "No"

        if best_match["Suspicious"] == "Yes":
            suspicious_count += 1

        results.append(best_match)

    plagiarism_percent = (suspicious_count / len(chunks1)) * 100
    report = pd.DataFrame(results).sort_values(by="Final Score", ascending=False).reset_index(drop=True)

    return report, round(plagiarism_percent, 2)