import pandas as pd

class DataLoader:
    def __init__(self,original_csv:str,processed_csv:str):
        self.original_csv=original_csv
        self.processed_csv=processed_csv

    def process(self):
        df=pd.read_csv(self.original_csv, encoding='utf-8',on_bad_lines="skip").dropna()
        required_cols = {"series_id","title","overview","genre_ids","rating"}
        missing=required_cols - set(df.columns)
        if missing: 
            raise ValueError(f"Missing required columns: {missing}")
        df['combined_info']=(
            "Series ID: " + df['series_id'].astype(str) +
            "Title: " + df['title'].astype(str) +
            "Overview: " + df['overview'].astype(str) +
            "Genres: " + df['genre_ids'].astype(str)+
            "Rating: " + df['rating'].astype(str)
        )
        df[["series_id", "title", "combined_info"]].to_csv(self.processed_csv,index=False,encoding="utf-8")
        return self.processed_csv

    def user_process(self):
        df=pd.read_csv(self.original_csv, encoding='utf-8',on_bad_lines="skip").dropna()
        required_cols = {"user_id","series_id","interaction_type","rating","completion_pct"}
        missing=required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        df["rating"]=df["rating"].astype(float)
        df['completion_pct']=df['completion_pct'].astype(float)

        def interaction_score(row):
            score = (row["rating"] / 5) + (row["completion_pct"] / 100)
            if row["interaction_type"] == "like":
                score += 0.5
            return score
        
        df['interaction_score']=df.apply(interaction_score, axis=1)
        df = df.groupby( ["user_id", "series_id"], as_index=False)["interaction_score"].mean()
        df.to_csv(self.processed_csv, index=False, encoding="utf-8")
        return self.processed_csv
    