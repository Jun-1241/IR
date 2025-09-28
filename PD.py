# import pandas as pd

# import os
# os.chdir("C:\\Users\\user\\Desktop\\IR 202508")
# print("目前工作目錄：", os.getcwd())

#======
# 1.DIFF

# # 讀取 CSV
# df = pd.read_csv("C:\\Users\\user\\Desktop\\IR 202508\\data.csv")

# # 確保填寫時間轉為 datetime
# df["填寫時間"] = pd.to_datetime(df["填寫時間"])

# # 只保留至少兩筆紀錄的系統識別碼
# df_filtered = df.groupby("系統識別碼").filter(lambda x: len(x) >= 2)

# # 針對每個系統識別碼，取最舊和最新
# df_two = (
#     df_filtered.sort_values(["系統識別碼", "填寫時間"])
#     .groupby("系統識別碼")
#     .agg({"填寫時間": ["first", "last"], "團隊合作": ["first", "last"]})
# )

# # 扁平化欄位名稱
# df_two.columns = ["填寫時間_舊", "填寫時間_新", "團隊合作_舊", "團隊合作_新"]
# df_two = df_two.reset_index()

# # 計算差值 (新 - 舊)
# df_two["團隊合作差值"] = df_two["團隊合作_新"] - df_two["團隊合作_舊"]

# # 只輸出需要的欄位
# result = df_two[["系統識別碼", "團隊合作差值", "填寫時間_舊", "填寫時間_新"]]

# # 匯出成 CSV
# result.to_csv("團隊合作差值.csv", index=False, encoding="utf-8-sig")

# print("已完成輸出：團隊合作差值.csv")
#======

#======
#2. Class

# # 讀取兩個 CSV
# df_diff = pd.read_csv("teamwork_diff.csv")   # 包含 系統識別碼, 團隊合作差值
# df_course = pd.read_csv("總成績.csv")     # 包含 系統識別碼, 學年, 學期, 課號, 班別, 學期總成績, 學分數

# # 只保留有出現在差值表中的識別碼
# df_filtered = df_course[df_course["系統識別碼"].isin(df_diff["系統識別碼"])]

# # 匯出成新 CSV
# df_filtered.to_csv("課程成績_篩選後.csv", index=False, encoding="utf-8-sig")

# print("已完成輸出：課程成績_篩選後.csv")

# df_course_filtered = pd.read_csv("課程成績_篩選後.csv")
# # 合併
# df_merged = pd.merge(df_course_filtered, df_diff, on="系統識別碼", how="inner")
# # 每門課的平均團隊合作差值
# course_effect = (
#     df_merged.groupby("課號")["團隊合作差值"]
#     .mean()
#     .sort_values(ascending=False)
# )
# print(course_effect.head(10))   # 影響最大的前10門課
# print(course_effect.tail(10))   # 影響最小的10門課
# import matplotlib.pyplot as plt

# # 取前20名課程
# top_courses = course_effect.head(20)

# course_effect_weighted = (
#     df_merged.groupby("課號")
#     .apply(lambda x: (x["團隊合作差值"] * x["學分數"]).sum() / x["學分數"].sum())
#     .sort_values(ascending=False)
# )

# plt.figure(figsize=(10,6))

# top_courses.plot(kind="barh")
# plt.xlabel("Average Teamwork Improvement")
# plt.ylabel("Class Code")
# plt.title("Top 20 Courses Impacting Teamwork Improvement")
# plt.gca().invert_yaxis()
# plt.show()

#======

# import pandas as pd

# # 讀取核心識別碼
# df_diff = pd.read_csv("teamwork_diff.csv")
# id_list = set(df_diff["系統識別碼"])

# # 讀取服務學習與工讀
# df_service = pd.read_csv("服務學習.csv")
# df_work = pd.read_csv("工讀時數.csv")

# # 篩選出基準識別碼
# df_service = df_service[df_service["系統識別碼"].isin(id_list)]
# df_work = df_work[df_work["系統識別碼"].isin(id_list)]

