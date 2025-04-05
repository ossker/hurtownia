def create_dict(df):
    return df.groupby('woj')['uczelnia'].apply(list).to_dict()

def transform_excel(df) -> dict:
    df = df.dropna(subset=["woj", "uczelnia"])
    df["woj"] = df["woj"].str.strip()
    df["uczelnia"] = df["uczelnia"].str.strip()
    df = df.drop_duplicates()
    uni_dict = create_dict(df)
    return uni_dict
