import pandas as pd

def shop_conf_fee_calculate():
    return False


exl1 = pd.read_excel('./quotation.xlsx', header=0)
# print(exl1)
# filtered_rows = exl1[(exl1['渠道类型'].str.contains('OA普船海派', na=False, case=False)) &
#                    (exl1['收货仓'].str.contains('LGB8 92376-8624', na=False, case=False))]

# print(filtered_rows)

df_query1 = exl1[exl1['渠道类型'].str.contains('OA普船海派', case=False)]
df_query2 = exl1[exl1['收货仓'].str.contains('LGB8 92376-8624', case=False)]
# query_result = exl1[(exl1['渠道类型'] == 'OA普船海派') & (exl1['收货仓'] == 'LGB8 92376-8624')]
# query_result = exl1[exl1['渠道类型'].str.contains('OA普船海派', case=False) & exl1['收货仓'].str.contains('LGB8 92376-8624', case=False)]
query_result = pd.concat([df_query1, df_query2]).drop_duplicates()

# 输出查询结果
print(query_result)

exl2 = pd.read_excel('./sources/aaa.xlsx', header=0)

# for index, row in exl2.iterrows():
#     print(row)
    