# # 加總每個學生的服務學習與工讀時數
# service_sum = df_service.groupby("系統識別碼")["服務學習時數"].sum().reset_index()
# work_sum = df_work.groupby("系統識別碼")["時數"].sum().reset_index()

# # 合併成總表
# df_total_hours = pd.merge(service_sum, work_sum, on="系統識別碼", how="outer").fillna(0)

# # 匯出
# df_total_hours.to_csv("服務與工讀總時數.csv", index=False, encoding="utf-8-sig")
# print("已完成匯出：服務與工讀總時數.csv")

# import pandas as pd

# # 讀取核心識別碼
# df_diff = pd.read_csv("teamwork_diff.csv")
# id_list = set(df_diff["系統識別碼"])

# # 讀取社團資料
# df_leader = pd.read_csv("社團幹部.csv")
# df_club = pd.read_csv("社團參與.csv")

# # 篩選識別碼，只保留有在核心ID裡的
# df_leader = df_leader[df_leader["系統識別碼"].isin(id_list)]
# df_club = df_club[df_club["系統識別碼"].isin(id_list)]

# # 對每個識別碼檢查是否有出現，去重複
# df_leader_binary = df_leader.drop_duplicates(subset=["系統識別碼"])
# df_leader_binary["社團幹部"] = 1

# df_club_binary = df_club.drop_duplicates(subset=["系統識別碼"])
# df_club_binary["社團參與"] = 1

# # 建立完整ID清單，缺的補0
# all_ids = pd.DataFrame({"系統識別碼": list(id_list)})

# # 合併社團幹部資訊
# all_ids = all_ids.merge(df_leader_binary[["系統識別碼","社團幹部"]], 
#                         on="系統識別碼", how="left").fillna(0)
# # 合併社團參與資訊
# all_ids = all_ids.merge(df_club_binary[["系統識別碼","社團參與"]],
#                         on="系統識別碼", how="left").fillna(0)

# # 將欄位轉為整數
# all_ids["社團幹部"] = all_ids["社團幹部"].astype(int)
# all_ids["社團參與"] = all_ids["社團參與"].astype(int)

# # 匯出
# all_ids.to_csv("社團資訊.csv", index=False, encoding="utf-8-sig")
# print("已完成匯出：社團資訊.csv")

# import pandas as pd

# # 讀取團隊合作差值，作為篩選基準
# df_diff = pd.read_csv("teamwork_diff.csv")
# id_list = set(df_diff["系統識別碼"])

# # 讀取排名資料
# df_rank = pd.read_csv("排名.csv")

# # 篩選出有出現在 diff 的學生
# df_rank = df_rank[df_rank["系統識別碼"].isin(id_list)]

# # 計算每個學生的平均成績和平均PR
# df_rank_summary = df_rank.groupby("系統識別碼")[["修課平均成績", "系排PR"]].mean().reset_index()

# # 匯出
# df_rank_summary.to_csv("排名與平均成績.csv", index=False, encoding="utf-8-sig")
# print("已完成輸出：排名與平均成績.csv")

# import pandas as pd
# import os
# os.chdir("C:\\Users\\user\\Desktop\\IR 202508\\分析資料")

# # 讀取各份 CSV
# df_diff = pd.read_csv("teamwork_diff.csv")                # 系統識別碼, 團隊合作差值
# df_hours = pd.read_csv("服務與工讀總時數.csv")           # 系統識別碼, 服務學習時數, 工讀時數
# df_club = pd.read_csv("社團資訊.csv")                     # 系統識別碼, 社團幹部, 社團參與
# df_rank = pd.read_csv("排名與平均成績.csv")               # 系統識別碼, 平均成績, PR

# # 依序合併 (以 df_diff 為基準)
# df_merged = df_diff.copy()
# df_merged = pd.merge(df_merged, df_hours, on="系統識別碼", how="left")
# df_merged = pd.merge(df_merged, df_club, on="系統識別碼", how="left")
# df_merged = pd.merge(df_merged, df_rank, on="系統識別碼", how="left")

# # 如果有缺值（學生沒有服務/工讀/社團/排名資料），填 0
# fill_cols = ["服務學習時數","工讀時數","社團幹部","社團參與","修課平均成績","系排PR"]
# for col in fill_cols:
#     df_merged[col] = df_merged[col].fillna(0)

