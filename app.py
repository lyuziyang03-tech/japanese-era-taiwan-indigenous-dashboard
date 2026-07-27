# ------------------------------------------------------------
# 1. 所需modules
# ------------------------------------------------------------

# 用streamlit做dashboard
import streamlit as st

# 用pandas處理表格數據
import pandas as pd

# ------------------------------------------------------------
# 2. 基本信息
# ------------------------------------------------------------

# 瀏覽器顯示的名字和佈局
st.set_page_config(
    page_title="歷年高山族戶口",
    layout="wide"
)

# 主頁標題（title）
st.title("歷年高山族戶口（1906-1942）")

# 解釋（markdown）
st.markdown(
    """
    本可視化展板的數據來自1946年台灣省行政長官公署接收臺灣總督府總督官房統計課業務時，彙編的《臺灣五十一年來統計提要》。
    
    中央研究院已將此書數位化，開放瀏覽及下載（http://twstudy.iis.sinica.edu.tw/twstatistic50/index.htm）。

    本展板展示原書“統計戶口調查”部分的表53“歷年高山族戶口”。
    """
)

# ------------------------------------------------------------
# 3. 加載數據
# ------------------------------------------------------------

# 讀取csv
csv_file = "歷年高山族戶口.csv"

# 建立 DataFrame
df = pd.read_csv(
    csv_file,
    na_values=["."]
)

df["Year"] = pd.to_numeric(
    df["Year"]
)

df = df.sort_values("Year")

# 數值格式化函數
def format_number(value):
    if pd.isna(value):
        return "無資料"
    return f"{int(value):,}"

# ------------------------------------------------------------
# 4. 可調邊欄（sidebar）
# ------------------------------------------------------------

st.sidebar.header("調整 Dashboard")

st.sidebar.markdown(
    """
    可以在此調整分析方式與資料範圍。
    """
)

# 選擇分析模式
analysis_type = st.sidebar.radio(
    "選擇分析模式",
    [
        "單一年份分析",
        "歷年趨勢分析"
    ]
)

# ------------------------------------------------------------
# 單一年份分析
# ------------------------------------------------------------

if analysis_type == "單一年份分析":

    # 選擇要查看的年份
    selected_year = st.sidebar.selectbox(
        "選擇年份",
        sorted(df["Year"].unique()),
        index=len(df["Year"].unique()) - 1
    )

    # 篩選指定年份資料
    filtered_df = df[
        df["Year"] == selected_year
    ]

# ------------------------------------------------------------
# 歷年趨勢分析
# ------------------------------------------------------------

else:

    # 選擇年份範圍
    year_range = st.sidebar.slider(
        "選擇年份範圍",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=(
            int(df["Year"].min()),
            int(df["Year"].max())
        )
    )

    # 篩選年份區間資料
    filtered_df = df[
        (df["Year"] >= year_range[0]) &
        (df["Year"] <= year_range[1])
    ]

# ------------------------------------------------------------
# 5. 單一年份分析展示
# ------------------------------------------------------------

if analysis_type == "單一年份分析":

    # --------------------------------------------------------
    # 單一年份基本信息摘要
    # --------------------------------------------------------
    
    # 取得選定年份資料
    year_data = filtered_df.iloc[0]

    st.markdown("## 年份摘要")

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        st.metric(
            "年份",
            int(year_data["Year"])
        )

    with col2:
        st.metric(
            "戶數",
            format_number(year_data["Households"])
        )

    with col3:
        st.metric(
            "高山族總人口",
            format_number(year_data["Total_Population"])
        )

    with col4:
        st.metric(
            "男性人口",
            format_number(year_data["Total_Male"])
        )

    with col5:
        st.metric(
            "女性人口",
            format_number(year_data["Total_Female"])
        )

    with col6:
        st.metric(
            "有配偶者",
            format_number(year_data["Married_Persons"])
        )

    with col7:
        st.metric(
            "壯丁數",
            format_number(year_data["Adult_Males"])
        )

    # --------------------------------------------------------
    # 單一年份
    # --------------------------------------------------------

    # 建立民族資料表
    ethnic_chart = pd.DataFrame({
        "男性 Male": [
            year_data["Atayal_Male"],
            year_data["Saisiyat_Male"],
            year_data["Bunun_Male"],
            year_data["Tsou_Male"],
            year_data["Paiwan_Male"],
            year_data["Amis_Male"],
            year_data["Yami_Male"],
            year_data["Other_Male"]
        ],

        "女性 Female": [
            year_data["Atayal_Female"],
            year_data["Saisiyat_Female"],
            year_data["Bunun_Female"],
            year_data["Tsou_Female"],
            year_data["Paiwan_Female"],
            year_data["Amis_Female"],
            year_data["Yami_Female"],
            year_data["Other_Female"]
        ]
    }, index=[
        "泰雅族 Atayal",
        "賽夏族 Saisiyat",
        "布農族 Bunun",
        "鄒族 Tsou",
        "排灣族 Paiwan",
        "阿美族 Amis",
        "雅美族 Yami",
        "其他 Other"
    ])


    # 計算總人口
    ethnic_chart["總人口 Total"] = (
        ethnic_chart["男性 Male"] +
        ethnic_chart["女性 Female"]
    )


    # 顯示柱狀圖
    st.bar_chart(
        ethnic_chart
    )
    
    # --------------------------------------------------------
    # 單一年份族群摘要
    # --------------------------------------------------------

    st.markdown("## 族群結構摘要")


    # 泰雅族人口
    atayal_total = (
        year_data["Atayal_Male"] +
        year_data["Atayal_Female"]
    )


    # 泰雅族占全部高山族比例
    atayal_ratio = (
        atayal_total /
        year_data["Total_Population"] *
        100
    )


    # 找人口最多民族
    largest_ethnic = (
        ethnic_chart["總人口 Total"]
        .idxmax()
    )

    largest_population = (
        ethnic_chart["總人口 Total"]
        .max()
    )


    # 泰雅族男女比例
    atayal_male_ratio = (
        year_data["Atayal_Male"] /
        atayal_total *
        100
    )
    
    atayal_male_ratio = (
        year_data["Atayal_Female"] /
        atayal_total *
        100
    )


    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:
        st.metric(
            "泰雅族人口",
            format_number(atayal_total)
        )


    with col2:
        st.metric(
            "泰雅族占比",
            f"{atayal_ratio:.1f}%"
        )


    with col3:
        st.metric(
            "人口最多民族",
            largest_ethnic,
            f"{format_number(largest_population)} 人"
        )


    with col4:
        st.metric(
            "泰雅族男性比例",
            f"{atayal_male_ratio:.1f}%"
        )

    with col5:
        st.metric(
            "泰雅族女性比例",
            f"{atayal_male_ratio:.1f}%"
        )
    
