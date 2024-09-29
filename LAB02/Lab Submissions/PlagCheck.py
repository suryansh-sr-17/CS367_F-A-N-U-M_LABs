import heapq
import string
import os

def preprocess_text(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    sentences = text.split('.')
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

def a_star_alignment(doc1, doc2):
    open_list = []
    heapq.heappush(open_list, (0, 0, 0, []))  
    closed_list = set()
    
    while open_list:
        f, i, j, alignment = heapq.heappop(open_list)
        
        if i == len(doc1) and j == len(doc2):
            return alignment
        
        if (i, j) in closed_list:
            continue
        closed_list.add((i, j))
        
        if i < len(doc1) and j < len(doc2):
            cost = levenshtein_distance(doc1[i], doc2[j])
            h = heuristic(doc1[i+1:], doc2[j+1:])
            heapq.heappush(open_list, (f + cost + h, i + 1, j + 1, alignment + [(i, j, cost)]))
        
        if i < len(doc1):
            h = heuristic(doc1[i+1:], doc2[j:])
            heapq.heappush(open_list, (f + 1 + h, i + 1, j, alignment + [(i, -1, 1)]))  
        
        if j < len(doc2):
            h = heuristic(doc1[i:], doc2[j+1:])
            heapq.heappush(open_list, (f + 1 + h, i, j + 1, alignment + [(-1, j, 1)]))  
    
    return []

def heuristic(remaining_doc1, remaining_doc2):
    total_cost = 0
    for sentence1, sentence2 in zip(remaining_doc1, remaining_doc2):
        total_cost += levenshtein_distance(sentence1, sentence2)
    return total_cost

def detect_plagiarism(alignment, doc1, doc2, threshold=3):
    plagiarized_pairs = []
    for (i, j, cost) in alignment:
        if i != -1 and j != -1 and cost <= threshold:
            plagiarized_pairs.append((i, j, doc1[i], doc2[j], cost))
    return plagiarized_pairs

def classify_similarity(alignment, doc1, doc2):
    total_sentences = max(len(doc1), len(doc2))
    aligned_sentences = sum(1 for a in alignment if a[0] != -1 and a[1] != -1)
    low_edit_distance_sentences = sum(1 for a in alignment if a[2] <= 3)  
    if aligned_sentences == total_sentences and low_edit_distance_sentences == total_sentences:
        return "Test Case 1: Identical Documents"
    elif low_edit_distance_sentences > total_sentences // 2:
        return "Test Case 2: Slightly Modified Document"
    elif low_edit_distance_sentences == 0:
        return "Test Case 3: Completely Different Documents"
    else:
        return "Test Case 4: Partial Overlap"

def compare_documents(doc1_path, doc2_path):
    with open(doc1_path, 'r', encoding='utf-8') as file1, open(doc2_path, 'r', encoding='utf-8') as file2:
        doc1_text = file1.read()
        doc2_text = file2.read()

    doc1 = preprocess_text(doc1_text)
    doc2 = preprocess_text(doc2_text)

    alignment = a_star_alignment(doc1, doc2)

    plagiarized_pairs = detect_plagiarism(alignment, doc1, doc2)
    for i, j, s1, s2, cost in plagiarized_pairs:
        print(f"Sentence {i} in doc1 and Sentence {j} in doc2 are similar with cost {cost}:")
        print(f"doc1: {s1}")
        print(f"doc2: {s2}")
        print()

    similarity_type = classify_similarity(alignment, doc1, doc2)
    print("Document Comparison Result:", similarity_type)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    doc1_name = "main.txt"
    doc2_name = "temp.txt"

    doc1_path = os.path.join(current_dir, doc1_name)
    doc2_path = os.path.join(current_dir, doc2_name)

    compare_documents(doc1_path, doc2_path)

if __name__ == "__main__":
    main()