# # 匯出
# df_merged.to_csv("完整分析資料.csv", index=False, encoding="utf-8-sig")
# print("已完成匯出：完整分析資料.csv")

import pandas as pd
import os
os.chdir("C:\\Users\\user\\Desktop\\IR 202508\\分析資料")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import os

# === 1. 讀取資料 ===
df = pd.read_csv("完整分析資料.csv")

# 數值型變數
num_vars = ["服務學習時數","工讀時數","修課平均成績","系排PR"]
# 類別型變數 (0/1)
cat_vars = ["社團幹部","社團參與"]

# 中文 → 英文對應
num_vars_en = {
    "服務學習時數": "Service Learning Hours",
    "工讀時數": "Part-time Work Hours",
    "修課平均成績": "Average Course Grade",
    "系排PR": "Department Ranking (PR)"
}

cat_vars_en = {
    "社團幹部": "Club Leader",
    "社團參與": "Club Participation"
}

# 建立資料夾
os.makedirs("EDA_Report", exist_ok=True)

# === 2. 數值型散佈圖與相關係數 ===
num_corr = {}
for var in num_vars:
    x = df[var]
    y = df["團隊合作差值"]
    r, p = pearsonr(x, y)
    num_corr[var] = r
    
    plt.figure(figsize=(6,4))
    sns.scatterplot(x=x, y=y)
    sns.regplot(x=x, y=y, scatter=False, color='red')
    plt.xlabel(num_vars_en[var])
    plt.ylabel("Teamwork Score Change")
    plt.title(f"{num_vars_en[var]} vs Teamwork Score Change\nPearson r = {r:.2f}")
    plt.tight_layout()
    plt.savefig(f"EDA_Report/Scatter_{var}.png")
    plt.close()

pd.DataFrame.from_dict(num_corr, orient='index', columns=["Pearson_r"]).to_csv(
    "EDA_Report/Numerical_Variable_Correlation.csv", encoding="utf-8-sig"
)
print("數值型散佈圖與相關係數完成")

# === 3. 類別型箱型圖與平均值標註 ===
cat_summary_list = []
for var in cat_vars:
    plt.figure(figsize=(6,4))
    ax = sns.boxplot(x=var, y="團隊合作差值", data=df)
    
    # 計算平均值
    summary = df.groupby(var)["團隊合作差值"].mean().reset_index()
    summary["Variable"] = cat_vars_en[var]
    cat_summary_list.append(summary)
    
    # 標註平均值在箱型圖上
    for idx, row in summary.iterrows():
        ax.text(idx, row["團隊合作差值"] + 0.01, f"{row['團隊合作差值']:.2f}", 
                horizontalalignment='center', color='black')
    
    plt.xlabel(cat_vars_en[var])
    plt.ylabel("Teamwork Score Change")
    plt.title(f"{cat_vars_en[var]} vs Teamwork Score Change")
    plt.tight_layout()
    plt.savefig(f"EDA_Report/Boxplot_{var}.png")
    plt.close()

df_cat_summary = pd.concat(cat_summary_list, ignore_index=True)
df_cat_summary.to_csv("EDA_Report/Categorical_Variable_Mean.csv", index=False, encoding="utf-8-sig")
print("類別型箱型圖與平均值完成")

# === 4. 完整相關矩陣熱力圖 ===
all_vars = num_vars + cat_vars + ["團隊合作差值"]
corr_all = df[all_vars].corr()

# 中文 → 英文
col_map = {**num_vars_en, **cat_vars_en, "團隊合作差值": "Teamwork Score Change"}
corr_all.rename(index=col_map, columns=col_map, inplace=True)

plt.figure(figsize=(10,8))
sns.heatmap(corr_all, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix of All Variables and Teamwork Score Change", fontsize=14)
plt.tight_layout()
plt.savefig("EDA_Report/Correlation_Matrix.png")
plt.close()
corr_all.to_csv("EDA_Report/Correlation_Matrix.csv", encoding="utf-8-sig")
print("熱力圖完成")
