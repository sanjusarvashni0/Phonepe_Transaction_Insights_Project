import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📱 PhonePe Transaction Insights", layout="wide")

st.title("📊 PhonePe Business Case Analysis Dashboard")

# Create 5 tabs for 5 business cases
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Case 1: Transaction Dynamics",
    "Case 2: Device Dominance",
    "Case 3: Insurance Penetration",
    "Case 4: State & District Transactions",
    "Case 5: User Engagement"
])

with tab1:
    st.header("📈 Case 1: Decoding Transaction Dynamics on PhonePe")

    # Load CSVs
    q1 = pd.read_csv("data/c1_q1.csv")
    q2 = pd.read_csv("data/c1_q2.csv")
    q3 = pd.read_csv("data/c1_q3.csv")
    q4 = pd.read_csv("data/c1_q4.csv")
    q5 = pd.read_csv("data/c1_q5.csv")

    # Query 1
    st.subheader("Query 1: Total Transaction Amount and Count by Year")
    fig1 = px.line(q1, x='Year', y=['Total_Transactions', 'Total_Amount'],
                   markers=True, title="Yearly Transaction Trends")
    st.plotly_chart(fig1, use_container_width=True)

    # Query 2
    st.subheader("Query 2: Top 10 States by Total Transaction Amount")
    fig2 = px.bar(q2, x='State', y='Total_Transaction_Amount',
                  color='State', title="Top States by Transaction Amount")
    st.plotly_chart(fig2, use_container_width=True)

    # Query 3
    st.subheader("Query 3: Average Transaction Value by State")
    fig3 = px.bar(q3, x='State', y='Average_Transaction_Value',
                  color='Average_Transaction_Value',
                  title="States with Highest Average Transaction Value")
    fig3.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)

    # Query 4
    st.subheader("Query 4: Transaction Trends by Payment Type Over Time")
    fig4 = px.bar(q4, x='Year', y='Total_Amount', color='Transaction_Type',
                  barmode='group', title="Payment Type Distribution Over Years")
    st.plotly_chart(fig4, use_container_width=True)

    # Query 5
    st.subheader("Query 5: Top 5 Districts by Transaction Amount (Latest Year)")
    fig5 = px.bar(q5, x='District', y='Total_Transaction_Amount',
                  color='State', title="Top Performing Districts")
    st.plotly_chart(fig5, use_container_width=True)


