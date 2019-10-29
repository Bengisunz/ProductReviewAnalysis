from Cases.Takeaway.Codes.TakeawayCase import PreProcessingTakeaway
import pandas as pd
import ast

#region Having Main Df
def CreatingDfBasedOnColumns(columns):
    sub_df = df_review_combined[columns]
    return sub_df

ta_data_root = "C:/Users/bengisu.oniz/PyProjects/Main/Cases/Takeaway/Data/"
df_review_combined = PreProcessingTakeaway(ta_data_root)
#endregion


columns_related = ["asin","related"]
related_df = CreatingDfBasedOnColumns(columns_related)
print("Nullity Check:",pd.isnull(related_df).sum())
related_df.dropna(inplace=True)

len_list=[]
for i in range(10,1000,20):
    length= len(related_df["related"].loc[i])
    len_list.append(length)

len_set = set(len_list)

print("Length of the list", len(len_list),"Length of the set",len(len_set))

related_df = (pd.DataFrame(related_df["related"].apply(ast.literal_eval).values.tolist(), index=related_df['asin'])
       .stack()
       .reset_index()
       .rename(columns={'level_1': 'reatednesstype', 0: 'related_producs'})
              )


boughttogether_df= related_df[(related_df['reatednesstype']=="also_bought")]
boughttogether_df.drop('reatednesstype', axis=1, inplace=True)
boughttogether_df.rename(columns={'related_producs': 'products_bought_together'}, inplace=True)

# viewedtogether_df= related_df[(related_df['reatednesstype']=="also_viewed")]
# viewedtogether_df.drop('reatednesstype', axis=1,inplace=True)
# viewedtogether_df.rename(columns={'related_producs': 'products_viewed_together'}, inplace=True)
#
# viewedtogether_splitted_df = viewedtogether_df['products_viewed_together'].apply(pd.Series)
# viewedtogether_splitted_df = viewedtogether_splitted_df.rename(columns = lambda x : 'viewed_together_' + str(x))

boughttogether_splitted_df = boughttogether_df['products_bought_together'].apply(pd.Series)
boughttogether_splitted_df = boughttogether_splitted_df.rename(columns = lambda x : 'bought_together_' + str(x))

productlist = boughttogether_splitted_df.columns
productlist=list(productlist)

for i in productlist:
    index = productlist.index(i)
    if index < 5:
        boughttogether_df[i]=boughttogether_splitted_df[i]


boughttogether_df.drop('products_bought_together', axis=1, inplace=True)

