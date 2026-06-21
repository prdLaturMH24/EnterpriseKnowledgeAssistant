from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import evaluate
from datasets import Dataset
from typing import List, Dict


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

    return {
        "faithfulness": result["faithfulness"],
        "answer_relevancy": result["answer_relevancy"],
        "context_precision": result["context_precision"],
        "context_recall": result["context_recall"],
    }