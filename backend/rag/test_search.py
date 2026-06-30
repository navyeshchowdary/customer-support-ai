from vector_store import search_knowledge_base

queries = [
    "How do I get a refund?",
    "My product is not powering on",
    "What payment methods do you accept?",
]

for q in queries:
    print(f"\nQuery: {q}")
    results = search_knowledge_base(q, k=2)
    for i, r in enumerate(results, 1):
        print(f"  Result {i}: {r[:150]}...")