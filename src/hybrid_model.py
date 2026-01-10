import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class HybridRecommender:
    def __init__(self,user_interactions_csv: str,faiss_path: str, series_metadata_csv: str):
        self.user_df = pd.read_csv(user_interactions_csv)
        self.series_df = pd.read_csv(series_metadata_csv)
        self.series_df["series_id"] = self.series_df["series_id"].astype(str)
        self.user_df["series_id"] = self.user_df["series_id"].astype(str)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_db = FAISS.load_local(
            faiss_path,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

    def recommend(self, user_id: str, top_k: int = 5):
        user_history = self.user_df[self.user_df["user_id"] == user_id]
        if user_history.empty:
            return self._cold_start(top_k)
        seed_series_id = user_history.sort_values(
            "interaction_score", ascending=False
        ).iloc[0]["series_id"]
        seed_text = self._get_series_text(seed_series_id)
        similar_docs = self.vector_db.similarity_search(
            seed_text, k=top_k + 3
        )

        recommendations = []
        explanation_signals = {}

        for doc in similar_docs:
            series_id = doc.metadata.get("series_id")

            if series_id == seed_series_id:
                continue

            interaction_strength = self._user_interaction_score(
                user_id, series_id
            )

            content_similarity = 1.0  

            final_score = (
                0.6 * content_similarity
                + 0.4 * interaction_strength
            )

            title = self._get_title(series_id)

            recommendations.append({
                "series_id": series_id,
                "title": title,
                "score": round(final_score, 3),
            })

            explanation_signals[title] = {
                "content_similarity": round(content_similarity, 2),
                "user_interaction_strength": round(interaction_strength, 2),
                "seed_series": self._get_title(seed_series_id),
            }

        recommendations = sorted(
            recommendations,
            key=lambda x: x["score"],
            reverse=True,
        )[:top_k]

        return recommendations, explanation_signals

    def _user_interaction_score(self, user_id: str, series_id: str) -> float:
        row = self.user_df[
            (self.user_df["user_id"] == user_id)
            & (self.user_df["series_id"] == series_id)
        ]

        if row.empty:
            return 0.0

        return float(row["interaction_score"].values[0])

    def _get_series_text(self, series_id: str) -> str:
        return self.series_df[
            self.series_df["series_id"] == series_id
        ]["combined_info"].values[0]

    def _get_title(self, series_id: str) -> str:
        return self.series_df[
            self.series_df["series_id"] == series_id
        ]["title"].values[0]

    def _cold_start(self, top_k: int):
        top = self.series_df.sort_values(
            "rating", ascending=False
        ).head(top_k)

        recommendations = top[["series_id", "title", "rating"]].to_dict(
            orient="records"
        )

        explanation_signals = {
            row["title"]: {
                "reason": "Popular and highly rated series"
            }
            for _, row in top.iterrows()
        }

        return recommendations, explanation_signals