with tab2:
    st.header("📱 Case 2: Device Dominance and User Engagement Analysis")

    # --- Load Data ---
    q6 = pd.read_csv("data/c2_q6.csv")
    q7 = pd.read_csv("data/c2_q7.csv")
    q8 = pd.read_csv("data/c2_q8.csv")
    q9 = pd.read_csv("data/c2_q9.csv")
    q10 = pd.read_csv("data/c2_q10.csv")

    # --- Consistent Colors for Device Brands ---
    brand_colors = {
        "Xiaomi": "#F5761A", "Samsung": "#0D6EFD", "Vivo": "#8B5CF6",
        "Oppo": "#22C55E", "Realme": "#EAB308", "Apple": "#9CA3AF",
        "OnePlus": "#DC2626", "Motorola": "#0891B2", "Huawei": "#10B981",
        "Tecno": "#2563EB", "Lenovo": "#7C3AED", "Infinix": "#16A34A",
        "Asus": "#F97316", "Micromax": "#A855F7", "Lava": "#EA580C",
        "Gionee": "#F59E0B", "HMD Global": "#14B8A6", "Lyf": "#6B7280",
        "COOLPAD": "#71717A", "Others": "#9CA3AF"
    }

    # --- QUERY 6 ---
    st.subheader("Query 6: Yearly Growth of Registered Users & App Opens")
    fig6 = px.line(
        q6, x='Year', y=['Total_Registered_Users', 'Total_App_Opens'],
        markers=True, title="Yearly Growth in Registered Users and App Opens"
    )
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("""
    **Insight:** App engagement grew sharply post-2019, highlighting user adoption 
    and the maturing digital ecosystem after 2020.
    """)

    # --- QUERY 7 ---
    st.subheader("Query 7: Top 10 Device Brands by Registered Users (Latest Year)")
    fig7 = px.bar(
        q7, x='Device_Brand', y='Total_Registered_Users',
        color='Device_Brand', color_discrete_map=brand_colors,
        text='Total_Registered_Users',
        title="Top 10 Device Brands by Registered Users"
    )
    fig7.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown("""
    **Insight:** Vivo, Xiaomi, and Samsung dominate the user base, 
    confirming mid-range Android phones as PhonePe’s strongest demographic.
    """)

    # --- QUERY 8 ---
    st.subheader("Query 8: Engagement Rate (App Opens per Registered User) by Brand")
    fig8 = px.bar(
        q8.sort_values(by='Engagement_Rate', ascending=False).head(10),
        x='Device_Brand', y='Engagement_Rate', color='Device_Brand',
        color_discrete_map=brand_colors,
        title="Top 10 Brands by Engagement Rate"
    )
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown("""
    **Insight:** Tecno, OnePlus, and Apple users show higher loyalty and app-open frequency, 
    suggesting premium-segment engagement opportunities.
    """)

    # --- QUERY 9 ---
    st.subheader("Query 9: Device Dominance by State")

    # Find dominant device brand per state
    state_device = (
        q9.groupby("State")
        .apply(lambda x: x.loc[x['Top_Registered_Users'].idxmax()])
        .reset_index(drop=True)
    )

    # Working India geoJSON
    india_states = "https://raw.githubusercontent.com/plotly/datasets/master/india_states.geojson"

    # Create the choropleth map
    fig9 = px.choropleth(
        state_device,
        geojson=india_states,
        featureidkey="properties.ST_NM",
        locations="State",
        color="Device_Brand",
        color_discrete_map=brand_colors,
        title="Dominant Device Brand by State",
        hover_name="State"
    )

    fig9.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig9, use_container_width=True)

    st.markdown("""
    **Insight:** Each state has a dominant device brand. 
    Southern India shows higher Vivo and Realme dominance, 
    while Northern India leans toward Xiaomi and Samsung.
    """)

    # --- QUERY 10 ---
    st.subheader("Query 10: Underutilized Devices (High Users, Low Engagement)")
    underutilized = q10[q10["Engagement_Rate"] < q10["Engagement_Rate"].mean()]
    fig10 = px.scatter(
        underutilized, x='Total_Registered_Users', y='Engagement_Rate',
        color='Device_Brand', color_discrete_map=brand_colors,
        size='Total_Registered_Users',
        title="Underutilized Devices — High Users but Low Engagement",
        hover_name='Device_Brand'
    )
    st.plotly_chart(fig10, use_container_width=True)
    st.markdown("""
    **Insight:** Brands like Micromax and Lava have significant user bases but lag in engagement, 
    suggesting potential for reactivation campaigns.
    """)

