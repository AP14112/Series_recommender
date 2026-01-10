from src.hybrid_model import HybridRecommender
from src.recommender import Recommender


class RecommendationPipeline:
    def __init__(
        self,
        user_interactions_csv: str,
        faiss_path: str,
        series_metadata_csv: str,
        api_key: str,
        model_name: str,
    ):
        self.hybrid_model = HybridRecommender(
            user_interactions_csv=user_interactions_csv,
            faiss_path=faiss_path,
            series_metadata_csv=series_metadata_csv,
        )

        self.explainer = Recommender(
            api_key=api_key,
            model_name=model_name,
        )

    def run(self, user_id: str, top_k: int = 5):
        recommendations, explanation_signals = self.hybrid_model.recommend(
            user_id=user_id,
            top_k=top_k,
        )

        results = []

        for rec in recommendations:
            title = rec["title"]
            signals = explanation_signals.get(title, {})
            context = self._format_explanation_context(signals)
            explanation = self.explainer.explain(
                series_title=title,
                explanation_context=context,
            )

            rec["explanation"] = explanation
            results.append(rec)

        return results

    def _format_explanation_context(self, signals: dict) -> str:
        return "\n".join(f"{k}: {v}" for k, v in signals.items())
     