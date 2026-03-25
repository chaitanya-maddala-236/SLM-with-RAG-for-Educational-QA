"""
test_queries.py
---------------
Benchmark test set for the Educational RAG pipeline.

Contains 25+ structured test cases covering all major topics, including
follow-up and ambiguous queries to test context resolution.

Usage:
    python test_queries.py
"""

# Research addition: structured benchmark test set
TEST_SET = [
    # ── Water cycle ──────────────────────────────────────────────────────────
    {
        "query": "Explain the water cycle",
        "expected_topic": "water cycle",
        "expected_keywords": ["evaporation", "condensation", "precipitation", "water"],
    },
    {
        "query": "What causes rainfall in the water cycle?",
        "expected_topic": "water cycle",
        "expected_keywords": ["condensation", "precipitation", "clouds", "droplets"],
    },
    # ── Carbon cycle ──────────────────────────────────────────────────────────
    {
        "query": "How does carbon move through the environment?",
        "expected_topic": "carbon cycle",
        "expected_keywords": ["carbon", "dioxide", "atmosphere", "photosynthesis"],
    },
    {
        "query": "What is the role of decomposers in the carbon cycle?",
        "expected_topic": "carbon cycle",
        "expected_keywords": ["decomposers", "organic", "carbon", "release"],
    },
    # ── Bicycle ───────────────────────────────────────────────────────────────
    {
        "query": "How does a bicycle work?",
        "expected_topic": "bicycle",
        "expected_keywords": ["gears", "pedals", "chain", "wheels"],
    },
    {
        "query": "Explain bicycle gears and speed",
        "expected_topic": "bicycle",
        "expected_keywords": ["gears", "speed", "sprocket", "chain"],
    },
    # ── Photosynthesis ────────────────────────────────────────────────────────
    {
        "query": "How does photosynthesis work?",
        "expected_topic": "photosynthesis",
        "expected_keywords": ["chlorophyll", "light", "glucose", "oxygen"],
    },
    {
        "query": "What are the inputs and outputs of photosynthesis?",
        "expected_topic": "photosynthesis",
        "expected_keywords": ["carbon dioxide", "water", "glucose", "oxygen", "light"],
    },
    # ── Trigonometry ──────────────────────────────────────────────────────────
    {
        "query": "What is trigonometry used for?",
        "expected_topic": "trigonometry",
        "expected_keywords": ["sine", "cosine", "tangent", "angle"],
    },
    {
        "query": "Explain sine and cosine functions",
        "expected_topic": "trigonometry",
        "expected_keywords": ["sine", "cosine", "angle", "hypotenuse", "ratio"],
    },
    # ── Genetics ──────────────────────────────────────────────────────────────
    {
        "query": "What is DNA and how does it carry genetic information?",
        "expected_topic": "genetics",
        "expected_keywords": ["DNA", "genes", "chromosomes", "heredity"],
    },
    {
        "query": "How is genetic information inherited?",
        "expected_topic": "genetics",
        "expected_keywords": ["alleles", "dominant", "recessive", "inheritance"],
    },
    # ── Machine learning ─────────────────────────────────────────────────────
    {
        "query": "What is machine learning?",
        "expected_topic": "machine learning",
        "expected_keywords": ["model", "training", "data", "algorithm"],
    },
    {
        "query": "How do neural networks learn?",
        "expected_topic": "machine learning",
        "expected_keywords": ["neural", "weights", "backpropagation", "training"],
    },
    # ── Electricity ───────────────────────────────────────────────────────────
    {
        "query": "How does electricity flow in a circuit?",
        "expected_topic": "electricity",
        "expected_keywords": ["current", "voltage", "resistance", "circuit"],
    },
    # ── Magnetism ─────────────────────────────────────────────────────────────
    {
        "query": "What is a magnetic field?",
        "expected_topic": "magnetism",
        "expected_keywords": ["magnetic", "field", "poles", "force"],
    },
    # ── Nervous system ────────────────────────────────────────────────────────
    {
        "query": "How does the nervous system work?",
        "expected_topic": "nervous system",
        "expected_keywords": ["neurons", "brain", "spinal cord", "signals"],
    },
    # ── Evolution ─────────────────────────────────────────────────────────────
    {
        "query": "Explain the theory of evolution",
        "expected_topic": "evolution",
        "expected_keywords": ["natural selection", "adaptation", "species", "Darwin"],
    },
    # ── Cell structure ────────────────────────────────────────────────────────
    {
        "query": "What are the main parts of a cell?",
        "expected_topic": "cell structure",
        "expected_keywords": ["nucleus", "membrane", "mitochondria", "cytoplasm"],
    },
    # ── Cellular respiration ─────────────────────────────────────────────────
    {
        "query": "What is cellular respiration?",
        "expected_topic": "cellular respiration",
        "expected_keywords": ["glucose", "ATP", "oxygen", "mitochondria"],
    },
    # ── Nitrogen cycle ────────────────────────────────────────────────────────
    {
        "query": "How does nitrogen cycle through ecosystems?",
        "expected_topic": "nitrogen cycle",
        "expected_keywords": ["nitrogen", "fixation", "bacteria", "decomposition"],
    },
    # ── Digestion ─────────────────────────────────────────────────────────────
    {
        "query": "How does the digestive system break down food?",
        "expected_topic": "digestion",
        "expected_keywords": ["stomach", "enzymes", "intestine", "nutrients"],
    },
    # ── Immune system ────────────────────────────────────────────────────────
    {
        "query": "How does the immune system fight infection?",
        "expected_topic": "immune system",
        "expected_keywords": ["antibodies", "white blood cells", "pathogen", "immune"],
    },
    # ── Sound waves ──────────────────────────────────────────────────────────
    {
        "query": "What are sound waves?",
        "expected_topic": "sound waves",
        "expected_keywords": ["frequency", "amplitude", "vibration", "wavelength"],
    },
    # ── Cybersecurity ────────────────────────────────────────────────────────
    {
        "query": "What is cybersecurity?",
        "expected_topic": "cybersecurity",
        "expected_keywords": ["encryption", "firewall", "attack", "data"],
    },
    # ── Ambiguous / follow-up queries (context-resolution tests) ─────────────
    {
        "query": "why does it occur",
        "expected_topic": None,  # depends on conversation context
        "expected_keywords": [],
    },
    {
        "query": "what is cycle",
        "expected_topic": None,  # ambiguous: water / carbon / bicycle
        "expected_keywords": [],
    },
    {
        "query": "how does it move",
        "expected_topic": None,  # depends on context
        "expected_keywords": [],
    },
    {
        "query": "explain the process",
        "expected_topic": None,
        "expected_keywords": [],
    },
]


