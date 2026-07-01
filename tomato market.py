import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌾 Tomato Market Intelligence",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #ffffff; color: #1a1a2e; }
.main { background: #f8f9fa; }

.metric-card {
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 16px;
    padding: 18px 22px;
    margin: 7px 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }
.metric-label { color: #6c757d; font-size: 12px; font-weight: 500; margin-bottom: 4px; }
.metric-value { color: #1a1a2e; font-size: 26px; font-weight: 700; }
.metric-sub   { color: #2e7d32; font-size: 11px; margin-top: 3px; font-weight: 500; }

.section-header {
    background: linear-gradient(90deg, #e8f5e9 0%, #f1f8f1 100%);
    border-left: 4px solid #2e7d32;
    border-radius: 0 12px 12px 0;
    padding: 12px 18px;
    margin: 22px 0 14px 0;
    color: #1a1a2e;
    font-size: 17px;
    font-weight: 600;
}

.global-header {
    background: linear-gradient(90deg, #e3f2fd 0%, #e8eaf6 100%);
    border-left: 4px solid #1565c0;
    border-radius: 0 12px 12px 0;
    padding: 12px 18px;
    margin: 22px 0 14px 0;
    color: #1a1a2e;
    font-size: 17px;
    font-weight: 600;
}

.advisory-box {
    background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
    border: 1px solid #a5d6a7;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 10px 0;
    color: #1b5e20;
    font-size: 14px;
    line-height: 1.75;
}

.global-box {
    background: linear-gradient(135deg, #e3f2fd 0%, #e8eaf6 100%);
    border: 1px solid #90caf9;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 10px 0;
    color: #0d47a1;
    font-size: 14px;
    line-height: 1.75;
}

.risk-low    { background: linear-gradient(135deg,#e8f5e9,#f1f8e9); border:1px solid #66bb6a; border-radius:14px; padding:14px 18px; color:#1b5e20; }
.risk-medium { background: linear-gradient(135deg,#fff8e1,#fffde7); border:1px solid #ffca28; border-radius:14px; padding:14px 18px; color:#e65100; }
.risk-high   { background: linear-gradient(135deg,#ffebee,#fce4ec); border:1px solid #ef9a9a; border-radius:14px; padding:14px 18px; color:#b71c1c; }

.forecast-card {
    background: linear-gradient(135deg, #e3f2fd 0%, #e8f5e9 100%);
    border: 1px solid #90caf9;
    border-radius: 14px;
    padding: 16px 20px;
    text-align: center;
}
.forecast-days  { color: #546e7a; font-size: 12px; margin-bottom: 6px; font-weight: 500; }
.forecast-price { color: #1565c0; font-size: 24px; font-weight: 700; }
.forecast-trend { font-size: 16px; margin-top: 5px; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f1f8e9 0%, #e8f5e9 100%);
    border-right: 1px solid #c8e6c9;
}
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 14px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}
.stTabs [data-baseweb="tab-list"] { gap:6px; background:#f1f3f4; border-radius:12px; padding:5px; }
.stTabs [data-baseweb="tab"]      { border-radius:8px; color:#5f6368; font-weight:500; }
.stTabs [aria-selected="true"]    { background:#ffffff !important; color:#1a73e8 !important; box-shadow:0 1px 4px rgba(0,0,0,0.15); }

.hero-banner {
    background: linear-gradient(135deg, #e8f5e9 0%, #e3f2fd 50%, #e8f5e9 100%);
    border: 1px solid #a5d6a7;
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 24px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.hero-title { color: #1a1a2e; font-size: 34px; font-weight: 700; margin: 0; }
.hero-sub   { color: #2e7d32; font-size: 15px; margin-top: 6px; font-weight: 500; }

.country-card {
    background: #ffffff;
    border: 1px solid #bbdefb;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 5px 0;
    box-shadow: 0 1px 6px rgba(21,101,192,0.08);
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_india_data():
    df = pd.read_csv("Tomato_Merged_final_data_Clean.csv")
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date'])
    for col in ['Min Price', 'Max Price', 'Modal Price', 'Arrivals']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df[(df['Modal Price'] > 50) & (df['Modal Price'] < 100000)]
    valid_varieties = ['Local', 'Hybrid', 'Deshi', 'Tomato', 'Other']
    df['Variety'] = df['Variety'].apply(lambda x: x if x in valid_varieties else 'Other')
    valid_grades = ['FAQ', 'Other', 'Large', 'Medium', 'Small', 'Grade A', 'Grade B',
                    'Grade C', 'Non-FAQ', 'Grade Range-1', 'Grade Range-2', 'Grade Range-3']
    df['Grade'] = df['Grade'].apply(lambda x: x if x in valid_grades else 'FAQ')
    df['Month']      = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%B')
    df['Year']       = df['Date'].dt.year
    df['Week']       = df['Date'].dt.isocalendar().week
    return df


@st.cache_data(show_spinner=False)
def load_global_data():
    gdf = pd.read_excel("Tomato_Prices_INR_final_1.xlsx")
    # NOTE: the 'date' column in the source file is unreliable/scrambled.
    # 'DATE' is the correct chronological column and is used for ALL
    # time-based filtering, grouping, and charting in the Global dashboard.
    gdf['DATE'] = pd.to_datetime(gdf['DATE'], errors='coerce')
    gdf = gdf.dropna(subset=['DATE', 'Price_INR'])
    gdf['Price_INR'] = pd.to_numeric(gdf['Price_INR'], errors='coerce')
    gdf = gdf[gdf['Price_INR'] > 0]
    gdf = gdf.sort_values('DATE').reset_index(drop=True)
    gdf['Year']       = gdf['DATE'].dt.year
    gdf['Month']      = gdf['DATE'].dt.month
    gdf['Month_Name'] = gdf['DATE'].dt.strftime('%B')
    # Price per Quintal (1 Quintal = 100 kg)
    gdf['Price_INR_Q'] = gdf['Price_INR'] * 100
    return gdf


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🌾 Market Intelligence")
    st.markdown("---")

    # Dataset selector
    dataset_choice = st.radio(
        "🌍 Dataset",
        ["🇮🇳 India Market", "🌐 Global Market"],
        index=0
    )

    with st.spinner("Loading data..."):
        df  = load_india_data()
        gdf = load_global_data()

    st.markdown("---")

    if dataset_choice == "🇮🇳 India Market":
        st.markdown("#### 🇮🇳 India Filters")
        states = sorted(df['State'].dropna().unique().tolist())
        selected_state = st.selectbox("🗺️ Select State", ["All States"] + states)

        if selected_state != "All States":
            markets = sorted(df[df['State'] == selected_state]['Market'].dropna().unique().tolist())
        else:
            markets = sorted(df['Market'].dropna().unique().tolist())
        selected_market = st.selectbox("🏪 Select Market (Mandi)", ["All Markets"] + markets[:200])

        varieties = ["All"] + sorted(df['Variety'].dropna().unique().tolist())
        selected_variety = st.selectbox("🍅 Tomato Variety", varieties)

        grades = ["All"] + sorted(df['Grade'].dropna().unique().tolist())
        selected_grade = st.selectbox("⭐ Grade", grades)

        date_min = df['Date'].min().date()
        date_max = df['Date'].max().date()
        date_range = st.date_input("📅 Date Range",
                                   value=(date_min, date_max),
                                   min_value=date_min,
                                   max_value=date_max)
        st.markdown("---")
        st.markdown("#### 📊 India Dataset Info")
        st.markdown(f"- **Records:** {len(df):,}")
        st.markdown(f"- **States:** {df['State'].nunique()}")
        st.markdown(f"- **Markets:** {df['Market'].nunique()}")
        st.markdown(f"- **Range:** {date_min} → {date_max}")

    else:
        st.markdown("#### 🌐 Global Filters")
        all_countries = sorted(gdf['country_name'].dropna().unique().tolist())
        selected_countries = st.selectbox("🌎 Country", ["All Countries"] + all_countries)

        # Market list cascades based on selected country
        if selected_countries != "All Countries":
            g_market_pool = sorted(
                gdf[gdf['country_name'] == selected_countries]['market_name'].dropna().unique().tolist()
            )
        else:
            g_market_pool = sorted(gdf['market_name'].dropna().unique().tolist())
        selected_g_market = st.selectbox("🏪 Market", ["All Markets"] + g_market_pool)

        g_years = sorted(gdf['Year'].dropna().unique().tolist())
        selected_g_year = st.selectbox("📅 Year", ["All Years"] + g_years)

        all_commodities = sorted(gdf['commodity_name'].dropna().unique().tolist())
        selected_commodity = st.selectbox("🍅 Commodity", ["All"] + all_commodities)

        st.markdown("---")
        st.markdown("#### 📊 Global Dataset Info")
        st.markdown(f"- **Records:** {len(gdf):,}")
        st.markdown(f"- **Countries:** {gdf['country_name'].nunique()}")
        st.markdown(f"- **Markets:** {gdf['market_name'].nunique()}")
        st.markdown(f"- **Range:** {gdf['DATE'].min().date()} → {gdf['DATE'].max().date()}")

    st.markdown("---")
    st.caption("🚀 Powered by AI Agriculture Intelligence")


# ══════════════════════════════════════════════════════════════════════════════
# FILTER INDIA DATA
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def filter_india(df, state, market, variety, grade, d1, d2):
    mask = (df['Date'].dt.date >= d1) & (df['Date'].dt.date <= d2)
    if state   != "All States":  mask &= df['State']   == state
    if market  != "All Markets": mask &= df['Market']  == market
    if variety != "All":         mask &= df['Variety'] == variety
    if grade   != "All":         mask &= df['Grade']   == grade
    return df[mask].copy()


@st.cache_data
def filter_global(gdf, country, g_market, year, commodity):
    gf = gdf.copy()
    if country != "All Countries":
        gf = gf[gf['country_name'] == country]
    if g_market != "All Markets":
        gf = gf[gf['market_name'] == g_market]
    if year != "All Years":
        gf = gf[gf['Year'] == year]
    if commodity != "All":
        gf = gf[gf['commodity_name'] == commodity]
    return gf


# Apply filters
if dataset_choice == "🇮🇳 India Market":
    if len(date_range) == 2:
        fdf = filter_india(df, selected_state, selected_market,
                           selected_variety, selected_grade,
                           date_range[0], date_range[1])
    else:
        fdf = df.copy()
else:
    fgdf = filter_global(gdf, selected_countries, selected_g_market,
                         selected_g_year, selected_commodity)


# ══════════════════════════════════════════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
if dataset_choice == "🇮🇳 India Market":
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-title">🌾 Tomato Market Intelligence System</div>
      <div class="hero-sub">🇮🇳 India — AI-Powered Price Forecasting • Mandi Analysis • Farmer Advisory</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="hero-banner" style="background:linear-gradient(135deg,#e3f2fd 0%,#e8eaf6 50%,#e3f2fd 100%);border-color:#90caf9;">
      <div class="hero-title">🌍 Global Tomato Price Intelligence</div>
      <div class="hero-sub" style="color:#1565c0;">🌐 International Markets — Cross-Country Price Analysis • Trends • Comparison</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ═══════════════════  INDIA DASHBOARD  ═══════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════════
if dataset_choice == "🇮🇳 India Market":

    avg_modal  = fdf['Modal Price'].mean()
    max_price  = fdf['Modal Price'].max()
    min_price  = fdf['Modal Price'].min()
    avg_arr    = fdf['Arrivals'].mean()
    volatility = (fdf['Modal Price'].std() / avg_modal * 100) if avg_modal > 0 else 0

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("💰 Avg Modal Price", f"₹{avg_modal:,.0f}", "Rs./Quintal")
    k2.metric("📈 Highest Price",   f"₹{max_price:,.0f}", "Max recorded")
    k3.metric("📉 Lowest Price",    f"₹{min_price:,.0f}", "Min recorded")
    k4.metric("🚛 Avg Arrivals",    f"{avg_arr:.1f}",     "Metric Tonnes")
    k5.metric("📊 Volatility",      f"{volatility:.1f}%", "Price Std/Mean")

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Market Analysis",
        "📈 Price Forecast",
        "🏆 Mandi Ranking",
        "🌤️ Seasonal Trends",
        "🍅 Variety & Grade",
        "🗺️ State Intelligence",
        "🚜 Farmer Advisory"
    ])

    # ── TAB 1: MARKET ANALYSIS ───────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">💰 Market Price Analysis</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns([3, 2])
        with col_a:
            daily = fdf.groupby('Date')['Modal Price'].mean().reset_index()
            daily['7D_MA']  = daily['Modal Price'].rolling(7).mean()
            daily['30D_MA'] = daily['Modal Price'].rolling(30).mean()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily['Date'], y=daily['Modal Price'],
                name='Daily Price', line=dict(color='#1565c0', width=1.5), opacity=0.7))
            fig.add_trace(go.Scatter(x=daily['Date'], y=daily['7D_MA'],
                name='7-Day MA', line=dict(color='#e65100', width=2.5)))
            fig.add_trace(go.Scatter(x=daily['Date'], y=daily['30D_MA'],
                name='30-Day MA', line=dict(color='#c62828', width=2.5)))
            fig.update_layout(title='📈 Modal Price Trend with Moving Averages',
                template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=400, legend=dict(orientation='h', yanchor='bottom', y=1.02))
            fig.update_yaxes(title='Price (Rs./Quintal)')
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            fig2 = go.Figure()
            fig2.add_trace(go.Histogram(x=fdf['Modal Price'].clip(0, 15000),
                nbinsx=50, marker_color='#1565c0', opacity=0.8, name='Price Dist'))
            fig2.add_vline(x=avg_modal, line_dash='dash', line_color='#e65100',
                annotation_text=f'Avg: ₹{avg_modal:.0f}')
            fig2.update_layout(title='📊 Price Distribution',
                template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=400, xaxis_title='Modal Price (Rs./Quintal)', yaxis_title='Frequency')
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-header">📦 Supply-Demand Analysis</div>', unsafe_allow_html=True)
        col_c, col_d = st.columns(2)
        with col_c:
            scat_df = fdf.dropna(subset=['Arrivals', 'Modal Price'])
            scat_df = scat_df[(scat_df['Arrivals'] > 0) &
                               (scat_df['Arrivals'] < scat_df['Arrivals'].quantile(0.99))]
            fig3 = px.scatter(scat_df.sample(min(2000, len(scat_df))),
                x='Arrivals', y='Modal Price',
                color='State' if selected_state == 'All States' else 'Market',
                title='🔗 Arrivals vs Modal Price',
                template='plotly_white', opacity=0.6, trendline='ols')
            fig3.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=400)
            st.plotly_chart(fig3, use_container_width=True)

        with col_d:
            fig4 = px.box(fdf[fdf['Modal Price'] < fdf['Modal Price'].quantile(0.95)],
                x='Grade', y='Modal Price', color='Grade',
                title='📦 Price Distribution by Grade', template='plotly_white')
            fig4.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=400, showlegend=False)
            fig4.update_xaxes(tickangle=45)
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown('<div class="section-header">📋 Top Markets Summary</div>', unsafe_allow_html=True)
        mkt_summary = fdf.groupby('Market').agg(
            Avg_Modal=('Modal Price','mean'), Max_Price=('Modal Price','max'),
            Min_Price=('Modal Price','min'), Volatility=('Modal Price','std'),
            Total_Arrivals=('Arrivals','sum'), Records=('Modal Price','count')
        ).round(0).sort_values('Avg_Modal', ascending=False).head(20).reset_index()
        mkt_summary.columns = ['Market','Avg Price','Max Price','Min Price','Std Dev','Total Arrivals','Records']
        st.dataframe(mkt_summary, use_container_width=True, height=400)

    # ── TAB 2: PRICE FORECAST ────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">📈 AI Price Forecasting</div>', unsafe_allow_html=True)
        daily_avg = fdf.groupby('Date')['Modal Price'].mean().reset_index().sort_values('Date')

        if len(daily_avg) >= 14:
            recent_30 = daily_avg.tail(30)['Modal Price'].values
            recent_7  = daily_avg.tail(7)['Modal Price'].values

            x = np.arange(len(recent_30))
            trend_coef = np.polyfit(x, recent_30, 1)[0] if len(recent_30) >= 2 else 0

            base_price = recent_7.mean()
            current_month = daily_avg['Date'].max().month
            monthly_avg = fdf.groupby('Month')['Modal Price'].mean()
            overall_avg = fdf['Modal Price'].mean()
            seasonal_adj = monthly_avg.get(current_month, overall_avg) / overall_avg if overall_avg > 0 else 1

            f7  = max(base_price + trend_coef * 7  * seasonal_adj, 0)
            f15 = max(base_price + trend_coef * 15 * seasonal_adj, 0)
            f30 = max(base_price + trend_coef * 30 * seasonal_adj, 0)

            def trend_icon(cur, fc):
                return "⬆️ Rising" if fc > cur*1.05 else ("⬇️ Falling" if fc < cur*0.95 else "➡️ Stable")

            c1, c2, c3 = st.columns(3)
            for col, days, val in [(c1,7,f7),(c2,15,f15),(c3,30,f30)]:
                with col:
                    st.markdown(f"""<div class="forecast-card">
                        <div class="forecast-days">📅 {days}-Day Forecast</div>
                        <div class="forecast-price">₹{val:,.0f}</div>
                        <div class="forecast-trend">{trend_icon(base_price, val)}</div>
                        <div class="metric-sub">vs current ₹{base_price:,.0f}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            last_date = daily_avg['Date'].max()
            forecast_dates  = [last_date + timedelta(days=i) for i in range(1, 31)]
            forecast_prices = [base_price + trend_coef * i * seasonal_adj for i in range(1, 31)]
            std_price = recent_30.std() if len(recent_30) > 1 else base_price * 0.1
            upper = [p + std_price for p in forecast_prices]
            lower = [max(p - std_price, 0) for p in forecast_prices]

            fig_fc = go.Figure()
            fig_fc.add_trace(go.Scatter(x=daily_avg.tail(60)['Date'], y=daily_avg.tail(60)['Modal Price'],
                name='Historical Prices', line=dict(color='#1565c0', width=2)))
            fig_fc.add_trace(go.Scatter(x=forecast_dates, y=forecast_prices,
                name='30-Day Forecast', line=dict(color='#e65100', width=2.5, dash='dash'),
                mode='lines+markers', marker=dict(size=4)))
            fig_fc.add_trace(go.Scatter(
                x=forecast_dates + forecast_dates[::-1], y=upper + lower[::-1],
                fill='toself', fillcolor='rgba(230,81,0,0.08)',
                line=dict(color='rgba(0,0,0,0)'), name='Confidence Band'))
            fig_fc.add_vline(x=last_date, line_dash='dot', line_color='#9e9e9e')
            fig_fc.update_layout(title='🔮 Price Forecast — Next 30 Days',
                template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=450, yaxis_title='Modal Price (Rs./Quintal)')
            st.plotly_chart(fig_fc, use_container_width=True)

            ci = min(95, max(50, 95 - volatility))
            cm1, cm2, cm3, cm4 = st.columns(4)
            cm1.metric("📊 Current 7-Day Avg", f"₹{base_price:,.0f}")
            cm2.metric("📐 Trend/Day", f"₹{trend_coef:+.1f}")
            cm3.metric("🎯 Confidence Level", f"{ci:.0f}%")
            cm4.metric("📉 Volatility", f"{volatility:.1f}%")
        else:
            st.warning("⚠️ Not enough data for forecasting. Please select a wider date range.")

    # ── TAB 3: MANDI RANKING ─────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">🏆 Mandi Market Ranking & Comparison</div>', unsafe_allow_html=True)

        mkt_df = fdf.groupby(['Market','State']).agg(
            avg_price=('Modal Price','mean'), max_price=('Modal Price','max'),
            std_price=('Modal Price','std'), avg_arrivals=('Arrivals','mean'),
            records=('Modal Price','count')
        ).reset_index()
        mkt_df = mkt_df[mkt_df['records'] >= 5].copy()
        mkt_df['cv']              = (mkt_df['std_price'] / mkt_df['avg_price'] * 100).round(1).fillna(0)
        mkt_df['stability_score'] = (100 - mkt_df['cv']).clip(0, 100)
        mn, mx = mkt_df['avg_price'].min(), mkt_df['avg_price'].max()
        mkt_df['profit_score']    = ((mkt_df['avg_price'] - mn) / (mx - mn) * 100).round(1) if mx > mn else 50
        mkt_df['composite_score'] = (mkt_df['profit_score'] * 0.6 + mkt_df['stability_score'] * 0.4).round(1)
        mkt_df = mkt_df.sort_values('composite_score', ascending=False)

        col_rank1, col_rank2 = st.columns([2, 1])
        with col_rank1:
            top20 = mkt_df.head(20)
            fig_rank = go.Figure(go.Bar(
                x=top20['composite_score'], y=top20['Market'], orientation='h',
                marker=dict(color=top20['composite_score'], colorscale='Viridis',
                    showscale=True, colorbar=dict(title='Score')),
                text=[f"₹{p:.0f}" for p in top20['avg_price']], textposition='outside'))
            fig_rank.update_layout(title='🥇 Top 20 Mandis — Composite Score',
                template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=550, xaxis_title='Composite Score',
                yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_rank, use_container_width=True)

        with col_rank2:
            best = mkt_df.iloc[0]
            most_stable = mkt_df.sort_values('stability_score', ascending=False).iloc[0]
            st.markdown(f"""
            <div class="metric-card"><div class="metric-label">🥇 Best Overall Mandi</div>
            <div class="metric-value" style="font-size:18px;">{best['Market']}</div>
            <div class="metric-sub">{best['State']}</div></div>
            <div class="metric-card"><div class="metric-label">💰 Avg Price</div>
            <div class="metric-value">₹{best['avg_price']:,.0f}</div>
            <div class="metric-sub">Rs./Quintal</div></div>
            <div class="metric-card"><div class="metric-label">📊 Stability Score</div>
            <div class="metric-value">{best['stability_score']:.0f}/100</div>
            <div class="metric-sub">CV: {best['cv']:.1f}%</div></div>
            <div class="metric-card"><div class="metric-label">🏅 Composite Score</div>
            <div class="metric-value">{best['composite_score']:.0f}/100</div>
            <div class="metric-sub">Profit + Stability</div></div>
            <div class="metric-card"><div class="metric-label">🛡️ Most Stable Mandi</div>
            <div class="metric-value" style="font-size:18px;">{most_stable['Market']}</div>
            <div class="metric-sub">Stability: {most_stable['stability_score']:.0f}/100</div></div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">🔵 Price vs Stability Bubble Chart</div>', unsafe_allow_html=True)
        plot_df = mkt_df.head(50).copy()
        plot_df['avg_arrivals'] = pd.to_numeric(plot_df['avg_arrivals'], errors='coerce')
        plot_df['avg_arrivals'] = plot_df['avg_arrivals'].fillna(plot_df['avg_arrivals'].median()).clip(lower=1)
        fig_bubble = px.scatter(plot_df, x='avg_price', y='stability_score',
            size='avg_arrivals', color='State', hover_name='Market',
            size_max=40, template='plotly_white')
        fig_bubble.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=450,
            xaxis_title='Avg Modal Price (Rs./Quintal)', yaxis_title='Stability Score')
        st.plotly_chart(fig_bubble, use_container_width=True)

        st.markdown('<div class="section-header">📋 Complete Mandi Table</div>', unsafe_allow_html=True)
        display_df = mkt_df[['Market','State','avg_price','max_price','cv',
                              'stability_score','profit_score','composite_score','records']].copy()
        display_df.columns = ['Market','State','Avg Price (₹)','Max Price (₹)',
                              'CV%','Stability','Profit Score','Composite Score','Records']
        st.dataframe(display_df.round(1), use_container_width=True, height=400)

    # ── TAB 4: SEASONAL TRENDS ───────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-header">🌤️ Seasonal & Monthly Price Patterns</div>', unsafe_allow_html=True)

        monthly = fdf.groupby(['Year','Month','Month_Name'])['Modal Price'].agg(['mean','std','count']).reset_index()
        monthly.columns = ['Year','Month','Month_Name','Avg_Price','Std_Price','Count']

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            month_overall = fdf.groupby(['Month','Month_Name'])['Modal Price'].mean().reset_index().sort_values('Month')
            best_month  = month_overall.loc[month_overall['Modal Price'].idxmax(), 'Month_Name']
            worst_month = month_overall.loc[month_overall['Modal Price'].idxmin(), 'Month_Name']
            fig_month = go.Figure(go.Bar(
                x=month_overall['Month_Name'], y=month_overall['Modal Price'],
                marker=dict(color=month_overall['Modal Price'], colorscale='RdYlGn', showscale=True),
                text=[f"₹{p:.0f}" for p in month_overall['Modal Price']], textposition='outside'))
            fig_month.update_layout(title='📅 Average Price by Month',
                template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=400, yaxis_title='Avg Modal Price (Rs./Quintal)')
            st.plotly_chart(fig_month, use_container_width=True)
            st.markdown(f"""
            <div class="metric-card"><div class="metric-label">🌟 Best Month to Sell</div>
            <div class="metric-value">{best_month}</div>
            <div class="metric-sub">Historically highest average price</div></div>
            <div class="metric-card"><div class="metric-label">⚠️ Worst Month to Sell</div>
            <div class="metric-value">{worst_month}</div>
            <div class="metric-sub">Historically lowest average price</div></div>
            """, unsafe_allow_html=True)

        with col_s2:
            month_order = ["January","February","March","April","May","June",
                           "July","August","September","October","November","December"]
            if fdf['Year'].nunique() > 1:
                monthly_sorted = monthly.copy()
                monthly_sorted['Month_Name'] = pd.Categorical(monthly_sorted['Month_Name'],
                    categories=month_order, ordered=True)
                monthly_sorted = monthly_sorted.sort_values(['Year','Month_Name'])
                fig_yoy = px.line(monthly_sorted, x='Month_Name', y='Avg_Price', color='Year',
                    title='📊 Year-over-Year Monthly Comparison',
                    template='plotly_white', markers=True)
                fig_yoy.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=400,
                    yaxis_title='Avg Modal Price (Rs./Quintal)')
                st.plotly_chart(fig_yoy, use_container_width=True)
            else:
                weekly = fdf.groupby('Week')['Modal Price'].mean().reset_index()
                fig_wk = px.line(weekly, x='Week', y='Modal Price',
                    title='📊 Weekly Average Price', template='plotly_white', markers=True)
                fig_wk.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=400)
                st.plotly_chart(fig_wk, use_container_width=True)

        if fdf['Year'].nunique() > 1:
            st.markdown('<div class="section-header">🌡️ Monthly Price Heatmap</div>', unsafe_allow_html=True)
            heat_df = fdf.groupby(['Year','Month'])['Modal Price'].mean().reset_index()
            heat_pivot = heat_df.pivot(index='Year', columns='Month', values='Modal Price')
            mn_map = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                      7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
            heat_pivot.columns = [mn_map.get(c,c) for c in heat_pivot.columns]
            fig_heat = go.Figure(go.Heatmap(
                z=heat_pivot.values, x=heat_pivot.columns.tolist(),
                y=[str(y) for y in heat_pivot.index.tolist()],
                colorscale='RdYlGn',
                text=[[f"₹{v:.0f}" if not np.isnan(v) else "" for v in row] for row in heat_pivot.values],
                texttemplate='%{text}', colorbar=dict(title='Price (₹)')))
            fig_heat.update_layout(title='🌡️ Price Heatmap — Year × Month',
                template='plotly_white', paper_bgcolor='#ffffff', height=300)
            st.plotly_chart(fig_heat, use_container_width=True)

    # ── TAB 5: VARIETY & GRADE ───────────────────────────────────────────────
    with tab5:
        st.markdown('<div class="section-header">🍅 Variety & Grade Performance Analysis</div>', unsafe_allow_html=True)

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            var_df = fdf.groupby('Variety').agg(
                avg_price=('Modal Price','mean'), max_price=('Modal Price','max'),
                std_price=('Modal Price','std'), count=('Modal Price','count')
            ).reset_index().sort_values('avg_price', ascending=False)
            fig_var = px.bar(var_df, x='Variety', y='avg_price',
                color='avg_price', color_continuous_scale='Viridis',
                title='🍅 Average Price by Variety', template='plotly_white',
                text=[f"₹{p:.0f}" for p in var_df['avg_price']])
            fig_var.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=400, yaxis_title='Avg Modal Price', showlegend=False)
            fig_var.update_traces(textposition='outside')
            st.plotly_chart(fig_var, use_container_width=True)
            best_var = var_df.iloc[0]
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">🏆 Top Performing Variety</div>
                <div class="metric-value">{best_var['Variety']}</div>
                <div class="metric-sub">Avg ₹{best_var['avg_price']:,.0f}/Quintal</div>
            </div>""", unsafe_allow_html=True)

        with col_v2:
            grade_df = fdf.groupby('Grade').agg(
                avg_price=('Modal Price','mean'), count=('Modal Price','count')
            ).reset_index()
            grade_df = grade_df[grade_df['count'] >= 10].sort_values('avg_price', ascending=False)
            fig_grade = px.bar(grade_df, x='Grade', y='avg_price',
                color='avg_price', color_continuous_scale='RdYlGn',
                title='⭐ Average Price by Grade', template='plotly_white',
                text=[f"₹{p:.0f}" for p in grade_df['avg_price']])
            fig_grade.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=400, yaxis_title='Avg Modal Price', showlegend=False)
            fig_grade.update_traces(textposition='outside')
            fig_grade.update_xaxes(tickangle=45)
            st.plotly_chart(fig_grade, use_container_width=True)

        st.markdown('<div class="section-header">📈 Variety Price Trends Over Time</div>', unsafe_allow_html=True)
        var_time = fdf.groupby(['Date','Variety'])['Modal Price'].mean().reset_index()
        fig_vt = px.line(var_time, x='Date', y='Modal Price', color='Variety',
            title='🍅 Variety Price Trends', template='plotly_white')
        fig_vt.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=400,
            yaxis_title='Avg Modal Price (Rs./Quintal)')
        st.plotly_chart(fig_vt, use_container_width=True)

        st.markdown('<div class="section-header">🌡️ Variety × Grade Price Matrix</div>', unsafe_allow_html=True)
        vg_df = fdf.groupby(['Variety','Grade'])['Modal Price'].mean().reset_index()
        vg_pivot = vg_df.pivot(index='Variety', columns='Grade', values='Modal Price')
        valid_grades_vg = [c for c in vg_pivot.columns if vg_pivot[c].notna().sum() >= 2]
        vg_pivot = vg_pivot[valid_grades_vg]
        fig_vg = go.Figure(go.Heatmap(
            z=vg_pivot.values, x=vg_pivot.columns.tolist(), y=vg_pivot.index.tolist(),
            colorscale='RdYlGn',
            text=[[f"₹{v:.0f}" if not np.isnan(v) else "-" for v in row] for row in vg_pivot.values],
            texttemplate='%{text}', colorbar=dict(title='Avg Price')))
        fig_vg.update_layout(title='Variety × Grade Avg Price Matrix',
            template='plotly_white', paper_bgcolor='#ffffff', height=350)
        fig_vg.update_xaxes(tickangle=45)
        st.plotly_chart(fig_vg, use_container_width=True)

    # ── TAB 6: STATE INTELLIGENCE ────────────────────────────────────────────
    with tab6:
        st.markdown('<div class="section-header">🗺️ State-Wise Market Intelligence</div>', unsafe_allow_html=True)

        state_df = fdf.groupby('State').agg(
            avg_price=('Modal Price','mean'), max_price=('Modal Price','max'),
            min_price=('Modal Price','min'), std_price=('Modal Price','std'),
            avg_arrivals=('Arrivals','mean'), total_arrivals=('Arrivals','sum'),
            markets=('Market','nunique'), records=('Modal Price','count')
        ).reset_index().sort_values('avg_price', ascending=False)

        col_st1, col_st2 = st.columns([2, 1])
        with col_st1:
            fig_state = go.Figure(go.Bar(
                x=state_df['avg_price'], y=state_df['State'], orientation='h',
                marker=dict(color=state_df['avg_price'], colorscale='RdYlGn', showscale=True),
                text=[f"₹{p:,.0f}" for p in state_df['avg_price']], textposition='outside'))
            fig_state.update_layout(title='🗺️ Average Modal Price by State',
                template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=500, xaxis_title='Avg Modal Price (Rs./Quintal)',
                yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_state, use_container_width=True)

        with col_st2:
            best_state  = state_df.iloc[0]
            worst_state = state_df.iloc[-1]
            st.markdown(f"""
            <div class="metric-card"><div class="metric-label">🥇 Highest Price State</div>
            <div class="metric-value" style="font-size:18px;">{best_state['State']}</div>
            <div class="metric-sub">Avg ₹{best_state['avg_price']:,.0f}/Q</div></div>
            <div class="metric-card"><div class="metric-label">📉 Lowest Price State</div>
            <div class="metric-value" style="font-size:18px;">{worst_state['State']}</div>
            <div class="metric-sub">Avg ₹{worst_state['avg_price']:,.0f}/Q</div></div>
            """, unsafe_allow_html=True)
            for _, row in state_df.head(5).iterrows():
                cv = (row['std_price'] / row['avg_price'] * 100) if row['avg_price'] > 0 else 0
                st.markdown(f"""<div class="metric-card" style="margin:5px 0;padding:11px 15px;">
                    <div class="metric-label">{row['State']}</div>
                    <div class="metric-value" style="font-size:17px;">₹{row['avg_price']:,.0f}</div>
                    <div class="metric-sub">{row['markets']} mandis • CV {cv:.0f}%</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header">📈 State Price Trends</div>', unsafe_allow_html=True)
        top_states = state_df.head(8)['State'].tolist()
        st_trend = fdf[fdf['State'].isin(top_states)].groupby(
            ['Date','State'])['Modal Price'].mean().reset_index()
        fig_str = px.line(st_trend, x='Date', y='Modal Price', color='State',
            title='Top 8 States — Price Trends', template='plotly_white')
        fig_str.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=400,
            yaxis_title='Avg Modal Price')
        st.plotly_chart(fig_str, use_container_width=True)

        st.markdown('<div class="section-header">📋 State Summary Table</div>', unsafe_allow_html=True)
        state_display = state_df.copy()
        state_display['CV%'] = (state_display['std_price'] / state_display['avg_price'] * 100).round(1)
        state_display = state_display[['State','avg_price','max_price','min_price','CV%','markets','records']].round(0)
        state_display.columns = ['State','Avg Price (₹)','Max (₹)','Min (₹)','CV%','Markets','Records']
        st.dataframe(state_display, use_container_width=True)

    # ── TAB 7: FARMER ADVISORY ───────────────────────────────────────────────
    with tab7:
        st.markdown('<div class="section-header">🚜 Farmer Advisory & Risk Assessment</div>', unsafe_allow_html=True)

        recent_14d = fdf[fdf['Date'] >= fdf['Date'].max() - timedelta(days=14)]
        prev_14d   = fdf[(fdf['Date'] < fdf['Date'].max() - timedelta(days=14)) &
                          (fdf['Date'] >= fdf['Date'].max() - timedelta(days=28))]
        recent_avg = recent_14d['Modal Price'].mean() if len(recent_14d) > 0 else avg_modal
        prev_avg   = prev_14d['Modal Price'].mean()   if len(prev_14d)   > 0 else avg_modal
        price_change_pct = ((recent_avg - prev_avg) / prev_avg * 100) if prev_avg > 0 else 0

        best_mkt       = fdf.groupby('Market')['Modal Price'].mean().idxmax() if len(fdf) > 0 else "N/A"
        best_mkt_price = fdf.groupby('Market')['Modal Price'].mean().max()    if len(fdf) > 0 else 0

        risk_score, risk_reasons = 0, []
        if volatility > 40:   risk_score += 3; risk_reasons.append(f"High price volatility ({volatility:.0f}%)")
        elif volatility > 20: risk_score += 1; risk_reasons.append(f"Moderate volatility ({volatility:.0f}%)")
        if price_change_pct < -15: risk_score += 3; risk_reasons.append(f"Sharp price drop ({price_change_pct:.1f}% in 14 days)")
        elif price_change_pct < -5: risk_score += 1; risk_reasons.append(f"Price declining ({price_change_pct:.1f}% in 14 days)")
        if fdf['Arrivals'].mean() > fdf['Arrivals'].quantile(0.75):
            risk_score += 1; risk_reasons.append("High market arrivals (oversupply risk)")

        risk_level = "HIGH" if risk_score>=4 else "MEDIUM" if risk_score>=2 else "LOW"
        risk_class = "risk-high" if risk_score>=4 else "risk-medium" if risk_score>=2 else "risk-low"
        risk_emoji = "🔴" if risk_score>=4 else "🟡" if risk_score>=2 else "🟢"

        if price_change_pct > 5:
            sell_now = "Yes — Prices Rising"; strategy_detail = "Prices aabhi badh rahe hain. Jaldi sell karo!"; wait_days = "0"
        elif price_change_pct < -10:
            sell_now = "No — Wait for Recovery"; strategy_detail = "Prices gir rahe hain. Agar storage hai to 7-10 din rukna chahiye."; wait_days = "7-10"
        else:
            sell_now = "Flexible — Market Stable"; strategy_detail = "Market stable hai. Best mandi choose karo aur sell karo."; wait_days = "2-5"

        col_adv1, col_adv2 = st.columns(2)
        with col_adv1:
            st.markdown(f"""<div class="advisory-box">
                <h3 style="color:#2e7d32;margin-top:0;">🚜 Farmer Advisory (Hindi + English)</h3>
                <p><strong>📊 Market Status:</strong> Price change last 14 days:
                   <span style="color:{'#2e7d32' if price_change_pct>0 else '#c62828'}">{price_change_pct:+.1f}%</span></p>
                <p><strong>💰 Current Avg Price:</strong> ₹{recent_avg:,.0f}/Quintal</p>
                <p><strong>🏪 Best Mandi:</strong> {best_mkt} (₹{best_mkt_price:,.0f}/Q)</p>
                <hr style="border-color:#a5d6a7;">
                <p>📌 <strong>{strategy_detail}</strong></p>
                <p>🔑 <strong>Key advice:</strong> {best_mkt} mandi mein best rates mil rahe hain.</p>
                <p>💡 <strong>Extra Tip:</strong> Hybrid variety consistently better prices deti hai.</p>
                <p>📈 Expected profit vs average:
                   <strong style="color:#e65100;">~{((best_mkt_price-recent_avg)/recent_avg*100):.0f}% more</strong></p>
            </div>""", unsafe_allow_html=True)
            st.markdown(f"""<div class="metric-card" style="margin-top:14px;">
                <div class="metric-label">🛒 Selling Strategy</div>
                <table style="width:100%;color:#1a1a2e;font-size:13px;margin-top:8px;">
                    <tr><td style="color:#6c757d;padding:5px 0;">Sell Immediately</td>
                        <td style="color:#2e7d32;font-weight:600;">{sell_now}</td></tr>
                    <tr><td style="color:#6c757d;padding:5px 0;">Wait Period</td>
                        <td style="color:#e65100;font-weight:600;">{wait_days} days</td></tr>
                    <tr><td style="color:#6c757d;padding:5px 0;">Best Mandi</td>
                        <td style="color:#2e7d32;font-weight:600;">{best_mkt}</td></tr>
                    <tr><td style="color:#6c757d;padding:5px 0;">Potential Gain</td>
                        <td style="color:#2e7d32;font-weight:600;">+{((best_mkt_price-recent_avg)/recent_avg*100):.0f}%</td></tr>
                </table>
            </div>""", unsafe_allow_html=True)

        with col_adv2:
            st.markdown(f"""<div class="{risk_class}">
                <h3 style="margin-top:0;">{risk_emoji} Risk Level: {risk_level}</h3>
                <p><strong>Market Volatility:</strong> {volatility:.1f}%</p>
                <p><strong>Price Trend (14d):</strong> {price_change_pct:+.1f}%</p>
                {"<ul>"+"".join(f"<li>{r}</li>" for r in risk_reasons)+"</ul>" if risk_reasons else "<p>✅ No major risk factors detected</p>"}
            </div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            for label, value in {
                "💰 Current Price": f"₹{recent_avg:,.0f}/Q",
                "📈 14-Day Change": f"{price_change_pct:+.1f}%",
                "🏪 Best Mandi": best_mkt,
                "⭐ Best Variety": fdf.groupby('Variety')['Modal Price'].mean().idxmax() if len(fdf)>0 else "Hybrid",
                "📅 Best Month": fdf.groupby('Month_Name')['Modal Price'].mean().idxmax() if len(fdf)>0 else "Oct",
                "📊 Volatility": f"{volatility:.1f}% {'(High)' if volatility>30 else '(Moderate)' if volatility>15 else '(Low)'}",
            }.items():
                st.markdown(f"""<div class="metric-card" style="padding:10px 14px;margin:5px 0;">
                    <div class="metric-label">{label}</div>
                    <div style="color:#1a1a2e;font-weight:600;font-size:15px;">{value}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header">📊 Recent vs Historical Price</div>', unsafe_allow_html=True)
        monthly_comp = fdf.groupby(['Year','Month_Name','Month'])['Modal Price'].mean().reset_index().sort_values(['Year','Month'])
        fig_comp = px.bar(monthly_comp, x='Month_Name', y='Modal Price', color='Year',
            barmode='group', title='Year-wise Monthly Price Comparison', template='plotly_white')
        fig_comp.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=400,
            yaxis_title='Avg Modal Price (Rs./Quintal)')
        st.plotly_chart(fig_comp, use_container_width=True)

        st.markdown('<div class="section-header">🚛 Arrival Trends (Supply Monitor)</div>', unsafe_allow_html=True)
        arr_trend = fdf.groupby('Date')['Arrivals'].sum().reset_index()
        arr_trend['7D_MA'] = arr_trend['Arrivals'].rolling(7).mean()
        fig_arr = make_subplots(specs=[[{"secondary_y": True}]])
        fig_arr.add_trace(go.Bar(x=arr_trend['Date'], y=arr_trend['Arrivals'],
            name='Daily Arrivals', marker_color='rgba(21,101,192,0.25)'), secondary_y=False)
        fig_arr.add_trace(go.Scatter(x=arr_trend['Date'], y=arr_trend['7D_MA'],
            name='7D Moving Avg', line=dict(color='#e65100', width=2)), secondary_y=False)
        price_overlay = fdf.groupby('Date')['Modal Price'].mean().reset_index()
        fig_arr.add_trace(go.Scatter(x=price_overlay['Date'], y=price_overlay['Modal Price'],
            name='Modal Price', line=dict(color='#c62828', width=1.5)), secondary_y=True)
        fig_arr.update_layout(title='📦 Arrivals vs Price',
            template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=400)
        fig_arr.update_yaxes(title_text='Arrivals (MT)', secondary_y=False)
        fig_arr.update_yaxes(title_text='Modal Price (₹/Q)', secondary_y=True)
        st.plotly_chart(fig_arr, use_container_width=True)

    # Footer — India
    st.markdown("---")
    st.markdown(f"""<div style="text-align:center;color:#546e7a;font-size:13px;padding:14px;">
        🌾 <strong style="color:#2e7d32;">Tomato Market Intelligence — India</strong> •
        {len(df):,} records • {df['State'].nunique()} states • {df['Market'].nunique()} mandis<br>
        Built for Indian farmers to maximize profit through data-driven decisions
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ═══════════════════  GLOBAL DASHBOARD  ══════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════════
else:
    if len(fgdf) == 0:
        st.warning("⚠️ No global data for selected filters. Adjust the sidebar.")
        st.stop()

    g_avg      = fgdf['Price_INR_Q'].mean()
    g_max      = fgdf['Price_INR_Q'].max()
    g_min      = fgdf['Price_INR_Q'].min()
    g_vol      = (fgdf['Price_INR_Q'].std() / g_avg * 100) if g_avg > 0 else 0
    g_countries = fgdf['country_name'].nunique()
    g_markets   = fgdf['market_name'].nunique()

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.metric("🌍 Countries",    str(g_countries))
    k2.metric("🏪 Markets",      str(g_markets))
    k3.metric("💰 Avg Price",    f"₹{g_avg:,.0f}", "per Quintal (INR)")
    k4.metric("📈 Highest",      f"₹{g_max:,.0f}", "per Quintal")
    k5.metric("📉 Lowest",       f"₹{g_min:,.0f}", "per Quintal")
    k6.metric("📊 Volatility",   f"{g_vol:.1f}%",  "Price Std/Mean")

    st.markdown("---")

    gtab1, gtab2, gtab3, gtab4, gtab5, gtab6 = st.tabs([
        "🌍 Country Overview",
        "📈 Price Trends",
        "🏪 Market Comparison",
        "🌤️ Seasonal Analysis",
        "🔗 Country Correlation",
        "📊 Price Distribution",
    ])

    # ── GTAB 1: COUNTRY OVERVIEW ─────────────────────────────────────────────
    with gtab1:
        st.markdown('<div class="global-header">🌍 Country-wise Price Overview</div>', unsafe_allow_html=True)

        country_df = fgdf.groupby('country_name').agg(
            avg_price=('Price_INR_Q','mean'),
            max_price=('Price_INR_Q','max'),
            min_price=('Price_INR_Q','min'),
            std_price=('Price_INR_Q','std'),
            records=('Price_INR_Q','count'),
            markets=('market_name','nunique')
        ).reset_index().sort_values('avg_price', ascending=False)
        country_df['cv'] = (country_df['std_price'] / country_df['avg_price'] * 100).round(1).fillna(0)

        col_g1, col_g2 = st.columns([2, 1])
        with col_g1:
            fig_c = go.Figure(go.Bar(
                x=country_df['avg_price'], y=country_df['country_name'],
                orientation='h',
                marker=dict(color=country_df['avg_price'], colorscale='Blues', showscale=True,
                    colorbar=dict(title='₹/Quintal')),
                text=[f"₹{p:,.0f}" for p in country_df['avg_price']],
                textposition='outside'))
            fig_c.update_layout(title='🌍 Average Tomato Price by Country (INR/Quintal)',
                template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=420, xaxis_title='Avg Price (₹/Quintal)',
                yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_c, use_container_width=True)

        with col_g2:
            for _, row in country_df.iterrows():
                st.markdown(f"""<div class="country-card">
                    <div class="metric-label">🌍 {row['country_name']}</div>
                    <div style="color:#1565c0;font-size:20px;font-weight:700;">₹{row['avg_price']:,.0f}/Q</div>
                    <div style="color:#546e7a;font-size:11px;margin-top:3px;">
                        Max ₹{row['max_price']:,.0f} • Min ₹{row['min_price']:,.0f} •
                        CV {row['cv']:.0f}% • {row['markets']} markets
                    </div>
                </div>""", unsafe_allow_html=True)

        # Pie chart — price share
        st.markdown('<div class="global-header">📊 Country Price Share</div>', unsafe_allow_html=True)
        fig_pie = px.pie(country_df, names='country_name', values='avg_price',
            title='Share of Average Price by Country',
            template='plotly_white', hole=0.35,
            color_discrete_sequence=px.colors.qualitative.Set2)
        fig_pie.update_layout(paper_bgcolor='#ffffff', height=380)
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── GTAB 2: PRICE TRENDS ─────────────────────────────────────────────────
    with gtab2:
        st.markdown('<div class="global-header">📈 Global Price Trends Over Time</div>', unsafe_allow_html=True)

        trend_df = fgdf.groupby(['DATE','country_name'])['Price_INR_Q'].mean().reset_index()
        fig_trend = px.line(trend_df, x='DATE', y='Price_INR_Q', color='country_name',
            title='📈 Tomato Price Trends by Country (INR/Quintal)',
            template='plotly_white', markers=False)
        fig_trend.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=460,
            yaxis_title='Price (₹/Quintal)', xaxis_title='Date',
            legend=dict(orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig_trend, use_container_width=True)

        # Year-wise bar
        st.markdown('<div class="global-header">📅 Year-wise Average Price by Country</div>', unsafe_allow_html=True)
        yr_df = fgdf.groupby(['Year','country_name'])['Price_INR_Q'].mean().reset_index()
        fig_yr = px.bar(yr_df, x='Year', y='Price_INR_Q', color='country_name',
            barmode='group', title='Yearly Average Price (INR/Quintal)',
            template='plotly_white',
            color_discrete_sequence=px.colors.qualitative.Set2)
        fig_yr.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=400,
            yaxis_title='Avg Price (₹/Quintal)')
        st.plotly_chart(fig_yr, use_container_width=True)

        # Rolling average — data is monthly granularity, so use a 3-month
        # rolling window computed on the proper DATE timeline per country
        st.markdown('<div class="global-header">📉 3-Month Rolling Average Price</div>', unsafe_allow_html=True)
        roll_list = []
        for country, grp in fgdf.groupby('country_name'):
            g = grp.groupby('DATE')['Price_INR_Q'].mean().sort_index()
            g_roll = g.rolling(3, min_periods=1).mean()
            tmp = g_roll.reset_index()
            tmp.columns = ['DATE', 'Price_3M_MA']
            tmp['country_name'] = country
            roll_list.append(tmp)
        roll_df = pd.concat(roll_list, ignore_index=True) if roll_list else pd.DataFrame(
            columns=['DATE', 'Price_3M_MA', 'country_name'])

        fig_roll = px.line(roll_df.dropna(), x='DATE', y='Price_3M_MA', color='country_name',
            title='3-Month Rolling Average Price (INR/Quintal)', template='plotly_white')
        fig_roll.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=380,
            yaxis_title='3M Rolling Avg (₹/Quintal)', xaxis_title='Date')
        st.plotly_chart(fig_roll, use_container_width=True)

    # ── GTAB 3: MARKET COMPARISON ─────────────────────────────────────────────
    with gtab3:
        st.markdown('<div class="global-header">🏪 Global Market Comparison</div>', unsafe_allow_html=True)

        market_df = fgdf.groupby(['market_name','country_name']).agg(
            avg=('Price_INR_Q','mean'), mx=('Price_INR_Q','max'),
            mn=('Price_INR_Q','min'), std=('Price_INR_Q','std'),
            cnt=('Price_INR_Q','count')
        ).reset_index().sort_values('avg', ascending=False)
        market_df['cv'] = (market_df['std'] / market_df['avg'] * 100).round(1).fillna(0)

        top30m = market_df.head(30)
        fig_m = go.Figure(go.Bar(
            x=top30m['avg'], y=top30m['market_name'] + ' (' + top30m['country_name'] + ')',
            orientation='h',
            marker=dict(color=top30m['avg'], colorscale='RdYlGn', showscale=True),
            text=[f"₹{p:,.0f}" for p in top30m['avg']], textposition='outside'))
        fig_m.update_layout(title='🏪 Top 30 Global Markets by Avg Price (INR/Quintal)',
            template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
            height=700, xaxis_title='Avg Price (₹/Quintal)',
            yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_m, use_container_width=True)

        # Scatter — CV vs avg price
        fig_ms = px.scatter(market_df, x='avg', y='cv', color='country_name',
            size='cnt', hover_name='market_name',
            title='Price Level vs Volatility (bubble = data points)',
            template='plotly_white', size_max=40,
            color_discrete_sequence=px.colors.qualitative.Set2)
        fig_ms.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=420,
            xaxis_title='Avg Price (₹/Q)', yaxis_title='CV% (Volatility)')
        st.plotly_chart(fig_ms, use_container_width=True)

        # Table
        st.markdown('<div class="global-header">📋 Market Summary Table</div>', unsafe_allow_html=True)
        disp_m = market_df.rename(columns={'market_name':'Market','country_name':'Country',
            'avg':'Avg ₹/Q','mx':'Max ₹/Q','mn':'Min ₹/Q','cv':'CV%','cnt':'Records'})
        st.dataframe(disp_m[['Market','Country','Avg ₹/Q','Max ₹/Q','Min ₹/Q','CV%','Records']].round(1),
            use_container_width=True, height=400)

    # ── GTAB 4: SEASONAL ANALYSIS ─────────────────────────────────────────────
    with gtab4:
        st.markdown('<div class="global-header">🌤️ Global Seasonal Price Patterns</div>', unsafe_allow_html=True)

        col_gs1, col_gs2 = st.columns(2)
        with col_gs1:
            g_monthly = fgdf.groupby(['Month','Month_Name'])['Price_INR_Q'].mean().reset_index().sort_values('Month')
            fig_gm = go.Figure(go.Bar(
                x=g_monthly['Month_Name'], y=g_monthly['Price_INR_Q'],
                marker=dict(color=g_monthly['Price_INR_Q'], colorscale='RdYlGn', showscale=True),
                text=[f"₹{p:.0f}" for p in g_monthly['Price_INR_Q']], textposition='outside'))
            fig_gm.update_layout(title='📅 Global Avg Price by Month (INR/Quintal)',
                template='plotly_white', paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=400, yaxis_title='Price (₹/Quintal)')
            st.plotly_chart(fig_gm, use_container_width=True)

        with col_gs2:
            g_monthly_c = fgdf.groupby(['Month','country_name'])['Price_INR_Q'].mean().reset_index()
            fig_gmc = px.line(g_monthly_c, x='Month', y='Price_INR_Q', color='country_name',
                title='Monthly Price by Country', template='plotly_white', markers=True,
                color_discrete_sequence=px.colors.qualitative.Set2)
            fig_gmc.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=400,
                yaxis_title='Avg Price (₹/Quintal)',
                xaxis=dict(tickmode='array', tickvals=list(range(1,13)),
                    ticktext=['Jan','Feb','Mar','Apr','May','Jun',
                              'Jul','Aug','Sep','Oct','Nov','Dec']))
            st.plotly_chart(fig_gmc, use_container_width=True)

        # Year-month heatmap per country
        st.markdown('<div class="global-header">🌡️ Year × Month Heatmap (Global Avg)</div>', unsafe_allow_html=True)
        g_heat = fgdf.groupby(['Year','Month'])['Price_INR_Q'].mean().reset_index()
        g_heat_pivot = g_heat.pivot(index='Year', columns='Month', values='Price_INR_Q')
        mn_map = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                  7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
        g_heat_pivot.columns = [mn_map.get(c,c) for c in g_heat_pivot.columns]
        fig_gheat = go.Figure(go.Heatmap(
            z=g_heat_pivot.values, x=g_heat_pivot.columns.tolist(),
            y=[str(y) for y in g_heat_pivot.index],
            colorscale='RdYlGn',
            text=[[f"₹{v:.0f}" if not np.isnan(v) else "-" for v in row] for row in g_heat_pivot.values],
            texttemplate='%{text}', colorbar=dict(title='₹/Q')))
        fig_gheat.update_layout(title='Global Avg Price Heatmap (₹/Quintal)',
            template='plotly_white', paper_bgcolor='#ffffff', height=360)
        st.plotly_chart(fig_gheat, use_container_width=True)

    # ── GTAB 5: COUNTRY CORRELATION ───────────────────────────────────────────
    with gtab5:
        st.markdown('<div class="global-header">🔗 Country Price Correlation</div>', unsafe_allow_html=True)

        corr_pivot = fgdf.pivot_table(index='DATE', columns='country_name',
            values='Price_INR_Q', aggfunc='mean')
        corr_matrix = corr_pivot.corr()

        fig_corr = go.Figure(go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.columns.tolist(),
            colorscale='RdBu', zmid=0,
            text=[[f"{v:.2f}" if not np.isnan(v) else "-" for v in row] for row in corr_matrix.values],
            texttemplate='%{text}', colorbar=dict(title='Correlation')))
        fig_corr.update_layout(title='Country-to-Country Price Correlation Matrix',
            template='plotly_white', paper_bgcolor='#ffffff', height=450)
        st.plotly_chart(fig_corr, use_container_width=True)

        # Price sync over time — normalized (base = earliest DATE per country)
        st.markdown('<div class="global-header">📈 Normalized Price Trend (Base=100)</div>', unsafe_allow_html=True)
        norm_df = fgdf.groupby(['DATE','country_name'])['Price_INR_Q'].mean().reset_index()
        norm_df = norm_df.sort_values('DATE')
        base_prices = norm_df.groupby('country_name')['Price_INR_Q'].first()
        norm_df['Normalized'] = norm_df.apply(
            lambda r: (r['Price_INR_Q'] / base_prices.get(r['country_name'], r['Price_INR_Q'])) * 100, axis=1)
        fig_norm = px.line(norm_df, x='DATE', y='Normalized', color='country_name',
            title='Normalized Price Index (Earliest Record = 100)',
            template='plotly_white',
            color_discrete_sequence=px.colors.qualitative.Set2)
        fig_norm.add_hline(y=100, line_dash='dash', line_color='#9e9e9e',
            annotation_text='Base = 100')
        fig_norm.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa', height=420,
            yaxis_title='Price Index (Base=100)')
        st.plotly_chart(fig_norm, use_container_width=True)

    # ── GTAB 6: PRICE DISTRIBUTION ────────────────────────────────────────────
    with gtab6:
        st.markdown('<div class="global-header">📊 Global Price Distribution Analysis</div>', unsafe_allow_html=True)

        col_gd1, col_gd2 = st.columns(2)
        with col_gd1:
            fig_box = px.box(fgdf, x='country_name', y='Price_INR_Q', color='country_name',
                title='Price Distribution by Country (Box Plot)',
                template='plotly_white',
                color_discrete_sequence=px.colors.qualitative.Set2)
            fig_box.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=420, yaxis_title='Price (₹/Quintal)', showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)

        with col_gd2:
            fig_hist = px.histogram(fgdf, x='Price_INR_Q', color='country_name',
                nbins=60, barmode='overlay', opacity=0.7,
                title='Price Frequency Distribution by Country',
                template='plotly_white',
                color_discrete_sequence=px.colors.qualitative.Set2)
            fig_hist.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#fafafa',
                height=420, xaxis_title='Price (₹/Quintal)', yaxis_title='Frequency')
            st.plotly_chart(fig_hist, use_container_width=True)

        # Summary stats table
        st.markdown('<div class="global-header">📋 Global Price Statistics</div>', unsafe_allow_html=True)
        g_stats = fgdf.groupby('country_name')['Price_INR_Q'].describe().round(1).reset_index()
        g_stats.columns = ['Country','Count','Mean ₹/Q','Std Dev','Min ₹/Q',
                           'Q25','Median','Q75','Max ₹/Q']
        st.dataframe(g_stats, use_container_width=True)

        # Advisory for global
        st.markdown('<div class="global-header">🌍 Global Market Advisory</div>', unsafe_allow_html=True)
        best_g_country = fgdf.groupby('country_name')['Price_INR_Q'].mean().idxmax()
        best_g_price   = fgdf.groupby('country_name')['Price_INR_Q'].mean().max()
        st.markdown(f"""<div class="global-box">
            <h3 style="color:#1565c0;margin-top:0;">🌍 Global Market Intelligence</h3>
            <p>🏆 <strong>Highest Price Country:</strong> {best_g_country} — ₹{best_g_price:,.0f}/Quintal (INR equiv)</p>
            <p>📊 <strong>Global Avg Price:</strong> ₹{g_avg:,.0f}/Quintal</p>
            <p>📉 <strong>Volatility:</strong> {g_vol:.1f}% ({"High" if g_vol>40 else "Moderate" if g_vol>20 else "Low"})</p>
            <p>🌐 <strong>Countries Monitored:</strong> {g_countries} | <strong>Markets:</strong> {g_markets}</p>
            <hr style="border-color:#90caf9;">
            <p>💡 <strong>Insight:</strong> Comparing India's domestic prices with global rates helps identify
            export opportunities and import risks for the tomato supply chain.</p>
        </div>""", unsafe_allow_html=True)

    # Footer — Global
    st.markdown("---")
    st.markdown(f"""<div style="text-align:center;color:#546e7a;font-size:13px;padding:14px;">
        🌍 <strong style="color:#1565c0;">Global Tomato Price Intelligence</strong> •
        {len(gdf):,} records • {gdf['country_name'].nunique()} countries • {gdf['market_name'].nunique()} markets •
        {gdf['DATE'].min().year}–{gdf['DATE'].max().year}<br>
        Prices converted to INR equivalent for cross-country comparison
    </div>""", unsafe_allow_html=True)