# ------------------------------------------------------------
# 6. 歷年趨勢分析
# ------------------------------------------------------------

elif analysis_type == "歷年趨勢分析":

    st.markdown("## 歷年人口變化趨勢")


    # --------------------------------------------------------
    # 1. 各民族總人口與高山族總人口變化
    # --------------------------------------------------------

    st.markdown("### 各民族與總人口變化")

    ethnic_trend = pd.DataFrame({
        "總人口 Total Population": filtered_df["Total_Population"],

        "泰雅族 Atayal": (
            filtered_df["Atayal_Male"] +
            filtered_df["Atayal_Female"]
        ),

        "賽夏族 Saisiyat": (
            filtered_df["Saisiyat_Male"] +
            filtered_df["Saisiyat_Female"]
        ),

        "布農族 Bunun": (
            filtered_df["Bunun_Male"] +
            filtered_df["Bunun_Female"]
        ),

        "鄒族 Tsou": (
            filtered_df["Tsou_Male"] +
            filtered_df["Tsou_Female"]
        ),

        "排灣族 Paiwan": (
            filtered_df["Paiwan_Male"] +
            filtered_df["Paiwan_Female"]
        ),

        "阿美族 Amis": (
            filtered_df["Amis_Male"] +
            filtered_df["Amis_Female"]
        ),

        "雅美族 Yami": (
            filtered_df["Yami_Male"] +
            filtered_df["Yami_Female"]
        ),

        "其他 Other": (
            filtered_df["Other_Male"] +
            filtered_df["Other_Female"]
        )
    })


    ethnic_trend.index = filtered_df["Year"]

    st.line_chart(
        ethnic_trend
    )

    # --------------------------------------------------------
    # 2. 泰雅族男女人口變化
    # --------------------------------------------------------

    st.markdown("### 泰雅族男女人口變化")

    atayal_trend = pd.DataFrame({

        "泰雅族男性 Atayal Male":
            filtered_df["Atayal_Male"],

        "泰雅族女性 Atayal Female":
            filtered_df["Atayal_Female"]

    })


    atayal_trend.index = filtered_df["Year"]


    st.line_chart(
        atayal_trend
    )
    
    # --------------------------------------------------------
    # 歷年變化摘要
    # --------------------------------------------------------

    st.markdown("### 年代變化摘要")


    start_data = filtered_df.iloc[0]
    end_data = filtered_df.iloc[-1]


    # 泰雅族起始與結束人口

    atayal_start = (
        start_data["Atayal_Male"] +
        start_data["Atayal_Female"]
    )

    atayal_end = (
        end_data["Atayal_Male"] +
        end_data["Atayal_Female"]
    )


    # 泰雅族增長率

    atayal_growth = (
        (atayal_end - atayal_start)
        /
        atayal_start
        *
        100
    )


    # 全體人口增長率

    total_growth = (
        (
            end_data["Total_Population"]
            -
            start_data["Total_Population"]
        )
        /
        start_data["Total_Population"]
        *
        100
    )


    # 泰雅族比例變化

    atayal_ratio_start = (
        atayal_start /
        start_data["Total_Population"]
        *
        100
    )

    atayal_ratio_end = (
        atayal_end /
        end_data["Total_Population"]
        *
        100
    )


    ratio_change = (
        atayal_ratio_end -
        atayal_ratio_start
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.metric(
            "分析期間",
            f"{int(start_data['Year'])}-{int(end_data['Year'])}"
        )


    with col2:
        st.metric(
            "泰雅族人口增長率",
            f"{atayal_growth:.1f}%"
        )


    with col3:
        st.metric(
            "高山族總人口增長率",
            f"{total_growth:.1f}%"
        )


    with col4:
        st.metric(
            "泰雅族人口比例變化",
            f"{ratio_change:+.1f}%"
        )

# ------------------------------------------------------------
# 7. 原始數據展示
# ------------------------------------------------------------

st.markdown("## 查看資料")

st.markdown(
    """
    下方表格展示用於圖表分析的篩選後資料。
    可以幫助使用者驗證可視化結果是否基於正確的資料列與欄位。
    """
)

st.dataframe(filtered_df, use_container_width=True)