with tab3:
    st.header("💼 Case 3: Insurance Penetration and Growth Potential Analysis")

    # Load all CSVs
    q11 = pd.read_csv("data/c3_q11.csv")
    q12 = pd.read_csv("data/c3_q12.csv")
    q13 = pd.read_csv("data/c3_q13.csv")
    q14 = pd.read_csv("data/c3_q14.csv")
    q15 = pd.read_csv("data/c3_q15.csv")

    # --- QUERY 11 ---
    st.subheader("Query 11: Yearly Growth in Insurance Transactions and Amount")
    fig11 = px.line(
        q11, 
        x='Year', 
        y=['Total_Transactions', 'Total_Amount'], 
        markers=True, 
        title="Yearly Growth of Insurance Transactions and Amount"
    )
    st.plotly_chart(fig11, use_container_width=True)
    st.markdown("""
    **Insight:** Both insurance transactions and total amount have shown consistent year-on-year growth, 
    reflecting rising financial awareness and adoption of digital insurance services.
    """)

    # --- QUERY 12 ---
    st.subheader("Query 12: Top 10 States by Total Insurance Transaction Amount")
    fig12 = px.bar(
        q12, 
        x='State', 
        y='Total_Amount', 
        color='Total_Amount',
        text_auto='.2s',
        title="Top 10 States by Insurance Transaction Value"
    )
    fig12.update_traces(textposition='outside')
    st.plotly_chart(fig12, use_container_width=True)
    st.markdown("""
    **Insight:** Telangana, Karnataka, and Maharashtra dominate in insurance transaction value, 
    showing strong market maturity and digital adoption.
    """)

    # --- QUERY 13 ---
    st.subheader("Query 13: Average Transaction Value by State")
    fig13 = px.choropleth(
        q13,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13b9bef6a490ee44a4a8b3f7d80a3/raw/3b50b36a97b092b6c80d59b0e6e1b0b3b9b1b2f3/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="State",
        color="Avg_Transaction_Value",
        color_continuous_scale="Blues",
        title="Average Insurance Transaction Value by State"
    )
    fig13.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig13, use_container_width=True)
    st.markdown("""
    **Insight:** Northern and northeastern states such as Ladakh, Arunachal Pradesh, and Sikkim 
    exhibit higher average transaction values, possibly due to niche or high-value insurance products.
    """)

    # --- QUERY 14 ---
    st.subheader("Query 14: Year-over-Year Growth in Insurance Transactions")
    fig14 = px.bar(
        q14, 
        x='Year', 
        y='YoY_Growth_%', 
        text_auto='.2f',
        color='YoY_Growth_%',
        title="YoY Growth in Insurance Transactions"
    )
    st.plotly_chart(fig14, use_container_width=True)
    st.markdown("""
    **Insight:** The insurance sector witnessed rapid digital expansion between 2020 and 2022, 
    stabilizing with moderate growth from 2023 onwards.
    """)

    # --- QUERY 15 ---
    st.subheader("Query 15: States with Highest YoY Growth (2022–2023)")
    fig15 = px.bar(
        q15.sort_values(by='YoY_Growth_Percentage', ascending=False).head(10),
        x='State',
        y='YoY_Growth_Percentage',
        color='YoY_Growth_Percentage',
        text_auto='.2f',
        title="Top States by YoY Growth in Insurance Transactions (2023)"
    )
    st.plotly_chart(fig15, use_container_width=True)
    st.markdown("""
    **Insight:** Emerging regions like Ladakh, Madhya Pradesh, and northeastern states show 
    exceptionally high growth, indicating untapped market potential and increasing awareness.
    """)

# ------------------ CASE 4 ------------------
with tab4:
    st.header("💳 Case 4: Transaction Analysis Across States and Districts")

    # Load all CSVs
    q16 = pd.read_csv("data/c4_q16.csv")
    q17 = pd.read_csv("data/c4_q17.csv")
    q18 = pd.read_csv("data/c4_q18.csv")
    q19 = pd.read_csv("data/c4_q19.csv")
    q20 = pd.read_csv("data/c4_q20.csv")

    # --- QUERY 16 ---
    st.subheader("Query 16: Top 10 States by Transaction Volume and Amount")
    fig16 = px.bar(
        q16,
        x="State",
        y=["Total_Transactions", "Total_Amount"],
        barmode="group",
        title="Top 10 States by Total Transactions and Amount"
    )
    st.plotly_chart(fig16, use_container_width=True)
    st.markdown("""
    **Insight:** Telangana, Karnataka, and Maharashtra lead in both transaction volume 
    and monetary value, indicating strong digital payment adoption.
    """)

    # --- QUERY 17 ---
    st.subheader("Query 17: Top 10 Districts by Transaction Value")
    fig17 = px.bar(
        q17,
        x="District",
        y="Total_Amount",
        color="Total_Amount",
        title="Top 10 Districts by Total Transaction Amount"
    )
    fig17.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig17, use_container_width=True)
    st.markdown("""
    **Insight:** Bengaluru Urban, Pune, and Hyderabad are high-performing districts, 
    accounting for significant shares of India’s total digital payment value.
    """)

    # --- QUERY 18 ---
    st.subheader("Query 18: Average Transaction Value by District")
    fig18 = px.bar(
        q18,
        x="District",
        y="Avg_Transaction_Value",
        color="Avg_Transaction_Value",
        title="Average Transaction Value Across Top Districts"
    )
    fig18.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig18, use_container_width=True)
    st.markdown("""
    **Insight:** High-value districts tend to be major metros, suggesting that 
    premium transactions are concentrated in urban hubs.
    """)

    # --- QUERY 19 ---
    st.subheader("Query 19: Yearly Transaction Growth by State")
    fig19 = px.line(
        q19,
        x="Year",
        y="Total_Transactions",
        color="State",
        title="Yearly Growth in Transactions per State"
    )
    st.plotly_chart(fig19, use_container_width=True)
    st.markdown("""
    **Insight:** Most states show a steady upward trajectory in transaction counts, 
    with a visible surge post-2020 reflecting digital payment normalization.
    """)

    # --- QUERY 20 ---
    st.subheader("Query 20: Correlation between Transaction Count and Amount by State")
    fig20 = px.bar(
        q20.sort_values(by="Correlation_Count_Amount", ascending=False),
        x="State",
        y="Correlation_Count_Amount",
        color="Correlation_Count_Amount",
        title="Correlation between Transaction Count and Amount by State"
    )
    fig20.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig20, use_container_width=True)
    st.markdown("""
    **Insight:** Northeastern states like Manipur and Nagaland show the strongest 
    positive correlation between transaction volume and total amount — indicating 
    consistent spending patterns across transactions.
    """)

