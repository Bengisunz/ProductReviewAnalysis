from Cases.Takeaway.Codes.TakeawayCase import PreProcessingTakeaway
import pandas as pd
import ast


def CreatingDfBasedOnColumns(columns):
    sub_df = df_review_combined[columns]
    return sub_df

ta_data_root = "C:/Users/bengisu.oniz/PyProjects/Main/Cases/Takeaway/Data/"
df_review_combined = PreProcessingTakeaway(ta_data_root)

#helpfulness_reviews_df = CreatingDfBasedOnColumns(columnnames_helpfulness_reviews)

columns_categories = ["asin","categories"]
categories_df = CreatingDfBasedOnColumns(columns_categories)


def ParseStrDf(s):
    list = []
    s = s.replace("[[", "")
    s = s.replace("]]", "")
    s = s.replace("'", "")
    segments = s.split(',')
    for s in segments:
        list.append(s.strip())
    return list

categories_df['categories_list'] = categories_df['categories'].map(lambda name: ParseStrDf(name))
category_splitted_df = categories_df['categories_list'].apply(pd.Series)

category_splitted_df = category_splitted_df.rename(columns = lambda x : 'category_' + str(x))


for i in (category_splitted_df.columns):
    print(i+ " Nullity Check:", pd.isnull(category_splitted_df[i]).count())


category_splitted_df.fillna("none", inplace=True)

for i in (category_splitted_df.columns):
    num_nones = len(category_splitted_df[category_splitted_df[i]=="none"])
    len_of_column = len(category_splitted_df[i])
    per = num_nones/len_of_column*100
    print(i + " None Check:",num_nones,"len of the column", len_of_column,"percentage of empty columns",per)


for i in (category_splitted_df.columns):
    if category_splitted_df.columns.get_loc(i) > 2:
        category_splitted_df.drop(i, axis=1, inplace=True)


categories_df['categories_list_evalled'] = categories_df['categories'].map(lambda string: ast.literal_eval(string))
category_splitted__second_df = categories_df['categories_list_evalled'].apply(pd.Series)
category_splitted__second_df = category_splitted__second_df.rename(columns = lambda x : 'cat_' + str(x))

first_item_list=[]
second_item_list=[]

for i in range(len(category_splitted__second_df["cat_0"])):
    first_item_list.append(category_splitted__second_df["cat_0"][i][0])
    second_item_list.append(category_splitted__second_df["cat_0"][i][1])




print(df_review_combined["related"].loc[2]+"lkkk")