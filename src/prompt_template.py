class PromptTemplates:
    """
    Central place for all prompt templates used in the project.
    """

    @staticmethod
    def recommendation_explanation():
        """
        Explains why a particular web series was recommended to a user.
        """

        input_variables = [
            "series_title",
            "context",
        ]

        template = """
You are an explainable AI assistant for a web series recommender system.

Recommended series:
{series_title}

Recommendation context and signals:
{context}

Explain clearly and in simple language why this series
was recommended to the user. Do not mention embeddings,
vector databases, or internal system details. Focus on
the content similarity, user preferences, and what makes
this series a good match.
"""

        return template, input_variables

    @staticmethod
    def user_profile_summary():
        """
        Summarizes a user's viewing preferences.
        """

        input_variables = ["user_history"]

        template = """
You are given a user's viewing history and interaction scores.

User interaction data:
{user_history}

Summarize the user's preferences in 2–3 short sentences.
Focus on genres, themes, and viewing behavior.
"""

        return template, input_variables

    @staticmethod
    def cold_start_explanation():
        """
        Used when the user has little or no interaction history.
        """

        input_variables = ["series_description"]

        template = """
You are an explainable recommender system.

The user has limited viewing history.
The following series is being recommended based on
content similarity and general popularity.

Series description:
{series_description}

Explain the recommendation clearly and concisely.
"""

        return template, input_variables
