import sys
import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.hybrid_model import HybridRecommender
from src.recommender import Recommender


st.set_page_config(
    page_title="🎬 Series Recommender",
    layout="wide"
)

st.title("🎬 Explainable Series Recommender")
st.caption("Hybrid (Content + Interaction) Recommendation System")

st.divider()


USER_CSV = os.path.join(ROOT_DIR, "data", "processed_user_interactions.csv")
SERIES_CSV = os.path.join(ROOT_DIR, "data", "processed_series_metadata.csv")
FAISS_PATH = os.path.join(ROOT_DIR, "faiss_db")


for path in [USER_CSV, SERIES_CSV, FAISS_PATH]:
    if not os.path.exists(path):
        st.error(f"Missing required file or folder: {path}")
        st.stop()


@st.cache_resource
def load_models():
    hybrid = HybridRecommender(
        user_interactions_csv=USER_CSV,
        series_metadata_csv=SERIES_CSV,
        faiss_path=FAISS_PATH,
    )

    explainer = Recommender(
        api_key=os.getenv["GROQ_API_KEY"],
        model_name="openai/gpt-oss-120b",
    )

    return hybrid, explainer


@st.cache_data
def load_users():
    df = pd.read_csv(USER_CSV)
    return sorted(df["user_id"].unique().tolist())


hybrid_model, explainer = load_models()
user_ids = load_users()


st.sidebar.header(" Controls")

selected_user = st.sidebar.selectbox("Select User ID", user_ids)
top_k = st.sidebar.slider("Number of Recommendations", 1, 10, 5)

run_btn = st.sidebar.button(" Recommend")

if run_btn:
    with st.spinner("Generating recommendations..."):
        recommendations, explanation_signals = hybrid_model.recommend(
            user_id=selected_user,
            top_k=top_k,
        )

    st.success("Recommendations ready!")

    for i, rec in enumerate(recommendations, 1):
        st.subheader(f"{i}. {rec['title']}")
        st.write(f"**Score:** {rec.get('score', 'N/A')}")

        signals = explanation_signals.get(rec["title"], {})
        context = "\n".join(f"{k}: {v}" for k, v in signals.items())

        with st.expander(" Why was this recommended?"):
            explanation = explainer.explain(
                series_title=rec["title"],
                explanation_context=context,
            )
            st.write(explanation)