# ------------------ CASE 5 ------------------
with tab5:
    st.header("📱 Case 5: User Engagement and Growth Strategy")

    # Load all CSVs
    q21 = pd.read_csv("data/c5_q21.csv")
    q22 = pd.read_csv("data/c5_q22.csv")
    q23 = pd.read_csv("data/c5_q23.csv")
    q24 = pd.read_csv("data/c5_q24.csv")
    q25 = pd.read_csv("data/c5_q25.csv")

    # --- QUERY 21 ---
    st.subheader("Query 21: Top 10 States by Registered Users and App Opens")
    fig21 = px.bar(
        q21,
        x="State",
        y=["Total_Registered_Users", "Total_App_Opens"],
        barmode="group",
        title="Top 10 States by Total Registered Users and App Opens"
    )
    st.plotly_chart(fig21, use_container_width=True)
    st.markdown("""
    **Insight:** Maharashtra, Karnataka, and Uttar Pradesh dominate both user base 
    and engagement metrics, suggesting these are PhonePe’s strongest adoption regions.
    """)

    # --- QUERY 22 ---
    st.subheader("Query 22: Top 10 States with Highest Engagement Ratio")
    fig22 = px.bar(
        q22,
        x="State",
        y="Engagement_Ratio",
        color="Engagement_Ratio",
        title="Top 10 States by Engagement Ratio"
    )
    fig22.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig22, use_container_width=True)
    st.markdown("""
    **Insight:** Rajasthan and Andhra Pradesh lead in engagement, indicating users here 
    interact more frequently with the app relative to their user base.
    """)

    # --- QUERY 23 ---
    st.subheader("Query 23: States with Lower Engagement Ratios")
    fig23 = px.bar(
        q23,
        x="State",
        y="Engagement_Ratio",
        color="Engagement_Ratio",
        title="States with Low App Engagement Ratios"
    )
    fig23.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig23, use_container_width=True)
    st.markdown("""
    **Insight:** States like West Bengal, Gujarat, and Delhi exhibit lower engagement ratios 
    despite large user counts — indicating potential for targeted reactivation campaigns.
    """)

    # --- QUERY 24 ---
    st.subheader("Query 24: Yearly Growth of Registered Users per State")
    fig24 = px.line(
        q24,
        x="Year",
        y="Total_Registered_Users",
        color="State",
        title="Yearly Growth of Registered Users Across States"
    )
    st.plotly_chart(fig24, use_container_width=True)
    st.markdown("""
    **Insight:** Most states show exponential user growth from 2018 to 2022, 
    with metro states seeing the sharpest rise post-2020.
    """)

    # --- QUERY 25 ---
    st.subheader("Query 25: Year-over-Year Growth Percentage of Registered Users")
    fig25 = px.line(
        q25,
        x="Year",
        y="YoY_Growth_Percentage",
        color="State",
        title="YoY Growth Percentage of Registered Users"
    )
    st.plotly_chart(fig25, use_container_width=True)
    st.markdown("""
    **Insight:** Early adopter states like Karnataka and Telangana show strong initial growth 
    followed by stabilization, whereas emerging regions maintain higher YoY growth percentages.
    """)