# Research addition: benchmark runner function
def run_benchmark(pipeline, memory_cls, topic_manager_cls) -> dict:
    """
    Run all TEST_SET queries through the RAG pipeline and collect per-query metrics.

    Args:
        pipeline:           An initialised RAGPipeline instance.
        memory_cls:         ConversationMemory class (for fresh sessions).
        topic_manager_cls:  TopicMemoryManager class (for fresh sessions).

    Returns:
        A dict with:
            "results"  – list of per-query result dicts
            "summary"  – averaged metric values across all queries that
                         returned metrics
    """
    memory = memory_cls(max_turns=5)
    topic_manager = topic_manager_cls()

    results = []
    all_metrics: list[dict] = []

    for item in TEST_SET:
        query = item["query"]
        expected_topic = item["expected_topic"]
        expected_keywords = item["expected_keywords"]

        try:
            result = pipeline.run(
                user_query=query,
                memory=memory,
                topic_manager=topic_manager,
            )

            # Research addition: keyword hit rate — fraction of expected
            # keywords found in the answer (case-insensitive)
            keyword_hit_rate = 0.0
            if expected_keywords:
                answer_lower = result.answer.lower()
                hits = sum(
                    1 for kw in expected_keywords if kw.lower() in answer_lower
                )
                keyword_hit_rate = hits / len(expected_keywords)

            entry = {
                "query": query,
                "expected_topic": expected_topic,
                "detected_topic": result.detected_topic,
                "topic_correct": (
                    result.detected_topic == expected_topic
                    if expected_topic is not None
                    else None  # can't evaluate ambiguous queries
                ),
                "keyword_hit_rate": round(keyword_hit_rate, 3),
                "answer_snippet": result.answer[:120],
                "mode": result.mode,
                "metrics": result.metrics,
            }
            results.append(entry)

            if result.metrics:
                all_metrics.append(result.metrics)

        except Exception as exc:
            results.append({
                "query": query,
                "expected_topic": expected_topic,
                "error": str(exc),
                "metrics": {},
            })

    # Compute average metrics
    summary: dict = {}
    if all_metrics:
        for key in all_metrics[0]:
            summary[key] = round(
                sum(m[key] for m in all_metrics) / len(all_metrics), 3
            )

    return {"results": results, "summary": summary}


if __name__ == "__main__":
    print(f"Test set loaded: {len(TEST_SET)} queries")
    print("\nSample entries:")
    for item in TEST_SET[:3]:
        print(f"  query={item['query']!r}")
        print(f"  expected_topic={item['expected_topic']!r}")
        print(f"  expected_keywords={item['expected_keywords']}")
        print()
    print("To run a full benchmark, call run_benchmark(pipeline, ConversationMemory, TopicMemoryManager)")
