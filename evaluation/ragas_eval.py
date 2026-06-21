from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import evaluate
from datasets import Dataset
from typing import List, Dict


def _as_float(value) -> float:
    if isinstance(value, list):
        if not value:
            return 0.0
        return float(value[0])
    return float(value)


def interpret_scores(scores: Dict[str, float]) -> str:
    average_score = sum(scores.values()) / len(scores)
    if average_score >= 0.8:
        return "Strong: Answer appears well grounded and relevant."
    if average_score >= 0.6:
        return "Moderate: Answer is usable but may need improvement in grounding or relevance."
    return "Weak: Answer quality is low and should be refined with better evidence."


def evaluate_response(user_query: str, generated_answer: str, context: List[str]) -> Dict:
    """
    Evaluate generated_answer for the user_query using provided context via RAGAS metrics.
    Returns a dict with faithfulness, answer_relevancy, context_precision, context_recall scores.
    """
    data = {
        "question": [user_query],
        "answer": [generated_answer],
        "contexts": [context],
    }
    dataset = Dataset.from_dict(data)

    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
    )

    scores = {
        "faithfulness": _as_float(result["faithfulness"]),
        "answer_relevancy": _as_float(result["answer_relevancy"]),
        "context_precision": _as_float(result["context_precision"]),
        "context_recall": _as_float(result["context_recall"]),
    }

    return {
        **scores,
        "interpretation": interpret_scores(scores),
    }