from Core.CorePaths import FileReader
import warnings
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
sns.set(style="whitegrid")

def PreProcessingTakeaway(ta_data_root):
    ta_data_root = "C:/Users/bengisu.oniz/PyProjects/Main/Cases/Takeaway/Data/"
    reviews_raw_df = FileReader(ta_data_root).ReadCsv("reviews_Clothing_Shoes_and_Jewelry_5.csv")
    metadata_raw_df = FileReader(ta_data_root).ReadCsv("metadata_category_clothing_shoes_and_jewelry_only.csv")
    reviews_raw_df.rename(columns={'unnamed: 0': 'reviewid'}, inplace=True)

    reviewtime = []
    for index, row in reviews_raw_df.iterrows():
        time = datetime.utcfromtimestamp(row["unixreviewtime"]).strftime('%Y-%m-%d')
        reviewtime.append(time)

    reviews_raw_df["reviewtime_converted"] = reviewtime

    df_review_combined = metadata_raw_df.merge(reviews_raw_df, on=['asin'], how='inner')
    df_review_combined.dropna(subset=['reviewtext'], inplace=True)

    return df_review_combined


























