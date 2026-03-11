# # # # # # """
# # # # # # Kenya Economic Indicators Dashboard
# # # # # # Streamlit + Plotly data analysis project
# # # # # # Data source: World Bank Open Data
# # # # # # """

# # # # # # import streamlit as st
# # # # # # import pandas as pd
# # # # # # import plotly.express as px
# # # # # # import plotly.graph_objects as go
# # # # # # from plotly.subplots import make_subplots
# # # # # # import numpy as np
# # # # # # from scipy import stats

# # # # # # # ── Page config ──────────────────────────────────────────────────────────────
# # # # # # st.set_page_config(
# # # # # #     page_title="Kenya Economic Dashboard",
# # # # # #     page_icon="🇰🇪",
# # # # # #     layout="wide",
# # # # # #     initial_sidebar_state="expanded",
# # # # # # )

# # # # # # # ── Custom CSS ────────────────────────────────────────────────────────────────
# # # # # # st.markdown("""
# # # # # # <style>
# # # # # #     /* Main background */
# # # # # #     .stApp { background-color: #0a0f0d; }
# # # # # #     .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

# # # # # #     /* Sidebar */
# # # # # #     [data-testid="stSidebar"] { background-color: #111812; border-right: 1px solid #1e2e21; }
# # # # # #     [data-testid="stSidebar"] * { color: #e8f0ea !important; }

# # # # # #     /* KPI metric cards */
# # # # # #     [data-testid="metric-container"] {
# # # # # #         background: #111812;
# # # # # #         border: 1px solid #1e2e21;
# # # # # #         border-radius: 6px;
# # # # # #         padding: 1rem 1.2rem;
# # # # # #     }
# # # # # #     [data-testid="stMetricLabel"] { color: #6b7f6e !important; font-size: 0.75rem; }
# # # # # #     [data-testid="stMetricValue"] { color: #e8f0ea !important; }
# # # # # #     [data-testid="stMetricDelta"] { font-size: 0.8rem; }

# # # # # #     /* Headers */
# # # # # #     h1, h2, h3 { color: #e8f0ea !important; }
# # # # # #     p, li { color: #b0bfb3 !important; }

# # # # # #     /* Tabs */
# # # # # #     .stTabs [data-baseweb="tab-list"] { background-color: #111812; border-bottom: 1px solid #1e2e21; }
# # # # # #     .stTabs [data-baseweb="tab"] { color: #6b7f6e; }
# # # # # #     .stTabs [aria-selected="true"] { color: #3ddc6e !important; border-bottom-color: #3ddc6e !important; }

# # # # # #     /* Divider */
# # # # # #     hr { border-color: #1e2e21; }

# # # # # #     /* Info/success boxes */
# # # # # #     .stAlert { background-color: #111812; border-color: #1e2e21; }

# # # # # #     /* Section header style */
# # # # # #     .section-label {
# # # # # #         font-family: monospace;
# # # # # #         font-size: 0.65rem;
# # # # # #         letter-spacing: 0.2em;
# # # # # #         color: #3ddc6e;
# # # # # #         text-transform: uppercase;
# # # # # #         margin-bottom: 0.25rem;
# # # # # #     }
# # # # # #     .insight-box {
# # # # # #         background: #111812;
# # # # # #         border: 1px solid #1e2e21;
# # # # # #         border-left: 3px solid #3ddc6e;
# # # # # #         border-radius: 4px;
# # # # # #         padding: 1rem 1.2rem;
# # # # # #         margin-bottom: 0.75rem;
# # # # # #     }
# # # # # #     .insight-box.warn { border-left-color: #f5c842; }
# # # # # #     .insight-box.danger { border-left-color: #e85d4a; }
# # # # # #     .insight-box h4 { color: #e8f0ea !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# # # # # #     .insight-box p { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# # # # # # </style>
# # # # # # """, unsafe_allow_html=True)

# # # # # # # ── Data ──────────────────────────────────────────────────────────────────────
# # # # # # @st.cache_data
# # # # # # def load_data():
# # # # # #     data = {
# # # # # #         "Year":         list(range(2000, 2024)),
# # # # # #         "GDP_B":        [12.7,13.3,13.4,14.0,15.1,18.7,22.5,27.2,30.6,29.5,
# # # # # #                          32.2,34.0,41.1,47.6,60.9,63.4,70.5,79.3,87.8,95.5,
# # # # # #                          98.8,99.2,110.4,107.9],
# # # # # #         "GDP_Growth":   [0.6, 4.5, 0.3, 2.9, 4.6, 5.9, 6.5, 6.9, 1.5, 2.7,
# # # # # #                          8.4, 6.1, 4.6, 5.9, 5.4, 5.7, 5.9, 4.9, 6.3, 5.4,
# # # # # #                         -0.3, 7.6, 4.8, 5.6],
# # # # # #         "Inflation":    [10.0, 5.8, 2.0, 9.8,11.6,10.3, 6.0, 4.3,26.2,10.5,
# # # # # #                           4.0,14.0, 9.4, 5.7, 6.9, 6.6, 6.3, 8.0, 4.7, 5.2,
# # # # # #                           5.3, 6.1, 9.1, 6.3],
# # # # # #         "Unemployment": [9.8, 9.8, 9.8, 9.8, 9.8, 9.3, 8.7, 8.1, 7.4, 6.7,
# # # # # #                          6.1, 5.5, 4.9, 4.4, 3.9, 3.5, 2.8, 3.5, 4.3, 5.0,
# # # # # #                          5.6, 5.7, 5.7, 5.6],
# # # # # #         "Exports_GDP":  [25.2,24.8,23.6,23.0,24.0,23.8,23.0,24.5,24.1,20.4,
# # # # # #                          21.2,21.0,19.5,18.3,16.9,15.7,14.6,13.8,13.9,13.5,
# # # # # #                          12.4,13.5,14.2,13.8],
# # # # # #         "Imports_GDP":  [33.1,32.5,31.6,30.5,32.0,31.8,33.0,37.2,42.4,36.3,
# # # # # #                          36.1,40.0,38.5,37.3,34.5,32.5,30.6,29.8,31.9,29.5,
# # # # # #                          26.7,28.0,32.6,31.2],
# # # # # #     }
# # # # # #     df = pd.DataFrame(data)
# # # # # #     df["Trade_Balance"] = df["Exports_GDP"] - df["Imports_GDP"]
# # # # # #     df["Era"] = df["Year"].apply(
# # # # # #         lambda y: "🔴 COVID" if 2020 <= y <= 2021
# # # # # #         else ("🟡 Post-COVID" if y >= 2022
# # # # # #         else ("🟢 Growth" if y >= 2010
# # # # # #         else "🔵 Early 2000s"))
# # # # # #     )
# # # # # #     return df

# # # # # # df = load_data()

# # # # # # # ── Plotly theme defaults ─────────────────────────────────────────────────────
# # # # # # COLORS = {
# # # # # #     "bg":      "#0a0f0d",
# # # # # #     "surface": "#111812",
# # # # # #     "border":  "#1e2e21",
# # # # # #     "green":   "#3ddc6e",
# # # # # #     "yellow":  "#f5c842",
# # # # # #     "red":     "#e85d4a",
# # # # # #     "blue":    "#4a9de8",
# # # # # #     "muted":   "#6b7f6e",
# # # # # #     "text":    "#e8f0ea",
# # # # # # }

# # # # # # LAYOUT_BASE = dict(
# # # # # #     paper_bgcolor=COLORS["surface"],
# # # # # #     plot_bgcolor=COLORS["bg"],
# # # # # #     font=dict(family="DM Mono, monospace", color=COLORS["muted"], size=11),
# # # # # #     xaxis=dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], tickcolor=COLORS["border"]),
# # # # # #     yaxis=dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], tickcolor=COLORS["border"]),
# # # # # #     margin=dict(t=40, b=40, l=50, r=20),
# # # # # #     legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
# # # # # # )

# # # # # # # ── Sidebar ───────────────────────────────────────────────────────────────────
# # # # # # with st.sidebar:
# # # # # #     st.markdown("### 🇰🇪 Kenya Dashboard")
# # # # # #     st.markdown("---")

# # # # # #     st.markdown("**TIME RANGE**")
# # # # # #     year_range = st.slider(
# # # # # #         "Select years",
# # # # # #         min_value=2000, max_value=2023,
# # # # # #         value=(2005, 2023),
# # # # # #         label_visibility="collapsed"
# # # # # #     )

# # # # # #     st.markdown("---")
# # # # # #     st.markdown("**INDICATORS**")
# # # # # #     show_gdp      = st.checkbox("GDP & Growth",       value=True)
# # # # # #     show_inf      = st.checkbox("Inflation",           value=True)
# # # # # #     show_unemp    = st.checkbox("Unemployment",        value=True)
# # # # # #     show_trade    = st.checkbox("Trade Balance",       value=True)
# # # # # #     show_scatter  = st.checkbox("Correlation Analysis",value=True)
# # # # # #     show_stats    = st.checkbox("Statistical Summary", value=True)

# # # # # #     st.markdown("---")
# # # # # #     st.markdown("**HIGHLIGHT ERA**")
# # # # # #     highlight_covid = st.toggle("Highlight COVID period", value=True)

# # # # # #     st.markdown("---")
# # # # # #     st.markdown(
# # # # # #         "<small style='color:#3a4f3d'>Source: World Bank Open Data<br>"
# # # # # #         "Period: 2000–2023</small>",
# # # # # #         unsafe_allow_html=True
# # # # # #     )

# # # # # # # ── Filter data ───────────────────────────────────────────────────────────────
# # # # # # dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

# # # # # # # ── Header ────────────────────────────────────────────────────────────────────
# # # # # # st.markdown(
# # # # # #     "<p class='section-label'>REPUBLIC OF KENYA · KE · WORLD BANK OPEN DATA</p>",
# # # # # #     unsafe_allow_html=True
# # # # # # )
# # # # # # st.title("Economic Indicators Analysis")
# # # # # # st.markdown(
# # # # # #     f"**GDP · Inflation · Unemployment · Trade Balance** &nbsp;·&nbsp; "
# # # # # #     f"{year_range[0]}–{year_range[1]}",
# # # # # # )
# # # # # # st.markdown("---")

# # # # # # # ── KPI Cards ─────────────────────────────────────────────────────────────────
# # # # # # latest = dff.iloc[-1]
# # # # # # prev   = dff.iloc[-2]

# # # # # # k1, k2, k3, k4 = st.columns(4)
# # # # # # k1.metric("GDP (Latest Year)",        f"${latest['GDP_B']:.1f}B",
# # # # # #           f"{latest['GDP_Growth']:+.1f}% growth")
# # # # # # k2.metric("Inflation",                f"{latest['Inflation']:.1f}%",
# # # # # #           f"{latest['Inflation'] - prev['Inflation']:+.1f}pp vs prior year")
# # # # # # k3.metric("Unemployment",             f"{latest['Unemployment']:.1f}%",
# # # # # #           f"{latest['Unemployment'] - prev['Unemployment']:+.1f}pp vs prior year")
# # # # # # k4.metric("Trade Balance (% GDP)",    f"{latest['Trade_Balance']:.1f}%",
# # # # # #           f"{latest['Trade_Balance'] - prev['Trade_Balance']:+.1f}pp vs prior year")

# # # # # # st.markdown("---")

# # # # # # # ── Tabs ──────────────────────────────────────────────────────────────────────
# # # # # # tabs = st.tabs(["📈 GDP", "🔥 Inflation", "👷 Unemployment", "🌍 Trade", "🔗 Correlations", "📊 Statistics"])

# # # # # # # COVID shading helper
# # # # # # def add_covid_band(fig, y_min=None, y_max=None):
# # # # # #     if highlight_covid:
# # # # # #         fig.add_vrect(
# # # # # #             x0=2019.5, x1=2021.5,
# # # # # #             fillcolor="rgba(232,93,74,0.08)",
# # # # # #             line=dict(color="rgba(232,93,74,0.3)", width=1, dash="dot"),
# # # # # #             annotation_text="COVID", annotation_position="top left",
# # # # # #             annotation_font=dict(color=COLORS["red"], size=10),
# # # # # #         )
# # # # # #     return fig

# # # # # # # ── TAB 1: GDP ────────────────────────────────────────────────────────────────
# # # # # # with tabs[0]:
# # # # # #     if show_gdp:
# # # # # #         st.subheader("GDP Growth Over Time")

# # # # # #         fig = make_subplots(specs=[[{"secondary_y": True}]])

# # # # # #         fig.add_trace(
# # # # # #             go.Bar(
# # # # # #                 x=dff["Year"], y=dff["GDP_B"],
# # # # # #                 name="GDP (USD Billion)",
# # # # # #                 marker=dict(color=COLORS["green"], opacity=0.25,
# # # # # #                             line=dict(color=COLORS["green"], width=1)),
# # # # # #             ), secondary_y=False
# # # # # #         )
# # # # # #         fig.add_trace(
# # # # # #             go.Scatter(
# # # # # #                 x=dff["Year"], y=dff["GDP_Growth"],
# # # # # #                 name="GDP Growth %",
# # # # # #                 line=dict(color=COLORS["green"], width=2.5),
# # # # # #                 mode="lines+markers",
# # # # # #                 marker=dict(size=5, color=COLORS["green"]),
# # # # # #             ), secondary_y=True
# # # # # #         )

# # # # # #         fig.update_layout(**LAYOUT_BASE, height=380, title="")
# # # # # #         fig.update_yaxes(title_text="GDP (USD Billion)", secondary_y=False,
# # # # # #                          tickprefix="$", ticksuffix="B",
# # # # # #                          gridcolor=COLORS["border"], linecolor=COLORS["border"])
# # # # # #         fig.update_yaxes(title_text="Growth Rate (%)", secondary_y=True,
# # # # # #                          ticksuffix="%", gridcolor="rgba(0,0,0,0)")
# # # # # #         fig.update_xaxes(gridcolor=COLORS["border"])
# # # # # #         add_covid_band(fig)

# # # # # #         st.plotly_chart(fig, use_container_width=True)

# # # # # #         # GDP decomposition
# # # # # #         col1, col2 = st.columns(2)
# # # # # #         with col1:
# # # # # #             st.markdown("**Year-on-Year GDP Change (USD Billion)**")
# # # # # #             dff_copy = dff.copy()
# # # # # #             dff_copy["GDP_Change"] = dff_copy["GDP_B"].diff()
# # # # # #             fig2 = go.Figure(go.Bar(
# # # # # #                 x=dff_copy["Year"][1:], y=dff_copy["GDP_Change"][1:],
# # # # # #                 marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# # # # # #                               for v in dff_copy["GDP_Change"][1:]],
# # # # # #                 text=[f"${v:+.1f}B" for v in dff_copy["GDP_Change"][1:]],
# # # # # #                 textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# # # # # #             ))
# # # # # #             fig2.update_layout(**LAYOUT_BASE, height=280,
# # # # # #                                yaxis=dict(**LAYOUT_BASE["yaxis"], tickprefix="$", ticksuffix="B"))
# # # # # #             add_covid_band(fig2)
# # # # # #             st.plotly_chart(fig2, use_container_width=True)

# # # # # #         with col2:
# # # # # #             st.markdown("**GDP by Era (Average Growth %)**")
# # # # # #             era_avg = df.groupby("Era")["GDP_Growth"].mean().reset_index()
# # # # # #             fig3 = go.Figure(go.Bar(
# # # # # #                 x=era_avg["Era"], y=era_avg["GDP_Growth"],
# # # # # #                 marker_color=[COLORS["blue"], COLORS["red"], COLORS["green"], COLORS["yellow"]],
# # # # # #                 text=[f"{v:.1f}%" for v in era_avg["GDP_Growth"]],
# # # # # #                 textposition="outside", textfont=dict(size=10, color=COLORS["text"]),
# # # # # #             ))
# # # # # #             fig3.update_layout(**LAYOUT_BASE, height=280,
# # # # # #                                yaxis=dict(**LAYOUT_BASE["yaxis"], ticksuffix="%"))
# # # # # #             st.plotly_chart(fig3, use_container_width=True)

# # # # # # # ── TAB 2: Inflation ──────────────────────────────────────────────────────────
# # # # # # with tabs[1]:
# # # # # #     if show_inf:
# # # # # #         st.subheader("Inflation (CPI) Trend")

# # # # # #         fig = go.Figure()

# # # # # #         # Target band fill
# # # # # #         fig.add_trace(go.Scatter(
# # # # # #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# # # # # #             y=[7.5]*len(dff) + [2.5]*len(dff),
# # # # # #             fill="toself",
# # # # # #             fillcolor="rgba(61,220,110,0.06)",
# # # # # #             line=dict(color="rgba(0,0,0,0)"),
# # # # # #             name="CBK Target Band (2.5–7.5%)",
# # # # # #             showlegend=True,
# # # # # #         ))

# # # # # #         fig.add_hline(y=7.5, line=dict(color=COLORS["red"], dash="dot", width=1),
# # # # # #                       annotation_text="Upper target 7.5%",
# # # # # #                       annotation_font=dict(color=COLORS["red"], size=10))
# # # # # #         fig.add_hline(y=2.5, line=dict(color=COLORS["green"], dash="dot", width=1),
# # # # # #                       annotation_text="Lower target 2.5%",
# # # # # #                       annotation_font=dict(color=COLORS["green"], size=10))

# # # # # #         fig.add_trace(go.Scatter(
# # # # # #             x=dff["Year"], y=dff["Inflation"],
# # # # # #             name="CPI Inflation",
# # # # # #             line=dict(color=COLORS["yellow"], width=2.5),
# # # # # #             mode="lines+markers",
# # # # # #             marker=dict(size=5, color=dff["Inflation"].apply(
# # # # # #                 lambda v: COLORS["red"] if v > 7.5 else (COLORS["green"] if v < 2.5 else COLORS["yellow"])
# # # # # #             )),
# # # # # #             fill="tozeroy",
# # # # # #             fillcolor="rgba(245,200,66,0.07)",
# # # # # #         ))

# # # # # #         fig.update_layout(**LAYOUT_BASE, height=380,
# # # # # #                           yaxis=dict(**LAYOUT_BASE["yaxis"], ticksuffix="%", title="CPI %"))
# # # # # #         add_covid_band(fig)
# # # # # #         st.plotly_chart(fig, use_container_width=True)

# # # # # #         col1, col2 = st.columns(2)
# # # # # #         with col1:
# # # # # #             # Above/below target
# # # # # #             above = (dff["Inflation"] > 7.5).sum()
# # # # # #             within = ((dff["Inflation"] >= 2.5) & (dff["Inflation"] <= 7.5)).sum()
# # # # # #             below = (dff["Inflation"] < 2.5).sum()
# # # # # #             fig2 = go.Figure(go.Pie(
# # # # # #                 labels=["Above target (>7.5%)", "Within target", "Below target (<2.5%)"],
# # # # # #                 values=[above, within, below],
# # # # # #                 hole=0.55,
# # # # # #                 marker=dict(colors=[COLORS["red"], COLORS["green"], COLORS["blue"]]),
# # # # # #                 textfont=dict(color=COLORS["text"]),
# # # # # #             ))
# # # # # #             fig2.update_layout(**LAYOUT_BASE, height=280,
# # # # # #                                title=dict(text="Years Within CBK Target", font=dict(color=COLORS["text"])))
# # # # # #             st.plotly_chart(fig2, use_container_width=True)

# # # # # #         with col2:
# # # # # #             st.markdown("**Inflation Distribution**")
# # # # # #             fig3 = go.Figure(go.Histogram(
# # # # # #                 x=dff["Inflation"], nbinsx=10,
# # # # # #                 marker=dict(color=COLORS["yellow"], opacity=0.7,
# # # # # #                             line=dict(color=COLORS["bg"], width=1)),
# # # # # #                 name="Inflation %",
# # # # # #             ))
# # # # # #             fig3.add_vline(x=dff["Inflation"].mean(),
# # # # # #                            line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # # # # #                            annotation_text=f"Mean: {dff['Inflation'].mean():.1f}%",
# # # # # #                            annotation_font=dict(color=COLORS["text"], size=10))
# # # # # #             fig3.update_layout(**LAYOUT_BASE, height=280,
# # # # # #                                xaxis=dict(**LAYOUT_BASE["xaxis"], title="Inflation %"),
# # # # # #                                yaxis=dict(**LAYOUT_BASE["yaxis"], title="Count"))
# # # # # #             st.plotly_chart(fig3, use_container_width=True)

# # # # # # # ── TAB 3: Unemployment ───────────────────────────────────────────────────────
# # # # # # with tabs[2]:
# # # # # #     if show_unemp:
# # # # # #         st.subheader("Unemployment Rate Trajectory")

# # # # # #         fig = go.Figure()
# # # # # #         fig.add_trace(go.Scatter(
# # # # # #             x=dff["Year"], y=dff["Unemployment"],
# # # # # #             name="Unemployment %",
# # # # # #             line=dict(color=COLORS["red"], width=2.5),
# # # # # #             mode="lines+markers",
# # # # # #             marker=dict(size=6, color=COLORS["red"]),
# # # # # #             fill="tozeroy",
# # # # # #             fillcolor="rgba(232,93,74,0.1)",
# # # # # #         ))

# # # # # #         # Rolling average
# # # # # #         dff_copy = dff.copy()
# # # # # #         dff_copy["Unemp_MA3"] = dff_copy["Unemployment"].rolling(3, center=True).mean()
# # # # # #         fig.add_trace(go.Scatter(
# # # # # #             x=dff_copy["Year"], y=dff_copy["Unemp_MA3"],
# # # # # #             name="3-Year Rolling Avg",
# # # # # #             line=dict(color=COLORS["text"], width=1.5, dash="dot"),
# # # # # #             mode="lines",
# # # # # #         ))

# # # # # #         fig.update_layout(**LAYOUT_BASE, height=360,
# # # # # #                           yaxis=dict(**LAYOUT_BASE["yaxis"], ticksuffix="%", title="Unemployment %"))
# # # # # #         add_covid_band(fig)
# # # # # #         st.plotly_chart(fig, use_container_width=True)

# # # # # #         col1, col2, col3 = st.columns(3)
# # # # # #         col1.metric("Peak Unemployment", f"{dff['Unemployment'].max():.1f}%",
# # # # # #                     f"in {int(dff.loc[dff['Unemployment'].idxmax(), 'Year'])}")
# # # # # #         col2.metric("Lowest Unemployment", f"{dff['Unemployment'].min():.1f}%",
# # # # # #                     f"in {int(dff.loc[dff['Unemployment'].idxmin(), 'Year'])}")
# # # # # #         col3.metric("Average (Period)", f"{dff['Unemployment'].mean():.1f}%", "ILO modeled estimate")

# # # # # # # ── TAB 4: Trade ──────────────────────────────────────────────────────────────
# # # # # # with tabs[3]:
# # # # # #     if show_trade:
# # # # # #         st.subheader("Trade Balance: Exports vs Imports")

# # # # # #         fig = go.Figure()
# # # # # #         fig.add_trace(go.Scatter(
# # # # # #             x=dff["Year"], y=dff["Exports_GDP"],
# # # # # #             name="Exports % GDP",
# # # # # #             line=dict(color=COLORS["blue"], width=2.5),
# # # # # #             mode="lines+markers", marker=dict(size=4),
# # # # # #         ))
# # # # # #         fig.add_trace(go.Scatter(
# # # # # #             x=dff["Year"], y=dff["Imports_GDP"],
# # # # # #             name="Imports % GDP",
# # # # # #             line=dict(color=COLORS["yellow"], width=2.5),
# # # # # #             mode="lines+markers", marker=dict(size=4),
# # # # # #         ))

# # # # # #         # Fill between gap
# # # # # #         fig.add_trace(go.Scatter(
# # # # # #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# # # # # #             y=list(dff["Imports_GDP"]) + list(dff["Exports_GDP"])[::-1],
# # # # # #             fill="toself",
# # # # # #             fillcolor="rgba(232,93,74,0.08)",
# # # # # #             line=dict(color="rgba(0,0,0,0)"),
# # # # # #             name="Trade Deficit",
# # # # # #             showlegend=True,
# # # # # #         ))

# # # # # #         fig.update_layout(**LAYOUT_BASE, height=360,
# # # # # #                           yaxis=dict(**LAYOUT_BASE["yaxis"], ticksuffix="%", title="% of GDP"))
# # # # # #         add_covid_band(fig)
# # # # # #         st.plotly_chart(fig, use_container_width=True)

# # # # # #         st.markdown("**Net Trade Balance (% GDP)**")
# # # # # #         fig2 = go.Figure(go.Bar(
# # # # # #             x=dff["Year"], y=dff["Trade_Balance"],
# # # # # #             marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# # # # # #                           for v in dff["Trade_Balance"]],
# # # # # #             text=[f"{v:.1f}%" for v in dff["Trade_Balance"]],
# # # # # #             textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# # # # # #         ))
# # # # # #         fig2.add_hline(y=0, line=dict(color=COLORS["muted"], width=1))
# # # # # #         fig2.update_layout(**LAYOUT_BASE, height=280,
# # # # # #                            yaxis=dict(**LAYOUT_BASE["yaxis"], ticksuffix="%"))
# # # # # #         add_covid_band(fig2)
# # # # # #         st.plotly_chart(fig2, use_container_width=True)

# # # # # # # ── TAB 5: Correlations ───────────────────────────────────────────────────────
# # # # # # with tabs[4]:
# # # # # #     if show_scatter:
# # # # # #         st.subheader("Correlation Analysis")

# # # # # #         col1, col2 = st.columns(2)

# # # # # #         with col1:
# # # # # #             st.markdown("**GDP Growth vs Unemployment**")
# # # # # #             slope, intercept, r, p, _ = stats.linregress(dff["GDP_Growth"], dff["Unemployment"])
# # # # # #             trendline_x = np.linspace(dff["GDP_Growth"].min(), dff["GDP_Growth"].max(), 100)
# # # # # #             trendline_y = slope * trendline_x + intercept

# # # # # #             fig = go.Figure()
# # # # # #             fig.add_trace(go.Scatter(
# # # # # #                 x=dff["GDP_Growth"], y=dff["Unemployment"],
# # # # # #                 mode="markers+text",
# # # # # #                 text=dff["Year"],
# # # # # #                 textposition="top center",
# # # # # #                 textfont=dict(size=9, color=COLORS["muted"]),
# # # # # #                 marker=dict(
# # # # # #                     size=10,
# # # # # #                     color=dff["Year"],
# # # # # #                     colorscale=[[0, COLORS["blue"]], [0.45, COLORS["blue"]],
# # # # # #                                 [0.86, COLORS["red"]], [1.0, COLORS["green"]]],
# # # # # #                     showscale=True,
# # # # # #                     colorbar=dict(title="Year", tickfont=dict(color=COLORS["muted"])),
# # # # # #                 ),
# # # # # #                 name="Observations",
# # # # # #             ))
# # # # # #             fig.add_trace(go.Scatter(
# # # # # #                 x=trendline_x, y=trendline_y,
# # # # # #                 mode="lines",
# # # # # #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # # # # #                 name=f"Trend (R²={r**2:.2f})",
# # # # # #             ))
# # # # # #             fig.update_layout(**LAYOUT_BASE, height=360,
# # # # # #                               xaxis=dict(**LAYOUT_BASE["xaxis"], title="GDP Growth %", ticksuffix="%"),
# # # # # #                               yaxis=dict(**LAYOUT_BASE["yaxis"], title="Unemployment %", ticksuffix="%"))
# # # # # #             st.plotly_chart(fig, use_container_width=True)
# # # # # #             st.caption(f"Pearson r = {r:.3f} | R² = {r**2:.3f} | p-value = {p:.4f}")

# # # # # #         with col2:
# # # # # #             st.markdown("**Inflation vs GDP Growth**")
# # # # # #             slope2, intercept2, r2, p2, _ = stats.linregress(dff["Inflation"], dff["GDP_Growth"])
# # # # # #             tx = np.linspace(dff["Inflation"].min(), dff["Inflation"].max(), 100)
# # # # # #             ty = slope2 * tx + intercept2

# # # # # #             fig2 = go.Figure()
# # # # # #             fig2.add_trace(go.Scatter(
# # # # # #                 x=dff["Inflation"], y=dff["GDP_Growth"],
# # # # # #                 mode="markers+text",
# # # # # #                 text=dff["Year"],
# # # # # #                 textposition="top center",
# # # # # #                 textfont=dict(size=9, color=COLORS["muted"]),
# # # # # #                 marker=dict(size=10, color=COLORS["yellow"], opacity=0.8),
# # # # # #                 name="Observations",
# # # # # #             ))
# # # # # #             fig2.add_trace(go.Scatter(
# # # # # #                 x=tx, y=ty, mode="lines",
# # # # # #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # # # # #                 name=f"Trend (R²={r2**2:.2f})",
# # # # # #             ))
# # # # # #             fig2.update_layout(**LAYOUT_BASE, height=360,
# # # # # #                                xaxis=dict(**LAYOUT_BASE["xaxis"], title="Inflation %", ticksuffix="%"),
# # # # # #                                yaxis=dict(**LAYOUT_BASE["yaxis"], title="GDP Growth %", ticksuffix="%"))
# # # # # #             st.plotly_chart(fig2, use_container_width=True)
# # # # # #             st.caption(f"Pearson r = {r2:.3f} | R² = {r2**2:.3f} | p-value = {p2:.4f}")

# # # # # #         # Correlation heatmap
# # # # # #         st.markdown("**Full Correlation Matrix**")
# # # # # #         corr_cols = ["GDP_B", "GDP_Growth", "Inflation", "Unemployment", "Exports_GDP", "Imports_GDP", "Trade_Balance"]
# # # # # #         corr_labels = ["GDP (B)", "GDP Growth", "Inflation", "Unemployment", "Exports", "Imports", "Trade Bal."]
# # # # # #         corr = dff[corr_cols].corr().values

# # # # # #         fig3 = go.Figure(go.Heatmap(
# # # # # #             z=corr,
# # # # # #             x=corr_labels, y=corr_labels,
# # # # # #             colorscale=[[0, COLORS["red"]], [0.5, COLORS["surface"]], [1, COLORS["green"]]],
# # # # # #             zmid=0, zmin=-1, zmax=1,
# # # # # #             text=[[f"{v:.2f}" for v in row] for row in corr],
# # # # # #             texttemplate="%{text}",
# # # # # #             textfont=dict(size=11, color=COLORS["text"]),
# # # # # #         ))
# # # # # #         fig3.update_layout(**LAYOUT_BASE, height=380)
# # # # # #         st.plotly_chart(fig3, use_container_width=True)

# # # # # # # ── TAB 6: Statistics ─────────────────────────────────────────────────────────
# # # # # # with tabs[5]:
# # # # # #     if show_stats:
# # # # # #         st.subheader("Statistical Summary")

# # # # # #         summary_cols = ["GDP_Growth", "Inflation", "Unemployment", "Exports_GDP", "Imports_GDP", "Trade_Balance"]
# # # # # #         summary_labels = {
# # # # # #             "GDP_Growth": "GDP Growth %",
# # # # # #             "Inflation": "Inflation %",
# # # # # #             "Unemployment": "Unemployment %",
# # # # # #             "Exports_GDP": "Exports % GDP",
# # # # # #             "Imports_GDP": "Imports % GDP",
# # # # # #             "Trade_Balance": "Trade Balance % GDP",
# # # # # #         }
# # # # # #         stats_df = dff[summary_cols].describe().T.round(2)
# # # # # #         stats_df.index = [summary_labels[i] for i in stats_df.index]
# # # # # #         stats_df.columns = ["Count", "Mean", "Std Dev", "Min", "25th %ile", "Median", "75th %ile", "Max"]

# # # # # #         st.dataframe(
# # # # # #             stats_df.style.background_gradient(
# # # # # #                 subset=["Mean"], cmap="RdYlGn", axis=0
# # # # # #             ).format("{:.2f}"),
# # # # # #             use_container_width=True,
# # # # # #         )

# # # # # #         st.markdown("---")
# # # # # #         st.markdown("**Raw Data Table**")
# # # # # #         display_df = dff[["Year", "Era", "GDP_B", "GDP_Growth", "Inflation",
# # # # # #                            "Unemployment", "Exports_GDP", "Imports_GDP", "Trade_Balance"]].copy()
# # # # # #         display_df.columns = ["Year", "Era", "GDP ($B)", "GDP Growth %", "Inflation %",
# # # # # #                               "Unemployment %", "Exports % GDP", "Imports % GDP", "Trade Balance %"]
# # # # # #         st.dataframe(display_df.set_index("Year"), use_container_width=True)

# # # # # #         col1, col2 = st.columns(2)
# # # # # #         with col1:
# # # # # #             csv = display_df.to_csv(index=False).encode("utf-8")
# # # # # #             st.download_button(
# # # # # #                 "⬇️ Download CSV",
# # # # # #                 data=csv,
# # # # # #                 file_name="kenya_economic_data.csv",
# # # # # #                 mime="text/csv",
# # # # # #             )

# # # # # # # ── Key Insights panel ────────────────────────────────────────────────────────
# # # # # # st.markdown("---")
# # # # # # st.subheader("Key Insights")

# # # # # # col1, col2, col3 = st.columns(3)

# # # # # # with col1:
# # # # # #     st.markdown("""
# # # # # #     <div class='insight-box'>
# # # # # #         <h4>📈 Sustained Long-Term Growth</h4>
# # # # # #         <p>Kenya's GDP grew from ~$12B in 2000 to $108B in 2023 — nearly 9× in nominal terms. 
# # # # # #         Average real GDP growth held at 4.7% over the past decade, one of sub-Saharan Africa's strongest sustained performers.</p>
# # # # # #     </div>
# # # # # #     """, unsafe_allow_html=True)

# # # # # # with col2:
# # # # # #     st.markdown("""
# # # # # #     <div class='insight-box warn'>
# # # # # #         <h4>🔥 Inflation Volatility</h4>
# # # # # #         <p>Inflation spiked above 26% in 2008 tied to the global food/energy crisis and post-election unrest. 
# # # # # #         The government's 5±2.5% CBK target is regularly breached, averaging 7.7% over the study period.</p>
# # # # # #     </div>
# # # # # #     """, unsafe_allow_html=True)

# # # # # # with col3:
# # # # # #     st.markdown("""
# # # # # #     <div class='insight-box danger'>
# # # # # #         <h4>🌍 Structural Trade Deficit</h4>
# # # # # #         <p>Kenya consistently imports more than it exports, driven by fuel, machinery, and manufactured goods. 
# # # # # #         The deficit averaged -8% to -9% of GDP — a persistent structural challenge to external balance.</p>
# # # # # #     </div>
# # # # # #     """, unsafe_allow_html=True)

# # # # # # st.markdown(
# # # # # #     "<br><small style='color:#3a4f3d'>Data: World Bank Open Data · Kenya National Bureau of Statistics · IMF DataMapper · 2000–2023</small>",
# # # # # #     unsafe_allow_html=True
# # # # # # )

# # # # # """
# # # # # Kenya Economic Indicators Dashboard
# # # # # Streamlit + Plotly data analysis project
# # # # # Data source: World Bank Open Data
# # # # # """

# # # # # import streamlit as st
# # # # # import pandas as pd
# # # # # import plotly.express as px
# # # # # import plotly.graph_objects as go
# # # # # from plotly.subplots import make_subplots
# # # # # import numpy as np
# # # # # from scipy import stats

# # # # # # ── Page config ──────────────────────────────────────────────────────────────
# # # # # st.set_page_config(
# # # # #     page_title="Kenya Economic Dashboard",
# # # # #     page_icon="🇰🇪",
# # # # #     layout="wide",
# # # # #     initial_sidebar_state="expanded",
# # # # # )

# # # # # # ── Custom CSS ────────────────────────────────────────────────────────────────
# # # # # st.markdown("""
# # # # # <style>
# # # # #     /* Main background */
# # # # #     .stApp { background-color: #0a0f0d; }
# # # # #     .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

# # # # #     /* Sidebar */
# # # # #     [data-testid="stSidebar"] { background-color: #111812; border-right: 1px solid #1e2e21; }
# # # # #     [data-testid="stSidebar"] * { color: #e8f0ea !important; }

# # # # #     /* KPI metric cards */
# # # # #     [data-testid="metric-container"] {
# # # # #         background: #111812;
# # # # #         border: 1px solid #1e2e21;
# # # # #         border-radius: 6px;
# # # # #         padding: 1rem 1.2rem;
# # # # #     }
# # # # #     [data-testid="stMetricLabel"] { color: #6b7f6e !important; font-size: 0.75rem; }
# # # # #     [data-testid="stMetricValue"] { color: #e8f0ea !important; }
# # # # #     [data-testid="stMetricDelta"] { font-size: 0.8rem; }

# # # # #     /* Headers */
# # # # #     h1, h2, h3 { color: #e8f0ea !important; }
# # # # #     p, li { color: #b0bfb3 !important; }

# # # # #     /* Tabs */
# # # # #     .stTabs [data-baseweb="tab-list"] { background-color: #111812; border-bottom: 1px solid #1e2e21; }
# # # # #     .stTabs [data-baseweb="tab"] { color: #6b7f6e; }
# # # # #     .stTabs [aria-selected="true"] { color: #3ddc6e !important; border-bottom-color: #3ddc6e !important; }

# # # # #     /* Divider */
# # # # #     hr { border-color: #1e2e21; }

# # # # #     /* Info/success boxes */
# # # # #     .stAlert { background-color: #111812; border-color: #1e2e21; }

# # # # #     /* Section header style */
# # # # #     .section-label {
# # # # #         font-family: monospace;
# # # # #         font-size: 0.65rem;
# # # # #         letter-spacing: 0.2em;
# # # # #         color: #3ddc6e;
# # # # #         text-transform: uppercase;
# # # # #         margin-bottom: 0.25rem;
# # # # #     }
# # # # #     .insight-box {
# # # # #         background: #111812;
# # # # #         border: 1px solid #1e2e21;
# # # # #         border-left: 3px solid #3ddc6e;
# # # # #         border-radius: 4px;
# # # # #         padding: 1rem 1.2rem;
# # # # #         margin-bottom: 0.75rem;
# # # # #     }
# # # # #     .insight-box.warn { border-left-color: #f5c842; }
# # # # #     .insight-box.danger { border-left-color: #e85d4a; }
# # # # #     .insight-box h4 { color: #e8f0ea !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# # # # #     .insight-box p { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# # # # # </style>
# # # # # """, unsafe_allow_html=True)

# # # # # # ── Data ──────────────────────────────────────────────────────────────────────
# # # # # @st.cache_data
# # # # # def load_data():
# # # # #     data = {
# # # # #         "Year":         list(range(2000, 2024)),
# # # # #         "GDP_B":        [12.7,13.3,13.4,14.0,15.1,18.7,22.5,27.2,30.6,29.5,
# # # # #                          32.2,34.0,41.1,47.6,60.9,63.4,70.5,79.3,87.8,95.5,
# # # # #                          98.8,99.2,110.4,107.9],
# # # # #         "GDP_Growth":   [0.6, 4.5, 0.3, 2.9, 4.6, 5.9, 6.5, 6.9, 1.5, 2.7,
# # # # #                          8.4, 6.1, 4.6, 5.9, 5.4, 5.7, 5.9, 4.9, 6.3, 5.4,
# # # # #                         -0.3, 7.6, 4.8, 5.6],
# # # # #         "Inflation":    [10.0, 5.8, 2.0, 9.8,11.6,10.3, 6.0, 4.3,26.2,10.5,
# # # # #                           4.0,14.0, 9.4, 5.7, 6.9, 6.6, 6.3, 8.0, 4.7, 5.2,
# # # # #                           5.3, 6.1, 9.1, 6.3],
# # # # #         "Unemployment": [9.8, 9.8, 9.8, 9.8, 9.8, 9.3, 8.7, 8.1, 7.4, 6.7,
# # # # #                          6.1, 5.5, 4.9, 4.4, 3.9, 3.5, 2.8, 3.5, 4.3, 5.0,
# # # # #                          5.6, 5.7, 5.7, 5.6],
# # # # #         "Exports_GDP":  [25.2,24.8,23.6,23.0,24.0,23.8,23.0,24.5,24.1,20.4,
# # # # #                          21.2,21.0,19.5,18.3,16.9,15.7,14.6,13.8,13.9,13.5,
# # # # #                          12.4,13.5,14.2,13.8],
# # # # #         "Imports_GDP":  [33.1,32.5,31.6,30.5,32.0,31.8,33.0,37.2,42.4,36.3,
# # # # #                          36.1,40.0,38.5,37.3,34.5,32.5,30.6,29.8,31.9,29.5,
# # # # #                          26.7,28.0,32.6,31.2],
# # # # #     }
# # # # #     df = pd.DataFrame(data)
# # # # #     df["Trade_Balance"] = df["Exports_GDP"] - df["Imports_GDP"]
# # # # #     df["Era"] = df["Year"].apply(
# # # # #         lambda y: "🔴 COVID" if 2020 <= y <= 2021
# # # # #         else ("🟡 Post-COVID" if y >= 2022
# # # # #         else ("🟢 Growth" if y >= 2010
# # # # #         else "🔵 Early 2000s"))
# # # # #     )
# # # # #     return df

# # # # # df = load_data()

# # # # # # ── Plotly theme defaults ─────────────────────────────────────────────────────
# # # # # COLORS = {
# # # # #     "bg":      "#0a0f0d",
# # # # #     "surface": "#111812",
# # # # #     "border":  "#1e2e21",
# # # # #     "green":   "#3ddc6e",
# # # # #     "yellow":  "#f5c842",
# # # # #     "red":     "#e85d4a",
# # # # #     "blue":    "#4a9de8",
# # # # #     "muted":   "#6b7f6e",
# # # # #     "text":    "#e8f0ea",
# # # # # }

# # # # # GRID = dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], tickcolor=COLORS["border"])

# # # # # def layout(height=360, xaxis_extra=None, yaxis_extra=None, **kwargs):
# # # # #     """Return a fresh layout dict — avoids duplicate-keyword errors."""
# # # # #     x = {**GRID, **(xaxis_extra or {})}
# # # # #     y = {**GRID, **(yaxis_extra or {})}
# # # # #     return dict(
# # # # #         paper_bgcolor=COLORS["surface"],
# # # # #         plot_bgcolor=COLORS["bg"],
# # # # #         font=dict(family="DM Mono, monospace", color=COLORS["muted"], size=11),
# # # # #         xaxis=x,
# # # # #         yaxis=y,
# # # # #         margin=dict(t=40, b=40, l=50, r=20),
# # # # #         legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
# # # # #         height=height,
# # # # #         **kwargs,
# # # # #     )

# # # # # # ── Sidebar ───────────────────────────────────────────────────────────────────
# # # # # with st.sidebar:
# # # # #     st.markdown("### 🇰🇪 Kenya Dashboard")
# # # # #     st.markdown("---")

# # # # #     st.markdown("**TIME RANGE**")
# # # # #     year_range = st.slider(
# # # # #         "Select years",
# # # # #         min_value=2000, max_value=2023,
# # # # #         value=(2005, 2023),
# # # # #         label_visibility="collapsed"
# # # # #     )

# # # # #     st.markdown("---")
# # # # #     st.markdown("**INDICATORS**")
# # # # #     show_gdp      = st.checkbox("GDP & Growth",       value=True)
# # # # #     show_inf      = st.checkbox("Inflation",           value=True)
# # # # #     show_unemp    = st.checkbox("Unemployment",        value=True)
# # # # #     show_trade    = st.checkbox("Trade Balance",       value=True)
# # # # #     show_scatter  = st.checkbox("Correlation Analysis",value=True)
# # # # #     show_stats    = st.checkbox("Statistical Summary", value=True)

# # # # #     st.markdown("---")
# # # # #     st.markdown("**HIGHLIGHT ERA**")
# # # # #     highlight_covid = st.toggle("Highlight COVID period", value=True)

# # # # #     st.markdown("---")
# # # # #     st.markdown(
# # # # #         "<small style='color:#3a4f3d'>Source: World Bank Open Data<br>"
# # # # #         "Period: 2000–2023</small>",
# # # # #         unsafe_allow_html=True
# # # # #     )

# # # # # # ── Filter data ───────────────────────────────────────────────────────────────
# # # # # dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

# # # # # # ── Header ────────────────────────────────────────────────────────────────────
# # # # # st.markdown(
# # # # #     "<p class='section-label'>REPUBLIC OF KENYA · KE · WORLD BANK OPEN DATA</p>",
# # # # #     unsafe_allow_html=True
# # # # # )
# # # # # st.title("Economic Indicators Analysis")
# # # # # st.markdown(
# # # # #     f"**GDP · Inflation · Unemployment · Trade Balance** &nbsp;·&nbsp; "
# # # # #     f"{year_range[0]}–{year_range[1]}",
# # # # # )
# # # # # st.markdown("---")

# # # # # # ── KPI Cards ─────────────────────────────────────────────────────────────────
# # # # # latest = dff.iloc[-1]
# # # # # prev   = dff.iloc[-2]

# # # # # k1, k2, k3, k4 = st.columns(4)
# # # # # k1.metric("GDP (Latest Year)",        f"${latest['GDP_B']:.1f}B",
# # # # #           f"{latest['GDP_Growth']:+.1f}% growth")
# # # # # k2.metric("Inflation",                f"{latest['Inflation']:.1f}%",
# # # # #           f"{latest['Inflation'] - prev['Inflation']:+.1f}pp vs prior year")
# # # # # k3.metric("Unemployment",             f"{latest['Unemployment']:.1f}%",
# # # # #           f"{latest['Unemployment'] - prev['Unemployment']:+.1f}pp vs prior year")
# # # # # k4.metric("Trade Balance (% GDP)",    f"{latest['Trade_Balance']:.1f}%",
# # # # #           f"{latest['Trade_Balance'] - prev['Trade_Balance']:+.1f}pp vs prior year")

# # # # # st.markdown("---")

# # # # # # ── Tabs ──────────────────────────────────────────────────────────────────────
# # # # # tabs = st.tabs(["📈 GDP", "🔥 Inflation", "👷 Unemployment", "🌍 Trade", "🔗 Correlations", "📊 Statistics"])

# # # # # # COVID shading helper
# # # # # def add_covid_band(fig, y_min=None, y_max=None):
# # # # #     if highlight_covid:
# # # # #         fig.add_vrect(
# # # # #             x0=2019.5, x1=2021.5,
# # # # #             fillcolor="rgba(232,93,74,0.08)",
# # # # #             line=dict(color="rgba(232,93,74,0.3)", width=1, dash="dot"),
# # # # #             annotation_text="COVID", annotation_position="top left",
# # # # #             annotation_font=dict(color=COLORS["red"], size=10),
# # # # #         )
# # # # #     return fig

# # # # # # ── TAB 1: GDP ────────────────────────────────────────────────────────────────
# # # # # with tabs[0]:
# # # # #     if show_gdp:
# # # # #         st.subheader("GDP Growth Over Time")

# # # # #         fig = make_subplots(specs=[[{"secondary_y": True}]])

# # # # #         fig.add_trace(
# # # # #             go.Bar(
# # # # #                 x=dff["Year"], y=dff["GDP_B"],
# # # # #                 name="GDP (USD Billion)",
# # # # #                 marker=dict(color=COLORS["green"], opacity=0.25,
# # # # #                             line=dict(color=COLORS["green"], width=1)),
# # # # #             ), secondary_y=False
# # # # #         )
# # # # #         fig.add_trace(
# # # # #             go.Scatter(
# # # # #                 x=dff["Year"], y=dff["GDP_Growth"],
# # # # #                 name="GDP Growth %",
# # # # #                 line=dict(color=COLORS["green"], width=2.5),
# # # # #                 mode="lines+markers",
# # # # #                 marker=dict(size=5, color=COLORS["green"]),
# # # # #             ), secondary_y=True
# # # # #         )

# # # # #         fig.update_layout(**layout(height=380), title="")
# # # # #         fig.update_yaxes(title_text="GDP (USD Billion)", secondary_y=False,
# # # # #                          tickprefix="$", ticksuffix="B",
# # # # #                          gridcolor=COLORS["border"], linecolor=COLORS["border"])
# # # # #         fig.update_yaxes(title_text="Growth Rate (%)", secondary_y=True,
# # # # #                          ticksuffix="%", gridcolor="rgba(0,0,0,0)")
# # # # #         fig.update_xaxes(gridcolor=COLORS["border"])
# # # # #         add_covid_band(fig)

# # # # #         st.plotly_chart(fig, use_container_width=True)

# # # # #         # GDP decomposition
# # # # #         col1, col2 = st.columns(2)
# # # # #         with col1:
# # # # #             st.markdown("**Year-on-Year GDP Change (USD Billion)**")
# # # # #             dff_copy = dff.copy()
# # # # #             dff_copy["GDP_Change"] = dff_copy["GDP_B"].diff()
# # # # #             fig2 = go.Figure(go.Bar(
# # # # #                 x=dff_copy["Year"][1:], y=dff_copy["GDP_Change"][1:],
# # # # #                 marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# # # # #                               for v in dff_copy["GDP_Change"][1:]],
# # # # #                 text=[f"${v:+.1f}B" for v in dff_copy["GDP_Change"][1:]],
# # # # #                 textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# # # # #             ))
# # # # #             fig2.update_layout(**layout(height=280, yaxis_extra=dict(tickprefix="$", ticksuffix="B")))
# # # # #             add_covid_band(fig2)
# # # # #             st.plotly_chart(fig2, use_container_width=True)

# # # # #         with col2:
# # # # #             st.markdown("**GDP by Era (Average Growth %)**")
# # # # #             era_avg = df.groupby("Era")["GDP_Growth"].mean().reset_index()
# # # # #             fig3 = go.Figure(go.Bar(
# # # # #                 x=era_avg["Era"], y=era_avg["GDP_Growth"],
# # # # #                 marker_color=[COLORS["blue"], COLORS["red"], COLORS["green"], COLORS["yellow"]],
# # # # #                 text=[f"{v:.1f}%" for v in era_avg["GDP_Growth"]],
# # # # #                 textposition="outside", textfont=dict(size=10, color=COLORS["text"]),
# # # # #             ))
# # # # #             fig3.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
# # # # #             st.plotly_chart(fig3, use_container_width=True)

# # # # # # ── TAB 2: Inflation ──────────────────────────────────────────────────────────
# # # # # with tabs[1]:
# # # # #     if show_inf:
# # # # #         st.subheader("Inflation (CPI) Trend")

# # # # #         fig = go.Figure()

# # # # #         # Target band fill
# # # # #         fig.add_trace(go.Scatter(
# # # # #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# # # # #             y=[7.5]*len(dff) + [2.5]*len(dff),
# # # # #             fill="toself",
# # # # #             fillcolor="rgba(61,220,110,0.06)",
# # # # #             line=dict(color="rgba(0,0,0,0)"),
# # # # #             name="CBK Target Band (2.5–7.5%)",
# # # # #             showlegend=True,
# # # # #         ))

# # # # #         fig.add_hline(y=7.5, line=dict(color=COLORS["red"], dash="dot", width=1),
# # # # #                       annotation_text="Upper target 7.5%",
# # # # #                       annotation_font=dict(color=COLORS["red"], size=10))
# # # # #         fig.add_hline(y=2.5, line=dict(color=COLORS["green"], dash="dot", width=1),
# # # # #                       annotation_text="Lower target 2.5%",
# # # # #                       annotation_font=dict(color=COLORS["green"], size=10))

# # # # #         fig.add_trace(go.Scatter(
# # # # #             x=dff["Year"], y=dff["Inflation"],
# # # # #             name="CPI Inflation",
# # # # #             line=dict(color=COLORS["yellow"], width=2.5),
# # # # #             mode="lines+markers",
# # # # #             marker=dict(size=5, color=dff["Inflation"].apply(
# # # # #                 lambda v: COLORS["red"] if v > 7.5 else (COLORS["green"] if v < 2.5 else COLORS["yellow"])
# # # # #             )),
# # # # #             fill="tozeroy",
# # # # #             fillcolor="rgba(245,200,66,0.07)",
# # # # #         ))

# # # # #         fig.update_layout(**layout(height=380, yaxis_extra=dict(ticksuffix="%", title="CPI %")))
# # # # #         add_covid_band(fig)
# # # # #         st.plotly_chart(fig, use_container_width=True)

# # # # #         col1, col2 = st.columns(2)
# # # # #         with col1:
# # # # #             # Above/below target
# # # # #             above = (dff["Inflation"] > 7.5).sum()
# # # # #             within = ((dff["Inflation"] >= 2.5) & (dff["Inflation"] <= 7.5)).sum()
# # # # #             below = (dff["Inflation"] < 2.5).sum()
# # # # #             fig2 = go.Figure(go.Pie(
# # # # #                 labels=["Above target (>7.5%)", "Within target", "Below target (<2.5%)"],
# # # # #                 values=[above, within, below],
# # # # #                 hole=0.55,
# # # # #                 marker=dict(colors=[COLORS["red"], COLORS["green"], COLORS["blue"]]),
# # # # #                 textfont=dict(color=COLORS["text"]),
# # # # #             ))
# # # # #             fig2.update_layout(**layout(height=280),
# # # # #                                title=dict(text="Years Within CBK Target", font=dict(color=COLORS["text"])))
# # # # #             st.plotly_chart(fig2, use_container_width=True)

# # # # #         with col2:
# # # # #             st.markdown("**Inflation Distribution**")
# # # # #             fig3 = go.Figure(go.Histogram(
# # # # #                 x=dff["Inflation"], nbinsx=10,
# # # # #                 marker=dict(color=COLORS["yellow"], opacity=0.7,
# # # # #                             line=dict(color=COLORS["bg"], width=1)),
# # # # #                 name="Inflation %",
# # # # #             ))
# # # # #             fig3.add_vline(x=dff["Inflation"].mean(),
# # # # #                            line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # # # #                            annotation_text=f"Mean: {dff['Inflation'].mean():.1f}%",
# # # # #                            annotation_font=dict(color=COLORS["text"], size=10))
# # # # #             fig3.update_layout(**layout(height=280,
# # # # #                                xaxis_extra=dict(title="Inflation %"),
# # # # #                                yaxis_extra=dict(title="Count")))
# # # # #             st.plotly_chart(fig3, use_container_width=True)

# # # # # # ── TAB 3: Unemployment ───────────────────────────────────────────────────────
# # # # # with tabs[2]:
# # # # #     if show_unemp:
# # # # #         st.subheader("Unemployment Rate Trajectory")

# # # # #         fig = go.Figure()
# # # # #         fig.add_trace(go.Scatter(
# # # # #             x=dff["Year"], y=dff["Unemployment"],
# # # # #             name="Unemployment %",
# # # # #             line=dict(color=COLORS["red"], width=2.5),
# # # # #             mode="lines+markers",
# # # # #             marker=dict(size=6, color=COLORS["red"]),
# # # # #             fill="tozeroy",
# # # # #             fillcolor="rgba(232,93,74,0.1)",
# # # # #         ))

# # # # #         # Rolling average
# # # # #         dff_copy = dff.copy()
# # # # #         dff_copy["Unemp_MA3"] = dff_copy["Unemployment"].rolling(3, center=True).mean()
# # # # #         fig.add_trace(go.Scatter(
# # # # #             x=dff_copy["Year"], y=dff_copy["Unemp_MA3"],
# # # # #             name="3-Year Rolling Avg",
# # # # #             line=dict(color=COLORS["text"], width=1.5, dash="dot"),
# # # # #             mode="lines",
# # # # #         ))

# # # # #         fig.update_layout(**layout(height=360, yaxis_extra=dict(ticksuffix="%", title="Unemployment %")))
# # # # #         add_covid_band(fig)
# # # # #         st.plotly_chart(fig, use_container_width=True)

# # # # #         col1, col2, col3 = st.columns(3)
# # # # #         col1.metric("Peak Unemployment", f"{dff['Unemployment'].max():.1f}%",
# # # # #                     f"in {int(dff.loc[dff['Unemployment'].idxmax(), 'Year'])}")
# # # # #         col2.metric("Lowest Unemployment", f"{dff['Unemployment'].min():.1f}%",
# # # # #                     f"in {int(dff.loc[dff['Unemployment'].idxmin(), 'Year'])}")
# # # # #         col3.metric("Average (Period)", f"{dff['Unemployment'].mean():.1f}%", "ILO modeled estimate")

# # # # # # ── TAB 4: Trade ──────────────────────────────────────────────────────────────
# # # # # with tabs[3]:
# # # # #     if show_trade:
# # # # #         st.subheader("Trade Balance: Exports vs Imports")

# # # # #         fig = go.Figure()
# # # # #         fig.add_trace(go.Scatter(
# # # # #             x=dff["Year"], y=dff["Exports_GDP"],
# # # # #             name="Exports % GDP",
# # # # #             line=dict(color=COLORS["blue"], width=2.5),
# # # # #             mode="lines+markers", marker=dict(size=4),
# # # # #         ))
# # # # #         fig.add_trace(go.Scatter(
# # # # #             x=dff["Year"], y=dff["Imports_GDP"],
# # # # #             name="Imports % GDP",
# # # # #             line=dict(color=COLORS["yellow"], width=2.5),
# # # # #             mode="lines+markers", marker=dict(size=4),
# # # # #         ))

# # # # #         # Fill between gap
# # # # #         fig.add_trace(go.Scatter(
# # # # #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# # # # #             y=list(dff["Imports_GDP"]) + list(dff["Exports_GDP"])[::-1],
# # # # #             fill="toself",
# # # # #             fillcolor="rgba(232,93,74,0.08)",
# # # # #             line=dict(color="rgba(0,0,0,0)"),
# # # # #             name="Trade Deficit",
# # # # #             showlegend=True,
# # # # #         ))

# # # # #         fig.update_layout(**layout(height=360, yaxis_extra=dict(ticksuffix="%", title="% of GDP")))
# # # # #         add_covid_band(fig)
# # # # #         st.plotly_chart(fig, use_container_width=True)

# # # # #         st.markdown("**Net Trade Balance (% GDP)**")
# # # # #         fig2 = go.Figure(go.Bar(
# # # # #             x=dff["Year"], y=dff["Trade_Balance"],
# # # # #             marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# # # # #                           for v in dff["Trade_Balance"]],
# # # # #             text=[f"{v:.1f}%" for v in dff["Trade_Balance"]],
# # # # #             textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# # # # #         ))
# # # # #         fig2.add_hline(y=0, line=dict(color=COLORS["muted"], width=1))
# # # # #         fig2.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
# # # # #         add_covid_band(fig2)
# # # # #         st.plotly_chart(fig2, use_container_width=True)

# # # # # # ── TAB 5: Correlations ───────────────────────────────────────────────────────
# # # # # with tabs[4]:
# # # # #     if show_scatter:
# # # # #         st.subheader("Correlation Analysis")

# # # # #         col1, col2 = st.columns(2)

# # # # #         with col1:
# # # # #             st.markdown("**GDP Growth vs Unemployment**")
# # # # #             slope, intercept, r, p, _ = stats.linregress(dff["GDP_Growth"], dff["Unemployment"])
# # # # #             trendline_x = np.linspace(dff["GDP_Growth"].min(), dff["GDP_Growth"].max(), 100)
# # # # #             trendline_y = slope * trendline_x + intercept

# # # # #             fig = go.Figure()
# # # # #             fig.add_trace(go.Scatter(
# # # # #                 x=dff["GDP_Growth"], y=dff["Unemployment"],
# # # # #                 mode="markers+text",
# # # # #                 text=dff["Year"],
# # # # #                 textposition="top center",
# # # # #                 textfont=dict(size=9, color=COLORS["muted"]),
# # # # #                 marker=dict(
# # # # #                     size=10,
# # # # #                     color=dff["Year"],
# # # # #                     colorscale=[[0, COLORS["blue"]], [0.45, COLORS["blue"]],
# # # # #                                 [0.86, COLORS["red"]], [1.0, COLORS["green"]]],
# # # # #                     showscale=True,
# # # # #                     colorbar=dict(title="Year", tickfont=dict(color=COLORS["muted"])),
# # # # #                 ),
# # # # #                 name="Observations",
# # # # #             ))
# # # # #             fig.add_trace(go.Scatter(
# # # # #                 x=trendline_x, y=trendline_y,
# # # # #                 mode="lines",
# # # # #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # # # #                 name=f"Trend (R²={r**2:.2f})",
# # # # #             ))
# # # # #             fig.update_layout(**layout(height=360,
# # # # #                               xaxis_extra=dict(title="GDP Growth %", ticksuffix="%"),
# # # # #                               yaxis_extra=dict(title="Unemployment %", ticksuffix="%")))
# # # # #             st.plotly_chart(fig, use_container_width=True)
# # # # #             st.caption(f"Pearson r = {r:.3f} | R² = {r**2:.3f} | p-value = {p:.4f}")

# # # # #         with col2:
# # # # #             st.markdown("**Inflation vs GDP Growth**")
# # # # #             slope2, intercept2, r2, p2, _ = stats.linregress(dff["Inflation"], dff["GDP_Growth"])
# # # # #             tx = np.linspace(dff["Inflation"].min(), dff["Inflation"].max(), 100)
# # # # #             ty = slope2 * tx + intercept2

# # # # #             fig2 = go.Figure()
# # # # #             fig2.add_trace(go.Scatter(
# # # # #                 x=dff["Inflation"], y=dff["GDP_Growth"],
# # # # #                 mode="markers+text",
# # # # #                 text=dff["Year"],
# # # # #                 textposition="top center",
# # # # #                 textfont=dict(size=9, color=COLORS["muted"]),
# # # # #                 marker=dict(size=10, color=COLORS["yellow"], opacity=0.8),
# # # # #                 name="Observations",
# # # # #             ))
# # # # #             fig2.add_trace(go.Scatter(
# # # # #                 x=tx, y=ty, mode="lines",
# # # # #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # # # #                 name=f"Trend (R²={r2**2:.2f})",
# # # # #             ))
# # # # #             fig2.update_layout(**layout(height=360,
# # # # #                                xaxis_extra=dict(title="Inflation %", ticksuffix="%"),
# # # # #                                yaxis_extra=dict(title="GDP Growth %", ticksuffix="%")))
# # # # #             st.plotly_chart(fig2, use_container_width=True)
# # # # #             st.caption(f"Pearson r = {r2:.3f} | R² = {r2**2:.3f} | p-value = {p2:.4f}")

# # # # #         # Correlation heatmap
# # # # #         st.markdown("**Full Correlation Matrix**")
# # # # #         corr_cols = ["GDP_B", "GDP_Growth", "Inflation", "Unemployment", "Exports_GDP", "Imports_GDP", "Trade_Balance"]
# # # # #         corr_labels = ["GDP (B)", "GDP Growth", "Inflation", "Unemployment", "Exports", "Imports", "Trade Bal."]
# # # # #         corr = dff[corr_cols].corr().values

# # # # #         fig3 = go.Figure(go.Heatmap(
# # # # #             z=corr,
# # # # #             x=corr_labels, y=corr_labels,
# # # # #             colorscale=[[0, COLORS["red"]], [0.5, COLORS["surface"]], [1, COLORS["green"]]],
# # # # #             zmid=0, zmin=-1, zmax=1,
# # # # #             text=[[f"{v:.2f}" for v in row] for row in corr],
# # # # #             texttemplate="%{text}",
# # # # #             textfont=dict(size=11, color=COLORS["text"]),
# # # # #         ))
# # # # #         fig3.update_layout(**layout(height=380))
# # # # #         st.plotly_chart(fig3, use_container_width=True)

# # # # # # ── TAB 6: Statistics ─────────────────────────────────────────────────────────
# # # # # with tabs[5]:
# # # # #     if show_stats:
# # # # #         st.subheader("Statistical Summary")

# # # # #         summary_cols = ["GDP_Growth", "Inflation", "Unemployment", "Exports_GDP", "Imports_GDP", "Trade_Balance"]
# # # # #         summary_labels = {
# # # # #             "GDP_Growth": "GDP Growth %",
# # # # #             "Inflation": "Inflation %",
# # # # #             "Unemployment": "Unemployment %",
# # # # #             "Exports_GDP": "Exports % GDP",
# # # # #             "Imports_GDP": "Imports % GDP",
# # # # #             "Trade_Balance": "Trade Balance % GDP",
# # # # #         }
# # # # #         stats_df = dff[summary_cols].describe().T.round(2)
# # # # #         stats_df.index = [summary_labels[i] for i in stats_df.index]
# # # # #         stats_df.columns = ["Count", "Mean", "Std Dev", "Min", "25th %ile", "Median", "75th %ile", "Max"]

# # # # #         st.dataframe(
# # # # #             stats_df.style.background_gradient(
# # # # #                 subset=["Mean"], cmap="RdYlGn", axis=0
# # # # #             ).format("{:.2f}"),
# # # # #             use_container_width=True,
# # # # #         )

# # # # #         st.markdown("---")
# # # # #         st.markdown("**Raw Data Table**")
# # # # #         display_df = dff[["Year", "Era", "GDP_B", "GDP_Growth", "Inflation",
# # # # #                            "Unemployment", "Exports_GDP", "Imports_GDP", "Trade_Balance"]].copy()
# # # # #         display_df.columns = ["Year", "Era", "GDP ($B)", "GDP Growth %", "Inflation %",
# # # # #                               "Unemployment %", "Exports % GDP", "Imports % GDP", "Trade Balance %"]
# # # # #         st.dataframe(display_df.set_index("Year"), use_container_width=True)

# # # # #         col1, col2 = st.columns(2)
# # # # #         with col1:
# # # # #             csv = display_df.to_csv(index=False).encode("utf-8")
# # # # #             st.download_button(
# # # # #                 "⬇️ Download CSV",
# # # # #                 data=csv,
# # # # #                 file_name="kenya_economic_data.csv",
# # # # #                 mime="text/csv",
# # # # #             )

# # # # # # ── Key Insights panel ────────────────────────────────────────────────────────
# # # # # st.markdown("---")
# # # # # st.subheader("Key Insights")

# # # # # col1, col2, col3 = st.columns(3)

# # # # # with col1:
# # # # #     st.markdown("""
# # # # #     <div class='insight-box'>
# # # # #         <h4>📈 Sustained Long-Term Growth</h4>
# # # # #         <p>Kenya's GDP grew from ~$12B in 2000 to $108B in 2023 — nearly 9× in nominal terms. 
# # # # #         Average real GDP growth held at 4.7% over the past decade, one of sub-Saharan Africa's strongest sustained performers.</p>
# # # # #     </div>
# # # # #     """, unsafe_allow_html=True)

# # # # # with col2:
# # # # #     st.markdown("""
# # # # #     <div class='insight-box warn'>
# # # # #         <h4>🔥 Inflation Volatility</h4>
# # # # #         <p>Inflation spiked above 26% in 2008 tied to the global food/energy crisis and post-election unrest. 
# # # # #         The government's 5±2.5% CBK target is regularly breached, averaging 7.7% over the study period.</p>
# # # # #     </div>
# # # # #     """, unsafe_allow_html=True)

# # # # # with col3:
# # # # #     st.markdown("""
# # # # #     <div class='insight-box danger'>
# # # # #         <h4>🌍 Structural Trade Deficit</h4>
# # # # #         <p>Kenya consistently imports more than it exports, driven by fuel, machinery, and manufactured goods. 
# # # # #         The deficit averaged -8% to -9% of GDP — a persistent structural challenge to external balance.</p>
# # # # #     </div>
# # # # #     """, unsafe_allow_html=True)

# # # # # st.markdown(
# # # # #     "<br><small style='color:#3a4f3d'>Data: World Bank Open Data · Kenya National Bureau of Statistics · IMF DataMapper · 2000–2023</small>",
# # # # #     unsafe_allow_html=True
# # # # # )

# # # # """
# # # # Kenya Economic Indicators Dashboard
# # # # Streamlit + Plotly | Phase 1 Upgrades:
# # # #   - Live World Bank API via wbgapi (falls back to built-in data)
# # # #   - 5-Year Forecasting Panel (Linear + Polynomial regression)
# # # # Data source: World Bank Open Data
# # # # """

# # # # import streamlit as st
# # # # import pandas as pd
# # # # import plotly.graph_objects as go
# # # # from plotly.subplots import make_subplots
# # # # import numpy as np
# # # # from scipy import stats
# # # # from sklearn.linear_model import LinearRegression
# # # # from sklearn.preprocessing import PolynomialFeatures
# # # # from sklearn.pipeline import make_pipeline
# # # # from datetime import datetime

# # # # # ── Page config ───────────────────────────────────────────────────────────────
# # # # st.set_page_config(
# # # #     page_title="Kenya Economic Dashboard",
# # # #     page_icon="🇰🇪",
# # # #     layout="wide",
# # # #     initial_sidebar_state="expanded",
# # # # )

# # # # # ── Custom CSS ────────────────────────────────────────────────────────────────
# # # # st.markdown("""
# # # # <style>
# # # #     .stApp { background-color: #0a0f0d; }
# # # #     .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
# # # #     [data-testid="stSidebar"] { background-color: #111812; border-right: 1px solid #1e2e21; }
# # # #     [data-testid="stSidebar"] * { color: #e8f0ea !important; }
# # # #     [data-testid="metric-container"] {
# # # #         background: #111812; border: 1px solid #1e2e21;
# # # #         border-radius: 6px; padding: 1rem 1.2rem;
# # # #     }
# # # #     [data-testid="stMetricLabel"] { color: #6b7f6e !important; font-size: 0.75rem; }
# # # #     [data-testid="stMetricValue"] { color: #e8f0ea !important; }
# # # #     [data-testid="stMetricDelta"]  { font-size: 0.8rem; }
# # # #     h1, h2, h3 { color: #e8f0ea !important; }
# # # #     p, li { color: #b0bfb3 !important; }
# # # #     .stTabs [data-baseweb="tab-list"] { background-color: #111812; border-bottom: 1px solid #1e2e21; }
# # # #     .stTabs [data-baseweb="tab"] { color: #6b7f6e; }
# # # #     .stTabs [aria-selected="true"] { color: #3ddc6e !important; border-bottom-color: #3ddc6e !important; }
# # # #     hr { border-color: #1e2e21; }
# # # #     .stAlert { background-color: #111812; border-color: #1e2e21; }
# # # #     .section-label {
# # # #         font-family: monospace; font-size: 0.65rem;
# # # #         letter-spacing: 0.2em; color: #3ddc6e;
# # # #         text-transform: uppercase; margin-bottom: 0.25rem;
# # # #     }
# # # #     .data-badge {
# # # #         display: inline-block; font-family: monospace;
# # # #         font-size: 0.62rem; letter-spacing: 0.1em;
# # # #         padding: 0.25rem 0.65rem; border-radius: 2px; margin-bottom: 1rem;
# # # #     }
# # # #     .badge-live  { background: rgba(61,220,110,0.15); color: #3ddc6e; border: 1px solid #3ddc6e; }
# # # #     .badge-cache { background: rgba(245,200,66,0.15); color: #f5c842; border: 1px solid #f5c842; }
# # # #     .insight-box {
# # # #         background: #111812; border: 1px solid #1e2e21;
# # # #         border-left: 3px solid #3ddc6e; border-radius: 4px;
# # # #         padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# # # #     }
# # # #     .insight-box.warn   { border-left-color: #f5c842; }
# # # #     .insight-box.danger { border-left-color: #e85d4a; }
# # # #     .insight-box h4 { color: #e8f0ea !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# # # #     .insight-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# # # #     .forecast-box {
# # # #         background: rgba(74,157,232,0.06); border: 1px solid rgba(74,157,232,0.25);
# # # #         border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# # # #     }
# # # #     .forecast-box h4 { color: #4a9de8 !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# # # #     .forecast-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# # # # </style>
# # # # """, unsafe_allow_html=True)

# # # # # ── Colors & layout helper ────────────────────────────────────────────────────
# # # # COLORS = {
# # # #     "bg": "#0a0f0d", "surface": "#111812", "border": "#1e2e21",
# # # #     "green": "#3ddc6e", "yellow": "#f5c842", "red": "#e85d4a",
# # # #     "blue": "#4a9de8", "purple": "#a78bfa", "muted": "#6b7f6e", "text": "#e8f0ea",
# # # # }
# # # # GRID = dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], tickcolor=COLORS["border"])

# # # # def layout(height=360, xaxis_extra=None, yaxis_extra=None, **kwargs):
# # # #     return dict(
# # # #         paper_bgcolor=COLORS["surface"], plot_bgcolor=COLORS["bg"],
# # # #         font=dict(family="DM Mono, monospace", color=COLORS["muted"], size=11),
# # # #         xaxis={**GRID, **(xaxis_extra or {})},
# # # #         yaxis={**GRID, **(yaxis_extra or {})},
# # # #         margin=dict(t=40, b=40, l=55, r=20),
# # # #         legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
# # # #         height=height, **kwargs,
# # # #     )

# # # # # ── World Bank indicator codes ────────────────────────────────────────────────
# # # # WB_INDICATORS = {
# # # #     "GDP_B":        "NY.GDP.MKTP.CD",
# # # #     "GDP_Growth":   "NY.GDP.MKTP.KD.ZG",
# # # #     "Inflation":    "FP.CPI.TOTL.ZG",
# # # #     "Unemployment": "SL.UEM.TOTL.ZS",
# # # #     "Exports_GDP":  "NE.EXP.GNFS.ZS",
# # # #     "Imports_GDP":  "NE.IMP.GNFS.ZS",
# # # # }

# # # # # ── Fallback built-in data ────────────────────────────────────────────────────
# # # # FALLBACK = {
# # # #     "Year":        list(range(2000, 2024)),
# # # #     "GDP_B":       [12.7,13.3,13.4,14.0,15.1,18.7,22.5,27.2,30.6,29.5,
# # # #                     32.2,34.0,41.1,47.6,60.9,63.4,70.5,79.3,87.8,95.5,
# # # #                     98.8,99.2,110.4,107.9],
# # # #     "GDP_Growth":  [0.6,4.5,0.3,2.9,4.6,5.9,6.5,6.9,1.5,2.7,
# # # #                     8.4,6.1,4.6,5.9,5.4,5.7,5.9,4.9,6.3,5.4,
# # # #                     -0.3,7.6,4.8,5.6],
# # # #     "Inflation":   [10.0,5.8,2.0,9.8,11.6,10.3,6.0,4.3,26.2,10.5,
# # # #                     4.0,14.0,9.4,5.7,6.9,6.6,6.3,8.0,4.7,5.2,
# # # #                     5.3,6.1,9.1,6.3],
# # # #     "Unemployment":[9.8,9.8,9.8,9.8,9.8,9.3,8.7,8.1,7.4,6.7,
# # # #                     6.1,5.5,4.9,4.4,3.9,3.5,2.8,3.5,4.3,5.0,
# # # #                     5.6,5.7,5.7,5.6],
# # # #     "Exports_GDP": [25.2,24.8,23.6,23.0,24.0,23.8,23.0,24.5,24.1,20.4,
# # # #                     21.2,21.0,19.5,18.3,16.9,15.7,14.6,13.8,13.9,13.5,
# # # #                     12.4,13.5,14.2,13.8],
# # # #     "Imports_GDP": [33.1,32.5,31.6,30.5,32.0,31.8,33.0,37.2,42.4,36.3,
# # # #                     36.1,40.0,38.5,37.3,34.5,32.5,30.6,29.8,31.9,29.5,
# # # #                     26.7,28.0,32.6,31.2],
# # # # }

# # # # # ── Live World Bank data loader ───────────────────────────────────────────────
# # # # @st.cache_data(ttl=3600, show_spinner=False)
# # # # def fetch_wb_data():
# # # #     """Try live World Bank API; fall back to built-in data if unavailable."""
# # # #     try:
# # # #         import wbgapi as wb
# # # #         frames = []
# # # #         for col, code in WB_INDICATORS.items():
# # # #             series = wb.data.DataFrame(code, "KEN", mrv=30, numericTimeKeys=True)
# # # #             series = series.T.reset_index()
# # # #             series.columns = ["Year", col]
# # # #             series["Year"] = series["Year"].astype(int)
# # # #             frames.append(series.set_index("Year"))
# # # #         df = pd.concat(frames, axis=1).reset_index()
# # # #         df = df[df["Year"] >= 2000].dropna(subset=["GDP_Growth"]).sort_values("Year")
# # # #         df["GDP_B"] = df["GDP_B"] / 1e9
# # # #         return _enrich(df), "live"
# # # #     except Exception:
# # # #         return _enrich(pd.DataFrame(FALLBACK)), "cached"

# # # # def _enrich(df):
# # # #     df["Trade_Balance"] = df["Exports_GDP"] - df["Imports_GDP"]
# # # #     df["Era"] = df["Year"].apply(
# # # #         lambda y: "🔴 COVID" if 2020 <= y <= 2021
# # # #         else ("🟡 Post-COVID" if y >= 2022
# # # #         else ("🟢 Growth" if y >= 2010 else "🔵 Early 2000s"))
# # # #     )
# # # #     return df.reset_index(drop=True)

# # # # # ── Load data ─────────────────────────────────────────────────────────────────
# # # # with st.spinner("Fetching latest World Bank data…"):
# # # #     df, data_source = fetch_wb_data()

# # # # last_year = int(df["Year"].max())

# # # # # ── Sidebar ───────────────────────────────────────────────────────────────────
# # # # with st.sidebar:
# # # #     st.markdown("### 🇰🇪 Kenya Dashboard")
# # # #     if data_source == "live":
# # # #         st.markdown("<span class='data-badge badge-live'>🟢 LIVE — World Bank API</span>",
# # # #                     unsafe_allow_html=True)
# # # #     else:
# # # #         st.markdown("<span class='data-badge badge-cache'>🟡 OFFLINE — Built-in data</span>",
# # # #                     unsafe_allow_html=True)
# # # #     if st.button("🔄 Refresh Data"):
# # # #         st.cache_data.clear()
# # # #         st.rerun()

# # # #     st.markdown("---")
# # # #     st.markdown("**TIME RANGE**")
# # # #     year_range = st.slider("Select years", min_value=2000, max_value=last_year,
# # # #                            value=(2005, last_year), label_visibility="collapsed")

# # # #     st.markdown("---")
# # # #     st.markdown("**INDICATORS**")
# # # #     show_gdp     = st.checkbox("GDP & Growth",        value=True)
# # # #     show_inf     = st.checkbox("Inflation",            value=True)
# # # #     show_unemp   = st.checkbox("Unemployment",         value=True)
# # # #     show_trade   = st.checkbox("Trade Balance",        value=True)
# # # #     show_scatter = st.checkbox("Correlation Analysis", value=True)
# # # #     show_stats   = st.checkbox("Statistical Summary",  value=True)

# # # #     st.markdown("---")
# # # #     st.markdown("**FORECASTING**")
# # # #     show_forecast  = st.checkbox("5-Year Forecast", value=True)
# # # #     forecast_years = st.slider("Forecast horizon (years)", 1, 10, 5,
# # # #                                disabled=not show_forecast)
# # # #     forecast_model = st.radio("Model",
# # # #                               ["Linear", "Polynomial (deg 2)", "Polynomial (deg 3)"],
# # # #                               disabled=not show_forecast)

# # # #     st.markdown("---")
# # # #     st.markdown("**DISPLAY**")
# # # #     highlight_covid = st.toggle("Highlight COVID period", value=True)

# # # #     st.markdown("---")
# # # #     st.markdown(
# # # #         f"<small style='color:#3a4f3d'>Source: World Bank Open Data<br>"
# # # #         f"Last updated: {datetime.now().strftime('%d %b %Y')}</small>",
# # # #         unsafe_allow_html=True,
# # # #     )

# # # # # ── Filtered data ─────────────────────────────────────────────────────────────
# # # # dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

# # # # # ── Header ────────────────────────────────────────────────────────────────────
# # # # st.markdown("<p class='section-label'>REPUBLIC OF KENYA · KE · WORLD BANK OPEN DATA</p>",
# # # #             unsafe_allow_html=True)
# # # # st.title("Economic Indicators Analysis")
# # # # st.markdown(f"**GDP · Inflation · Unemployment · Trade Balance** &nbsp;·&nbsp; "
# # # #             f"{year_range[0]}–{year_range[1]}")
# # # # st.markdown("---")

# # # # # ── KPI Cards ─────────────────────────────────────────────────────────────────
# # # # latest = dff.iloc[-1]
# # # # prev   = dff.iloc[-2]
# # # # k1, k2, k3, k4 = st.columns(4)
# # # # k1.metric("GDP (Latest)",          f"${latest['GDP_B']:.1f}B",
# # # #           f"{latest['GDP_Growth']:+.1f}% growth")
# # # # k2.metric("Inflation",             f"{latest['Inflation']:.1f}%",
# # # #           f"{latest['Inflation']-prev['Inflation']:+.1f}pp vs prior year")
# # # # k3.metric("Unemployment",          f"{latest['Unemployment']:.1f}%",
# # # #           f"{latest['Unemployment']-prev['Unemployment']:+.1f}pp vs prior year")
# # # # k4.metric("Trade Balance (% GDP)", f"{latest['Trade_Balance']:.1f}%",
# # # #           f"{latest['Trade_Balance']-prev['Trade_Balance']:+.1f}pp vs prior year")

# # # # st.markdown("---")

# # # # # ── Tabs ──────────────────────────────────────────────────────────────────────
# # # # tabs = st.tabs([
# # # #     "📈 GDP", "🔥 Inflation", "👷 Unemployment",
# # # #     "🌍 Trade", "🔗 Correlations", "🔮 Forecast", "📊 Statistics",
# # # # ])

# # # # # ── COVID band helper ─────────────────────────────────────────────────────────
# # # # def add_covid_band(fig):
# # # #     if highlight_covid:
# # # #         fig.add_vrect(
# # # #             x0=2019.5, x1=2021.5,
# # # #             fillcolor="rgba(232,93,74,0.08)",
# # # #             line=dict(color="rgba(232,93,74,0.3)", width=1, dash="dot"),
# # # #             annotation_text="COVID", annotation_position="top left",
# # # #             annotation_font=dict(color=COLORS["red"], size=10),
# # # #         )
# # # #     return fig

# # # # # ── Forecast engine ───────────────────────────────────────────────────────────
# # # # def run_forecast(series_years, series_values, horizon, model_name):
# # # #     X = np.array(series_years).reshape(-1, 1)
# # # #     y = np.array(series_values)
# # # #     if model_name == "Linear":
# # # #         model = LinearRegression()
# # # #     elif model_name == "Polynomial (deg 2)":
# # # #         model = make_pipeline(PolynomialFeatures(2), LinearRegression())
# # # #     else:
# # # #         model = make_pipeline(PolynomialFeatures(3), LinearRegression())
# # # #     model.fit(X, y)
# # # #     future   = np.arange(series_years[-1] + 1, series_years[-1] + horizon + 1)
# # # #     pred     = model.predict(future.reshape(-1, 1))
# # # #     residuals = y - model.predict(X)
# # # #     ci        = 1.96 * np.std(residuals) * np.sqrt(1 + 1 / len(y))
# # # #     return future.tolist(), pred.tolist(), (pred - ci).tolist(), (pred + ci).tolist()

# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # # TAB 1 — GDP
# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # with tabs[0]:
# # # #     if show_gdp:
# # # #         st.subheader("GDP Growth Over Time")
# # # #         fig = make_subplots(specs=[[{"secondary_y": True}]])
# # # #         fig.add_trace(go.Bar(
# # # #             x=dff["Year"], y=dff["GDP_B"], name="GDP (USD B)",
# # # #             marker=dict(color=COLORS["green"], opacity=0.22,
# # # #                         line=dict(color=COLORS["green"], width=1)),
# # # #         ), secondary_y=False)
# # # #         fig.add_trace(go.Scatter(
# # # #             x=dff["Year"], y=dff["GDP_Growth"], name="GDP Growth %",
# # # #             line=dict(color=COLORS["green"], width=2.5),
# # # #             mode="lines+markers", marker=dict(size=5),
# # # #         ), secondary_y=True)
# # # #         fig.update_layout(**layout(height=380), title="")
# # # #         fig.update_yaxes(title_text="GDP (USD B)", secondary_y=False,
# # # #                          tickprefix="$", ticksuffix="B",
# # # #                          gridcolor=COLORS["border"], linecolor=COLORS["border"])
# # # #         fig.update_yaxes(title_text="Growth %", secondary_y=True,
# # # #                          ticksuffix="%", gridcolor="rgba(0,0,0,0)")
# # # #         fig.update_xaxes(gridcolor=COLORS["border"])
# # # #         add_covid_band(fig)
# # # #         st.plotly_chart(fig, use_container_width=True)

# # # #         col1, col2 = st.columns(2)
# # # #         with col1:
# # # #             st.markdown("**Year-on-Year GDP Change**")
# # # #             dc = dff.copy(); dc["GDP_Change"] = dc["GDP_B"].diff()
# # # #             fig2 = go.Figure(go.Bar(
# # # #                 x=dc["Year"][1:], y=dc["GDP_Change"][1:],
# # # #                 marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# # # #                               for v in dc["GDP_Change"][1:]],
# # # #                 text=[f"${v:+.1f}B" for v in dc["GDP_Change"][1:]],
# # # #                 textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# # # #             ))
# # # #             fig2.update_layout(**layout(height=280,
# # # #                                yaxis_extra=dict(tickprefix="$", ticksuffix="B")))
# # # #             add_covid_band(fig2)
# # # #             st.plotly_chart(fig2, use_container_width=True)
# # # #         with col2:
# # # #             st.markdown("**Avg GDP Growth by Era**")
# # # #             era_avg = df.groupby("Era")["GDP_Growth"].mean().reset_index()
# # # #             fig3 = go.Figure(go.Bar(
# # # #                 x=era_avg["Era"], y=era_avg["GDP_Growth"],
# # # #                 marker_color=[COLORS["blue"],COLORS["red"],COLORS["green"],COLORS["yellow"]],
# # # #                 text=[f"{v:.1f}%" for v in era_avg["GDP_Growth"]],
# # # #                 textposition="outside", textfont=dict(size=10, color=COLORS["text"]),
# # # #             ))
# # # #             fig3.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
# # # #             st.plotly_chart(fig3, use_container_width=True)

# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # # TAB 2 — Inflation
# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # with tabs[1]:
# # # #     if show_inf:
# # # #         st.subheader("Inflation (CPI) Trend")
# # # #         fig = go.Figure()
# # # #         fig.add_trace(go.Scatter(
# # # #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# # # #             y=[7.5]*len(dff) + [2.5]*len(dff),
# # # #             fill="toself", fillcolor="rgba(61,220,110,0.06)",
# # # #             line=dict(color="rgba(0,0,0,0)"), name="CBK Target Band (2.5–7.5%)",
# # # #         ))
# # # #         fig.add_hline(y=7.5, line=dict(color=COLORS["red"], dash="dot", width=1),
# # # #                       annotation_text="Upper 7.5%",
# # # #                       annotation_font=dict(color=COLORS["red"], size=10))
# # # #         fig.add_hline(y=2.5, line=dict(color=COLORS["green"], dash="dot", width=1),
# # # #                       annotation_text="Lower 2.5%",
# # # #                       annotation_font=dict(color=COLORS["green"], size=10))
# # # #         fig.add_trace(go.Scatter(
# # # #             x=dff["Year"], y=dff["Inflation"], name="CPI Inflation",
# # # #             line=dict(color=COLORS["yellow"], width=2.5), mode="lines+markers",
# # # #             marker=dict(size=5, color=[
# # # #                 COLORS["red"] if v > 7.5 else
# # # #                 (COLORS["green"] if v < 2.5 else COLORS["yellow"])
# # # #                 for v in dff["Inflation"]
# # # #             ]),
# # # #             fill="tozeroy", fillcolor="rgba(245,200,66,0.07)",
# # # #         ))
# # # #         fig.update_layout(**layout(height=380,
# # # #                           yaxis_extra=dict(ticksuffix="%", title="CPI %")))
# # # #         add_covid_band(fig)
# # # #         st.plotly_chart(fig, use_container_width=True)

# # # #         col1, col2 = st.columns(2)
# # # #         with col1:
# # # #             above  = (dff["Inflation"] > 7.5).sum()
# # # #             within = ((dff["Inflation"] >= 2.5) & (dff["Inflation"] <= 7.5)).sum()
# # # #             below  = (dff["Inflation"] < 2.5).sum()
# # # #             fig2 = go.Figure(go.Pie(
# # # #                 labels=["Above target","Within target","Below target"],
# # # #                 values=[above, within, below], hole=0.55,
# # # #                 marker=dict(colors=[COLORS["red"],COLORS["green"],COLORS["blue"]]),
# # # #                 textfont=dict(color=COLORS["text"]),
# # # #             ))
# # # #             fig2.update_layout(**layout(height=280),
# # # #                                title=dict(text="Years Within CBK Target",
# # # #                                           font=dict(color=COLORS["text"])))
# # # #             st.plotly_chart(fig2, use_container_width=True)
# # # #         with col2:
# # # #             st.markdown("**Inflation Distribution**")
# # # #             fig3 = go.Figure(go.Histogram(
# # # #                 x=dff["Inflation"], nbinsx=10,
# # # #                 marker=dict(color=COLORS["yellow"], opacity=0.7,
# # # #                             line=dict(color=COLORS["bg"], width=1)),
# # # #             ))
# # # #             fig3.add_vline(x=dff["Inflation"].mean(),
# # # #                            line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # # #                            annotation_text=f"Mean: {dff['Inflation'].mean():.1f}%",
# # # #                            annotation_font=dict(color=COLORS["text"], size=10))
# # # #             fig3.update_layout(**layout(height=280,
# # # #                                xaxis_extra=dict(title="Inflation %"),
# # # #                                yaxis_extra=dict(title="Count")))
# # # #             st.plotly_chart(fig3, use_container_width=True)

# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # # TAB 3 — Unemployment
# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # with tabs[2]:
# # # #     if show_unemp:
# # # #         st.subheader("Unemployment Rate Trajectory")
# # # #         fig = go.Figure()
# # # #         fig.add_trace(go.Scatter(
# # # #             x=dff["Year"], y=dff["Unemployment"], name="Unemployment %",
# # # #             line=dict(color=COLORS["red"], width=2.5), mode="lines+markers",
# # # #             marker=dict(size=6), fill="tozeroy",
# # # #             fillcolor="rgba(232,93,74,0.1)",
# # # #         ))
# # # #         dc2 = dff.copy()
# # # #         dc2["MA3"] = dc2["Unemployment"].rolling(3, center=True).mean()
# # # #         fig.add_trace(go.Scatter(
# # # #             x=dc2["Year"], y=dc2["MA3"], name="3-Year Rolling Avg",
# # # #             line=dict(color=COLORS["text"], width=1.5, dash="dot"), mode="lines",
# # # #         ))
# # # #         fig.update_layout(**layout(height=360,
# # # #                           yaxis_extra=dict(ticksuffix="%", title="Unemployment %")))
# # # #         add_covid_band(fig)
# # # #         st.plotly_chart(fig, use_container_width=True)

# # # #         c1, c2, c3 = st.columns(3)
# # # #         c1.metric("Peak",    f"{dff['Unemployment'].max():.1f}%",
# # # #                   f"in {int(dff.loc[dff['Unemployment'].idxmax(),'Year'])}")
# # # #         c2.metric("Lowest",  f"{dff['Unemployment'].min():.1f}%",
# # # #                   f"in {int(dff.loc[dff['Unemployment'].idxmin(),'Year'])}")
# # # #         c3.metric("Average", f"{dff['Unemployment'].mean():.1f}%", "ILO modeled")

# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # # TAB 4 — Trade
# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # with tabs[3]:
# # # #     if show_trade:
# # # #         st.subheader("Trade Balance: Exports vs Imports")
# # # #         fig = go.Figure()
# # # #         fig.add_trace(go.Scatter(
# # # #             x=dff["Year"], y=dff["Exports_GDP"], name="Exports % GDP",
# # # #             line=dict(color=COLORS["blue"], width=2.5),
# # # #             mode="lines+markers", marker=dict(size=4),
# # # #         ))
# # # #         fig.add_trace(go.Scatter(
# # # #             x=dff["Year"], y=dff["Imports_GDP"], name="Imports % GDP",
# # # #             line=dict(color=COLORS["yellow"], width=2.5),
# # # #             mode="lines+markers", marker=dict(size=4),
# # # #         ))
# # # #         fig.add_trace(go.Scatter(
# # # #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# # # #             y=list(dff["Imports_GDP"]) + list(dff["Exports_GDP"])[::-1],
# # # #             fill="toself", fillcolor="rgba(232,93,74,0.08)",
# # # #             line=dict(color="rgba(0,0,0,0)"), name="Trade Deficit",
# # # #         ))
# # # #         fig.update_layout(**layout(height=360,
# # # #                           yaxis_extra=dict(ticksuffix="%", title="% of GDP")))
# # # #         add_covid_band(fig)
# # # #         st.plotly_chart(fig, use_container_width=True)

# # # #         st.markdown("**Net Trade Balance (% GDP)**")
# # # #         fig2 = go.Figure(go.Bar(
# # # #             x=dff["Year"], y=dff["Trade_Balance"],
# # # #             marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# # # #                           for v in dff["Trade_Balance"]],
# # # #             text=[f"{v:.1f}%" for v in dff["Trade_Balance"]],
# # # #             textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# # # #         ))
# # # #         fig2.add_hline(y=0, line=dict(color=COLORS["muted"], width=1))
# # # #         fig2.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
# # # #         add_covid_band(fig2)
# # # #         st.plotly_chart(fig2, use_container_width=True)

# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # # TAB 5 — Correlations
# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # with tabs[4]:
# # # #     if show_scatter:
# # # #         st.subheader("Correlation Analysis")
# # # #         col1, col2 = st.columns(2)

# # # #         with col1:
# # # #             st.markdown("**GDP Growth vs Unemployment**")
# # # #             sl, ic, r, p, _ = stats.linregress(dff["GDP_Growth"], dff["Unemployment"])
# # # #             tx = np.linspace(dff["GDP_Growth"].min(), dff["GDP_Growth"].max(), 100)
# # # #             fig = go.Figure()
# # # #             fig.add_trace(go.Scatter(
# # # #                 x=dff["GDP_Growth"], y=dff["Unemployment"],
# # # #                 mode="markers+text", text=dff["Year"],
# # # #                 textposition="top center",
# # # #                 textfont=dict(size=9, color=COLORS["muted"]),
# # # #                 marker=dict(size=10, color=dff["Year"],
# # # #                             colorscale=[[0,COLORS["blue"]],[0.86,COLORS["red"]],[1,COLORS["green"]]],
# # # #                             showscale=True,
# # # #                             colorbar=dict(title="Year", tickfont=dict(color=COLORS["muted"]))),
# # # #                 name="Observations",
# # # #             ))
# # # #             fig.add_trace(go.Scatter(
# # # #                 x=tx, y=sl*tx+ic, mode="lines",
# # # #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # # #                 name=f"Trend (R²={r**2:.2f})",
# # # #             ))
# # # #             fig.update_layout(**layout(height=360,
# # # #                               xaxis_extra=dict(title="GDP Growth %", ticksuffix="%"),
# # # #                               yaxis_extra=dict(title="Unemployment %", ticksuffix="%")))
# # # #             st.plotly_chart(fig, use_container_width=True)
# # # #             st.caption(f"Pearson r = {r:.3f} | R² = {r**2:.3f} | p = {p:.4f}")

# # # #         with col2:
# # # #             st.markdown("**Inflation vs GDP Growth**")
# # # #             sl2, ic2, r2, p2, _ = stats.linregress(dff["Inflation"], dff["GDP_Growth"])
# # # #             tx2 = np.linspace(dff["Inflation"].min(), dff["Inflation"].max(), 100)
# # # #             fig2 = go.Figure()
# # # #             fig2.add_trace(go.Scatter(
# # # #                 x=dff["Inflation"], y=dff["GDP_Growth"],
# # # #                 mode="markers+text", text=dff["Year"],
# # # #                 textposition="top center",
# # # #                 textfont=dict(size=9, color=COLORS["muted"]),
# # # #                 marker=dict(size=10, color=COLORS["yellow"], opacity=0.8),
# # # #                 name="Observations",
# # # #             ))
# # # #             fig2.add_trace(go.Scatter(
# # # #                 x=tx2, y=sl2*tx2+ic2, mode="lines",
# # # #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # # #                 name=f"Trend (R²={r2**2:.2f})",
# # # #             ))
# # # #             fig2.update_layout(**layout(height=360,
# # # #                                xaxis_extra=dict(title="Inflation %", ticksuffix="%"),
# # # #                                yaxis_extra=dict(title="GDP Growth %", ticksuffix="%")))
# # # #             st.plotly_chart(fig2, use_container_width=True)
# # # #             st.caption(f"Pearson r = {r2:.3f} | R² = {r2**2:.3f} | p = {p2:.4f}")

# # # #         st.markdown("**Full Correlation Matrix**")
# # # #         corr_cols   = ["GDP_B","GDP_Growth","Inflation","Unemployment",
# # # #                        "Exports_GDP","Imports_GDP","Trade_Balance"]
# # # #         corr_labels = ["GDP (B)","GDP Growth","Inflation","Unemployment",
# # # #                        "Exports","Imports","Trade Bal."]
# # # #         corr = dff[corr_cols].corr().values
# # # #         fig3 = go.Figure(go.Heatmap(
# # # #             z=corr, x=corr_labels, y=corr_labels,
# # # #             colorscale=[[0,COLORS["red"]],[0.5,COLORS["surface"]],[1,COLORS["green"]]],
# # # #             zmid=0, zmin=-1, zmax=1,
# # # #             text=[[f"{v:.2f}" for v in row] for row in corr],
# # # #             texttemplate="%{text}", textfont=dict(size=11, color=COLORS["text"]),
# # # #         ))
# # # #         fig3.update_layout(**layout(height=380))
# # # #         st.plotly_chart(fig3, use_container_width=True)

# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # # TAB 6 — FORECAST  ✨ NEW
# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # with tabs[5]:
# # # #     if show_forecast:
# # # #         st.subheader(f"Economic Forecast · {last_year+1}–{last_year+forecast_years}")
# # # #         st.caption(f"Model: **{forecast_model}** regression trained on "
# # # #                    f"{year_range[0]}–{last_year} | Shaded area = 95% confidence interval")

# # # #         train = df[(df["Year"] >= year_range[0]) & (df["Year"] <= last_year)].dropna()

# # # #         indicators = [
# # # #             ("GDP_Growth",   "GDP Growth %",     COLORS["green"],  "%",  ""),
# # # #             ("GDP_B",        "GDP (USD Billion)", COLORS["green"],  "B",  "$"),
# # # #             ("Inflation",    "Inflation %",       COLORS["yellow"], "%",  ""),
# # # #             ("Unemployment", "Unemployment %",    COLORS["red"],    "%",  ""),
# # # #         ]

# # # #         col1, col2 = st.columns(2)
# # # #         forecast_results = {}

# # # #         for i, (col, label, color, unit, prefix) in enumerate(indicators):
# # # #             fut_yrs, pred, lo, hi = run_forecast(
# # # #                 train["Year"].tolist(),
# # # #                 train[col].tolist(),
# # # #                 forecast_years,
# # # #                 forecast_model,
# # # #             )
# # # #             forecast_results[col] = {"years": fut_yrs, "pred": pred, "lo": lo, "hi": hi}

# # # #             # Parse hex color → rgba for CI band
# # # #             r_hex = int(color[1:3], 16)
# # # #             g_hex = int(color[3:5], 16)
# # # #             b_hex = int(color[5:7], 16)

# # # #             fig = go.Figure()
# # # #             # Historical
# # # #             fig.add_trace(go.Scatter(
# # # #                 x=train["Year"], y=train[col], name="Historical",
# # # #                 line=dict(color=color, width=2.5), mode="lines+markers",
# # # #                 marker=dict(size=4),
# # # #             ))
# # # #             # CI band
# # # #             fig.add_trace(go.Scatter(
# # # #                 x=fut_yrs + fut_yrs[::-1],
# # # #                 y=hi + lo[::-1],
# # # #                 fill="toself",
# # # #                 fillcolor=f"rgba({r_hex},{g_hex},{b_hex},0.12)",
# # # #                 line=dict(color="rgba(0,0,0,0)"),
# # # #                 name="95% CI", showlegend=True,
# # # #             ))
# # # #             # Forecast line
# # # #             fig.add_trace(go.Scatter(
# # # #                 x=fut_yrs, y=pred, name="Forecast",
# # # #                 line=dict(color=color, width=2, dash="dash"),
# # # #                 mode="lines+markers",
# # # #                 marker=dict(size=6, symbol="diamond"),
# # # #             ))
# # # #             # Divider
# # # #             fig.add_vline(x=last_year + 0.5,
# # # #                           line=dict(color=COLORS["muted"], dash="dot", width=1),
# # # #                           annotation_text="Forecast →",
# # # #                           annotation_font=dict(color=COLORS["muted"], size=9))
# # # #             add_covid_band(fig)

# # # #             tick_suffix = unit if unit != "B" else ""
# # # #             fig.update_layout(**layout(
# # # #                 height=300,
# # # #                 yaxis_extra=dict(title=label,
# # # #                                  ticksuffix=tick_suffix,
# # # #                                  tickprefix=prefix),
# # # #             ))

# # # #             target_col = col1 if i % 2 == 0 else col2
# # # #             with target_col:
# # # #                 st.plotly_chart(fig, use_container_width=True)

# # # #         # ── Summary table ──────────────────────────────────────────────────
# # # #         st.markdown("---")
# # # #         st.markdown("**📋 Forecast Summary**")
# # # #         rows = []
# # # #         for idx, yr in enumerate(forecast_results["GDP_Growth"]["years"]):
# # # #             rows.append({
# # # #                 "Year":           yr,
# # # #                 "GDP Growth %":   f"{forecast_results['GDP_Growth']['pred'][idx]:.1f}%",
# # # #                 "GDP (USD B)":    f"${forecast_results['GDP_B']['pred'][idx]:.1f}B",
# # # #                 "Inflation %":    f"{forecast_results['Inflation']['pred'][idx]:.1f}%",
# # # #                 "Unemployment %": f"{forecast_results['Unemployment']['pred'][idx]:.1f}%",
# # # #             })
# # # #         st.dataframe(pd.DataFrame(rows).set_index("Year"), use_container_width=True)

# # # #         # ── Notes ──────────────────────────────────────────────────────────
# # # #         st.markdown("---")
# # # #         n1, n2, n3 = st.columns(3)
# # # #         with n1:
# # # #             st.markdown("""<div class='forecast-box'><h4>📐 Model Info</h4>
# # # #             <p>Forecasts use scikit-learn regression fitted on the selected historical range.
# # # #             Shaded bands show 95% confidence intervals based on residual standard error.</p>
# # # #             </div>""", unsafe_allow_html=True)
# # # #         with n2:
# # # #             st.markdown("""<div class='forecast-box'><h4>⚠️ Limitations</h4>
# # # #             <p>Models assume past trends continue. They do not account for policy shocks,
# # # #             global crises, commodity price swings, or structural breaks in the economy.</p>
# # # #             </div>""", unsafe_allow_html=True)
# # # #         with n3:
# # # #             st.markdown("""<div class='forecast-box'><h4>🔍 Best Use</h4>
# # # #             <p>Use Linear for stable long-run trends. Polynomial deg 2–3 captures curvature
# # # #             but may overfit on short windows. Compare models using the sidebar selector.</p>
# # # #             </div>""", unsafe_allow_html=True)
# # # #     else:
# # # #         st.info("Enable **5-Year Forecast** in the sidebar to view projections.")

# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # # TAB 7 — Statistics
# # # # # ═════════════════════════════════════════════════════════════════════════════
# # # # with tabs[6]:
# # # #     if show_stats:
# # # #         st.subheader("Statistical Summary")
# # # #         summary_cols = ["GDP_Growth","Inflation","Unemployment",
# # # #                         "Exports_GDP","Imports_GDP","Trade_Balance"]
# # # #         label_map    = {
# # # #             "GDP_Growth":"GDP Growth %", "Inflation":"Inflation %",
# # # #             "Unemployment":"Unemployment %", "Exports_GDP":"Exports % GDP",
# # # #             "Imports_GDP":"Imports % GDP", "Trade_Balance":"Trade Balance % GDP",
# # # #         }
# # # #         stats_df = dff[summary_cols].describe().T.round(2)
# # # #         stats_df.index = [label_map[i] for i in stats_df.index]
# # # #         stats_df.columns = ["Count","Mean","Std Dev","Min",
# # # #                             "25th %ile","Median","75th %ile","Max"]
# # # #         st.dataframe(
# # # #             stats_df.style.background_gradient(subset=["Mean"], cmap="RdYlGn", axis=0)
# # # #                           .format("{:.2f}"),
# # # #             use_container_width=True,
# # # #         )

# # # #         st.markdown("---")
# # # #         st.markdown("**Raw Data Table**")
# # # #         disp = dff[["Year","Era","GDP_B","GDP_Growth","Inflation",
# # # #                     "Unemployment","Exports_GDP","Imports_GDP","Trade_Balance"]].copy()
# # # #         disp.columns = ["Year","Era","GDP ($B)","GDP Growth %","Inflation %",
# # # #                         "Unemployment %","Exports % GDP","Imports % GDP","Trade Balance %"]
# # # #         st.dataframe(disp.set_index("Year"), use_container_width=True)
# # # #         csv = disp.to_csv(index=False).encode("utf-8")
# # # #         st.download_button("⬇️ Download CSV", data=csv,
# # # #                            file_name="kenya_economic_data.csv", mime="text/csv")

# # # # # ── Key Insights ──────────────────────────────────────────────────────────────
# # # # st.markdown("---")
# # # # st.subheader("Key Insights")
# # # # c1, c2, c3 = st.columns(3)
# # # # with c1:
# # # #     st.markdown("""<div class='insight-box'>
# # # #         <h4>📈 Sustained Long-Term Growth</h4>
# # # #         <p>Kenya's GDP grew from ~$12B in 2000 to $108B in 2023 — nearly 9× in nominal terms.
# # # #         Average real GDP growth held at 4.7% over the past decade, one of sub-Saharan Africa's
# # # #         strongest sustained performers.</p></div>""", unsafe_allow_html=True)
# # # # with c2:
# # # #     st.markdown("""<div class='insight-box warn'>
# # # #         <h4>🔥 Inflation Volatility</h4>
# # # #         <p>Inflation spiked above 26% in 2008 tied to the global food/energy crisis.
# # # #         The CBK's 5±2.5% target is regularly breached, averaging 7.7% over the study period.</p>
# # # #         </div>""", unsafe_allow_html=True)
# # # # with c3:
# # # #     st.markdown("""<div class='insight-box danger'>
# # # #         <h4>🌍 Structural Trade Deficit</h4>
# # # #         <p>Kenya consistently imports more than it exports, driven by fuel, machinery, and
# # # #         manufactured goods. The deficit averaged -8% to -9% of GDP throughout the period.</p>
# # # #         </div>""", unsafe_allow_html=True)

# # # # st.markdown(
# # # #     "<br><small style='color:#3a4f3d'>Data: World Bank Open Data · "
# # # #     "Kenya National Bureau of Statistics · IMF DataMapper</small>",
# # # #     unsafe_allow_html=True,
# # # # )

# # # """
# # # Africa Economic Indicators Dashboard
# # # Streamlit + Plotly | Phase 2 Upgrades:
# # #   - Live World Bank API (wbgapi) with offline fallback
# # #   - 5-Year Forecasting Panel
# # #   - Country Comparison — all 54 African countries, any selection
# # # Data source: World Bank Open Data
# # # """

# # # import streamlit as st
# # # import pandas as pd
# # # import plotly.graph_objects as go
# # # from plotly.subplots import make_subplots
# # # import numpy as np
# # # from scipy import stats
# # # from sklearn.linear_model import LinearRegression
# # # from sklearn.preprocessing import PolynomialFeatures
# # # from sklearn.pipeline import make_pipeline
# # # from datetime import datetime

# # # # ── Page config ───────────────────────────────────────────────────────────────
# # # st.set_page_config(
# # #     page_title="Africa Economic Dashboard",
# # #     page_icon="🌍",
# # #     layout="wide",
# # #     initial_sidebar_state="expanded",
# # # )

# # # # ── CSS ───────────────────────────────────────────────────────────────────────
# # # st.markdown("""
# # # <style>
# # #     .stApp { background-color: #0a0f0d; }
# # #     .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
# # #     [data-testid="stSidebar"] { background-color: #111812; border-right: 1px solid #1e2e21; }
# # #     [data-testid="stSidebar"] * { color: #e8f0ea !important; }
# # #     [data-testid="metric-container"] {
# # #         background: #111812; border: 1px solid #1e2e21;
# # #         border-radius: 6px; padding: 1rem 1.2rem;
# # #     }
# # #     [data-testid="stMetricLabel"] { color: #6b7f6e !important; font-size: 0.75rem; }
# # #     [data-testid="stMetricValue"] { color: #e8f0ea !important; }
# # #     [data-testid="stMetricDelta"] { font-size: 0.8rem; }
# # #     h1, h2, h3 { color: #e8f0ea !important; }
# # #     p, li { color: #b0bfb3 !important; }
# # #     .stTabs [data-baseweb="tab-list"] { background-color: #111812; border-bottom: 1px solid #1e2e21; }
# # #     .stTabs [data-baseweb="tab"] { color: #6b7f6e; }
# # #     .stTabs [aria-selected="true"] { color: #3ddc6e !important; border-bottom-color: #3ddc6e !important; }
# # #     hr { border-color: #1e2e21; }
# # #     .stAlert { background-color: #111812; border-color: #1e2e21; }
# # #     .section-label {
# # #         font-family: monospace; font-size: 0.65rem; letter-spacing: 0.2em;
# # #         color: #3ddc6e; text-transform: uppercase; margin-bottom: 0.25rem;
# # #     }
# # #     .data-badge {
# # #         display: inline-block; font-family: monospace; font-size: 0.62rem;
# # #         letter-spacing: 0.1em; padding: 0.25rem 0.65rem;
# # #         border-radius: 2px; margin-bottom: 1rem;
# # #     }
# # #     .badge-live  { background: rgba(61,220,110,0.15); color: #3ddc6e; border: 1px solid #3ddc6e; }
# # #     .badge-cache { background: rgba(245,200,66,0.15); color: #f5c842; border: 1px solid #f5c842; }
# # #     .insight-box {
# # #         background: #111812; border: 1px solid #1e2e21;
# # #         border-left: 3px solid #3ddc6e; border-radius: 4px;
# # #         padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# # #     }
# # #     .insight-box.warn   { border-left-color: #f5c842; }
# # #     .insight-box.danger { border-left-color: #e85d4a; }
# # #     .insight-box h4 { color: #e8f0ea !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# # #     .insight-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# # #     .forecast-box {
# # #         background: rgba(74,157,232,0.06); border: 1px solid rgba(74,157,232,0.25);
# # #         border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# # #     }
# # #     .forecast-box h4 { color: #4a9de8 !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# # #     .forecast-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# # #     .compare-box {
# # #         background: rgba(167,139,250,0.06); border: 1px solid rgba(167,139,250,0.25);
# # #         border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# # #     }
# # #     .compare-box h4 { color: #a78bfa !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# # #     .compare-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # ── Colors & layout ───────────────────────────────────────────────────────────
# # # COLORS = {
# # #     "bg": "#0a0f0d", "surface": "#111812", "border": "#1e2e21",
# # #     "green": "#3ddc6e", "yellow": "#f5c842", "red": "#e85d4a",
# # #     "blue": "#4a9de8", "purple": "#a78bfa", "muted": "#6b7f6e", "text": "#e8f0ea",
# # # }

# # # # Distinct palette for multi-country lines
# # # COUNTRY_PALETTE = [
# # #     "#3ddc6e", "#4a9de8", "#f5c842", "#e85d4a", "#a78bfa",
# # #     "#f97316", "#06b6d4", "#ec4899", "#84cc16", "#fb923c",
# # # ]

# # # GRID = dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], tickcolor=COLORS["border"])

# # # def layout(height=360, xaxis_extra=None, yaxis_extra=None, **kwargs):
# # #     return dict(
# # #         paper_bgcolor=COLORS["surface"], plot_bgcolor=COLORS["bg"],
# # #         font=dict(family="DM Mono, monospace", color=COLORS["muted"], size=11),
# # #         xaxis={**GRID, **(xaxis_extra or {})},
# # #         yaxis={**GRID, **(yaxis_extra or {})},
# # #         margin=dict(t=40, b=40, l=55, r=20),
# # #         legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
# # #         height=height, **kwargs,
# # #     )

# # # # ── All 54 African countries — ISO3 codes + display names + data quality ──────
# # # AFRICA_COUNTRIES = {
# # #     # Code : (Display Name, Data Quality)  🟢 full  🟡 partial  🔴 sparse
# # #     "DZA": ("🇩🇿 Algeria",              "🟢"),
# # #     "AGO": ("🇦🇴 Angola",               "🟡"),
# # #     "BEN": ("🇧🇯 Benin",                "🟡"),
# # #     "BWA": ("🇧🇼 Botswana",             "🟢"),
# # #     "BFA": ("🇧🇫 Burkina Faso",         "🟡"),
# # #     "BDI": ("🇧🇮 Burundi",              "🟡"),
# # #     "CPV": ("🇨🇻 Cabo Verde",           "🟡"),
# # #     "CMR": ("🇨🇲 Cameroon",             "🟢"),
# # #     "CAF": ("🇨🇫 Central African Rep.", "🔴"),
# # #     "TCD": ("🇹🇩 Chad",                 "🟡"),
# # #     "COM": ("🇰🇲 Comoros",              "🔴"),
# # #     "COD": ("🇨🇩 DR Congo",             "🟡"),
# # #     "COG": ("🇨🇬 Republic of Congo",    "🟡"),
# # #     "CIV": ("🇨🇮 Côte d'Ivoire",        "🟢"),
# # #     "DJI": ("🇩🇯 Djibouti",             "🟡"),
# # #     "EGY": ("🇪🇬 Egypt",                "🟢"),
# # #     "GNQ": ("🇬🇶 Equatorial Guinea",    "🟡"),
# # #     "ERI": ("🇪🇷 Eritrea",              "🔴"),
# # #     "SWZ": ("🇸🇿 Eswatini",             "🟡"),
# # #     "ETH": ("🇪🇹 Ethiopia",             "🟢"),
# # #     "GAB": ("🇬🇦 Gabon",                "🟡"),
# # #     "GMB": ("🇬🇲 Gambia",               "🟡"),
# # #     "GHA": ("🇬🇭 Ghana",                "🟢"),
# # #     "GIN": ("🇬🇳 Guinea",               "🟡"),
# # #     "GNB": ("🇬🇼 Guinea-Bissau",        "🔴"),
# # #     "KEN": ("🇰🇪 Kenya",                "🟢"),
# # #     "LSO": ("🇱🇸 Lesotho",              "🟡"),
# # #     "LBR": ("🇱🇷 Liberia",              "🟡"),
# # #     "LBY": ("🇱🇾 Libya",                "🔴"),
# # #     "MDG": ("🇲🇬 Madagascar",           "🟡"),
# # #     "MWI": ("🇲🇼 Malawi",               "🟡"),
# # #     "MLI": ("🇲🇱 Mali",                 "🟡"),
# # #     "MRT": ("🇲🇷 Mauritania",           "🟡"),
# # #     "MUS": ("🇲🇺 Mauritius",            "🟢"),
# # #     "MAR": ("🇲🇦 Morocco",              "🟢"),
# # #     "MOZ": ("🇲🇿 Mozambique",           "🟡"),
# # #     "NAM": ("🇳🇦 Namibia",              "🟢"),
# # #     "NER": ("🇳🇪 Niger",                "🟡"),
# # #     "NGA": ("🇳🇬 Nigeria",              "🟢"),
# # #     "RWA": ("🇷🇼 Rwanda",               "🟢"),
# # #     "STP": ("🇸🇹 São Tomé & Príncipe",  "🔴"),
# # #     "SEN": ("🇸🇳 Senegal",              "🟢"),
# # #     "SLE": ("🇸🇱 Sierra Leone",         "🟡"),
# # #     "SOM": ("🇸🇴 Somalia",              "🔴"),
# # #     "ZAF": ("🇿🇦 South Africa",         "🟢"),
# # #     "SSD": ("🇸🇸 South Sudan",          "🔴"),
# # #     "SDN": ("🇸🇩 Sudan",                "🔴"),
# # #     "TZA": ("🇹🇿 Tanzania",             "🟢"),
# # #     "TGO": ("🇹🇬 Togo",                 "🟡"),
# # #     "TUN": ("🇹🇳 Tunisia",              "🟢"),
# # #     "UGA": ("🇺🇬 Uganda",               "🟢"),
# # #     "ZMB": ("🇿🇲 Zambia",               "🟢"),
# # #     "ZWE": ("🇿🇼 Zimbabwe",             "🟡"),
# # #     "SYC": ("🇸🇨 Seychelles",           "🟡"),
# # # }

# # # # Sorted dropdown options: "🟢 Kenya (KEN)" style
# # # COUNTRY_OPTIONS = {
# # #     code: f"{quality} {name}"
# # #     for code, (name, quality) in sorted(AFRICA_COUNTRIES.items(), key=lambda x: x[1][0])
# # # }

# # # # ── World Bank indicators ─────────────────────────────────────────────────────
# # # WB_INDICATORS = {
# # #     "GDP_B":        "NY.GDP.MKTP.CD",
# # #     "GDP_Growth":   "NY.GDP.MKTP.KD.ZG",
# # #     "Inflation":    "FP.CPI.TOTL.ZG",
# # #     "Unemployment": "SL.UEM.TOTL.ZS",
# # #     "Exports_GDP":  "NE.EXP.GNFS.ZS",
# # #     "Imports_GDP":  "NE.IMP.GNFS.ZS",
# # # }

# # # # ── Kenya fallback data ───────────────────────────────────────────────────────
# # # KENYA_FALLBACK = {
# # #     "Year":        list(range(2000, 2024)),
# # #     "GDP_B":       [12.7,13.3,13.4,14.0,15.1,18.7,22.5,27.2,30.6,29.5,
# # #                     32.2,34.0,41.1,47.6,60.9,63.4,70.5,79.3,87.8,95.5,
# # #                     98.8,99.2,110.4,107.9],
# # #     "GDP_Growth":  [0.6,4.5,0.3,2.9,4.6,5.9,6.5,6.9,1.5,2.7,
# # #                     8.4,6.1,4.6,5.9,5.4,5.7,5.9,4.9,6.3,5.4,
# # #                     -0.3,7.6,4.8,5.6],
# # #     "Inflation":   [10.0,5.8,2.0,9.8,11.6,10.3,6.0,4.3,26.2,10.5,
# # #                     4.0,14.0,9.4,5.7,6.9,6.6,6.3,8.0,4.7,5.2,
# # #                     5.3,6.1,9.1,6.3],
# # #     "Unemployment":[9.8,9.8,9.8,9.8,9.8,9.3,8.7,8.1,7.4,6.7,
# # #                     6.1,5.5,4.9,4.4,3.9,3.5,2.8,3.5,4.3,5.0,
# # #                     5.6,5.7,5.7,5.6],
# # #     "Exports_GDP": [25.2,24.8,23.6,23.0,24.0,23.8,23.0,24.5,24.1,20.4,
# # #                     21.2,21.0,19.5,18.3,16.9,15.7,14.6,13.8,13.9,13.5,
# # #                     12.4,13.5,14.2,13.8],
# # #     "Imports_GDP": [33.1,32.5,31.6,30.5,32.0,31.8,33.0,37.2,42.4,36.3,
# # #                     36.1,40.0,38.5,37.3,34.5,32.5,30.6,29.8,31.9,29.5,
# # #                     26.7,28.0,32.6,31.2],
# # # }

# # # # ── Data loaders ─────────────────────────────────────────────────────────────
# # # def _enrich(df):
# # #     df["Trade_Balance"] = df["Exports_GDP"] - df["Imports_GDP"]
# # #     df["Era"] = df["Year"].apply(
# # #         lambda y: "🔴 COVID" if 2020 <= y <= 2021
# # #         else ("🟡 Post-COVID" if y >= 2022
# # #         else ("🟢 Growth" if y >= 2010 else "🔵 Early 2000s"))
# # #     )
# # #     return df.reset_index(drop=True)

# # # @st.cache_data(ttl=3600, show_spinner=False)
# # # def fetch_single_country(iso3: str):
# # #     """Fetch one country from World Bank API; returns (df, source)."""
# # #     try:
# # #         import wbgapi as wb
# # #         frames = []
# # #         for col, code in WB_INDICATORS.items():
# # #             s = wb.data.DataFrame(code, iso3, mrv=30, numericTimeKeys=True)
# # #             s = s.T.reset_index()
# # #             s.columns = ["Year", col]
# # #             s["Year"] = s["Year"].astype(int)
# # #             frames.append(s.set_index("Year"))
# # #         df = pd.concat(frames, axis=1).reset_index()
# # #         df = df[df["Year"] >= 2000].sort_values("Year")
# # #         df["GDP_B"] = df["GDP_B"] / 1e9
# # #         return _enrich(df), "live"
# # #     except Exception:
# # #         if iso3 == "KEN":
# # #             return _enrich(pd.DataFrame(KENYA_FALLBACK)), "cached"
# # #         return None, "unavailable"

# # # @st.cache_data(ttl=3600, show_spinner=False)
# # # def fetch_primary_country(iso3: str):
# # #     df, source = fetch_single_country(iso3)
# # #     return df, source

# # # # ── Sidebar ───────────────────────────────────────────────────────────────────
# # # with st.sidebar:
# # #     st.markdown("### 🌍 Africa Dashboard")
# # #     st.markdown("---")

# # #     st.markdown("**PRIMARY COUNTRY**")
# # #     primary_code = st.selectbox(
# # #         "Primary country",
# # #         options=list(COUNTRY_OPTIONS.keys()),
# # #         format_func=lambda c: COUNTRY_OPTIONS[c],
# # #         index=list(COUNTRY_OPTIONS.keys()).index("KEN"),
# # #         label_visibility="collapsed",
# # #     )

# # #     st.markdown("---")
# # #     st.markdown("**TIME RANGE**")
# # #     year_range = st.slider("Years", min_value=2000, max_value=2023,
# # #                            value=(2005, 2023), label_visibility="collapsed")

# # #     st.markdown("---")
# # #     st.markdown("**INDICATORS**")
# # #     show_gdp     = st.checkbox("GDP & Growth",        value=True)
# # #     show_inf     = st.checkbox("Inflation",            value=True)
# # #     show_unemp   = st.checkbox("Unemployment",         value=True)
# # #     show_trade   = st.checkbox("Trade Balance",        value=True)
# # #     show_scatter = st.checkbox("Correlation Analysis", value=True)
# # #     show_stats   = st.checkbox("Statistical Summary",  value=True)

# # #     st.markdown("---")
# # #     st.markdown("**FORECASTING**")
# # #     show_forecast  = st.checkbox("5-Year Forecast", value=True)
# # #     forecast_years = st.slider("Horizon (years)", 1, 10, 5,
# # #                                disabled=not show_forecast)
# # #     forecast_model = st.radio("Model",
# # #                               ["Linear", "Polynomial (deg 2)", "Polynomial (deg 3)"],
# # #                               disabled=not show_forecast)

# # #     st.markdown("---")
# # #     st.markdown("**DISPLAY**")
# # #     highlight_covid = st.toggle("Highlight COVID period", value=True)

# # #     st.markdown("---")
# # #     st.markdown(
# # #         f"<small style='color:#3a4f3d'>Source: World Bank Open Data<br>"
# # #         f"54 African countries · {datetime.now().strftime('%d %b %Y')}</small>",
# # #         unsafe_allow_html=True,
# # #     )

# # # # ── Load primary country ──────────────────────────────────────────────────────
# # # with st.spinner(f"Loading data for {COUNTRY_OPTIONS[primary_code]}…"):
# # #     df, data_source = fetch_primary_country(primary_code)

# # # if df is None:
# # #     st.error(f"Could not load data for {COUNTRY_OPTIONS[primary_code]}. Try another country.")
# # #     st.stop()

# # # last_year    = int(df["Year"].max())
# # # country_name = AFRICA_COUNTRIES[primary_code][0]
# # # dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

# # # # ── Header ────────────────────────────────────────────────────────────────────
# # # st.markdown(
# # #     f"<p class='section-label'>AFRICA ECONOMIC DASHBOARD · WORLD BANK OPEN DATA · "
# # #     f"{'LIVE' if data_source == 'live' else 'OFFLINE'}</p>",
# # #     unsafe_allow_html=True,
# # # )
# # # col_h1, col_h2 = st.columns([3, 1])
# # # with col_h1:
# # #     st.title(f"{country_name} — Economic Analysis")
# # #     st.markdown(f"**GDP · Inflation · Unemployment · Trade** &nbsp;·&nbsp; {year_range[0]}–{year_range[1]}")
# # # with col_h2:
# # #     if data_source == "live":
# # #         st.markdown("<div style='padding-top:2rem'><span class='data-badge badge-live'>🟢 LIVE — World Bank</span></div>",
# # #                     unsafe_allow_html=True)
# # #     else:
# # #         st.markdown("<div style='padding-top:2rem'><span class='data-badge badge-cache'>🟡 OFFLINE — Built-in</span></div>",
# # #                     unsafe_allow_html=True)
# # #     if st.button("🔄 Refresh"):
# # #         st.cache_data.clear()
# # #         st.rerun()

# # # st.markdown("---")

# # # # ── KPI Cards ─────────────────────────────────────────────────────────────────
# # # latest = dff.iloc[-1]
# # # prev   = dff.iloc[-2]
# # # k1, k2, k3, k4 = st.columns(4)
# # # k1.metric("GDP (Latest)",          f"${latest['GDP_B']:.1f}B",
# # #           f"{latest['GDP_Growth']:+.1f}% growth")
# # # k2.metric("Inflation",             f"{latest['Inflation']:.1f}%",
# # #           f"{latest['Inflation']-prev['Inflation']:+.1f}pp vs prior year")
# # # k3.metric("Unemployment",          f"{latest['Unemployment']:.1f}%",
# # #           f"{latest['Unemployment']-prev['Unemployment']:+.1f}pp vs prior year")
# # # k4.metric("Trade Balance (% GDP)", f"{latest['Trade_Balance']:.1f}%",
# # #           f"{latest['Trade_Balance']-prev['Trade_Balance']:+.1f}pp vs prior year")

# # # st.markdown("---")

# # # # ── Tabs ──────────────────────────────────────────────────────────────────────
# # # tabs = st.tabs([
# # #     "📈 GDP", "🔥 Inflation", "👷 Unemployment",
# # #     "🌍 Trade", "🔗 Correlations", "🔮 Forecast",
# # #     "🗺️ Compare", "📊 Statistics",
# # # ])

# # # # ── Helpers ───────────────────────────────────────────────────────────────────
# # # def add_covid_band(fig):
# # #     if highlight_covid:
# # #         fig.add_vrect(
# # #             x0=2019.5, x1=2021.5,
# # #             fillcolor="rgba(232,93,74,0.08)",
# # #             line=dict(color="rgba(232,93,74,0.3)", width=1, dash="dot"),
# # #             annotation_text="COVID", annotation_position="top left",
# # #             annotation_font=dict(color=COLORS["red"], size=10),
# # #         )
# # #     return fig

# # # def run_forecast(years, values, horizon, model_name):
# # #     X = np.array(years).reshape(-1, 1)
# # #     y = np.array(values)
# # #     if model_name == "Linear":
# # #         model = LinearRegression()
# # #     elif model_name == "Polynomial (deg 2)":
# # #         model = make_pipeline(PolynomialFeatures(2), LinearRegression())
# # #     else:
# # #         model = make_pipeline(PolynomialFeatures(3), LinearRegression())
# # #     model.fit(X, y)
# # #     future = np.arange(years[-1] + 1, years[-1] + horizon + 1)
# # #     pred   = model.predict(future.reshape(-1, 1))
# # #     ci     = 1.96 * np.std(y - model.predict(X)) * np.sqrt(1 + 1 / len(y))
# # #     return future.tolist(), pred.tolist(), (pred - ci).tolist(), (pred + ci).tolist()

# # # # ═════════════════════════════════════════════════════════════════════════════
# # # # TAB 1 — GDP
# # # # ═════════════════════════════════════════════════════════════════════════════
# # # with tabs[0]:
# # #     if show_gdp:
# # #         st.subheader(f"GDP — {country_name}")
# # #         fig = make_subplots(specs=[[{"secondary_y": True}]])
# # #         fig.add_trace(go.Bar(
# # #             x=dff["Year"], y=dff["GDP_B"], name="GDP (USD B)",
# # #             marker=dict(color=COLORS["green"], opacity=0.22,
# # #                         line=dict(color=COLORS["green"], width=1)),
# # #         ), secondary_y=False)
# # #         fig.add_trace(go.Scatter(
# # #             x=dff["Year"], y=dff["GDP_Growth"], name="GDP Growth %",
# # #             line=dict(color=COLORS["green"], width=2.5),
# # #             mode="lines+markers", marker=dict(size=5),
# # #         ), secondary_y=True)
# # #         fig.update_layout(**layout(height=380), title="")
# # #         fig.update_yaxes(title_text="GDP (USD B)", secondary_y=False,
# # #                          tickprefix="$", ticksuffix="B",
# # #                          gridcolor=COLORS["border"], linecolor=COLORS["border"])
# # #         fig.update_yaxes(title_text="Growth %", secondary_y=True,
# # #                          ticksuffix="%", gridcolor="rgba(0,0,0,0)")
# # #         fig.update_xaxes(gridcolor=COLORS["border"])
# # #         add_covid_band(fig)
# # #         st.plotly_chart(fig, use_container_width=True)

# # #         c1, c2 = st.columns(2)
# # #         with c1:
# # #             dc = dff.copy(); dc["GDP_Change"] = dc["GDP_B"].diff()
# # #             fig2 = go.Figure(go.Bar(
# # #                 x=dc["Year"][1:], y=dc["GDP_Change"][1:],
# # #                 marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# # #                               for v in dc["GDP_Change"][1:]],
# # #                 text=[f"${v:+.1f}B" for v in dc["GDP_Change"][1:]],
# # #                 textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# # #             ))
# # #             fig2.update_layout(**layout(height=280,
# # #                                yaxis_extra=dict(tickprefix="$", ticksuffix="B")))
# # #             add_covid_band(fig2)
# # #             st.plotly_chart(fig2, use_container_width=True)
# # #         with c2:
# # #             era_avg = df.groupby("Era")["GDP_Growth"].mean().reset_index()
# # #             fig3 = go.Figure(go.Bar(
# # #                 x=era_avg["Era"], y=era_avg["GDP_Growth"],
# # #                 marker_color=[COLORS["blue"],COLORS["red"],COLORS["green"],COLORS["yellow"]],
# # #                 text=[f"{v:.1f}%" for v in era_avg["GDP_Growth"]],
# # #                 textposition="outside", textfont=dict(size=10, color=COLORS["text"]),
# # #             ))
# # #             fig3.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
# # #             st.plotly_chart(fig3, use_container_width=True)

# # # # ═════════════════════════════════════════════════════════════════════════════
# # # # TAB 2 — Inflation
# # # # ═════════════════════════════════════════════════════════════════════════════
# # # with tabs[1]:
# # #     if show_inf:
# # #         st.subheader(f"Inflation — {country_name}")
# # #         fig = go.Figure()
# # #         fig.add_trace(go.Scatter(
# # #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# # #             y=[7.5]*len(dff) + [2.5]*len(dff),
# # #             fill="toself", fillcolor="rgba(61,220,110,0.06)",
# # #             line=dict(color="rgba(0,0,0,0)"), name="Target Band (2.5–7.5%)",
# # #         ))
# # #         fig.add_hline(y=7.5, line=dict(color=COLORS["red"], dash="dot", width=1),
# # #                       annotation_text="Upper 7.5%",
# # #                       annotation_font=dict(color=COLORS["red"], size=10))
# # #         fig.add_hline(y=2.5, line=dict(color=COLORS["green"], dash="dot", width=1),
# # #                       annotation_text="Lower 2.5%",
# # #                       annotation_font=dict(color=COLORS["green"], size=10))
# # #         fig.add_trace(go.Scatter(
# # #             x=dff["Year"], y=dff["Inflation"], name="CPI Inflation",
# # #             line=dict(color=COLORS["yellow"], width=2.5), mode="lines+markers",
# # #             marker=dict(size=5, color=[
# # #                 COLORS["red"] if v > 7.5 else
# # #                 (COLORS["green"] if v < 2.5 else COLORS["yellow"])
# # #                 for v in dff["Inflation"]
# # #             ]),
# # #             fill="tozeroy", fillcolor="rgba(245,200,66,0.07)",
# # #         ))
# # #         fig.update_layout(**layout(height=380,
# # #                           yaxis_extra=dict(ticksuffix="%", title="CPI %")))
# # #         add_covid_band(fig)
# # #         st.plotly_chart(fig, use_container_width=True)

# # #         c1, c2 = st.columns(2)
# # #         with c1:
# # #             above  = (dff["Inflation"] > 7.5).sum()
# # #             within = ((dff["Inflation"] >= 2.5) & (dff["Inflation"] <= 7.5)).sum()
# # #             below  = (dff["Inflation"] < 2.5).sum()
# # #             fig2 = go.Figure(go.Pie(
# # #                 labels=["Above target","Within target","Below target"],
# # #                 values=[above, within, below], hole=0.55,
# # #                 marker=dict(colors=[COLORS["red"],COLORS["green"],COLORS["blue"]]),
# # #                 textfont=dict(color=COLORS["text"]),
# # #             ))
# # #             fig2.update_layout(**layout(height=280),
# # #                                title=dict(text="Years Within Target Band",
# # #                                           font=dict(color=COLORS["text"])))
# # #             st.plotly_chart(fig2, use_container_width=True)
# # #         with c2:
# # #             fig3 = go.Figure(go.Histogram(
# # #                 x=dff["Inflation"], nbinsx=10,
# # #                 marker=dict(color=COLORS["yellow"], opacity=0.7,
# # #                             line=dict(color=COLORS["bg"], width=1)),
# # #             ))
# # #             fig3.add_vline(x=dff["Inflation"].mean(),
# # #                            line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # #                            annotation_text=f"Mean: {dff['Inflation'].mean():.1f}%",
# # #                            annotation_font=dict(color=COLORS["text"], size=10))
# # #             fig3.update_layout(**layout(height=280,
# # #                                xaxis_extra=dict(title="Inflation %"),
# # #                                yaxis_extra=dict(title="Count")))
# # #             st.plotly_chart(fig3, use_container_width=True)

# # # # ═════════════════════════════════════════════════════════════════════════════
# # # # TAB 3 — Unemployment
# # # # ═════════════════════════════════════════════════════════════════════════════
# # # with tabs[2]:
# # #     if show_unemp:
# # #         st.subheader(f"Unemployment — {country_name}")
# # #         fig = go.Figure()
# # #         fig.add_trace(go.Scatter(
# # #             x=dff["Year"], y=dff["Unemployment"], name="Unemployment %",
# # #             line=dict(color=COLORS["red"], width=2.5), mode="lines+markers",
# # #             marker=dict(size=6), fill="tozeroy", fillcolor="rgba(232,93,74,0.1)",
# # #         ))
# # #         dc2 = dff.copy()
# # #         dc2["MA3"] = dc2["Unemployment"].rolling(3, center=True).mean()
# # #         fig.add_trace(go.Scatter(
# # #             x=dc2["Year"], y=dc2["MA3"], name="3-Year Rolling Avg",
# # #             line=dict(color=COLORS["text"], width=1.5, dash="dot"), mode="lines",
# # #         ))
# # #         fig.update_layout(**layout(height=360,
# # #                           yaxis_extra=dict(ticksuffix="%", title="Unemployment %")))
# # #         add_covid_band(fig)
# # #         st.plotly_chart(fig, use_container_width=True)

# # #         c1, c2, c3 = st.columns(3)
# # #         c1.metric("Peak",    f"{dff['Unemployment'].max():.1f}%",
# # #                   f"in {int(dff.loc[dff['Unemployment'].idxmax(),'Year'])}")
# # #         c2.metric("Lowest",  f"{dff['Unemployment'].min():.1f}%",
# # #                   f"in {int(dff.loc[dff['Unemployment'].idxmin(),'Year'])}")
# # #         c3.metric("Average", f"{dff['Unemployment'].mean():.1f}%", "ILO modeled")

# # # # ═════════════════════════════════════════════════════════════════════════════
# # # # TAB 4 — Trade
# # # # ═════════════════════════════════════════════════════════════════════════════
# # # with tabs[3]:
# # #     if show_trade:
# # #         st.subheader(f"Trade Balance — {country_name}")
# # #         fig = go.Figure()
# # #         fig.add_trace(go.Scatter(
# # #             x=dff["Year"], y=dff["Exports_GDP"], name="Exports % GDP",
# # #             line=dict(color=COLORS["blue"], width=2.5),
# # #             mode="lines+markers", marker=dict(size=4),
# # #         ))
# # #         fig.add_trace(go.Scatter(
# # #             x=dff["Year"], y=dff["Imports_GDP"], name="Imports % GDP",
# # #             line=dict(color=COLORS["yellow"], width=2.5),
# # #             mode="lines+markers", marker=dict(size=4),
# # #         ))
# # #         fig.add_trace(go.Scatter(
# # #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# # #             y=list(dff["Imports_GDP"]) + list(dff["Exports_GDP"])[::-1],
# # #             fill="toself", fillcolor="rgba(232,93,74,0.08)",
# # #             line=dict(color="rgba(0,0,0,0)"), name="Trade Deficit",
# # #         ))
# # #         fig.update_layout(**layout(height=360,
# # #                           yaxis_extra=dict(ticksuffix="%", title="% of GDP")))
# # #         add_covid_band(fig)
# # #         st.plotly_chart(fig, use_container_width=True)

# # #         fig2 = go.Figure(go.Bar(
# # #             x=dff["Year"], y=dff["Trade_Balance"],
# # #             marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# # #                           for v in dff["Trade_Balance"]],
# # #             text=[f"{v:.1f}%" for v in dff["Trade_Balance"]],
# # #             textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# # #         ))
# # #         fig2.add_hline(y=0, line=dict(color=COLORS["muted"], width=1))
# # #         fig2.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
# # #         add_covid_band(fig2)
# # #         st.plotly_chart(fig2, use_container_width=True)

# # # # ═════════════════════════════════════════════════════════════════════════════
# # # # TAB 5 — Correlations
# # # # ═════════════════════════════════════════════════════════════════════════════
# # # with tabs[4]:
# # #     if show_scatter:
# # #         st.subheader(f"Correlation Analysis — {country_name}")
# # #         c1, c2 = st.columns(2)
# # #         with c1:
# # #             sl, ic, r, p, _ = stats.linregress(dff["GDP_Growth"], dff["Unemployment"])
# # #             tx = np.linspace(dff["GDP_Growth"].min(), dff["GDP_Growth"].max(), 100)
# # #             fig = go.Figure()
# # #             fig.add_trace(go.Scatter(
# # #                 x=dff["GDP_Growth"], y=dff["Unemployment"],
# # #                 mode="markers+text", text=dff["Year"],
# # #                 textposition="top center",
# # #                 textfont=dict(size=9, color=COLORS["muted"]),
# # #                 marker=dict(size=10, color=dff["Year"],
# # #                             colorscale=[[0,COLORS["blue"]],[0.86,COLORS["red"]],[1,COLORS["green"]]],
# # #                             showscale=True,
# # #                             colorbar=dict(title="Year", tickfont=dict(color=COLORS["muted"]))),
# # #                 name="Observations",
# # #             ))
# # #             fig.add_trace(go.Scatter(
# # #                 x=tx, y=sl*tx+ic, mode="lines",
# # #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # #                 name=f"Trend (R²={r**2:.2f})",
# # #             ))
# # #             fig.update_layout(**layout(height=360,
# # #                               xaxis_extra=dict(title="GDP Growth %", ticksuffix="%"),
# # #                               yaxis_extra=dict(title="Unemployment %", ticksuffix="%")))
# # #             st.plotly_chart(fig, use_container_width=True)
# # #             st.caption(f"Pearson r = {r:.3f} | R² = {r**2:.3f} | p = {p:.4f}")

# # #         with c2:
# # #             sl2, ic2, r2, p2, _ = stats.linregress(dff["Inflation"], dff["GDP_Growth"])
# # #             tx2 = np.linspace(dff["Inflation"].min(), dff["Inflation"].max(), 100)
# # #             fig2 = go.Figure()
# # #             fig2.add_trace(go.Scatter(
# # #                 x=dff["Inflation"], y=dff["GDP_Growth"],
# # #                 mode="markers+text", text=dff["Year"],
# # #                 textposition="top center",
# # #                 textfont=dict(size=9, color=COLORS["muted"]),
# # #                 marker=dict(size=10, color=COLORS["yellow"], opacity=0.8),
# # #                 name="Observations",
# # #             ))
# # #             fig2.add_trace(go.Scatter(
# # #                 x=tx2, y=sl2*tx2+ic2, mode="lines",
# # #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# # #                 name=f"Trend (R²={r2**2:.2f})",
# # #             ))
# # #             fig2.update_layout(**layout(height=360,
# # #                                xaxis_extra=dict(title="Inflation %", ticksuffix="%"),
# # #                                yaxis_extra=dict(title="GDP Growth %", ticksuffix="%")))
# # #             st.plotly_chart(fig2, use_container_width=True)
# # #             st.caption(f"Pearson r = {r2:.3f} | R² = {r2**2:.3f} | p = {p2:.4f}")

# # #         corr_cols   = ["GDP_B","GDP_Growth","Inflation","Unemployment",
# # #                        "Exports_GDP","Imports_GDP","Trade_Balance"]
# # #         corr_labels = ["GDP (B)","GDP Growth","Inflation","Unemployment",
# # #                        "Exports","Imports","Trade Bal."]
# # #         corr = dff[corr_cols].corr().values
# # #         fig3 = go.Figure(go.Heatmap(
# # #             z=corr, x=corr_labels, y=corr_labels,
# # #             colorscale=[[0,COLORS["red"]],[0.5,COLORS["surface"]],[1,COLORS["green"]]],
# # #             zmid=0, zmin=-1, zmax=1,
# # #             text=[[f"{v:.2f}" for v in row] for row in corr],
# # #             texttemplate="%{text}", textfont=dict(size=11, color=COLORS["text"]),
# # #         ))
# # #         fig3.update_layout(**layout(height=380))
# # #         st.plotly_chart(fig3, use_container_width=True)

# # # # ═════════════════════════════════════════════════════════════════════════════
# # # # TAB 6 — Forecast
# # # # ═════════════════════════════════════════════════════════════════════════════
# # # with tabs[5]:
# # #     if show_forecast:
# # #         st.subheader(f"Forecast — {country_name} · {last_year+1}–{last_year+forecast_years}")
# # #         st.caption(f"Model: **{forecast_model}** | Trained on {year_range[0]}–{last_year} | Shaded = 95% CI")

# # #         train = df[(df["Year"] >= year_range[0]) & (df["Year"] <= last_year)].dropna()
# # #         indicators = [
# # #             ("GDP_Growth",   "GDP Growth %",     COLORS["green"],  "%",  ""),
# # #             ("GDP_B",        "GDP (USD Billion)", COLORS["green"],  "B",  "$"),
# # #             ("Inflation",    "Inflation %",       COLORS["yellow"], "%",  ""),
# # #             ("Unemployment", "Unemployment %",    COLORS["red"],    "%",  ""),
# # #         ]
# # #         fc1, fc2 = st.columns(2)
# # #         forecast_results = {}

# # #         for i, (col, label, color, unit, prefix) in enumerate(indicators):
# # #             valid = train[["Year", col]].dropna()
# # #             if len(valid) < 3:
# # #                 continue
# # #             fut_yrs, pred, lo, hi = run_forecast(
# # #                 valid["Year"].tolist(), valid[col].tolist(),
# # #                 forecast_years, forecast_model,
# # #             )
# # #             forecast_results[col] = {"years": fut_yrs, "pred": pred}

# # #             rh = int(color[1:3], 16); rg = int(color[3:5], 16); rb = int(color[5:7], 16)
# # #             fig = go.Figure()
# # #             fig.add_trace(go.Scatter(
# # #                 x=valid["Year"], y=valid[col], name="Historical",
# # #                 line=dict(color=color, width=2.5), mode="lines+markers",
# # #                 marker=dict(size=4),
# # #             ))
# # #             fig.add_trace(go.Scatter(
# # #                 x=fut_yrs + fut_yrs[::-1], y=hi + lo[::-1],
# # #                 fill="toself",
# # #                 fillcolor=f"rgba({rh},{rg},{rb},0.12)",
# # #                 line=dict(color="rgba(0,0,0,0)"), name="95% CI",
# # #             ))
# # #             fig.add_trace(go.Scatter(
# # #                 x=fut_yrs, y=pred, name="Forecast",
# # #                 line=dict(color=color, width=2, dash="dash"),
# # #                 mode="lines+markers", marker=dict(size=6, symbol="diamond"),
# # #             ))
# # #             fig.add_vline(x=last_year + 0.5,
# # #                           line=dict(color=COLORS["muted"], dash="dot", width=1),
# # #                           annotation_text="Forecast →",
# # #                           annotation_font=dict(color=COLORS["muted"], size=9))
# # #             add_covid_band(fig)
# # #             fig.update_layout(**layout(height=300,
# # #                               yaxis_extra=dict(title=label,
# # #                                                ticksuffix="" if unit == "B" else unit,
# # #                                                tickprefix=prefix)))
# # #             with (fc1 if i % 2 == 0 else fc2):
# # #                 st.plotly_chart(fig, use_container_width=True)

# # #         if forecast_results:
# # #             st.markdown("---")
# # #             st.markdown("**📋 Forecast Summary**")
# # #             rows = []
# # #             ref_col = list(forecast_results.keys())[0]
# # #             for idx, yr in enumerate(forecast_results[ref_col]["years"]):
# # #                 row = {"Year": yr}
# # #                 for col, res in forecast_results.items():
# # #                     lbl = {"GDP_Growth":"GDP Growth %","GDP_B":"GDP (USD B)",
# # #                            "Inflation":"Inflation %","Unemployment":"Unemployment %"}
# # #                     fmt = f"${res['pred'][idx]:.1f}B" if col == "GDP_B" else f"{res['pred'][idx]:.1f}%"
# # #                     row[lbl.get(col, col)] = fmt
# # #                 rows.append(row)
# # #             st.dataframe(pd.DataFrame(rows).set_index("Year"), use_container_width=True)
# # #     else:
# # #         st.info("Enable **5-Year Forecast** in the sidebar.")

# # # # ═════════════════════════════════════════════════════════════════════════════
# # # # TAB 7 — COUNTRY COMPARISON  ✨ NEW
# # # # ═════════════════════════════════════════════════════════════════════════════
# # # with tabs[6]:
# # #     st.subheader("🗺️ Country Comparison — All 54 African Nations")
# # #     st.caption("Select up to 5 countries to compare side by side. "
# # #                "🟢 = full data · 🟡 = partial · 🔴 = sparse")

# # #     # ── Comparison controls ───────────────────────────────────────────────
# # #     cc1, cc2, cc3 = st.columns([2, 1, 1])
# # #     with cc1:
# # #         compare_codes = st.multiselect(
# # #             "Select countries to compare (up to 5)",
# # #             options=list(COUNTRY_OPTIONS.keys()),
# # #             default=["KEN", "NGA", "ZAF", "ETH", "GHA"],
# # #             format_func=lambda c: COUNTRY_OPTIONS[c],
# # #             max_selections=5,
# # #         )
# # #     with cc2:
# # #         compare_indicator = st.selectbox(
# # #             "Indicator",
# # #             options=["GDP_Growth", "GDP_B", "Inflation", "Unemployment",
# # #                      "Exports_GDP", "Imports_GDP", "Trade_Balance"],
# # #             format_func=lambda x: {
# # #                 "GDP_Growth":   "GDP Growth %",
# # #                 "GDP_B":        "GDP (USD Billion)",
# # #                 "Inflation":    "Inflation %",
# # #                 "Unemployment": "Unemployment %",
# # #                 "Exports_GDP":  "Exports % GDP",
# # #                 "Imports_GDP":  "Imports % GDP",
# # #                 "Trade_Balance":"Trade Balance % GDP",
# # #             }[x],
# # #         )
# # #     with cc3:
# # #         compare_range = st.slider(
# # #             "Year range", min_value=2000, max_value=2023,
# # #             value=(2005, 2023), key="compare_range",
# # #         )

# # #     if not compare_codes:
# # #         st.info("Select at least one country above to begin.")
# # #     else:
# # #         # ── Load all selected countries ───────────────────────────────────
# # #         country_data = {}
# # #         load_errors  = []

# # #         progress = st.progress(0, text="Loading country data…")
# # #         for i, code in enumerate(compare_codes):
# # #             progress.progress((i + 1) / len(compare_codes),
# # #                               text=f"Loading {AFRICA_COUNTRIES[code][0]}…")
# # #             cdf, csrc = fetch_single_country(code)
# # #             if cdf is not None:
# # #                 country_data[code] = cdf
# # #             else:
# # #                 load_errors.append(AFRICA_COUNTRIES[code][0])
# # #         progress.empty()

# # #         if load_errors:
# # #             st.warning(f"Could not load: {', '.join(load_errors)}. These may have no World Bank data.")

# # #         if country_data:
# # #             ind_labels = {
# # #                 "GDP_Growth":   ("GDP Growth %",        "%",  ""),
# # #                 "GDP_B":        ("GDP (USD Billion)",    "B",  "$"),
# # #                 "Inflation":    ("Inflation %",          "%",  ""),
# # #                 "Unemployment": ("Unemployment %",       "%",  ""),
# # #                 "Exports_GDP":  ("Exports % of GDP",     "%",  ""),
# # #                 "Imports_GDP":  ("Imports % of GDP",     "%",  ""),
# # #                 "Trade_Balance":("Trade Balance % GDP",  "%",  ""),
# # #             }
# # #             ind_label, ind_unit, ind_prefix = ind_labels[compare_indicator]

# # #             # ── Main comparison line chart ────────────────────────────────
# # #             st.markdown(f"### {ind_label} — Side-by-Side Comparison")
# # #             fig = go.Figure()

# # #             for idx, (code, cdf) in enumerate(country_data.items()):
# # #                 cdf_f = cdf[(cdf["Year"] >= compare_range[0]) &
# # #                             (cdf["Year"] <= compare_range[1])].copy()
# # #                 if compare_indicator not in cdf_f.columns:
# # #                     continue
# # #                 valid = cdf_f.dropna(subset=[compare_indicator])
# # #                 if valid.empty:
# # #                     continue
# # #                 color = COUNTRY_PALETTE[idx % len(COUNTRY_PALETTE)]
# # #                 name  = AFRICA_COUNTRIES[code][0]
# # #                 fig.add_trace(go.Scatter(
# # #                     x=valid["Year"], y=valid[compare_indicator],
# # #                     name=name,
# # #                     line=dict(color=color, width=2.5),
# # #                     mode="lines+markers",
# # #                     marker=dict(size=5, color=color),
# # #                     hovertemplate=f"<b>{name}</b><br>Year: %{{x}}<br>{ind_label}: %{{y:.1f}}<extra></extra>",
# # #                 ))

# # #             tick_suffix = "" if ind_unit == "B" else ind_unit
# # #             fig.update_layout(**layout(
# # #                 height=420,
# # #                 yaxis_extra=dict(title=ind_label, ticksuffix=tick_suffix, tickprefix=ind_prefix),
# # #             ))
# # #             if highlight_covid:
# # #                 add_covid_band(fig)
# # #             st.plotly_chart(fig, use_container_width=True)

# # #             # ── Latest value bar chart ────────────────────────────────────
# # #             st.markdown(f"### Latest Available Value — {ind_label}")
# # #             bar_data = []
# # #             for code, cdf in country_data.items():
# # #                 valid = cdf.dropna(subset=[compare_indicator])
# # #                 if not valid.empty:
# # #                     latest_val  = valid.iloc[-1][compare_indicator]
# # #                     latest_yr   = int(valid.iloc[-1]["Year"])
# # #                     bar_data.append({
# # #                         "Country": AFRICA_COUNTRIES[code][0],
# # #                         "Value":   latest_val,
# # #                         "Year":    latest_yr,
# # #                         "Code":    code,
# # #                     })

# # #             if bar_data:
# # #                 bar_df = pd.DataFrame(bar_data).sort_values("Value", ascending=True)
# # #                 fig_bar = go.Figure(go.Bar(
# # #                     x=bar_df["Value"],
# # #                     y=bar_df["Country"],
# # #                     orientation="h",
# # #                     marker=dict(
# # #                         color=bar_df["Value"],
# # #                         colorscale=[[0, COLORS["red"]], [0.5, COLORS["yellow"]], [1, COLORS["green"]]],
# # #                         showscale=True,
# # #                         colorbar=dict(title=ind_label, tickfont=dict(color=COLORS["muted"])),
# # #                     ),
# # #                     text=[f"{v:.1f}{ind_unit if ind_unit != 'B' else 'B'} ({y})"
# # #                           for v, y in zip(bar_df["Value"], bar_df["Year"])],
# # #                     textposition="outside",
# # #                     textfont=dict(size=10, color=COLORS["text"]),
# # #                 ))
# # #                 fig_bar.update_layout(**layout(
# # #                     height=max(250, len(bar_data) * 55),
# # #                     yaxis_extra=dict(title=""),
# # #                     xaxis_extra=dict(title=ind_label,
# # #                                      ticksuffix=tick_suffix, tickprefix=ind_prefix),
# # #                 ))
# # #                 st.plotly_chart(fig_bar, use_container_width=True)

# # #             # ── All-indicators summary table ──────────────────────────────
# # #             st.markdown("### 📋 All Indicators — Latest Values")
# # #             table_rows = []
# # #             for code, cdf in country_data.items():
# # #                 row = {"Country": AFRICA_COUNTRIES[code][0], "Data": AFRICA_COUNTRIES[code][1]}
# # #                 for ind, (lbl, unit, pfx) in ind_labels.items():
# # #                     valid = cdf.dropna(subset=[ind])
# # #                     if not valid.empty:
# # #                         v = valid.iloc[-1][ind]
# # #                         yr = int(valid.iloc[-1]["Year"])
# # #                         row[lbl] = f"{pfx}{v:.1f}{unit if unit != 'B' else 'B'} ({yr})"
# # #                     else:
# # #                         row[lbl] = "—"
# # #                 table_rows.append(row)

# # #             table_df = pd.DataFrame(table_rows).set_index("Country")
# # #             st.dataframe(table_df, use_container_width=True)

# # #             # ── Download comparison data ──────────────────────────────────
# # #             all_frames = []
# # #             for code, cdf in country_data.items():
# # #                 tmp = cdf.copy()
# # #                 tmp.insert(0, "Country", AFRICA_COUNTRIES[code][0])
# # #                 tmp.insert(1, "ISO3", code)
# # #                 all_frames.append(tmp)
# # #             combined = pd.concat(all_frames, ignore_index=True)
# # #             csv = combined.to_csv(index=False).encode("utf-8")
# # #             st.download_button(
# # #                 "⬇️ Download Comparison CSV",
# # #                 data=csv,
# # #                 file_name="africa_comparison.csv",
# # #                 mime="text/csv",
# # #             )

# # # # ═════════════════════════════════════════════════════════════════════════════
# # # # TAB 8 — Statistics
# # # # ═════════════════════════════════════════════════════════════════════════════
# # # with tabs[7]:
# # #     if show_stats:
# # #         st.subheader(f"Statistical Summary — {country_name}")
# # #         summary_cols = ["GDP_Growth","Inflation","Unemployment",
# # #                         "Exports_GDP","Imports_GDP","Trade_Balance"]
# # #         label_map    = {
# # #             "GDP_Growth":"GDP Growth %","Inflation":"Inflation %",
# # #             "Unemployment":"Unemployment %","Exports_GDP":"Exports % GDP",
# # #             "Imports_GDP":"Imports % GDP","Trade_Balance":"Trade Balance % GDP",
# # #         }
# # #         stats_df = dff[summary_cols].describe().T.round(2)
# # #         stats_df.index = [label_map[i] for i in stats_df.index]
# # #         stats_df.columns = ["Count","Mean","Std Dev","Min",
# # #                             "25th %ile","Median","75th %ile","Max"]
# # #         st.dataframe(
# # #             stats_df.style.background_gradient(subset=["Mean"], cmap="RdYlGn", axis=0)
# # #                           .format("{:.2f}"),
# # #             use_container_width=True,
# # #         )

# # #         st.markdown("---")
# # #         st.markdown("**Raw Data**")
# # #         disp = dff[["Year","Era","GDP_B","GDP_Growth","Inflation",
# # #                     "Unemployment","Exports_GDP","Imports_GDP","Trade_Balance"]].copy()
# # #         disp.columns = ["Year","Era","GDP ($B)","GDP Growth %","Inflation %",
# # #                         "Unemployment %","Exports % GDP","Imports % GDP","Trade Balance %"]
# # #         st.dataframe(disp.set_index("Year"), use_container_width=True)
# # #         csv = disp.to_csv(index=False).encode("utf-8")
# # #         st.download_button("⬇️ Download CSV", data=csv,
# # #                            file_name=f"{primary_code}_economic_data.csv",
# # #                            mime="text/csv")

# # # # ── Insights ──────────────────────────────────────────────────────────────────
# # # st.markdown("---")
# # # st.subheader("Key Insights")
# # # c1, c2, c3 = st.columns(3)
# # # with c1:
# # #     st.markdown("""<div class='insight-box'>
# # #         <h4>📈 Sustained Long-Term Growth</h4>
# # #         <p>Many African economies have recorded GDP growth rates of 4–8% annually over the
# # #         past two decades, outpacing global averages and demonstrating strong structural
# # #         development trajectories.</p></div>""", unsafe_allow_html=True)
# # # with c2:
# # #     st.markdown("""<div class='insight-box warn'>
# # #         <h4>🔥 Inflation Pressures</h4>
# # #         <p>Inflation remains a persistent challenge across the continent, amplified by
# # #         global food and energy price shocks in 2008 and 2022, and structural import
# # #         dependency on commodities.</p></div>""", unsafe_allow_html=True)
# # # with c3:
# # #     st.markdown("""<div class='insight-box danger'>
# # #         <h4>🌍 Trade Imbalances</h4>
# # #         <p>Most African economies run persistent trade deficits driven by fuel, machinery,
# # #         and manufactured goods imports. Diversification of exports remains a key
# # #         development challenge across the region.</p></div>""", unsafe_allow_html=True)

# # # st.markdown(
# # #     "<br><small style='color:#3a4f3d'>Data: World Bank Open Data · IMF DataMapper · "
# # #     "54 African countries · All indicators sourced from official national statistics.</small>",
# # #     unsafe_allow_html=True,
# # # )


# # """
# # Africa Economic Indicators Dashboard
# # Streamlit + Plotly | All Upgrades:
# #   - Live World Bank API (wbgapi) with offline fallback
# #   - 5-Year Forecasting Panel
# #   - Country Comparison — all 54 African countries
# #   - AI Insights Tab — powered by Google Gemini
# # Data source: World Bank Open Data
# # """

# # import os
# # import streamlit as st
# # import pandas as pd
# # import plotly.graph_objects as go
# # from plotly.subplots import make_subplots
# # import numpy as np
# # from scipy import stats
# # from sklearn.linear_model import LinearRegression
# # from sklearn.preprocessing import PolynomialFeatures
# # from sklearn.pipeline import make_pipeline
# # from datetime import datetime

# # # Load .env file if present (for local development)
# # try:
# #     from dotenv import load_dotenv
# #     load_dotenv()
# # except ImportError:
# #     pass

# # # ── Page config ───────────────────────────────────────────────────────────────
# # st.set_page_config(
# #     page_title="Africa Economic Dashboard",
# #     page_icon="🌍",
# #     layout="wide",
# #     initial_sidebar_state="expanded",
# # )

# # # ── CSS ───────────────────────────────────────────────────────────────────────
# # st.markdown("""
# # <style>
# #     .stApp { background-color: #0a0f0d; }
# #     .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
# #     [data-testid="stSidebar"] { background-color: #111812; border-right: 1px solid #1e2e21; }
# #     [data-testid="stSidebar"] * { color: #e8f0ea !important; }
# #     [data-testid="metric-container"] {
# #         background: #111812; border: 1px solid #1e2e21;
# #         border-radius: 6px; padding: 1rem 1.2rem;
# #     }
# #     [data-testid="stMetricLabel"] { color: #6b7f6e !important; font-size: 0.75rem; }
# #     [data-testid="stMetricValue"] { color: #e8f0ea !important; }
# #     [data-testid="stMetricDelta"] { font-size: 0.8rem; }
# #     h1, h2, h3 { color: #e8f0ea !important; }
# #     p, li { color: #b0bfb3 !important; }
# #     .stTabs [data-baseweb="tab-list"] { background-color: #111812; border-bottom: 1px solid #1e2e21; }
# #     .stTabs [data-baseweb="tab"] { color: #6b7f6e; }
# #     .stTabs [aria-selected="true"] { color: #3ddc6e !important; border-bottom-color: #3ddc6e !important; }
# #     hr { border-color: #1e2e21; }
# #     .stAlert { background-color: #111812; border-color: #1e2e21; }
# #     .section-label {
# #         font-family: monospace; font-size: 0.65rem; letter-spacing: 0.2em;
# #         color: #3ddc6e; text-transform: uppercase; margin-bottom: 0.25rem;
# #     }
# #     .data-badge {
# #         display: inline-block; font-family: monospace; font-size: 0.62rem;
# #         letter-spacing: 0.1em; padding: 0.25rem 0.65rem;
# #         border-radius: 2px; margin-bottom: 1rem;
# #     }
# #     .badge-live  { background: rgba(61,220,110,0.15); color: #3ddc6e; border: 1px solid #3ddc6e; }
# #     .badge-cache { background: rgba(245,200,66,0.15); color: #f5c842; border: 1px solid #f5c842; }
# #     .insight-box {
# #         background: #111812; border: 1px solid #1e2e21;
# #         border-left: 3px solid #3ddc6e; border-radius: 4px;
# #         padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# #     }
# #     .insight-box.warn   { border-left-color: #f5c842; }
# #     .insight-box.danger { border-left-color: #e85d4a; }
# #     .insight-box h4 { color: #e8f0ea !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# #     .insight-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# #     .forecast-box {
# #         background: rgba(74,157,232,0.06); border: 1px solid rgba(74,157,232,0.25);
# #         border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# #     }
# #     .forecast-box h4 { color: #4a9de8 !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# #     .forecast-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# #     .compare-box {
# #         background: rgba(167,139,250,0.06); border: 1px solid rgba(167,139,250,0.25);
# #         border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# #     }
# #     .compare-box h4 { color: #a78bfa !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# #     .compare-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# #     .ai-response {
# #         background: #0d1a0f; border: 1px solid #1e2e21;
# #         border-left: 3px solid #3ddc6e; border-radius: 4px;
# #         padding: 1.4rem 1.6rem; margin-top: 1rem;
# #         font-size: 0.88rem; line-height: 1.8; color: #c8d8cb !important;
# #         white-space: pre-wrap;
# #     }
# #     .ai-question-btn {
# #         background: #111812; border: 1px solid #1e2e21;
# #         border-radius: 4px; padding: 0.6rem 1rem;
# #         margin: 0.3rem; cursor: pointer; font-size: 0.8rem;
# #         color: #6b7f6e; transition: all 0.2s;
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # ── Colors & layout ───────────────────────────────────────────────────────────
# # COLORS = {
# #     "bg": "#0a0f0d", "surface": "#111812", "border": "#1e2e21",
# #     "green": "#3ddc6e", "yellow": "#f5c842", "red": "#e85d4a",
# #     "blue": "#4a9de8", "purple": "#a78bfa", "muted": "#6b7f6e", "text": "#e8f0ea",
# # }
# # COUNTRY_PALETTE = [
# #     "#3ddc6e","#4a9de8","#f5c842","#e85d4a","#a78bfa",
# #     "#f97316","#06b6d4","#ec4899","#84cc16","#fb923c",
# # ]
# # GRID = dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], tickcolor=COLORS["border"])

# # def layout(height=360, xaxis_extra=None, yaxis_extra=None, **kwargs):
# #     return dict(
# #         paper_bgcolor=COLORS["surface"], plot_bgcolor=COLORS["bg"],
# #         font=dict(family="DM Mono, monospace", color=COLORS["muted"], size=11),
# #         xaxis={**GRID, **(xaxis_extra or {})},
# #         yaxis={**GRID, **(yaxis_extra or {})},
# #         margin=dict(t=40, b=40, l=55, r=20),
# #         legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
# #         height=height, **kwargs,
# #     )

# # # ── All 54 African countries ──────────────────────────────────────────────────
# # AFRICA_COUNTRIES = {
# #     "DZA": ("🇩🇿 Algeria",              "🟢"),
# #     "AGO": ("🇦🇴 Angola",               "🟡"),
# #     "BEN": ("🇧🇯 Benin",                "🟡"),
# #     "BWA": ("🇧🇼 Botswana",             "🟢"),
# #     "BFA": ("🇧🇫 Burkina Faso",         "🟡"),
# #     "BDI": ("🇧🇮 Burundi",              "🟡"),
# #     "CPV": ("🇨🇻 Cabo Verde",           "🟡"),
# #     "CMR": ("🇨🇲 Cameroon",             "🟢"),
# #     "CAF": ("🇨🇫 Central African Rep.", "🔴"),
# #     "TCD": ("🇹🇩 Chad",                 "🟡"),
# #     "COM": ("🇰🇲 Comoros",              "🔴"),
# #     "COD": ("🇨🇩 DR Congo",             "🟡"),
# #     "COG": ("🇨🇬 Republic of Congo",    "🟡"),
# #     "CIV": ("🇨🇮 Côte d'Ivoire",        "🟢"),
# #     "DJI": ("🇩🇯 Djibouti",             "🟡"),
# #     "EGY": ("🇪🇬 Egypt",                "🟢"),
# #     "GNQ": ("🇬🇶 Equatorial Guinea",    "🟡"),
# #     "ERI": ("🇪🇷 Eritrea",              "🔴"),
# #     "SWZ": ("🇸🇿 Eswatini",             "🟡"),
# #     "ETH": ("🇪🇹 Ethiopia",             "🟢"),
# #     "GAB": ("🇬🇦 Gabon",                "🟡"),
# #     "GMB": ("🇬🇲 Gambia",               "🟡"),
# #     "GHA": ("🇬🇭 Ghana",                "🟢"),
# #     "GIN": ("🇬🇳 Guinea",               "🟡"),
# #     "GNB": ("🇬🇼 Guinea-Bissau",        "🔴"),
# #     "KEN": ("🇰🇪 Kenya",                "🟢"),
# #     "LSO": ("🇱🇸 Lesotho",              "🟡"),
# #     "LBR": ("🇱🇷 Liberia",              "🟡"),
# #     "LBY": ("🇱🇾 Libya",                "🔴"),
# #     "MDG": ("🇲🇬 Madagascar",           "🟡"),
# #     "MWI": ("🇲🇼 Malawi",               "🟡"),
# #     "MLI": ("🇲🇱 Mali",                 "🟡"),
# #     "MRT": ("🇲🇷 Mauritania",           "🟡"),
# #     "MUS": ("🇲🇺 Mauritius",            "🟢"),
# #     "MAR": ("🇲🇦 Morocco",              "🟢"),
# #     "MOZ": ("🇲🇿 Mozambique",           "🟡"),
# #     "NAM": ("🇳🇦 Namibia",              "🟢"),
# #     "NER": ("🇳🇪 Niger",                "🟡"),
# #     "NGA": ("🇳🇬 Nigeria",              "🟢"),
# #     "RWA": ("🇷🇼 Rwanda",               "🟢"),
# #     "STP": ("🇸🇹 São Tomé & Príncipe",  "🔴"),
# #     "SEN": ("🇸🇳 Senegal",              "🟢"),
# #     "SLE": ("🇸🇱 Sierra Leone",         "🟡"),
# #     "SOM": ("🇸🇴 Somalia",              "🔴"),
# #     "ZAF": ("🇿🇦 South Africa",         "🟢"),
# #     "SSD": ("🇸🇸 South Sudan",          "🔴"),
# #     "SDN": ("🇸🇩 Sudan",                "🔴"),
# #     "TZA": ("🇹🇿 Tanzania",             "🟢"),
# #     "TGO": ("🇹🇬 Togo",                 "🟡"),
# #     "TUN": ("🇹🇳 Tunisia",              "🟢"),
# #     "UGA": ("🇺🇬 Uganda",               "🟢"),
# #     "ZMB": ("🇿🇲 Zambia",               "🟢"),
# #     "ZWE": ("🇿🇼 Zimbabwe",             "🟡"),
# #     "SYC": ("🇸🇨 Seychelles",           "🟡"),
# # }
# # COUNTRY_OPTIONS = {
# #     code: f"{quality} {name}"
# #     for code, (name, quality) in sorted(AFRICA_COUNTRIES.items(), key=lambda x: x[1][0])
# # }

# # # ── World Bank indicators ─────────────────────────────────────────────────────
# # WB_INDICATORS = {
# #     "GDP_B":        "NY.GDP.MKTP.CD",
# #     "GDP_Growth":   "NY.GDP.MKTP.KD.ZG",
# #     "Inflation":    "FP.CPI.TOTL.ZG",
# #     "Unemployment": "SL.UEM.TOTL.ZS",
# #     "Exports_GDP":  "NE.EXP.GNFS.ZS",
# #     "Imports_GDP":  "NE.IMP.GNFS.ZS",
# # }

# # # ── Kenya fallback ────────────────────────────────────────────────────────────
# # KENYA_FALLBACK = {
# #     "Year":        list(range(2000, 2024)),
# #     "GDP_B":       [12.7,13.3,13.4,14.0,15.1,18.7,22.5,27.2,30.6,29.5,
# #                     32.2,34.0,41.1,47.6,60.9,63.4,70.5,79.3,87.8,95.5,
# #                     98.8,99.2,110.4,107.9],
# #     "GDP_Growth":  [0.6,4.5,0.3,2.9,4.6,5.9,6.5,6.9,1.5,2.7,
# #                     8.4,6.1,4.6,5.9,5.4,5.7,5.9,4.9,6.3,5.4,
# #                     -0.3,7.6,4.8,5.6],
# #     "Inflation":   [10.0,5.8,2.0,9.8,11.6,10.3,6.0,4.3,26.2,10.5,
# #                     4.0,14.0,9.4,5.7,6.9,6.6,6.3,8.0,4.7,5.2,
# #                     5.3,6.1,9.1,6.3],
# #     "Unemployment":[9.8,9.8,9.8,9.8,9.8,9.3,8.7,8.1,7.4,6.7,
# #                     6.1,5.5,4.9,4.4,3.9,3.5,2.8,3.5,4.3,5.0,
# #                     5.6,5.7,5.7,5.6],
# #     "Exports_GDP": [25.2,24.8,23.6,23.0,24.0,23.8,23.0,24.5,24.1,20.4,
# #                     21.2,21.0,19.5,18.3,16.9,15.7,14.6,13.8,13.9,13.5,
# #                     12.4,13.5,14.2,13.8],
# #     "Imports_GDP": [33.1,32.5,31.6,30.5,32.0,31.8,33.0,37.2,42.4,36.3,
# #                     36.1,40.0,38.5,37.3,34.5,32.5,30.6,29.8,31.9,29.5,
# #                     26.7,28.0,32.6,31.2],
# # }

# # # ── Data helpers ──────────────────────────────────────────────────────────────
# # def _enrich(df):
# #     df["Trade_Balance"] = df["Exports_GDP"] - df["Imports_GDP"]
# #     df["Era"] = df["Year"].apply(
# #         lambda y: "🔴 COVID" if 2020 <= y <= 2021
# #         else ("🟡 Post-COVID" if y >= 2022
# #         else ("🟢 Growth" if y >= 2010 else "🔵 Early 2000s"))
# #     )
# #     return df.reset_index(drop=True)

# # @st.cache_data(ttl=3600, show_spinner=False)
# # def fetch_single_country(iso3: str):
# #     try:
# #         import wbgapi as wb
# #         frames = []
# #         for col, code in WB_INDICATORS.items():
# #             s = wb.data.DataFrame(code, iso3, mrv=30, numericTimeKeys=True)
# #             s = s.T.reset_index()
# #             s.columns = ["Year", col]
# #             s["Year"] = s["Year"].astype(int)
# #             frames.append(s.set_index("Year"))
# #         df = pd.concat(frames, axis=1).reset_index()
# #         df = df[df["Year"] >= 2000].sort_values("Year")
# #         df["GDP_B"] = df["GDP_B"] / 1e9
# #         return _enrich(df), "live"
# #     except Exception:
# #         if iso3 == "KEN":
# #             return _enrich(pd.DataFrame(KENYA_FALLBACK)), "cached"
# #         return None, "unavailable"

# # @st.cache_data(ttl=3600, show_spinner=False)
# # def fetch_primary_country(iso3: str):
# #     return fetch_single_country(iso3)

# # # ── Gemini AI helper ──────────────────────────────────────────────────────────
# # def build_data_summary(df, country_name, year_range):
# #     """Build a concise data summary string to pass to Gemini."""
# #     dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()
# #     latest = dff.iloc[-1]
# #     lines = [
# #         f"Country: {country_name}",
# #         f"Period: {year_range[0]}–{year_range[1]}",
# #         f"Latest Year: {int(latest['Year'])}",
# #         f"GDP: ${latest['GDP_B']:.1f}B (growth: {latest['GDP_Growth']:.1f}%)",
# #         f"Inflation: {latest['Inflation']:.1f}%",
# #         f"Unemployment: {latest['Unemployment']:.1f}%",
# #         f"Trade Balance: {latest['Trade_Balance']:.1f}% of GDP",
# #         "",
# #         "Year-by-year GDP growth (%):",
# #         ", ".join([f"{int(r.Year)}: {r.GDP_Growth:.1f}%" for _, r in dff.iterrows() if not pd.isna(r.GDP_Growth)]),
# #         "",
# #         "Year-by-year Inflation (%):",
# #         ", ".join([f"{int(r.Year)}: {r.Inflation:.1f}%" for _, r in dff.iterrows() if not pd.isna(r.Inflation)]),
# #         "",
# #         "Year-by-year Unemployment (%):",
# #         ", ".join([f"{int(r.Year)}: {r.Unemployment:.1f}%" for _, r in dff.iterrows() if not pd.isna(r.Unemployment)]),
# #         "",
# #         f"Avg GDP Growth: {dff['GDP_Growth'].mean():.1f}%",
# #         f"Peak Inflation: {dff['Inflation'].max():.1f}% in {int(dff.loc[dff['Inflation'].idxmax(), 'Year'])}",
# #         f"Lowest Unemployment: {dff['Unemployment'].min():.1f}% in {int(dff.loc[dff['Unemployment'].idxmin(), 'Year'])}",
# #     ]
# #     return "\n".join(lines)

# # def call_gemini(prompt: str, api_key: str) -> str:
# #     """Call Gemini Flash and return the text response."""
# #     try:
# #         import google.generativeai as genai
# #         genai.configure(api_key=api_key)
# #         model = genai.GenerativeModel("gemini-1.5-flash")
# #         response = model.generate_content(prompt)
# #         return response.text
# #     except ImportError:
# #         return "❌ google-generativeai not installed. Run: pip install google-generativeai"
# #     except Exception as e:
# #         return f"❌ Gemini error: {str(e)}"

# # # ── Sidebar ───────────────────────────────────────────────────────────────────
# # with st.sidebar:
# #     st.markdown("### 🌍 Africa Dashboard")
# #     st.markdown("---")

# #     st.markdown("**PRIMARY COUNTRY**")
# #     primary_code = st.selectbox(
# #         "Primary country",
# #         options=list(COUNTRY_OPTIONS.keys()),
# #         format_func=lambda c: COUNTRY_OPTIONS[c],
# #         index=list(COUNTRY_OPTIONS.keys()).index("KEN"),
# #         label_visibility="collapsed",
# #     )

# #     st.markdown("---")
# #     st.markdown("**TIME RANGE**")
# #     year_range = st.slider("Years", min_value=2000, max_value=2023,
# #                            value=(2005, 2023), label_visibility="collapsed")

# #     st.markdown("---")
# #     st.markdown("**INDICATORS**")
# #     show_gdp     = st.checkbox("GDP & Growth",        value=True)
# #     show_inf     = st.checkbox("Inflation",            value=True)
# #     show_unemp   = st.checkbox("Unemployment",         value=True)
# #     show_trade   = st.checkbox("Trade Balance",        value=True)
# #     show_scatter = st.checkbox("Correlation Analysis", value=True)
# #     show_stats   = st.checkbox("Statistical Summary",  value=True)

# #     st.markdown("---")
# #     st.markdown("**FORECASTING**")
# #     show_forecast  = st.checkbox("5-Year Forecast", value=True)
# #     forecast_years = st.slider("Horizon (years)", 1, 10, 5,
# #                                disabled=not show_forecast)
# #     forecast_model = st.radio("Model",
# #                               ["Linear", "Polynomial (deg 2)", "Polynomial (deg 3)"],
# #                               disabled=not show_forecast)

# #     st.markdown("---")
# #     st.markdown("**AI INSIGHTS**")
# #     gemini_key = st.text_input(
# #         "Gemini API Key",
# #         value=os.getenv("GEMINI_API_KEY", ""),
# #         type="password",
# #         placeholder="AIzaSy...",
# #         help="Get your free key at aistudio.google.com",
# #     )

# #     st.markdown("---")
# #     st.markdown("**DISPLAY**")
# #     highlight_covid = st.toggle("Highlight COVID period", value=True)

# #     st.markdown("---")
# #     st.markdown(
# #         f"<small style='color:#3a4f3d'>Source: World Bank Open Data<br>"
# #         f"54 African countries · {datetime.now().strftime('%d %b %Y')}</small>",
# #         unsafe_allow_html=True,
# #     )

# # # ── Load primary country ──────────────────────────────────────────────────────
# # with st.spinner(f"Loading data…"):
# #     df, data_source = fetch_primary_country(primary_code)

# # if df is None:
# #     st.error(f"Could not load data for {COUNTRY_OPTIONS[primary_code]}.")
# #     st.stop()

# # last_year    = int(df["Year"].max())
# # country_name = AFRICA_COUNTRIES[primary_code][0]
# # dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

# # # ── Header ────────────────────────────────────────────────────────────────────
# # st.markdown(
# #     f"<p class='section-label'>AFRICA ECONOMIC DASHBOARD · WORLD BANK · "
# #     f"{'LIVE' if data_source == 'live' else 'OFFLINE'}</p>",
# #     unsafe_allow_html=True,
# # )
# # col_h1, col_h2 = st.columns([3, 1])
# # with col_h1:
# #     st.title(f"{country_name} — Economic Analysis")
# #     st.markdown(f"**GDP · Inflation · Unemployment · Trade** &nbsp;·&nbsp; {year_range[0]}–{year_range[1]}")
# # with col_h2:
# #     badge = "badge-live" if data_source == "live" else "badge-cache"
# #     label = "🟢 LIVE" if data_source == "live" else "🟡 OFFLINE"
# #     st.markdown(f"<div style='padding-top:2rem'><span class='data-badge {badge}'>{label}</span></div>",
# #                 unsafe_allow_html=True)
# #     if st.button("🔄 Refresh"):
# #         st.cache_data.clear()
# #         st.rerun()

# # st.markdown("---")

# # # ── KPI Cards ─────────────────────────────────────────────────────────────────
# # latest = dff.iloc[-1]
# # prev   = dff.iloc[-2]
# # k1, k2, k3, k4 = st.columns(4)
# # k1.metric("GDP (Latest)",          f"${latest['GDP_B']:.1f}B",
# #           f"{latest['GDP_Growth']:+.1f}% growth")
# # k2.metric("Inflation",             f"{latest['Inflation']:.1f}%",
# #           f"{latest['Inflation']-prev['Inflation']:+.1f}pp vs prior year")
# # k3.metric("Unemployment",          f"{latest['Unemployment']:.1f}%",
# #           f"{latest['Unemployment']-prev['Unemployment']:+.1f}pp vs prior year")
# # k4.metric("Trade Balance (% GDP)", f"{latest['Trade_Balance']:.1f}%",
# #           f"{latest['Trade_Balance']-prev['Trade_Balance']:+.1f}pp vs prior year")

# # st.markdown("---")

# # # ── Tabs ──────────────────────────────────────────────────────────────────────
# # tabs = st.tabs([
# #     "📈 GDP", "🔥 Inflation", "👷 Unemployment",
# #     "🌍 Trade", "🔗 Correlations", "🔮 Forecast",
# #     "🗺️ Compare", "🤖 AI Insights", "📊 Statistics",
# # ])

# # # ── Shared helpers ────────────────────────────────────────────────────────────
# # def add_covid_band(fig):
# #     if highlight_covid:
# #         fig.add_vrect(
# #             x0=2019.5, x1=2021.5,
# #             fillcolor="rgba(232,93,74,0.08)",
# #             line=dict(color="rgba(232,93,74,0.3)", width=1, dash="dot"),
# #             annotation_text="COVID", annotation_position="top left",
# #             annotation_font=dict(color=COLORS["red"], size=10),
# #         )
# #     return fig

# # def run_forecast(years, values, horizon, model_name):
# #     X = np.array(years).reshape(-1, 1)
# #     y = np.array(values)
# #     if model_name == "Linear":
# #         model = LinearRegression()
# #     elif model_name == "Polynomial (deg 2)":
# #         model = make_pipeline(PolynomialFeatures(2), LinearRegression())
# #     else:
# #         model = make_pipeline(PolynomialFeatures(3), LinearRegression())
# #     model.fit(X, y)
# #     future = np.arange(years[-1] + 1, years[-1] + horizon + 1)
# #     pred   = model.predict(future.reshape(-1, 1))
# #     ci     = 1.96 * np.std(y - model.predict(X)) * np.sqrt(1 + 1 / len(y))
# #     return future.tolist(), pred.tolist(), (pred - ci).tolist(), (pred + ci).tolist()

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 1 — GDP
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[0]:
# #     if show_gdp:
# #         st.subheader(f"GDP — {country_name}")
# #         fig = make_subplots(specs=[[{"secondary_y": True}]])
# #         fig.add_trace(go.Bar(
# #             x=dff["Year"], y=dff["GDP_B"], name="GDP (USD B)",
# #             marker=dict(color=COLORS["green"], opacity=0.22,
# #                         line=dict(color=COLORS["green"], width=1)),
# #         ), secondary_y=False)
# #         fig.add_trace(go.Scatter(
# #             x=dff["Year"], y=dff["GDP_Growth"], name="GDP Growth %",
# #             line=dict(color=COLORS["green"], width=2.5),
# #             mode="lines+markers", marker=dict(size=5),
# #         ), secondary_y=True)
# #         fig.update_layout(**layout(height=380), title="")
# #         fig.update_yaxes(title_text="GDP (USD B)", secondary_y=False,
# #                          tickprefix="$", ticksuffix="B",
# #                          gridcolor=COLORS["border"], linecolor=COLORS["border"])
# #         fig.update_yaxes(title_text="Growth %", secondary_y=True,
# #                          ticksuffix="%", gridcolor="rgba(0,0,0,0)")
# #         fig.update_xaxes(gridcolor=COLORS["border"])
# #         add_covid_band(fig)
# #         st.plotly_chart(fig, use_container_width=True)

# #         c1, c2 = st.columns(2)
# #         with c1:
# #             dc = dff.copy(); dc["GDP_Change"] = dc["GDP_B"].diff()
# #             fig2 = go.Figure(go.Bar(
# #                 x=dc["Year"][1:], y=dc["GDP_Change"][1:],
# #                 marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# #                               for v in dc["GDP_Change"][1:]],
# #                 text=[f"${v:+.1f}B" for v in dc["GDP_Change"][1:]],
# #                 textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# #             ))
# #             fig2.update_layout(**layout(height=280,
# #                                yaxis_extra=dict(tickprefix="$", ticksuffix="B")))
# #             add_covid_band(fig2)
# #             st.plotly_chart(fig2, use_container_width=True)
# #         with c2:
# #             era_avg = df.groupby("Era")["GDP_Growth"].mean().reset_index()
# #             fig3 = go.Figure(go.Bar(
# #                 x=era_avg["Era"], y=era_avg["GDP_Growth"],
# #                 marker_color=[COLORS["blue"],COLORS["red"],COLORS["green"],COLORS["yellow"]],
# #                 text=[f"{v:.1f}%" for v in era_avg["GDP_Growth"]],
# #                 textposition="outside", textfont=dict(size=10, color=COLORS["text"]),
# #             ))
# #             fig3.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
# #             st.plotly_chart(fig3, use_container_width=True)

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 2 — Inflation
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[1]:
# #     if show_inf:
# #         st.subheader(f"Inflation — {country_name}")
# #         fig = go.Figure()
# #         fig.add_trace(go.Scatter(
# #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# #             y=[7.5]*len(dff) + [2.5]*len(dff),
# #             fill="toself", fillcolor="rgba(61,220,110,0.06)",
# #             line=dict(color="rgba(0,0,0,0)"), name="Target Band (2.5–7.5%)",
# #         ))
# #         fig.add_hline(y=7.5, line=dict(color=COLORS["red"], dash="dot", width=1),
# #                       annotation_text="Upper 7.5%",
# #                       annotation_font=dict(color=COLORS["red"], size=10))
# #         fig.add_hline(y=2.5, line=dict(color=COLORS["green"], dash="dot", width=1),
# #                       annotation_text="Lower 2.5%",
# #                       annotation_font=dict(color=COLORS["green"], size=10))
# #         fig.add_trace(go.Scatter(
# #             x=dff["Year"], y=dff["Inflation"], name="CPI Inflation",
# #             line=dict(color=COLORS["yellow"], width=2.5), mode="lines+markers",
# #             marker=dict(size=5, color=[
# #                 COLORS["red"] if v > 7.5 else
# #                 (COLORS["green"] if v < 2.5 else COLORS["yellow"])
# #                 for v in dff["Inflation"]
# #             ]),
# #             fill="tozeroy", fillcolor="rgba(245,200,66,0.07)",
# #         ))
# #         fig.update_layout(**layout(height=380,
# #                           yaxis_extra=dict(ticksuffix="%", title="CPI %")))
# #         add_covid_band(fig)
# #         st.plotly_chart(fig, use_container_width=True)

# #         c1, c2 = st.columns(2)
# #         with c1:
# #             above  = (dff["Inflation"] > 7.5).sum()
# #             within = ((dff["Inflation"] >= 2.5) & (dff["Inflation"] <= 7.5)).sum()
# #             below  = (dff["Inflation"] < 2.5).sum()
# #             fig2 = go.Figure(go.Pie(
# #                 labels=["Above target","Within target","Below target"],
# #                 values=[above, within, below], hole=0.55,
# #                 marker=dict(colors=[COLORS["red"],COLORS["green"],COLORS["blue"]]),
# #                 textfont=dict(color=COLORS["text"]),
# #             ))
# #             fig2.update_layout(**layout(height=280),
# #                                title=dict(text="Years Within Target Band",
# #                                           font=dict(color=COLORS["text"])))
# #             st.plotly_chart(fig2, use_container_width=True)
# #         with c2:
# #             fig3 = go.Figure(go.Histogram(
# #                 x=dff["Inflation"], nbinsx=10,
# #                 marker=dict(color=COLORS["yellow"], opacity=0.7,
# #                             line=dict(color=COLORS["bg"], width=1)),
# #             ))
# #             fig3.add_vline(x=dff["Inflation"].mean(),
# #                            line=dict(color=COLORS["text"], dash="dash", width=1.5),
# #                            annotation_text=f"Mean: {dff['Inflation'].mean():.1f}%",
# #                            annotation_font=dict(color=COLORS["text"], size=10))
# #             fig3.update_layout(**layout(height=280,
# #                                xaxis_extra=dict(title="Inflation %"),
# #                                yaxis_extra=dict(title="Count")))
# #             st.plotly_chart(fig3, use_container_width=True)

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 3 — Unemployment
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[2]:
# #     if show_unemp:
# #         st.subheader(f"Unemployment — {country_name}")
# #         fig = go.Figure()
# #         fig.add_trace(go.Scatter(
# #             x=dff["Year"], y=dff["Unemployment"], name="Unemployment %",
# #             line=dict(color=COLORS["red"], width=2.5), mode="lines+markers",
# #             marker=dict(size=6), fill="tozeroy", fillcolor="rgba(232,93,74,0.1)",
# #         ))
# #         dc2 = dff.copy()
# #         dc2["MA3"] = dc2["Unemployment"].rolling(3, center=True).mean()
# #         fig.add_trace(go.Scatter(
# #             x=dc2["Year"], y=dc2["MA3"], name="3-Year Rolling Avg",
# #             line=dict(color=COLORS["text"], width=1.5, dash="dot"), mode="lines",
# #         ))
# #         fig.update_layout(**layout(height=360,
# #                           yaxis_extra=dict(ticksuffix="%", title="Unemployment %")))
# #         add_covid_band(fig)
# #         st.plotly_chart(fig, use_container_width=True)

# #         c1, c2, c3 = st.columns(3)
# #         c1.metric("Peak",    f"{dff['Unemployment'].max():.1f}%",
# #                   f"in {int(dff.loc[dff['Unemployment'].idxmax(),'Year'])}")
# #         c2.metric("Lowest",  f"{dff['Unemployment'].min():.1f}%",
# #                   f"in {int(dff.loc[dff['Unemployment'].idxmin(),'Year'])}")
# #         c3.metric("Average", f"{dff['Unemployment'].mean():.1f}%", "ILO modeled")

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 4 — Trade
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[3]:
# #     if show_trade:
# #         st.subheader(f"Trade Balance — {country_name}")
# #         fig = go.Figure()
# #         fig.add_trace(go.Scatter(
# #             x=dff["Year"], y=dff["Exports_GDP"], name="Exports % GDP",
# #             line=dict(color=COLORS["blue"], width=2.5),
# #             mode="lines+markers", marker=dict(size=4),
# #         ))
# #         fig.add_trace(go.Scatter(
# #             x=dff["Year"], y=dff["Imports_GDP"], name="Imports % GDP",
# #             line=dict(color=COLORS["yellow"], width=2.5),
# #             mode="lines+markers", marker=dict(size=4),
# #         ))
# #         fig.add_trace(go.Scatter(
# #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# #             y=list(dff["Imports_GDP"]) + list(dff["Exports_GDP"])[::-1],
# #             fill="toself", fillcolor="rgba(232,93,74,0.08)",
# #             line=dict(color="rgba(0,0,0,0)"), name="Trade Deficit",
# #         ))
# #         fig.update_layout(**layout(height=360,
# #                           yaxis_extra=dict(ticksuffix="%", title="% of GDP")))
# #         add_covid_band(fig)
# #         st.plotly_chart(fig, use_container_width=True)

# #         fig2 = go.Figure(go.Bar(
# #             x=dff["Year"], y=dff["Trade_Balance"],
# #             marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# #                           for v in dff["Trade_Balance"]],
# #             text=[f"{v:.1f}%" for v in dff["Trade_Balance"]],
# #             textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# #         ))
# #         fig2.add_hline(y=0, line=dict(color=COLORS["muted"], width=1))
# #         fig2.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
# #         add_covid_band(fig2)
# #         st.plotly_chart(fig2, use_container_width=True)

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 5 — Correlations
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[4]:
# #     if show_scatter:
# #         st.subheader(f"Correlation Analysis — {country_name}")
# #         c1, c2 = st.columns(2)
# #         with c1:
# #             sl, ic, r, p, _ = stats.linregress(dff["GDP_Growth"], dff["Unemployment"])
# #             tx = np.linspace(dff["GDP_Growth"].min(), dff["GDP_Growth"].max(), 100)
# #             fig = go.Figure()
# #             fig.add_trace(go.Scatter(
# #                 x=dff["GDP_Growth"], y=dff["Unemployment"],
# #                 mode="markers+text", text=dff["Year"],
# #                 textposition="top center",
# #                 textfont=dict(size=9, color=COLORS["muted"]),
# #                 marker=dict(size=10, color=dff["Year"],
# #                             colorscale=[[0,COLORS["blue"]],[0.86,COLORS["red"]],[1,COLORS["green"]]],
# #                             showscale=True,
# #                             colorbar=dict(title="Year", tickfont=dict(color=COLORS["muted"]))),
# #                 name="Observations",
# #             ))
# #             fig.add_trace(go.Scatter(
# #                 x=tx, y=sl*tx+ic, mode="lines",
# #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# #                 name=f"Trend (R²={r**2:.2f})",
# #             ))
# #             fig.update_layout(**layout(height=360,
# #                               xaxis_extra=dict(title="GDP Growth %", ticksuffix="%"),
# #                               yaxis_extra=dict(title="Unemployment %", ticksuffix="%")))
# #             st.plotly_chart(fig, use_container_width=True)
# #             st.caption(f"Pearson r = {r:.3f} | R² = {r**2:.3f} | p = {p:.4f}")

# #         with c2:
# #             sl2, ic2, r2, p2, _ = stats.linregress(dff["Inflation"], dff["GDP_Growth"])
# #             tx2 = np.linspace(dff["Inflation"].min(), dff["Inflation"].max(), 100)
# #             fig2 = go.Figure()
# #             fig2.add_trace(go.Scatter(
# #                 x=dff["Inflation"], y=dff["GDP_Growth"],
# #                 mode="markers+text", text=dff["Year"],
# #                 textposition="top center",
# #                 textfont=dict(size=9, color=COLORS["muted"]),
# #                 marker=dict(size=10, color=COLORS["yellow"], opacity=0.8),
# #                 name="Observations",
# #             ))
# #             fig2.add_trace(go.Scatter(
# #                 x=tx2, y=sl2*tx2+ic2, mode="lines",
# #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# #                 name=f"Trend (R²={r2**2:.2f})",
# #             ))
# #             fig2.update_layout(**layout(height=360,
# #                                xaxis_extra=dict(title="Inflation %", ticksuffix="%"),
# #                                yaxis_extra=dict(title="GDP Growth %", ticksuffix="%")))
# #             st.plotly_chart(fig2, use_container_width=True)
# #             st.caption(f"Pearson r = {r2:.3f} | R² = {r2**2:.3f} | p = {p2:.4f}")

# #         corr_cols   = ["GDP_B","GDP_Growth","Inflation","Unemployment",
# #                        "Exports_GDP","Imports_GDP","Trade_Balance"]
# #         corr_labels = ["GDP (B)","GDP Growth","Inflation","Unemployment",
# #                        "Exports","Imports","Trade Bal."]
# #         corr = dff[corr_cols].corr().values
# #         fig3 = go.Figure(go.Heatmap(
# #             z=corr, x=corr_labels, y=corr_labels,
# #             colorscale=[[0,COLORS["red"]],[0.5,COLORS["surface"]],[1,COLORS["green"]]],
# #             zmid=0, zmin=-1, zmax=1,
# #             text=[[f"{v:.2f}" for v in row] for row in corr],
# #             texttemplate="%{text}", textfont=dict(size=11, color=COLORS["text"]),
# #         ))
# #         fig3.update_layout(**layout(height=380))
# #         st.plotly_chart(fig3, use_container_width=True)

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 6 — Forecast
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[5]:
# #     if show_forecast:
# #         st.subheader(f"Forecast — {country_name} · {last_year+1}–{last_year+forecast_years}")
# #         st.caption(f"Model: **{forecast_model}** | Trained on {year_range[0]}–{last_year} | Shaded = 95% CI")

# #         train = df[(df["Year"] >= year_range[0]) & (df["Year"] <= last_year)].dropna()
# #         indicators = [
# #             ("GDP_Growth",   "GDP Growth %",     COLORS["green"],  "%",  ""),
# #             ("GDP_B",        "GDP (USD Billion)", COLORS["green"],  "B",  "$"),
# #             ("Inflation",    "Inflation %",       COLORS["yellow"], "%",  ""),
# #             ("Unemployment", "Unemployment %",    COLORS["red"],    "%",  ""),
# #         ]
# #         fc1, fc2 = st.columns(2)
# #         forecast_results = {}

# #         for i, (col, label, color, unit, prefix) in enumerate(indicators):
# #             valid = train[["Year", col]].dropna()
# #             if len(valid) < 3:
# #                 continue
# #             fut_yrs, pred, lo, hi = run_forecast(
# #                 valid["Year"].tolist(), valid[col].tolist(),
# #                 forecast_years, forecast_model,
# #             )
# #             forecast_results[col] = {"years": fut_yrs, "pred": pred}
# #             rh = int(color[1:3],16); rg = int(color[3:5],16); rb = int(color[5:7],16)

# #             fig = go.Figure()
# #             fig.add_trace(go.Scatter(
# #                 x=valid["Year"], y=valid[col], name="Historical",
# #                 line=dict(color=color, width=2.5), mode="lines+markers",
# #                 marker=dict(size=4),
# #             ))
# #             fig.add_trace(go.Scatter(
# #                 x=fut_yrs + fut_yrs[::-1], y=hi + lo[::-1],
# #                 fill="toself", fillcolor=f"rgba({rh},{rg},{rb},0.12)",
# #                 line=dict(color="rgba(0,0,0,0)"), name="95% CI",
# #             ))
# #             fig.add_trace(go.Scatter(
# #                 x=fut_yrs, y=pred, name="Forecast",
# #                 line=dict(color=color, width=2, dash="dash"),
# #                 mode="lines+markers", marker=dict(size=6, symbol="diamond"),
# #             ))
# #             fig.add_vline(x=last_year + 0.5,
# #                           line=dict(color=COLORS["muted"], dash="dot", width=1),
# #                           annotation_text="Forecast →",
# #                           annotation_font=dict(color=COLORS["muted"], size=9))
# #             add_covid_band(fig)
# #             fig.update_layout(**layout(height=300,
# #                               yaxis_extra=dict(title=label,
# #                                                ticksuffix="" if unit=="B" else unit,
# #                                                tickprefix=prefix)))
# #             with (fc1 if i % 2 == 0 else fc2):
# #                 st.plotly_chart(fig, use_container_width=True)

# #         if forecast_results:
# #             st.markdown("---")
# #             st.markdown("**📋 Forecast Summary**")
# #             rows = []
# #             ref = list(forecast_results.keys())[0]
# #             lbl_map = {"GDP_Growth":"GDP Growth %","GDP_B":"GDP (USD B)",
# #                        "Inflation":"Inflation %","Unemployment":"Unemployment %"}
# #             for idx, yr in enumerate(forecast_results[ref]["years"]):
# #                 row = {"Year": yr}
# #                 for col, res in forecast_results.items():
# #                     fmt = f"${res['pred'][idx]:.1f}B" if col=="GDP_B" else f"{res['pred'][idx]:.1f}%"
# #                     row[lbl_map.get(col, col)] = fmt
# #                 rows.append(row)
# #             st.dataframe(pd.DataFrame(rows).set_index("Year"), use_container_width=True)
# #     else:
# #         st.info("Enable **5-Year Forecast** in the sidebar.")

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 7 — Country Comparison
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[6]:
# #     st.subheader("🗺️ Country Comparison — All 54 African Nations")
# #     st.caption("🟢 = full data · 🟡 = partial · 🔴 = sparse")

# #     cc1, cc2, cc3 = st.columns([2, 1, 1])
# #     with cc1:
# #         compare_codes = st.multiselect(
# #             "Select countries (up to 5)",
# #             options=list(COUNTRY_OPTIONS.keys()),
# #             default=["KEN","NGA","ZAF","ETH","GHA"],
# #             format_func=lambda c: COUNTRY_OPTIONS[c],
# #             max_selections=5,
# #         )
# #     with cc2:
# #         compare_indicator = st.selectbox(
# #             "Indicator",
# #             options=["GDP_Growth","GDP_B","Inflation","Unemployment",
# #                      "Exports_GDP","Imports_GDP","Trade_Balance"],
# #             format_func=lambda x: {
# #                 "GDP_Growth":"GDP Growth %","GDP_B":"GDP (USD B)",
# #                 "Inflation":"Inflation %","Unemployment":"Unemployment %",
# #                 "Exports_GDP":"Exports % GDP","Imports_GDP":"Imports % GDP",
# #                 "Trade_Balance":"Trade Balance % GDP",
# #             }[x],
# #         )
# #     with cc3:
# #         compare_range = st.slider("Year range", 2000, 2023, (2005, 2023), key="cmp_range")

# #     if not compare_codes:
# #         st.info("Select at least one country above.")
# #     else:
# #         country_data = {}
# #         load_errors  = []
# #         progress = st.progress(0, text="Loading…")
# #         for i, code in enumerate(compare_codes):
# #             progress.progress((i+1)/len(compare_codes),
# #                               text=f"Loading {AFRICA_COUNTRIES[code][0]}…")
# #             cdf, _ = fetch_single_country(code)
# #             if cdf is not None:
# #                 country_data[code] = cdf
# #             else:
# #                 load_errors.append(AFRICA_COUNTRIES[code][0])
# #         progress.empty()

# #         if load_errors:
# #             st.warning(f"Could not load: {', '.join(load_errors)}")

# #         if country_data:
# #             ind_labels = {
# #                 "GDP_Growth":    ("GDP Growth %",       "%", ""),
# #                 "GDP_B":         ("GDP (USD Billion)",  "B", "$"),
# #                 "Inflation":     ("Inflation %",        "%", ""),
# #                 "Unemployment":  ("Unemployment %",     "%", ""),
# #                 "Exports_GDP":   ("Exports % of GDP",   "%", ""),
# #                 "Imports_GDP":   ("Imports % of GDP",   "%", ""),
# #                 "Trade_Balance": ("Trade Balance % GDP","%", ""),
# #             }
# #             ind_label, ind_unit, ind_prefix = ind_labels[compare_indicator]
# #             tick_suffix = "" if ind_unit == "B" else ind_unit

# #             # Line chart
# #             st.markdown(f"### {ind_label} — Over Time")
# #             fig = go.Figure()
# #             for idx, (code, cdf) in enumerate(country_data.items()):
# #                 cdf_f = cdf[(cdf["Year"] >= compare_range[0]) &
# #                             (cdf["Year"] <= compare_range[1])].dropna(subset=[compare_indicator])
# #                 if cdf_f.empty:
# #                     continue
# #                 color = COUNTRY_PALETTE[idx % len(COUNTRY_PALETTE)]
# #                 name  = AFRICA_COUNTRIES[code][0]
# #                 fig.add_trace(go.Scatter(
# #                     x=cdf_f["Year"], y=cdf_f[compare_indicator], name=name,
# #                     line=dict(color=color, width=2.5), mode="lines+markers",
# #                     marker=dict(size=5),
# #                     hovertemplate=f"<b>{name}</b><br>Year: %{{x}}<br>{ind_label}: %{{y:.1f}}<extra></extra>",
# #                 ))
# #             fig.update_layout(**layout(height=420,
# #                               yaxis_extra=dict(title=ind_label,
# #                                                ticksuffix=tick_suffix, tickprefix=ind_prefix)))
# #             if highlight_covid:
# #                 add_covid_band(fig)
# #             st.plotly_chart(fig, use_container_width=True)

# #             # Bar chart — latest values
# #             st.markdown(f"### Latest Value — {ind_label}")
# #             bar_data = []
# #             for code, cdf in country_data.items():
# #                 valid = cdf.dropna(subset=[compare_indicator])
# #                 if not valid.empty:
# #                     bar_data.append({
# #                         "Country": AFRICA_COUNTRIES[code][0],
# #                         "Value":   valid.iloc[-1][compare_indicator],
# #                         "Year":    int(valid.iloc[-1]["Year"]),
# #                     })
# #             if bar_data:
# #                 bar_df = pd.DataFrame(bar_data).sort_values("Value", ascending=True)
# #                 fig_bar = go.Figure(go.Bar(
# #                     x=bar_df["Value"], y=bar_df["Country"], orientation="h",
# #                     marker=dict(
# #                         color=bar_df["Value"],
# #                         colorscale=[[0,COLORS["red"]],[0.5,COLORS["yellow"]],[1,COLORS["green"]]],
# #                         showscale=True,
# #                         colorbar=dict(title=ind_label, tickfont=dict(color=COLORS["muted"])),
# #                     ),
# #                     text=[f"{v:.1f}{ind_unit if ind_unit!='B' else 'B'} ({y})"
# #                           for v, y in zip(bar_df["Value"], bar_df["Year"])],
# #                     textposition="outside",
# #                     textfont=dict(size=10, color=COLORS["text"]),
# #                 ))
# #                 fig_bar.update_layout(**layout(
# #                     height=max(250, len(bar_data)*55),
# #                     yaxis_extra=dict(title=""),
# #                     xaxis_extra=dict(title=ind_label,
# #                                      ticksuffix=tick_suffix, tickprefix=ind_prefix),
# #                 ))
# #                 st.plotly_chart(fig_bar, use_container_width=True)

# #             # Summary table
# #             st.markdown("### 📋 All Indicators — Latest Values")
# #             table_rows = []
# #             for code, cdf in country_data.items():
# #                 row = {"Country": AFRICA_COUNTRIES[code][0], "Quality": AFRICA_COUNTRIES[code][1]}
# #                 for ind, (lbl, unit, pfx) in ind_labels.items():
# #                     valid = cdf.dropna(subset=[ind])
# #                     if not valid.empty:
# #                         v  = valid.iloc[-1][ind]
# #                         yr = int(valid.iloc[-1]["Year"])
# #                         row[lbl] = f"{pfx}{v:.1f}{unit if unit!='B' else 'B'} ({yr})"
# #                     else:
# #                         row[lbl] = "—"
# #                 table_rows.append(row)
# #             st.dataframe(pd.DataFrame(table_rows).set_index("Country"), use_container_width=True)

# #             # Download
# #             all_frames = []
# #             for code, cdf in country_data.items():
# #                 tmp = cdf.copy()
# #                 tmp.insert(0, "Country", AFRICA_COUNTRIES[code][0])
# #                 tmp.insert(1, "ISO3", code)
# #                 all_frames.append(tmp)
# #             combined = pd.concat(all_frames, ignore_index=True)
# #             st.download_button("⬇️ Download Comparison CSV",
# #                                data=combined.to_csv(index=False).encode("utf-8"),
# #                                file_name="africa_comparison.csv", mime="text/csv")

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 8 — AI INSIGHTS  ✨ NEW
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[7]:
# #     st.subheader(f"🤖 AI Insights — {country_name}")
# #     st.caption("Powered by Google Gemini · Reads your actual loaded data, not hardcoded text")

# #     if not gemini_key:
# #         st.warning(
# #             "**Add your Gemini API key to enable AI Insights.**\n\n"
# #             "1. Go to [aistudio.google.com](https://aistudio.google.com) → Get API Key\n"
# #             "2. Paste it into the **AI Insights** field in the sidebar\n"
# #             "3. Or add `GEMINI_API_KEY=your_key` to your `.env` file"
# #         )
# #     else:
# #         # Build the data context once
# #         data_summary = build_data_summary(df, country_name, year_range)

# #         # ── Preset analysis buttons ───────────────────────────────────────
# #         st.markdown("**Quick Analysis — click any button to generate:**")

# #         PRESETS = {
# #             "📊 Full Economic Overview": (
# #                 f"You are an expert economist specializing in African economies. "
# #                 f"Analyze the following economic data for {country_name} and write a "
# #                 f"comprehensive 4-paragraph economic overview. Cover: (1) GDP growth trajectory "
# #                 f"and key turning points, (2) inflation patterns and monetary policy implications, "
# #                 f"(3) unemployment trends and labor market dynamics, (4) trade balance and "
# #                 f"structural economic challenges. Be specific — reference actual numbers from the data.\n\n"
# #                 f"DATA:\n{data_summary}"
# #             ),
# #             "📉 COVID Impact Analysis": (
# #                 f"Analyze the specific economic impact of COVID-19 (2020–2021) on {country_name} "
# #                 f"based on this data. Compare pre-COVID averages (2015–2019) to COVID years and "
# #                 f"the recovery period (2022–2023). Quantify the damage and recovery across all "
# #                 f"indicators. Write 3 focused paragraphs.\n\nDATA:\n{data_summary}"
# #             ),
# #             "🔮 Outlook & Risks": (
# #                 f"Based on the historical economic trends for {country_name}, write a forward-looking "
# #                 f"assessment covering: (1) what the data suggests about growth momentum, "
# #                 f"(2) the biggest economic risks and vulnerabilities, (3) structural opportunities "
# #                 f"for the economy. Ground every point in the actual data provided.\n\nDATA:\n{data_summary}"
# #             ),
# #             "🌍 Regional Context": (
# #                 f"Place {country_name}'s economic performance in the context of sub-Saharan Africa. "
# #                 f"Based on this data, assess whether the country is an outperformer, average, or "
# #                 f"underperformer relative to typical African economies. Discuss inflation management, "
# #                 f"growth consistency, and trade dynamics. Write 3 concise paragraphs.\n\nDATA:\n{data_summary}"
# #             ),
# #             "📈 Best & Worst Years": (
# #                 f"From the data provided for {country_name}, identify and explain the 3 best and "
# #                 f"3 worst economic years. For each year, explain what likely caused the performance "
# #                 f"based on the indicators. Reference specific numbers. Write in a clear analytical style.\n\nDATA:\n{data_summary}"
# #             ),
# #         }

# #         cols = st.columns(3)
# #         for i, (btn_label, _) in enumerate(PRESETS.items()):
# #             with cols[i % 3]:
# #                 if st.button(btn_label, use_container_width=True):
# #                     st.session_state["ai_prompt"]   = PRESETS[btn_label]
# #                     st.session_state["ai_btn_label"] = btn_label

# #         st.markdown("---")

# #         # ── Custom question ───────────────────────────────────────────────
# #         st.markdown("**Or ask a custom question:**")
# #         custom_q = st.text_area(
# #             "Your question",
# #             placeholder=f"e.g. Why did inflation spike so high in {country_name}? "
# #                         f"What does the trade deficit mean for economic growth?",
# #             height=80,
# #             label_visibility="collapsed",
# #         )
# #         if st.button("🔍 Ask Gemini", use_container_width=False):
# #             if custom_q.strip():
# #                 full_prompt = (
# #                     f"You are an expert economist. Answer the following question about "
# #                     f"{country_name} using the data provided. Be specific and reference "
# #                     f"actual numbers.\n\nQUESTION: {custom_q}\n\nDATA:\n{data_summary}"
# #                 )
# #                 st.session_state["ai_prompt"]   = full_prompt
# #                 st.session_state["ai_btn_label"] = f"❓ {custom_q[:60]}…"

# #         # ── Run Gemini and show response ──────────────────────────────────
# #         if "ai_prompt" in st.session_state:
# #             st.markdown("---")
# #             st.markdown(f"**{st.session_state.get('ai_btn_label', 'Analysis')}**")
# #             with st.spinner("Gemini is analyzing the data…"):
# #                 response = call_gemini(st.session_state["ai_prompt"], gemini_key)
# #             st.markdown(
# #                 f"<div class='ai-response'>{response}</div>",
# #                 unsafe_allow_html=True,
# #             )
# #             # Copy button
# #             st.download_button(
# #                 "⬇️ Download Analysis",
# #                 data=response.encode("utf-8"),
# #                 file_name=f"{primary_code}_ai_analysis.txt",
# #                 mime="text/plain",
# #             )
# #             if st.button("🗑️ Clear"):
# #                 del st.session_state["ai_prompt"]
# #                 del st.session_state["ai_btn_label"]
# #                 st.rerun()

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 9 — Statistics
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[8]:
# #     if show_stats:
# #         st.subheader(f"Statistical Summary — {country_name}")
# #         summary_cols = ["GDP_Growth","Inflation","Unemployment",
# #                         "Exports_GDP","Imports_GDP","Trade_Balance"]
# #         label_map = {
# #             "GDP_Growth":"GDP Growth %","Inflation":"Inflation %",
# #             "Unemployment":"Unemployment %","Exports_GDP":"Exports % GDP",
# #             "Imports_GDP":"Imports % GDP","Trade_Balance":"Trade Balance % GDP",
# #         }
# #         stats_df = dff[summary_cols].describe().T.round(2)
# #         stats_df.index = [label_map[i] for i in stats_df.index]
# #         stats_df.columns = ["Count","Mean","Std Dev","Min",
# #                             "25th %ile","Median","75th %ile","Max"]
# #         st.dataframe(
# #             stats_df.style.background_gradient(subset=["Mean"], cmap="RdYlGn", axis=0)
# #                           .format("{:.2f}"),
# #             use_container_width=True,
# #         )
# #         st.markdown("---")
# #         disp = dff[["Year","Era","GDP_B","GDP_Growth","Inflation",
# #                     "Unemployment","Exports_GDP","Imports_GDP","Trade_Balance"]].copy()
# #         disp.columns = ["Year","Era","GDP ($B)","GDP Growth %","Inflation %",
# #                         "Unemployment %","Exports % GDP","Imports % GDP","Trade Balance %"]
# #         st.dataframe(disp.set_index("Year"), use_container_width=True)
# #         st.download_button("⬇️ Download CSV",
# #                            data=disp.to_csv(index=False).encode("utf-8"),
# #                            file_name=f"{primary_code}_data.csv", mime="text/csv")

# # # ── Footer insights ───────────────────────────────────────────────────────────
# # st.markdown("---")
# # st.subheader("Key Insights")
# # c1, c2, c3 = st.columns(3)
# # with c1:
# #     st.markdown("""<div class='insight-box'>
# #         <h4>📈 Sustained Long-Term Growth</h4>
# #         <p>Many African economies have recorded GDP growth of 4–8% annually over two decades,
# #         outpacing global averages and demonstrating strong structural development.</p>
# #         </div>""", unsafe_allow_html=True)
# # with c2:
# #     st.markdown("""<div class='insight-box warn'>
# #         <h4>🔥 Inflation Pressures</h4>
# #         <p>Inflation remains a persistent challenge, amplified by global food and energy
# #         shocks in 2008 and 2022 and structural import dependency across the continent.</p>
# #         </div>""", unsafe_allow_html=True)
# # with c3:
# #     st.markdown("""<div class='insight-box danger'>
# #         <h4>🌍 Trade Imbalances</h4>
# #         <p>Most African economies run persistent trade deficits driven by fuel, machinery,
# #         and manufactured goods imports. Export diversification remains a key challenge.</p>
# #         </div>""", unsafe_allow_html=True)

# # st.markdown(
# #     "<br><small style='color:#3a4f3d'>Data: World Bank Open Data · IMF DataMapper · "
# #     "54 African countries · All indicators from official national statistics.</small>",
# #     unsafe_allow_html=True,
# # )

# # """
# # Africa Economic Indicators Dashboard
# # Streamlit + Plotly | All Upgrades:
# #   - Live World Bank API (wbgapi) with offline fallback
# #   - 5-Year Forecasting Panel
# #   - Country Comparison — all 54 African countries
# #   - AI Insights Tab — powered by Google Gemini
# # Data source: World Bank Open Data
# # """

# # import os
# # import streamlit as st
# # import pandas as pd
# # import plotly.graph_objects as go
# # from plotly.subplots import make_subplots
# # import numpy as np
# # from scipy import stats
# # from sklearn.linear_model import LinearRegression
# # from sklearn.preprocessing import PolynomialFeatures
# # from sklearn.pipeline import make_pipeline
# # from datetime import datetime

# # # Load .env file if present (for local development)
# # try:
# #     from dotenv import load_dotenv
# #     load_dotenv()
# # except ImportError:
# #     pass

# # # ── Page config ───────────────────────────────────────────────────────────────
# # st.set_page_config(
# #     page_title="Africa Economic Dashboard",
# #     page_icon="🌍",
# #     layout="wide",
# #     initial_sidebar_state="expanded",
# # )

# # # ── CSS ───────────────────────────────────────────────────────────────────────
# # st.markdown("""
# # <style>
# #     .stApp { background-color: #0a0f0d; }
# #     .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
# #     [data-testid="stSidebar"] { background-color: #111812; border-right: 1px solid #1e2e21; }
# #     [data-testid="stSidebar"] * { color: #e8f0ea !important; }
# #     [data-testid="metric-container"] {
# #         background: #111812; border: 1px solid #1e2e21;
# #         border-radius: 6px; padding: 1rem 1.2rem;
# #     }
# #     [data-testid="stMetricLabel"] { color: #6b7f6e !important; font-size: 0.75rem; }
# #     [data-testid="stMetricValue"] { color: #e8f0ea !important; }
# #     [data-testid="stMetricDelta"] { font-size: 0.8rem; }
# #     h1, h2, h3 { color: #e8f0ea !important; }
# #     p, li { color: #b0bfb3 !important; }
# #     .stTabs [data-baseweb="tab-list"] { background-color: #111812; border-bottom: 1px solid #1e2e21; }
# #     .stTabs [data-baseweb="tab"] { color: #6b7f6e; }
# #     .stTabs [aria-selected="true"] { color: #3ddc6e !important; border-bottom-color: #3ddc6e !important; }
# #     hr { border-color: #1e2e21; }
# #     .stAlert { background-color: #111812; border-color: #1e2e21; }
# #     .section-label {
# #         font-family: monospace; font-size: 0.65rem; letter-spacing: 0.2em;
# #         color: #3ddc6e; text-transform: uppercase; margin-bottom: 0.25rem;
# #     }
# #     .data-badge {
# #         display: inline-block; font-family: monospace; font-size: 0.62rem;
# #         letter-spacing: 0.1em; padding: 0.25rem 0.65rem;
# #         border-radius: 2px; margin-bottom: 1rem;
# #     }
# #     .badge-live  { background: rgba(61,220,110,0.15); color: #3ddc6e; border: 1px solid #3ddc6e; }
# #     .badge-cache { background: rgba(245,200,66,0.15); color: #f5c842; border: 1px solid #f5c842; }
# #     .insight-box {
# #         background: #111812; border: 1px solid #1e2e21;
# #         border-left: 3px solid #3ddc6e; border-radius: 4px;
# #         padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# #     }
# #     .insight-box.warn   { border-left-color: #f5c842; }
# #     .insight-box.danger { border-left-color: #e85d4a; }
# #     .insight-box h4 { color: #e8f0ea !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# #     .insight-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# #     .forecast-box {
# #         background: rgba(74,157,232,0.06); border: 1px solid rgba(74,157,232,0.25);
# #         border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# #     }
# #     .forecast-box h4 { color: #4a9de8 !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# #     .forecast-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# #     .compare-box {
# #         background: rgba(167,139,250,0.06); border: 1px solid rgba(167,139,250,0.25);
# #         border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
# #     }
# #     .compare-box h4 { color: #a78bfa !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
# #     .compare-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
# #     .ai-response {
# #         background: #0d1a0f; border: 1px solid #1e2e21;
# #         border-left: 3px solid #3ddc6e; border-radius: 4px;
# #         padding: 1.4rem 1.6rem; margin-top: 1rem;
# #         font-size: 0.88rem; line-height: 1.8; color: #c8d8cb !important;
# #         white-space: pre-wrap;
# #     }
# #     .ai-question-btn {
# #         background: #111812; border: 1px solid #1e2e21;
# #         border-radius: 4px; padding: 0.6rem 1rem;
# #         margin: 0.3rem; cursor: pointer; font-size: 0.8rem;
# #         color: #6b7f6e; transition: all 0.2s;
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # ── Colors & layout ───────────────────────────────────────────────────────────
# # COLORS = {
# #     "bg": "#0a0f0d", "surface": "#111812", "border": "#1e2e21",
# #     "green": "#3ddc6e", "yellow": "#f5c842", "red": "#e85d4a",
# #     "blue": "#4a9de8", "purple": "#a78bfa", "muted": "#6b7f6e", "text": "#e8f0ea",
# # }
# # COUNTRY_PALETTE = [
# #     "#3ddc6e","#4a9de8","#f5c842","#e85d4a","#a78bfa",
# #     "#f97316","#06b6d4","#ec4899","#84cc16","#fb923c",
# # ]
# # GRID = dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], tickcolor=COLORS["border"])

# # def layout(height=360, xaxis_extra=None, yaxis_extra=None, **kwargs):
# #     return dict(
# #         paper_bgcolor=COLORS["surface"], plot_bgcolor=COLORS["bg"],
# #         font=dict(family="DM Mono, monospace", color=COLORS["muted"], size=11),
# #         xaxis={**GRID, **(xaxis_extra or {})},
# #         yaxis={**GRID, **(yaxis_extra or {})},
# #         margin=dict(t=40, b=40, l=55, r=20),
# #         legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
# #         height=height, **kwargs,
# #     )

# # # ── All 54 African countries ──────────────────────────────────────────────────
# # AFRICA_COUNTRIES = {
# #     "DZA": ("🇩🇿 Algeria",              "🟢"),
# #     "AGO": ("🇦🇴 Angola",               "🟡"),
# #     "BEN": ("🇧🇯 Benin",                "🟡"),
# #     "BWA": ("🇧🇼 Botswana",             "🟢"),
# #     "BFA": ("🇧🇫 Burkina Faso",         "🟡"),
# #     "BDI": ("🇧🇮 Burundi",              "🟡"),
# #     "CPV": ("🇨🇻 Cabo Verde",           "🟡"),
# #     "CMR": ("🇨🇲 Cameroon",             "🟢"),
# #     "CAF": ("🇨🇫 Central African Rep.", "🔴"),
# #     "TCD": ("🇹🇩 Chad",                 "🟡"),
# #     "COM": ("🇰🇲 Comoros",              "🔴"),
# #     "COD": ("🇨🇩 DR Congo",             "🟡"),
# #     "COG": ("🇨🇬 Republic of Congo",    "🟡"),
# #     "CIV": ("🇨🇮 Côte d'Ivoire",        "🟢"),
# #     "DJI": ("🇩🇯 Djibouti",             "🟡"),
# #     "EGY": ("🇪🇬 Egypt",                "🟢"),
# #     "GNQ": ("🇬🇶 Equatorial Guinea",    "🟡"),
# #     "ERI": ("🇪🇷 Eritrea",              "🔴"),
# #     "SWZ": ("🇸🇿 Eswatini",             "🟡"),
# #     "ETH": ("🇪🇹 Ethiopia",             "🟢"),
# #     "GAB": ("🇬🇦 Gabon",                "🟡"),
# #     "GMB": ("🇬🇲 Gambia",               "🟡"),
# #     "GHA": ("🇬🇭 Ghana",                "🟢"),
# #     "GIN": ("🇬🇳 Guinea",               "🟡"),
# #     "GNB": ("🇬🇼 Guinea-Bissau",        "🔴"),
# #     "KEN": ("🇰🇪 Kenya",                "🟢"),
# #     "LSO": ("🇱🇸 Lesotho",              "🟡"),
# #     "LBR": ("🇱🇷 Liberia",              "🟡"),
# #     "LBY": ("🇱🇾 Libya",                "🔴"),
# #     "MDG": ("🇲🇬 Madagascar",           "🟡"),
# #     "MWI": ("🇲🇼 Malawi",               "🟡"),
# #     "MLI": ("🇲🇱 Mali",                 "🟡"),
# #     "MRT": ("🇲🇷 Mauritania",           "🟡"),
# #     "MUS": ("🇲🇺 Mauritius",            "🟢"),
# #     "MAR": ("🇲🇦 Morocco",              "🟢"),
# #     "MOZ": ("🇲🇿 Mozambique",           "🟡"),
# #     "NAM": ("🇳🇦 Namibia",              "🟢"),
# #     "NER": ("🇳🇪 Niger",                "🟡"),
# #     "NGA": ("🇳🇬 Nigeria",              "🟢"),
# #     "RWA": ("🇷🇼 Rwanda",               "🟢"),
# #     "STP": ("🇸🇹 São Tomé & Príncipe",  "🔴"),
# #     "SEN": ("🇸🇳 Senegal",              "🟢"),
# #     "SLE": ("🇸🇱 Sierra Leone",         "🟡"),
# #     "SOM": ("🇸🇴 Somalia",              "🔴"),
# #     "ZAF": ("🇿🇦 South Africa",         "🟢"),
# #     "SSD": ("🇸🇸 South Sudan",          "🔴"),
# #     "SDN": ("🇸🇩 Sudan",                "🔴"),
# #     "TZA": ("🇹🇿 Tanzania",             "🟢"),
# #     "TGO": ("🇹🇬 Togo",                 "🟡"),
# #     "TUN": ("🇹🇳 Tunisia",              "🟢"),
# #     "UGA": ("🇺🇬 Uganda",               "🟢"),
# #     "ZMB": ("🇿🇲 Zambia",               "🟢"),
# #     "ZWE": ("🇿🇼 Zimbabwe",             "🟡"),
# #     "SYC": ("🇸🇨 Seychelles",           "🟡"),
# # }
# # COUNTRY_OPTIONS = {
# #     code: f"{quality} {name}"
# #     for code, (name, quality) in sorted(AFRICA_COUNTRIES.items(), key=lambda x: x[1][0])
# # }

# # # ── World Bank indicators ─────────────────────────────────────────────────────
# # WB_INDICATORS = {
# #     "GDP_B":        "NY.GDP.MKTP.CD",
# #     "GDP_Growth":   "NY.GDP.MKTP.KD.ZG",
# #     "Inflation":    "FP.CPI.TOTL.ZG",
# #     "Unemployment": "SL.UEM.TOTL.ZS",
# #     "Exports_GDP":  "NE.EXP.GNFS.ZS",
# #     "Imports_GDP":  "NE.IMP.GNFS.ZS",
# # }

# # # ── Kenya fallback ────────────────────────────────────────────────────────────
# # KENYA_FALLBACK = {
# #     "Year":        list(range(2000, 2024)),
# #     "GDP_B":       [12.7,13.3,13.4,14.0,15.1,18.7,22.5,27.2,30.6,29.5,
# #                     32.2,34.0,41.1,47.6,60.9,63.4,70.5,79.3,87.8,95.5,
# #                     98.8,99.2,110.4,107.9],
# #     "GDP_Growth":  [0.6,4.5,0.3,2.9,4.6,5.9,6.5,6.9,1.5,2.7,
# #                     8.4,6.1,4.6,5.9,5.4,5.7,5.9,4.9,6.3,5.4,
# #                     -0.3,7.6,4.8,5.6],
# #     "Inflation":   [10.0,5.8,2.0,9.8,11.6,10.3,6.0,4.3,26.2,10.5,
# #                     4.0,14.0,9.4,5.7,6.9,6.6,6.3,8.0,4.7,5.2,
# #                     5.3,6.1,9.1,6.3],
# #     "Unemployment":[9.8,9.8,9.8,9.8,9.8,9.3,8.7,8.1,7.4,6.7,
# #                     6.1,5.5,4.9,4.4,3.9,3.5,2.8,3.5,4.3,5.0,
# #                     5.6,5.7,5.7,5.6],
# #     "Exports_GDP": [25.2,24.8,23.6,23.0,24.0,23.8,23.0,24.5,24.1,20.4,
# #                     21.2,21.0,19.5,18.3,16.9,15.7,14.6,13.8,13.9,13.5,
# #                     12.4,13.5,14.2,13.8],
# #     "Imports_GDP": [33.1,32.5,31.6,30.5,32.0,31.8,33.0,37.2,42.4,36.3,
# #                     36.1,40.0,38.5,37.3,34.5,32.5,30.6,29.8,31.9,29.5,
# #                     26.7,28.0,32.6,31.2],
# # }

# # # ── Data helpers ──────────────────────────────────────────────────────────────
# # def _enrich(df):
# #     df["Trade_Balance"] = df["Exports_GDP"] - df["Imports_GDP"]
# #     df["Era"] = df["Year"].apply(
# #         lambda y: "🔴 COVID" if 2020 <= y <= 2021
# #         else ("🟡 Post-COVID" if y >= 2022
# #         else ("🟢 Growth" if y >= 2010 else "🔵 Early 2000s"))
# #     )
# #     return df.reset_index(drop=True)

# # @st.cache_data(ttl=3600, show_spinner=False)
# # def fetch_single_country(iso3: str):
# #     try:
# #         import wbgapi as wb
# #         frames = []
# #         for col, code in WB_INDICATORS.items():
# #             s = wb.data.DataFrame(code, iso3, mrv=30, numericTimeKeys=True)
# #             s = s.T.reset_index()
# #             s.columns = ["Year", col]
# #             s["Year"] = s["Year"].astype(int)
# #             frames.append(s.set_index("Year"))
# #         df = pd.concat(frames, axis=1).reset_index()
# #         df = df[df["Year"] >= 2000].sort_values("Year")
# #         df["GDP_B"] = df["GDP_B"] / 1e9
# #         return _enrich(df), "live"
# #     except Exception:
# #         if iso3 == "KEN":
# #             return _enrich(pd.DataFrame(KENYA_FALLBACK)), "cached"
# #         return None, "unavailable"

# # @st.cache_data(ttl=3600, show_spinner=False)
# # def fetch_primary_country(iso3: str):
# #     return fetch_single_country(iso3)

# # # ── Gemini AI helper ──────────────────────────────────────────────────────────
# # def build_data_summary(df, country_name, year_range):
# #     """Build a concise data summary string to pass to Gemini."""
# #     dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()
# #     latest = dff.iloc[-1]
# #     lines = [
# #         f"Country: {country_name}",
# #         f"Period: {year_range[0]}–{year_range[1]}",
# #         f"Latest Year: {int(latest['Year'])}",
# #         f"GDP: ${latest['GDP_B']:.1f}B (growth: {latest['GDP_Growth']:.1f}%)",
# #         f"Inflation: {latest['Inflation']:.1f}%",
# #         f"Unemployment: {latest['Unemployment']:.1f}%",
# #         f"Trade Balance: {latest['Trade_Balance']:.1f}% of GDP",
# #         "",
# #         "Year-by-year GDP growth (%):",
# #         ", ".join([f"{int(r.Year)}: {r.GDP_Growth:.1f}%" for _, r in dff.iterrows() if not pd.isna(r.GDP_Growth)]),
# #         "",
# #         "Year-by-year Inflation (%):",
# #         ", ".join([f"{int(r.Year)}: {r.Inflation:.1f}%" for _, r in dff.iterrows() if not pd.isna(r.Inflation)]),
# #         "",
# #         "Year-by-year Unemployment (%):",
# #         ", ".join([f"{int(r.Year)}: {r.Unemployment:.1f}%" for _, r in dff.iterrows() if not pd.isna(r.Unemployment)]),
# #         "",
# #         f"Avg GDP Growth: {dff['GDP_Growth'].mean():.1f}%",
# #         f"Peak Inflation: {dff['Inflation'].max():.1f}% in {int(dff.loc[dff['Inflation'].idxmax(), 'Year'])}",
# #         f"Lowest Unemployment: {dff['Unemployment'].min():.1f}% in {int(dff.loc[dff['Unemployment'].idxmin(), 'Year'])}",
# #     ]
# #     return "\n".join(lines)

# # def call_gemini(prompt: str, api_key: str) -> str:
# #     """Call Gemini Flash and return the text response."""
# #     try:
# #         import google.generativeai as genai
# #         genai.configure(api_key=api_key)
# #         model = genai.GenerativeModel("gemini-2.0-flash")
# #         response = model.generate_content(prompt)
# #         return response.text
# #     except ImportError:
# #         return "❌ google-generativeai not installed. Run: pip install google-generativeai"
# #     except Exception as e:
# #         return f"❌ Gemini error: {str(e)}"

# # # ── Sidebar ───────────────────────────────────────────────────────────────────
# # with st.sidebar:
# #     st.markdown("### 🌍 Africa Dashboard")
# #     st.markdown("---")

# #     st.markdown("**PRIMARY COUNTRY**")
# #     primary_code = st.selectbox(
# #         "Primary country",
# #         options=list(COUNTRY_OPTIONS.keys()),
# #         format_func=lambda c: COUNTRY_OPTIONS[c],
# #         index=list(COUNTRY_OPTIONS.keys()).index("KEN"),
# #         label_visibility="collapsed",
# #     )

# #     st.markdown("---")
# #     st.markdown("**TIME RANGE**")
# #     year_range = st.slider("Years", min_value=2000, max_value=2023,
# #                            value=(2005, 2023), label_visibility="collapsed")

# #     st.markdown("---")
# #     st.markdown("**INDICATORS**")
# #     show_gdp     = st.checkbox("GDP & Growth",        value=True)
# #     show_inf     = st.checkbox("Inflation",            value=True)
# #     show_unemp   = st.checkbox("Unemployment",         value=True)
# #     show_trade   = st.checkbox("Trade Balance",        value=True)
# #     show_scatter = st.checkbox("Correlation Analysis", value=True)
# #     show_stats   = st.checkbox("Statistical Summary",  value=True)

# #     st.markdown("---")
# #     st.markdown("**FORECASTING**")
# #     show_forecast  = st.checkbox("5-Year Forecast", value=True)
# #     forecast_years = st.slider("Horizon (years)", 1, 10, 5,
# #                                disabled=not show_forecast)
# #     forecast_model = st.radio("Model",
# #                               ["Linear", "Polynomial (deg 2)", "Polynomial (deg 3)"],
# #                               disabled=not show_forecast)

# #     st.markdown("---")
# #     st.markdown("**AI INSIGHTS**")
# #     gemini_key = st.text_input(
# #         "Gemini API Key",
# #         value=os.getenv("GEMINI_API_KEY", ""),
# #         type="password",
# #         placeholder="AIzaSy...",
# #         help="Get your free key at aistudio.google.com",
# #     )

# #     st.markdown("---")
# #     st.markdown("**DISPLAY**")
# #     highlight_covid = st.toggle("Highlight COVID period", value=True)

# #     st.markdown("---")
# #     st.markdown(
# #         f"<small style='color:#3a4f3d'>Source: World Bank Open Data<br>"
# #         f"54 African countries · {datetime.now().strftime('%d %b %Y')}</small>",
# #         unsafe_allow_html=True,
# #     )

# # # ── Load primary country ──────────────────────────────────────────────────────
# # with st.spinner(f"Loading data…"):
# #     df, data_source = fetch_primary_country(primary_code)

# # if df is None:
# #     st.error(f"Could not load data for {COUNTRY_OPTIONS[primary_code]}.")
# #     st.stop()

# # last_year    = int(df["Year"].max())
# # country_name = AFRICA_COUNTRIES[primary_code][0]
# # dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

# # # ── Header ────────────────────────────────────────────────────────────────────
# # st.markdown(
# #     f"<p class='section-label'>AFRICA ECONOMIC DASHBOARD · WORLD BANK · "
# #     f"{'LIVE' if data_source == 'live' else 'OFFLINE'}</p>",
# #     unsafe_allow_html=True,
# # )
# # col_h1, col_h2 = st.columns([3, 1])
# # with col_h1:
# #     st.title(f"{country_name} — Economic Analysis")
# #     st.markdown(f"**GDP · Inflation · Unemployment · Trade** &nbsp;·&nbsp; {year_range[0]}–{year_range[1]}")
# # with col_h2:
# #     badge = "badge-live" if data_source == "live" else "badge-cache"
# #     label = "🟢 LIVE" if data_source == "live" else "🟡 OFFLINE"
# #     st.markdown(f"<div style='padding-top:2rem'><span class='data-badge {badge}'>{label}</span></div>",
# #                 unsafe_allow_html=True)
# #     if st.button("🔄 Refresh"):
# #         st.cache_data.clear()
# #         st.rerun()

# # st.markdown("---")

# # # ── KPI Cards ─────────────────────────────────────────────────────────────────
# # latest = dff.iloc[-1]
# # prev   = dff.iloc[-2]
# # k1, k2, k3, k4 = st.columns(4)
# # k1.metric("GDP (Latest)",          f"${latest['GDP_B']:.1f}B",
# #           f"{latest['GDP_Growth']:+.1f}% growth")
# # k2.metric("Inflation",             f"{latest['Inflation']:.1f}%",
# #           f"{latest['Inflation']-prev['Inflation']:+.1f}pp vs prior year")
# # k3.metric("Unemployment",          f"{latest['Unemployment']:.1f}%",
# #           f"{latest['Unemployment']-prev['Unemployment']:+.1f}pp vs prior year")
# # k4.metric("Trade Balance (% GDP)", f"{latest['Trade_Balance']:.1f}%",
# #           f"{latest['Trade_Balance']-prev['Trade_Balance']:+.1f}pp vs prior year")

# # st.markdown("---")

# # # ── Tabs ──────────────────────────────────────────────────────────────────────
# # tabs = st.tabs([
# #     "📈 GDP", "🔥 Inflation", "👷 Unemployment",
# #     "🌍 Trade", "🔗 Correlations", "🔮 Forecast",
# #     "🗺️ Compare", "🤖 AI Insights", "📊 Statistics",
# # ])

# # # ── Shared helpers ────────────────────────────────────────────────────────────
# # def add_covid_band(fig):
# #     if highlight_covid:
# #         fig.add_vrect(
# #             x0=2019.5, x1=2021.5,
# #             fillcolor="rgba(232,93,74,0.08)",
# #             line=dict(color="rgba(232,93,74,0.3)", width=1, dash="dot"),
# #             annotation_text="COVID", annotation_position="top left",
# #             annotation_font=dict(color=COLORS["red"], size=10),
# #         )
# #     return fig

# # def run_forecast(years, values, horizon, model_name):
# #     X = np.array(years).reshape(-1, 1)
# #     y = np.array(values)
# #     if model_name == "Linear":
# #         model = LinearRegression()
# #     elif model_name == "Polynomial (deg 2)":
# #         model = make_pipeline(PolynomialFeatures(2), LinearRegression())
# #     else:
# #         model = make_pipeline(PolynomialFeatures(3), LinearRegression())
# #     model.fit(X, y)
# #     future = np.arange(years[-1] + 1, years[-1] + horizon + 1)
# #     pred   = model.predict(future.reshape(-1, 1))
# #     ci     = 1.96 * np.std(y - model.predict(X)) * np.sqrt(1 + 1 / len(y))
# #     return future.tolist(), pred.tolist(), (pred - ci).tolist(), (pred + ci).tolist()

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 1 — GDP
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[0]:
# #     if show_gdp:
# #         st.subheader(f"GDP — {country_name}")
# #         fig = make_subplots(specs=[[{"secondary_y": True}]])
# #         fig.add_trace(go.Bar(
# #             x=dff["Year"], y=dff["GDP_B"], name="GDP (USD B)",
# #             marker=dict(color=COLORS["green"], opacity=0.22,
# #                         line=dict(color=COLORS["green"], width=1)),
# #         ), secondary_y=False)
# #         fig.add_trace(go.Scatter(
# #             x=dff["Year"], y=dff["GDP_Growth"], name="GDP Growth %",
# #             line=dict(color=COLORS["green"], width=2.5),
# #             mode="lines+markers", marker=dict(size=5),
# #         ), secondary_y=True)
# #         fig.update_layout(**layout(height=380), title="")
# #         fig.update_yaxes(title_text="GDP (USD B)", secondary_y=False,
# #                          tickprefix="$", ticksuffix="B",
# #                          gridcolor=COLORS["border"], linecolor=COLORS["border"])
# #         fig.update_yaxes(title_text="Growth %", secondary_y=True,
# #                          ticksuffix="%", gridcolor="rgba(0,0,0,0)")
# #         fig.update_xaxes(gridcolor=COLORS["border"])
# #         add_covid_band(fig)
# #         st.plotly_chart(fig, use_container_width=True)

# #         c1, c2 = st.columns(2)
# #         with c1:
# #             dc = dff.copy(); dc["GDP_Change"] = dc["GDP_B"].diff()
# #             fig2 = go.Figure(go.Bar(
# #                 x=dc["Year"][1:], y=dc["GDP_Change"][1:],
# #                 marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# #                               for v in dc["GDP_Change"][1:]],
# #                 text=[f"${v:+.1f}B" for v in dc["GDP_Change"][1:]],
# #                 textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# #             ))
# #             fig2.update_layout(**layout(height=280,
# #                                yaxis_extra=dict(tickprefix="$", ticksuffix="B")))
# #             add_covid_band(fig2)
# #             st.plotly_chart(fig2, use_container_width=True)
# #         with c2:
# #             era_avg = df.groupby("Era")["GDP_Growth"].mean().reset_index()
# #             fig3 = go.Figure(go.Bar(
# #                 x=era_avg["Era"], y=era_avg["GDP_Growth"],
# #                 marker_color=[COLORS["blue"],COLORS["red"],COLORS["green"],COLORS["yellow"]],
# #                 text=[f"{v:.1f}%" for v in era_avg["GDP_Growth"]],
# #                 textposition="outside", textfont=dict(size=10, color=COLORS["text"]),
# #             ))
# #             fig3.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
# #             st.plotly_chart(fig3, use_container_width=True)

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 2 — Inflation
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[1]:
# #     if show_inf:
# #         st.subheader(f"Inflation — {country_name}")
# #         fig = go.Figure()
# #         fig.add_trace(go.Scatter(
# #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# #             y=[7.5]*len(dff) + [2.5]*len(dff),
# #             fill="toself", fillcolor="rgba(61,220,110,0.06)",
# #             line=dict(color="rgba(0,0,0,0)"), name="Target Band (2.5–7.5%)",
# #         ))
# #         fig.add_hline(y=7.5, line=dict(color=COLORS["red"], dash="dot", width=1),
# #                       annotation_text="Upper 7.5%",
# #                       annotation_font=dict(color=COLORS["red"], size=10))
# #         fig.add_hline(y=2.5, line=dict(color=COLORS["green"], dash="dot", width=1),
# #                       annotation_text="Lower 2.5%",
# #                       annotation_font=dict(color=COLORS["green"], size=10))
# #         fig.add_trace(go.Scatter(
# #             x=dff["Year"], y=dff["Inflation"], name="CPI Inflation",
# #             line=dict(color=COLORS["yellow"], width=2.5), mode="lines+markers",
# #             marker=dict(size=5, color=[
# #                 COLORS["red"] if v > 7.5 else
# #                 (COLORS["green"] if v < 2.5 else COLORS["yellow"])
# #                 for v in dff["Inflation"]
# #             ]),
# #             fill="tozeroy", fillcolor="rgba(245,200,66,0.07)",
# #         ))
# #         fig.update_layout(**layout(height=380,
# #                           yaxis_extra=dict(ticksuffix="%", title="CPI %")))
# #         add_covid_band(fig)
# #         st.plotly_chart(fig, use_container_width=True)

# #         c1, c2 = st.columns(2)
# #         with c1:
# #             above  = (dff["Inflation"] > 7.5).sum()
# #             within = ((dff["Inflation"] >= 2.5) & (dff["Inflation"] <= 7.5)).sum()
# #             below  = (dff["Inflation"] < 2.5).sum()
# #             fig2 = go.Figure(go.Pie(
# #                 labels=["Above target","Within target","Below target"],
# #                 values=[above, within, below], hole=0.55,
# #                 marker=dict(colors=[COLORS["red"],COLORS["green"],COLORS["blue"]]),
# #                 textfont=dict(color=COLORS["text"]),
# #             ))
# #             fig2.update_layout(**layout(height=280),
# #                                title=dict(text="Years Within Target Band",
# #                                           font=dict(color=COLORS["text"])))
# #             st.plotly_chart(fig2, use_container_width=True)
# #         with c2:
# #             fig3 = go.Figure(go.Histogram(
# #                 x=dff["Inflation"], nbinsx=10,
# #                 marker=dict(color=COLORS["yellow"], opacity=0.7,
# #                             line=dict(color=COLORS["bg"], width=1)),
# #             ))
# #             fig3.add_vline(x=dff["Inflation"].mean(),
# #                            line=dict(color=COLORS["text"], dash="dash", width=1.5),
# #                            annotation_text=f"Mean: {dff['Inflation'].mean():.1f}%",
# #                            annotation_font=dict(color=COLORS["text"], size=10))
# #             fig3.update_layout(**layout(height=280,
# #                                xaxis_extra=dict(title="Inflation %"),
# #                                yaxis_extra=dict(title="Count")))
# #             st.plotly_chart(fig3, use_container_width=True)

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 3 — Unemployment
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[2]:
# #     if show_unemp:
# #         st.subheader(f"Unemployment — {country_name}")
# #         fig = go.Figure()
# #         fig.add_trace(go.Scatter(
# #             x=dff["Year"], y=dff["Unemployment"], name="Unemployment %",
# #             line=dict(color=COLORS["red"], width=2.5), mode="lines+markers",
# #             marker=dict(size=6), fill="tozeroy", fillcolor="rgba(232,93,74,0.1)",
# #         ))
# #         dc2 = dff.copy()
# #         dc2["MA3"] = dc2["Unemployment"].rolling(3, center=True).mean()
# #         fig.add_trace(go.Scatter(
# #             x=dc2["Year"], y=dc2["MA3"], name="3-Year Rolling Avg",
# #             line=dict(color=COLORS["text"], width=1.5, dash="dot"), mode="lines",
# #         ))
# #         fig.update_layout(**layout(height=360,
# #                           yaxis_extra=dict(ticksuffix="%", title="Unemployment %")))
# #         add_covid_band(fig)
# #         st.plotly_chart(fig, use_container_width=True)

# #         c1, c2, c3 = st.columns(3)
# #         c1.metric("Peak",    f"{dff['Unemployment'].max():.1f}%",
# #                   f"in {int(dff.loc[dff['Unemployment'].idxmax(),'Year'])}")
# #         c2.metric("Lowest",  f"{dff['Unemployment'].min():.1f}%",
# #                   f"in {int(dff.loc[dff['Unemployment'].idxmin(),'Year'])}")
# #         c3.metric("Average", f"{dff['Unemployment'].mean():.1f}%", "ILO modeled")

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 4 — Trade
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[3]:
# #     if show_trade:
# #         st.subheader(f"Trade Balance — {country_name}")
# #         fig = go.Figure()
# #         fig.add_trace(go.Scatter(
# #             x=dff["Year"], y=dff["Exports_GDP"], name="Exports % GDP",
# #             line=dict(color=COLORS["blue"], width=2.5),
# #             mode="lines+markers", marker=dict(size=4),
# #         ))
# #         fig.add_trace(go.Scatter(
# #             x=dff["Year"], y=dff["Imports_GDP"], name="Imports % GDP",
# #             line=dict(color=COLORS["yellow"], width=2.5),
# #             mode="lines+markers", marker=dict(size=4),
# #         ))
# #         fig.add_trace(go.Scatter(
# #             x=list(dff["Year"]) + list(dff["Year"])[::-1],
# #             y=list(dff["Imports_GDP"]) + list(dff["Exports_GDP"])[::-1],
# #             fill="toself", fillcolor="rgba(232,93,74,0.08)",
# #             line=dict(color="rgba(0,0,0,0)"), name="Trade Deficit",
# #         ))
# #         fig.update_layout(**layout(height=360,
# #                           yaxis_extra=dict(ticksuffix="%", title="% of GDP")))
# #         add_covid_band(fig)
# #         st.plotly_chart(fig, use_container_width=True)

# #         fig2 = go.Figure(go.Bar(
# #             x=dff["Year"], y=dff["Trade_Balance"],
# #             marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
# #                           for v in dff["Trade_Balance"]],
# #             text=[f"{v:.1f}%" for v in dff["Trade_Balance"]],
# #             textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
# #         ))
# #         fig2.add_hline(y=0, line=dict(color=COLORS["muted"], width=1))
# #         fig2.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
# #         add_covid_band(fig2)
# #         st.plotly_chart(fig2, use_container_width=True)

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 5 — Correlations
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[4]:
# #     if show_scatter:
# #         st.subheader(f"Correlation Analysis — {country_name}")
# #         c1, c2 = st.columns(2)
# #         with c1:
# #             sl, ic, r, p, _ = stats.linregress(dff["GDP_Growth"], dff["Unemployment"])
# #             tx = np.linspace(dff["GDP_Growth"].min(), dff["GDP_Growth"].max(), 100)
# #             fig = go.Figure()
# #             fig.add_trace(go.Scatter(
# #                 x=dff["GDP_Growth"], y=dff["Unemployment"],
# #                 mode="markers+text", text=dff["Year"],
# #                 textposition="top center",
# #                 textfont=dict(size=9, color=COLORS["muted"]),
# #                 marker=dict(size=10, color=dff["Year"],
# #                             colorscale=[[0,COLORS["blue"]],[0.86,COLORS["red"]],[1,COLORS["green"]]],
# #                             showscale=True,
# #                             colorbar=dict(title="Year", tickfont=dict(color=COLORS["muted"]))),
# #                 name="Observations",
# #             ))
# #             fig.add_trace(go.Scatter(
# #                 x=tx, y=sl*tx+ic, mode="lines",
# #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# #                 name=f"Trend (R²={r**2:.2f})",
# #             ))
# #             fig.update_layout(**layout(height=360,
# #                               xaxis_extra=dict(title="GDP Growth %", ticksuffix="%"),
# #                               yaxis_extra=dict(title="Unemployment %", ticksuffix="%")))
# #             st.plotly_chart(fig, use_container_width=True)
# #             st.caption(f"Pearson r = {r:.3f} | R² = {r**2:.3f} | p = {p:.4f}")

# #         with c2:
# #             sl2, ic2, r2, p2, _ = stats.linregress(dff["Inflation"], dff["GDP_Growth"])
# #             tx2 = np.linspace(dff["Inflation"].min(), dff["Inflation"].max(), 100)
# #             fig2 = go.Figure()
# #             fig2.add_trace(go.Scatter(
# #                 x=dff["Inflation"], y=dff["GDP_Growth"],
# #                 mode="markers+text", text=dff["Year"],
# #                 textposition="top center",
# #                 textfont=dict(size=9, color=COLORS["muted"]),
# #                 marker=dict(size=10, color=COLORS["yellow"], opacity=0.8),
# #                 name="Observations",
# #             ))
# #             fig2.add_trace(go.Scatter(
# #                 x=tx2, y=sl2*tx2+ic2, mode="lines",
# #                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
# #                 name=f"Trend (R²={r2**2:.2f})",
# #             ))
# #             fig2.update_layout(**layout(height=360,
# #                                xaxis_extra=dict(title="Inflation %", ticksuffix="%"),
# #                                yaxis_extra=dict(title="GDP Growth %", ticksuffix="%")))
# #             st.plotly_chart(fig2, use_container_width=True)
# #             st.caption(f"Pearson r = {r2:.3f} | R² = {r2**2:.3f} | p = {p2:.4f}")

# #         corr_cols   = ["GDP_B","GDP_Growth","Inflation","Unemployment",
# #                        "Exports_GDP","Imports_GDP","Trade_Balance"]
# #         corr_labels = ["GDP (B)","GDP Growth","Inflation","Unemployment",
# #                        "Exports","Imports","Trade Bal."]
# #         corr = dff[corr_cols].corr().values
# #         fig3 = go.Figure(go.Heatmap(
# #             z=corr, x=corr_labels, y=corr_labels,
# #             colorscale=[[0,COLORS["red"]],[0.5,COLORS["surface"]],[1,COLORS["green"]]],
# #             zmid=0, zmin=-1, zmax=1,
# #             text=[[f"{v:.2f}" for v in row] for row in corr],
# #             texttemplate="%{text}", textfont=dict(size=11, color=COLORS["text"]),
# #         ))
# #         fig3.update_layout(**layout(height=380))
# #         st.plotly_chart(fig3, use_container_width=True)

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 6 — Forecast
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[5]:
# #     if show_forecast:
# #         st.subheader(f"Forecast — {country_name} · {last_year+1}–{last_year+forecast_years}")
# #         st.caption(f"Model: **{forecast_model}** | Trained on {year_range[0]}–{last_year} | Shaded = 95% CI")

# #         train = df[(df["Year"] >= year_range[0]) & (df["Year"] <= last_year)].dropna()
# #         indicators = [
# #             ("GDP_Growth",   "GDP Growth %",     COLORS["green"],  "%",  ""),
# #             ("GDP_B",        "GDP (USD Billion)", COLORS["green"],  "B",  "$"),
# #             ("Inflation",    "Inflation %",       COLORS["yellow"], "%",  ""),
# #             ("Unemployment", "Unemployment %",    COLORS["red"],    "%",  ""),
# #         ]
# #         fc1, fc2 = st.columns(2)
# #         forecast_results = {}

# #         for i, (col, label, color, unit, prefix) in enumerate(indicators):
# #             valid = train[["Year", col]].dropna()
# #             if len(valid) < 3:
# #                 continue
# #             fut_yrs, pred, lo, hi = run_forecast(
# #                 valid["Year"].tolist(), valid[col].tolist(),
# #                 forecast_years, forecast_model,
# #             )
# #             forecast_results[col] = {"years": fut_yrs, "pred": pred}
# #             rh = int(color[1:3],16); rg = int(color[3:5],16); rb = int(color[5:7],16)

# #             fig = go.Figure()
# #             fig.add_trace(go.Scatter(
# #                 x=valid["Year"], y=valid[col], name="Historical",
# #                 line=dict(color=color, width=2.5), mode="lines+markers",
# #                 marker=dict(size=4),
# #             ))
# #             fig.add_trace(go.Scatter(
# #                 x=fut_yrs + fut_yrs[::-1], y=hi + lo[::-1],
# #                 fill="toself", fillcolor=f"rgba({rh},{rg},{rb},0.12)",
# #                 line=dict(color="rgba(0,0,0,0)"), name="95% CI",
# #             ))
# #             fig.add_trace(go.Scatter(
# #                 x=fut_yrs, y=pred, name="Forecast",
# #                 line=dict(color=color, width=2, dash="dash"),
# #                 mode="lines+markers", marker=dict(size=6, symbol="diamond"),
# #             ))
# #             fig.add_vline(x=last_year + 0.5,
# #                           line=dict(color=COLORS["muted"], dash="dot", width=1),
# #                           annotation_text="Forecast →",
# #                           annotation_font=dict(color=COLORS["muted"], size=9))
# #             add_covid_band(fig)
# #             fig.update_layout(**layout(height=300,
# #                               yaxis_extra=dict(title=label,
# #                                                ticksuffix="" if unit=="B" else unit,
# #                                                tickprefix=prefix)))
# #             with (fc1 if i % 2 == 0 else fc2):
# #                 st.plotly_chart(fig, use_container_width=True)

# #         if forecast_results:
# #             st.markdown("---")
# #             st.markdown("**📋 Forecast Summary**")
# #             rows = []
# #             ref = list(forecast_results.keys())[0]
# #             lbl_map = {"GDP_Growth":"GDP Growth %","GDP_B":"GDP (USD B)",
# #                        "Inflation":"Inflation %","Unemployment":"Unemployment %"}
# #             for idx, yr in enumerate(forecast_results[ref]["years"]):
# #                 row = {"Year": yr}
# #                 for col, res in forecast_results.items():
# #                     fmt = f"${res['pred'][idx]:.1f}B" if col=="GDP_B" else f"{res['pred'][idx]:.1f}%"
# #                     row[lbl_map.get(col, col)] = fmt
# #                 rows.append(row)
# #             st.dataframe(pd.DataFrame(rows).set_index("Year"), use_container_width=True)
# #     else:
# #         st.info("Enable **5-Year Forecast** in the sidebar.")

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 7 — Country Comparison
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[6]:
# #     st.subheader("🗺️ Country Comparison — All 54 African Nations")
# #     st.caption("🟢 = full data · 🟡 = partial · 🔴 = sparse")

# #     cc1, cc2, cc3 = st.columns([2, 1, 1])
# #     with cc1:
# #         compare_codes = st.multiselect(
# #             "Select countries (up to 5)",
# #             options=list(COUNTRY_OPTIONS.keys()),
# #             default=["KEN","NGA","ZAF","ETH","GHA"],
# #             format_func=lambda c: COUNTRY_OPTIONS[c],
# #             max_selections=5,
# #         )
# #     with cc2:
# #         compare_indicator = st.selectbox(
# #             "Indicator",
# #             options=["GDP_Growth","GDP_B","Inflation","Unemployment",
# #                      "Exports_GDP","Imports_GDP","Trade_Balance"],
# #             format_func=lambda x: {
# #                 "GDP_Growth":"GDP Growth %","GDP_B":"GDP (USD B)",
# #                 "Inflation":"Inflation %","Unemployment":"Unemployment %",
# #                 "Exports_GDP":"Exports % GDP","Imports_GDP":"Imports % GDP",
# #                 "Trade_Balance":"Trade Balance % GDP",
# #             }[x],
# #         )
# #     with cc3:
# #         compare_range = st.slider("Year range", 2000, 2023, (2005, 2023), key="cmp_range")

# #     if not compare_codes:
# #         st.info("Select at least one country above.")
# #     else:
# #         country_data = {}
# #         load_errors  = []
# #         progress = st.progress(0, text="Loading…")
# #         for i, code in enumerate(compare_codes):
# #             progress.progress((i+1)/len(compare_codes),
# #                               text=f"Loading {AFRICA_COUNTRIES[code][0]}…")
# #             cdf, _ = fetch_single_country(code)
# #             if cdf is not None:
# #                 country_data[code] = cdf
# #             else:
# #                 load_errors.append(AFRICA_COUNTRIES[code][0])
# #         progress.empty()

# #         if load_errors:
# #             st.warning(f"Could not load: {', '.join(load_errors)}")

# #         if country_data:
# #             ind_labels = {
# #                 "GDP_Growth":    ("GDP Growth %",       "%", ""),
# #                 "GDP_B":         ("GDP (USD Billion)",  "B", "$"),
# #                 "Inflation":     ("Inflation %",        "%", ""),
# #                 "Unemployment":  ("Unemployment %",     "%", ""),
# #                 "Exports_GDP":   ("Exports % of GDP",   "%", ""),
# #                 "Imports_GDP":   ("Imports % of GDP",   "%", ""),
# #                 "Trade_Balance": ("Trade Balance % GDP","%", ""),
# #             }
# #             ind_label, ind_unit, ind_prefix = ind_labels[compare_indicator]
# #             tick_suffix = "" if ind_unit == "B" else ind_unit

# #             # Line chart
# #             st.markdown(f"### {ind_label} — Over Time")
# #             fig = go.Figure()
# #             for idx, (code, cdf) in enumerate(country_data.items()):
# #                 cdf_f = cdf[(cdf["Year"] >= compare_range[0]) &
# #                             (cdf["Year"] <= compare_range[1])].dropna(subset=[compare_indicator])
# #                 if cdf_f.empty:
# #                     continue
# #                 color = COUNTRY_PALETTE[idx % len(COUNTRY_PALETTE)]
# #                 name  = AFRICA_COUNTRIES[code][0]
# #                 fig.add_trace(go.Scatter(
# #                     x=cdf_f["Year"], y=cdf_f[compare_indicator], name=name,
# #                     line=dict(color=color, width=2.5), mode="lines+markers",
# #                     marker=dict(size=5),
# #                     hovertemplate=f"<b>{name}</b><br>Year: %{{x}}<br>{ind_label}: %{{y:.1f}}<extra></extra>",
# #                 ))
# #             fig.update_layout(**layout(height=420,
# #                               yaxis_extra=dict(title=ind_label,
# #                                                ticksuffix=tick_suffix, tickprefix=ind_prefix)))
# #             if highlight_covid:
# #                 add_covid_band(fig)
# #             st.plotly_chart(fig, use_container_width=True)

# #             # Bar chart — latest values
# #             st.markdown(f"### Latest Value — {ind_label}")
# #             bar_data = []
# #             for code, cdf in country_data.items():
# #                 valid = cdf.dropna(subset=[compare_indicator])
# #                 if not valid.empty:
# #                     bar_data.append({
# #                         "Country": AFRICA_COUNTRIES[code][0],
# #                         "Value":   valid.iloc[-1][compare_indicator],
# #                         "Year":    int(valid.iloc[-1]["Year"]),
# #                     })
# #             if bar_data:
# #                 bar_df = pd.DataFrame(bar_data).sort_values("Value", ascending=True)
# #                 fig_bar = go.Figure(go.Bar(
# #                     x=bar_df["Value"], y=bar_df["Country"], orientation="h",
# #                     marker=dict(
# #                         color=bar_df["Value"],
# #                         colorscale=[[0,COLORS["red"]],[0.5,COLORS["yellow"]],[1,COLORS["green"]]],
# #                         showscale=True,
# #                         colorbar=dict(title=ind_label, tickfont=dict(color=COLORS["muted"])),
# #                     ),
# #                     text=[f"{v:.1f}{ind_unit if ind_unit!='B' else 'B'} ({y})"
# #                           for v, y in zip(bar_df["Value"], bar_df["Year"])],
# #                     textposition="outside",
# #                     textfont=dict(size=10, color=COLORS["text"]),
# #                 ))
# #                 fig_bar.update_layout(**layout(
# #                     height=max(250, len(bar_data)*55),
# #                     yaxis_extra=dict(title=""),
# #                     xaxis_extra=dict(title=ind_label,
# #                                      ticksuffix=tick_suffix, tickprefix=ind_prefix),
# #                 ))
# #                 st.plotly_chart(fig_bar, use_container_width=True)

# #             # Summary table
# #             st.markdown("### 📋 All Indicators — Latest Values")
# #             table_rows = []
# #             for code, cdf in country_data.items():
# #                 row = {"Country": AFRICA_COUNTRIES[code][0], "Quality": AFRICA_COUNTRIES[code][1]}
# #                 for ind, (lbl, unit, pfx) in ind_labels.items():
# #                     valid = cdf.dropna(subset=[ind])
# #                     if not valid.empty:
# #                         v  = valid.iloc[-1][ind]
# #                         yr = int(valid.iloc[-1]["Year"])
# #                         row[lbl] = f"{pfx}{v:.1f}{unit if unit!='B' else 'B'} ({yr})"
# #                     else:
# #                         row[lbl] = "—"
# #                 table_rows.append(row)
# #             st.dataframe(pd.DataFrame(table_rows).set_index("Country"), use_container_width=True)

# #             # Download
# #             all_frames = []
# #             for code, cdf in country_data.items():
# #                 tmp = cdf.copy()
# #                 tmp.insert(0, "Country", AFRICA_COUNTRIES[code][0])
# #                 tmp.insert(1, "ISO3", code)
# #                 all_frames.append(tmp)
# #             combined = pd.concat(all_frames, ignore_index=True)
# #             st.download_button("⬇️ Download Comparison CSV",
# #                                data=combined.to_csv(index=False).encode("utf-8"),
# #                                file_name="africa_comparison.csv", mime="text/csv")

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 8 — AI INSIGHTS  ✨ NEW
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[7]:
# #     st.subheader(f"🤖 AI Insights — {country_name}")
# #     st.caption("Powered by Google Gemini · Reads your actual loaded data, not hardcoded text")

# #     if not gemini_key:
# #         st.warning(
# #             "**Add your Gemini API key to enable AI Insights.**\n\n"
# #             "1. Go to [aistudio.google.com](https://aistudio.google.com) → Get API Key\n"
# #             "2. Paste it into the **AI Insights** field in the sidebar\n"
# #             "3. Or add `GEMINI_API_KEY=your_key` to your `.env` file"
# #         )
# #     else:
# #         # Build the data context once
# #         data_summary = build_data_summary(df, country_name, year_range)

# #         # ── Preset analysis buttons ───────────────────────────────────────
# #         st.markdown("**Quick Analysis — click any button to generate:**")

# #         PRESETS = {
# #             "📊 Full Economic Overview": (
# #                 f"You are an expert economist specializing in African economies. "
# #                 f"Analyze the following economic data for {country_name} and write a "
# #                 f"comprehensive 4-paragraph economic overview. Cover: (1) GDP growth trajectory "
# #                 f"and key turning points, (2) inflation patterns and monetary policy implications, "
# #                 f"(3) unemployment trends and labor market dynamics, (4) trade balance and "
# #                 f"structural economic challenges. Be specific — reference actual numbers from the data.\n\n"
# #                 f"DATA:\n{data_summary}"
# #             ),
# #             "📉 COVID Impact Analysis": (
# #                 f"Analyze the specific economic impact of COVID-19 (2020–2021) on {country_name} "
# #                 f"based on this data. Compare pre-COVID averages (2015–2019) to COVID years and "
# #                 f"the recovery period (2022–2023). Quantify the damage and recovery across all "
# #                 f"indicators. Write 3 focused paragraphs.\n\nDATA:\n{data_summary}"
# #             ),
# #             "🔮 Outlook & Risks": (
# #                 f"Based on the historical economic trends for {country_name}, write a forward-looking "
# #                 f"assessment covering: (1) what the data suggests about growth momentum, "
# #                 f"(2) the biggest economic risks and vulnerabilities, (3) structural opportunities "
# #                 f"for the economy. Ground every point in the actual data provided.\n\nDATA:\n{data_summary}"
# #             ),
# #             "🌍 Regional Context": (
# #                 f"Place {country_name}'s economic performance in the context of sub-Saharan Africa. "
# #                 f"Based on this data, assess whether the country is an outperformer, average, or "
# #                 f"underperformer relative to typical African economies. Discuss inflation management, "
# #                 f"growth consistency, and trade dynamics. Write 3 concise paragraphs.\n\nDATA:\n{data_summary}"
# #             ),
# #             "📈 Best & Worst Years": (
# #                 f"From the data provided for {country_name}, identify and explain the 3 best and "
# #                 f"3 worst economic years. For each year, explain what likely caused the performance "
# #                 f"based on the indicators. Reference specific numbers. Write in a clear analytical style.\n\nDATA:\n{data_summary}"
# #             ),
# #         }

# #         cols = st.columns(3)
# #         for i, (btn_label, _) in enumerate(PRESETS.items()):
# #             with cols[i % 3]:
# #                 if st.button(btn_label, use_container_width=True):
# #                     st.session_state["ai_prompt"]   = PRESETS[btn_label]
# #                     st.session_state["ai_btn_label"] = btn_label

# #         st.markdown("---")

# #         # ── Custom question ───────────────────────────────────────────────
# #         st.markdown("**Or ask a custom question:**")
# #         custom_q = st.text_area(
# #             "Your question",
# #             placeholder=f"e.g. Why did inflation spike so high in {country_name}? "
# #                         f"What does the trade deficit mean for economic growth?",
# #             height=80,
# #             label_visibility="collapsed",
# #         )
# #         if st.button("🔍 Ask Gemini", use_container_width=False):
# #             if custom_q.strip():
# #                 full_prompt = (
# #                     f"You are an expert economist. Answer the following question about "
# #                     f"{country_name} using the data provided. Be specific and reference "
# #                     f"actual numbers.\n\nQUESTION: {custom_q}\n\nDATA:\n{data_summary}"
# #                 )
# #                 st.session_state["ai_prompt"]   = full_prompt
# #                 st.session_state["ai_btn_label"] = f"❓ {custom_q[:60]}…"

# #         # ── Run Gemini and show response ──────────────────────────────────
# #         if "ai_prompt" in st.session_state:
# #             st.markdown("---")
# #             st.markdown(f"**{st.session_state.get('ai_btn_label', 'Analysis')}**")
# #             with st.spinner("Gemini is analyzing the data…"):
# #                 response = call_gemini(st.session_state["ai_prompt"], gemini_key)
# #             st.markdown(
# #                 f"<div class='ai-response'>{response}</div>",
# #                 unsafe_allow_html=True,
# #             )
# #             # Copy button
# #             st.download_button(
# #                 "⬇️ Download Analysis",
# #                 data=response.encode("utf-8"),
# #                 file_name=f"{primary_code}_ai_analysis.txt",
# #                 mime="text/plain",
# #             )
# #             if st.button("🗑️ Clear"):
# #                 del st.session_state["ai_prompt"]
# #                 del st.session_state["ai_btn_label"]
# #                 st.rerun()

# # # ═════════════════════════════════════════════════════════════════════════════
# # # TAB 9 — Statistics
# # # ═════════════════════════════════════════════════════════════════════════════
# # with tabs[8]:
# #     if show_stats:
# #         st.subheader(f"Statistical Summary — {country_name}")
# #         summary_cols = ["GDP_Growth","Inflation","Unemployment",
# #                         "Exports_GDP","Imports_GDP","Trade_Balance"]
# #         label_map = {
# #             "GDP_Growth":"GDP Growth %","Inflation":"Inflation %",
# #             "Unemployment":"Unemployment %","Exports_GDP":"Exports % GDP",
# #             "Imports_GDP":"Imports % GDP","Trade_Balance":"Trade Balance % GDP",
# #         }
# #         stats_df = dff[summary_cols].describe().T.round(2)
# #         stats_df.index = [label_map[i] for i in stats_df.index]
# #         stats_df.columns = ["Count","Mean","Std Dev","Min",
# #                             "25th %ile","Median","75th %ile","Max"]
# #         st.dataframe(
# #             stats_df.style.background_gradient(subset=["Mean"], cmap="RdYlGn", axis=0)
# #                           .format("{:.2f}"),
# #             use_container_width=True,
# #         )
# #         st.markdown("---")
# #         disp = dff[["Year","Era","GDP_B","GDP_Growth","Inflation",
# #                     "Unemployment","Exports_GDP","Imports_GDP","Trade_Balance"]].copy()
# #         disp.columns = ["Year","Era","GDP ($B)","GDP Growth %","Inflation %",
# #                         "Unemployment %","Exports % GDP","Imports % GDP","Trade Balance %"]
# #         st.dataframe(disp.set_index("Year"), use_container_width=True)
# #         st.download_button("⬇️ Download CSV",
# #                            data=disp.to_csv(index=False).encode("utf-8"),
# #                            file_name=f"{primary_code}_data.csv", mime="text/csv")

# # # ── Footer insights ───────────────────────────────────────────────────────────
# # st.markdown("---")
# # st.subheader("Key Insights")
# # c1, c2, c3 = st.columns(3)
# # with c1:
# #     st.markdown("""<div class='insight-box'>
# #         <h4>📈 Sustained Long-Term Growth</h4>
# #         <p>Many African economies have recorded GDP growth of 4–8% annually over two decades,
# #         outpacing global averages and demonstrating strong structural development.</p>
# #         </div>""", unsafe_allow_html=True)
# # with c2:
# #     st.markdown("""<div class='insight-box warn'>
# #         <h4>🔥 Inflation Pressures</h4>
# #         <p>Inflation remains a persistent challenge, amplified by global food and energy
# #         shocks in 2008 and 2022 and structural import dependency across the continent.</p>
# #         </div>""", unsafe_allow_html=True)
# # with c3:
# #     st.markdown("""<div class='insight-box danger'>
# #         <h4>🌍 Trade Imbalances</h4>
# #         <p>Most African economies run persistent trade deficits driven by fuel, machinery,
# #         and manufactured goods imports. Export diversification remains a key challenge.</p>
# #         </div>""", unsafe_allow_html=True)

# # st.markdown(
# #     "<br><small style='color:#3a4f3d'>Data: World Bank Open Data · IMF DataMapper · "
# #     "54 African countries · All indicators from official national statistics.</small>",
# #     unsafe_allow_html=True,
# # )

# """
# Africa Economic Intelligence Dashboard
# Streamlit + Plotly | All Upgrades:
#   - Live World Bank API (wbgapi) with offline fallback
#   - GDP Per Capita
#   - Public Debt
#   - Choropleth Map of Africa (indicator-selectable)
#   - Economic Ranking Table with Economic Health Score
#   - 5-Year Forecasting Panel
#   - Country Comparison — all 54 African countries
#   - AI Insights Tab — powered by Google Gemini
# Data source: World Bank Open Data
# """

# import os
# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# import plotly.express as px
# from plotly.subplots import make_subplots
# import numpy as np
# from scipy import stats
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.pipeline import make_pipeline
# from datetime import datetime

# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except ImportError:
#     pass

# # ── Page config ───────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Africa Economic Intelligence Dashboard",
#     page_icon="🌍",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ── CSS ───────────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
#     .stApp { background-color: #0a0f0d; }
#     .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
#     [data-testid="stSidebar"] { background-color: #111812; border-right: 1px solid #1e2e21; }
#     [data-testid="stSidebar"] * { color: #e8f0ea !important; }
#     [data-testid="metric-container"] {
#         background: #111812; border: 1px solid #1e2e21;
#         border-radius: 6px; padding: 1rem 1.2rem;
#     }
#     [data-testid="stMetricLabel"] { color: #6b7f6e !important; font-size: 0.75rem; }
#     [data-testid="stMetricValue"] { color: #e8f0ea !important; }
#     [data-testid="stMetricDelta"] { font-size: 0.8rem; }
#     h1, h2, h3 { color: #e8f0ea !important; }
#     p, li { color: #b0bfb3 !important; }
#     .stTabs [data-baseweb="tab-list"] { background-color: #111812; border-bottom: 1px solid #1e2e21; }
#     .stTabs [data-baseweb="tab"] { color: #6b7f6e; }
#     .stTabs [aria-selected="true"] { color: #3ddc6e !important; border-bottom-color: #3ddc6e !important; }
#     hr { border-color: #1e2e21; }
#     .stAlert { background-color: #111812; border-color: #1e2e21; }
#     .section-label {
#         font-family: monospace; font-size: 0.65rem; letter-spacing: 0.2em;
#         color: #3ddc6e; text-transform: uppercase; margin-bottom: 0.25rem;
#     }
#     .data-badge {
#         display: inline-block; font-family: monospace; font-size: 0.62rem;
#         letter-spacing: 0.1em; padding: 0.25rem 0.65rem;
#         border-radius: 2px; margin-bottom: 1rem;
#     }
#     .badge-live  { background: rgba(61,220,110,0.15); color: #3ddc6e; border: 1px solid #3ddc6e; }
#     .badge-cache { background: rgba(245,200,66,0.15); color: #f5c842; border: 1px solid #f5c842; }
#     .insight-box {
#         background: #111812; border: 1px solid #1e2e21;
#         border-left: 3px solid #3ddc6e; border-radius: 4px;
#         padding: 1rem 1.2rem; margin-bottom: 0.75rem;
#     }
#     .insight-box.warn   { border-left-color: #f5c842; }
#     .insight-box.danger { border-left-color: #e85d4a; }
#     .insight-box h4 { color: #e8f0ea !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
#     .insight-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
#     .forecast-box {
#         background: rgba(74,157,232,0.06); border: 1px solid rgba(74,157,232,0.25);
#         border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
#     }
#     .forecast-box h4 { color: #4a9de8 !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
#     .forecast-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
#     .compare-box {
#         background: rgba(167,139,250,0.06); border: 1px solid rgba(167,139,250,0.25);
#         border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
#     }
#     .compare-box h4 { color: #a78bfa !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
#     .compare-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
#     .ai-response {
#         background: #0d1a0f; border: 1px solid #1e2e21;
#         border-left: 3px solid #3ddc6e; border-radius: 4px;
#         padding: 1.4rem 1.6rem; margin-top: 1rem;
#         font-size: 0.88rem; line-height: 1.8; color: #c8d8cb !important;
#         white-space: pre-wrap;
#     }
#     .rank-gold   { color: #f5c842; font-weight: bold; }
#     .rank-silver { color: #c0c0c0; font-weight: bold; }
#     .rank-bronze { color: #cd7f32; font-weight: bold; }
#     .score-bar {
#         background: #1e2e21; border-radius: 3px; height: 8px; width: 100%;
#         margin-top: 4px;
#     }
#     .score-fill {
#         border-radius: 3px; height: 8px;
#         background: linear-gradient(90deg, #e85d4a, #f5c842, #3ddc6e);
#     }
# </style>
# """, unsafe_allow_html=True)

# # ── Colors & layout ───────────────────────────────────────────────────────────
# COLORS = {
#     "bg": "#0a0f0d", "surface": "#111812", "border": "#1e2e21",
#     "green": "#3ddc6e", "yellow": "#f5c842", "red": "#e85d4a",
#     "blue": "#4a9de8", "purple": "#a78bfa", "muted": "#6b7f6e", "text": "#e8f0ea",
# }
# COUNTRY_PALETTE = [
#     "#3ddc6e","#4a9de8","#f5c842","#e85d4a","#a78bfa",
#     "#f97316","#06b6d4","#ec4899","#84cc16","#fb923c",
# ]
# GRID = dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], tickcolor=COLORS["border"])

# def layout(height=360, xaxis_extra=None, yaxis_extra=None, **kwargs):
#     return dict(
#         paper_bgcolor=COLORS["surface"], plot_bgcolor=COLORS["bg"],
#         font=dict(family="DM Mono, monospace", color=COLORS["muted"], size=11),
#         xaxis={**GRID, **(xaxis_extra or {})},
#         yaxis={**GRID, **(yaxis_extra or {})},
#         margin=dict(t=40, b=40, l=55, r=20),
#         legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
#         height=height, **kwargs,
#     )

# # ── All 54 African countries ──────────────────────────────────────────────────
# AFRICA_COUNTRIES = {
#     "DZA": ("Algeria",              "🇩🇿", "🟢"),
#     "AGO": ("Angola",               "🇦🇴", "🟡"),
#     "BEN": ("Benin",                "🇧🇯", "🟡"),
#     "BWA": ("Botswana",             "🇧🇼", "🟢"),
#     "BFA": ("Burkina Faso",         "🇧🇫", "🟡"),
#     "BDI": ("Burundi",              "🇧🇮", "🟡"),
#     "CPV": ("Cabo Verde",           "🇨🇻", "🟡"),
#     "CMR": ("Cameroon",             "🇨🇲", "🟢"),
#     "CAF": ("Central African Rep.", "🇨🇫", "🔴"),
#     "TCD": ("Chad",                 "🇹🇩", "🟡"),
#     "COM": ("Comoros",              "🇰🇲", "🔴"),
#     "COD": ("DR Congo",             "🇨🇩", "🟡"),
#     "COG": ("Republic of Congo",    "🇨🇬", "🟡"),
#     "CIV": ("Côte d'Ivoire",        "🇨🇮", "🟢"),
#     "DJI": ("Djibouti",             "🇩🇯", "🟡"),
#     "EGY": ("Egypt",                "🇪🇬", "🟢"),
#     "GNQ": ("Equatorial Guinea",    "🇬🇶", "🟡"),
#     "ERI": ("Eritrea",              "🇪🇷", "🔴"),
#     "SWZ": ("Eswatini",             "🇸🇿", "🟡"),
#     "ETH": ("Ethiopia",             "🇪🇹", "🟢"),
#     "GAB": ("Gabon",                "🇬🇦", "🟡"),
#     "GMB": ("Gambia",               "🇬🇲", "🟡"),
#     "GHA": ("Ghana",                "🇬🇭", "🟢"),
#     "GIN": ("Guinea",               "🇬🇳", "🟡"),
#     "GNB": ("Guinea-Bissau",        "🇬🇼", "🔴"),
#     "KEN": ("Kenya",                "🇰🇪", "🟢"),
#     "LSO": ("Lesotho",              "🇱🇸", "🟡"),
#     "LBR": ("Liberia",              "🇱🇷", "🟡"),
#     "LBY": ("Libya",                "🇱🇾", "🔴"),
#     "MDG": ("Madagascar",           "🇲🇬", "🟡"),
#     "MWI": ("Malawi",               "🇲🇼", "🟡"),
#     "MLI": ("Mali",                 "🇲🇱", "🟡"),
#     "MRT": ("Mauritania",           "🇲🇷", "🟡"),
#     "MUS": ("Mauritius",            "🇲🇺", "🟢"),
#     "MAR": ("Morocco",              "🇲🇦", "🟢"),
#     "MOZ": ("Mozambique",           "🇲🇿", "🟡"),
#     "NAM": ("Namibia",              "🇳🇦", "🟢"),
#     "NER": ("Niger",                "🇳🇪", "🟡"),
#     "NGA": ("Nigeria",              "🇳🇬", "🟢"),
#     "RWA": ("Rwanda",               "🇷🇼", "🟢"),
#     "STP": ("São Tomé & Príncipe",  "🇸🇹", "🔴"),
#     "SEN": ("Senegal",              "🇸🇳", "🟢"),
#     "SLE": ("Sierra Leone",         "🇸🇱", "🟡"),
#     "SOM": ("Somalia",              "🇸🇴", "🔴"),
#     "ZAF": ("South Africa",         "🇿🇦", "🟢"),
#     "SSD": ("South Sudan",          "🇸🇸", "🔴"),
#     "SDN": ("Sudan",                "🇸🇩", "🔴"),
#     "TZA": ("Tanzania",             "🇹🇿", "🟢"),
#     "TGO": ("Togo",                 "🇹🇬", "🟡"),
#     "TUN": ("Tunisia",              "🇹🇳", "🟢"),
#     "UGA": ("Uganda",               "🇺🇬", "🟢"),
#     "ZMB": ("Zambia",               "🇿🇲", "🟢"),
#     "ZWE": ("Zimbabwe",             "🇿🇼", "🟡"),
#     "SYC": ("Seychelles",           "🇸🇨", "🟡"),
# }
# COUNTRY_OPTIONS = {
#     code: f"{info[2]} {info[1]} {info[0]}"
#     for code, info in sorted(AFRICA_COUNTRIES.items(), key=lambda x: x[1][0])
# }

# # ── World Bank indicators ─────────────────────────────────────────────────────
# WB_INDICATORS = {
#     "GDP_B":         "NY.GDP.MKTP.CD",
#     "GDP_Growth":    "NY.GDP.MKTP.KD.ZG",
#     "GDP_PerCapita": "NY.GDP.PCAP.CD",
#     "Inflation":     "FP.CPI.TOTL.ZG",
#     "Unemployment":  "SL.UEM.TOTL.ZS",
#     "Exports_GDP":   "NE.EXP.GNFS.ZS",
#     "Imports_GDP":   "NE.IMP.GNFS.ZS",
#     "Public_Debt":   "GC.DOD.TOTL.GD.ZS",
# }

# # ── Kenya fallback ────────────────────────────────────────────────────────────
# KENYA_FALLBACK = {
#     "Year":          list(range(2000, 2024)),
#     "GDP_B":         [12.7,13.3,13.4,14.0,15.1,18.7,22.5,27.2,30.6,29.5,
#                       32.2,34.0,41.1,47.6,60.9,63.4,70.5,79.3,87.8,95.5,
#                       98.8,99.2,110.4,107.9],
#     "GDP_Growth":    [0.6,4.5,0.3,2.9,4.6,5.9,6.5,6.9,1.5,2.7,
#                       8.4,6.1,4.6,5.9,5.4,5.7,5.9,4.9,6.3,5.4,
#                       -0.3,7.6,4.8,5.6],
#     "GDP_PerCapita": [381,394,393,404,426,515,604,713,780,738,
#                       789,816,972,1104,1378,1402,1517,1672,1818,1939,
#                       1965,1944,2121,2043],
#     "Inflation":     [10.0,5.8,2.0,9.8,11.6,10.3,6.0,4.3,26.2,10.5,
#                       4.0,14.0,9.4,5.7,6.9,6.6,6.3,8.0,4.7,5.2,
#                       5.3,6.1,9.1,6.3],
#     "Unemployment":  [9.8,9.8,9.8,9.8,9.8,9.3,8.7,8.1,7.4,6.7,
#                       6.1,5.5,4.9,4.4,3.9,3.5,2.8,3.5,4.3,5.0,
#                       5.6,5.7,5.7,5.6],
#     "Exports_GDP":   [25.2,24.8,23.6,23.0,24.0,23.8,23.0,24.5,24.1,20.4,
#                       21.2,21.0,19.5,18.3,16.9,15.7,14.6,13.8,13.9,13.5,
#                       12.4,13.5,14.2,13.8],
#     "Imports_GDP":   [33.1,32.5,31.6,30.5,32.0,31.8,33.0,37.2,42.4,36.3,
#                       36.1,40.0,38.5,37.3,34.5,32.5,30.6,29.8,31.9,29.5,
#                       26.7,28.0,32.6,31.2],
#     "Public_Debt":   [53.2,51.8,49.0,46.5,44.2,42.0,40.1,38.5,36.8,42.0,
#                       43.5,44.9,43.1,43.2,44.5,48.2,52.4,55.1,58.3,62.1,
#                       68.4,70.1,69.3,71.2],
# }

# # ── Static data for Africa map (latest values) ────────────────────────────────
# # Approximate latest values for choropleth (used when API unavailable)
# AFRICA_MAP_DATA = {
#     "DZA": {"GDP_Growth": 3.5, "Inflation": 9.3, "Unemployment": 11.7, "GDP_PerCapita": 3691, "Public_Debt": 57.8},
#     "AGO": {"GDP_Growth": 1.1, "Inflation": 13.2, "Unemployment": 7.7,  "GDP_PerCapita": 1987, "Public_Debt": 87.3},
#     "BEN": {"GDP_Growth": 6.0, "Inflation": 2.7,  "Unemployment": 1.4,  "GDP_PerCapita": 1321, "Public_Debt": 53.5},
#     "BWA": {"GDP_Growth": 5.5, "Inflation": 8.5,  "Unemployment": 17.6, "GDP_PerCapita": 7370, "Public_Debt": 20.1},
#     "BFA": {"GDP_Growth": 1.5, "Inflation": 14.1, "Unemployment": 4.9,  "GDP_PerCapita": 833,  "Public_Debt": 61.2},
#     "BDI": {"GDP_Growth": 1.8, "Inflation": 28.1, "Unemployment": 1.1,  "GDP_PerCapita": 265,  "Public_Debt": 68.3},
#     "CPV": {"GDP_Growth": 4.8, "Inflation": 7.1,  "Unemployment": 11.3, "GDP_PerCapita": 3861, "Public_Debt": 128.7},
#     "CMR": {"GDP_Growth": 3.8, "Inflation": 7.4,  "Unemployment": 3.6,  "GDP_PerCapita": 1620, "Public_Debt": 47.3},
#     "CAF": {"GDP_Growth": 1.0, "Inflation": 5.6,  "Unemployment": 6.8,  "GDP_PerCapita": 492,  "Public_Debt": 48.9},
#     "TCD": {"GDP_Growth": 3.3, "Inflation": 4.0,  "Unemployment": 1.7,  "GDP_PerCapita": 696,  "Public_Debt": 42.1},
#     "COM": {"GDP_Growth": 2.0, "Inflation": 11.1, "Unemployment": 4.0,  "GDP_PerCapita": 1387, "Public_Debt": 29.5},
#     "COD": {"GDP_Growth": 8.3, "Inflation": 18.2, "Unemployment": 4.5,  "GDP_PerCapita": 565,  "Public_Debt": 14.6},
#     "COG": {"GDP_Growth": 1.4, "Inflation": 3.0,  "Unemployment": 8.1,  "GDP_PerCapita": 2074, "Public_Debt": 93.5},
#     "CIV": {"GDP_Growth": 6.7, "Inflation": 4.2,  "Unemployment": 3.4,  "GDP_PerCapita": 2286, "Public_Debt": 56.8},
#     "DJI": {"GDP_Growth": 6.5, "Inflation": 4.0,  "Unemployment": 26.0, "GDP_PerCapita": 3460, "Public_Debt": 43.0},
#     "EGY": {"GDP_Growth": 3.8, "Inflation": 29.8, "Unemployment": 7.1,  "GDP_PerCapita": 3201, "Public_Debt": 95.8},
#     "GNQ": {"GDP_Growth":-5.0, "Inflation": 4.8,  "Unemployment": 8.6,  "GDP_PerCapita": 6732, "Public_Debt": 43.1},
#     "ERI": {"GDP_Growth": 2.9, "Inflation": 6.3,  "Unemployment": 5.8,  "GDP_PerCapita": 598,  "Public_Debt": 175.2},
#     "SWZ": {"GDP_Growth": 2.4, "Inflation": 4.8,  "Unemployment": 22.7, "GDP_PerCapita": 4156, "Public_Debt": 41.1},
#     "ETH": {"GDP_Growth": 6.1, "Inflation": 33.9, "Unemployment": 3.3,  "GDP_PerCapita": 925,  "Public_Debt": 55.0},
#     "GAB": {"GDP_Growth": 2.3, "Inflation": 3.4,  "Unemployment": 19.0, "GDP_PerCapita": 7562, "Public_Debt": 65.4},
#     "GMB": {"GDP_Growth": 4.3, "Inflation": 11.9, "Unemployment": 9.1,  "GDP_PerCapita": 756,  "Public_Debt": 79.9},
#     "GHA": {"GDP_Growth": 2.9, "Inflation": 38.1, "Unemployment": 4.5,  "GDP_PerCapita": 2390, "Public_Debt": 88.1},
#     "GIN": {"GDP_Growth": 4.7, "Inflation": 10.5, "Unemployment": 5.1,  "GDP_PerCapita": 1093, "Public_Debt": 35.8},
#     "GNB": {"GDP_Growth": 4.2, "Inflation": 7.4,  "Unemployment": 3.1,  "GDP_PerCapita": 757,  "Public_Debt": 78.2},
#     "KEN": {"GDP_Growth": 5.6, "Inflation": 6.3,  "Unemployment": 5.6,  "GDP_PerCapita": 2043, "Public_Debt": 71.2},
#     "LSO": {"GDP_Growth": 2.0, "Inflation": 6.3,  "Unemployment": 24.0, "GDP_PerCapita": 1038, "Public_Debt": 55.8},
#     "LBR": {"GDP_Growth": 4.8, "Inflation": 7.6,  "Unemployment": 2.8,  "GDP_PerCapita": 650,  "Public_Debt": 61.5},
#     "LBY": {"GDP_Growth": 17.9,"Inflation": 3.9,  "Unemployment": 19.6, "GDP_PerCapita": 6888, "Public_Debt": 5.9},
#     "MDG": {"GDP_Growth": 4.0, "Inflation": 9.7,  "Unemployment": 1.8,  "GDP_PerCapita": 519,  "Public_Debt": 54.6},
#     "MWI": {"GDP_Growth": 0.9, "Inflation": 26.6, "Unemployment": 5.7,  "GDP_PerCapita": 598,  "Public_Debt": 82.1},
#     "MLI": {"GDP_Growth": 2.0, "Inflation": 9.7,  "Unemployment": 7.8,  "GDP_PerCapita": 876,  "Public_Debt": 54.4},
#     "MRT": {"GDP_Growth": 5.2, "Inflation": 9.5,  "Unemployment": 10.7, "GDP_PerCapita": 1771, "Public_Debt": 60.4},
#     "MUS": {"GDP_Growth": 7.0, "Inflation": 10.8, "Unemployment": 8.0,  "GDP_PerCapita": 10267,"Public_Debt": 81.0},
#     "MAR": {"GDP_Growth": 3.0, "Inflation": 6.6,  "Unemployment": 12.9, "GDP_PerCapita": 3442, "Public_Debt": 70.2},
#     "MOZ": {"GDP_Growth": 5.0, "Inflation": 9.8,  "Unemployment": 3.2,  "GDP_PerCapita": 502,  "Public_Debt": 99.6},
#     "NAM": {"GDP_Growth": 4.2, "Inflation": 6.2,  "Unemployment": 19.9, "GDP_PerCapita": 4852, "Public_Debt": 68.4},
#     "NER": {"GDP_Growth": 7.3, "Inflation": 3.6,  "Unemployment": 0.5,  "GDP_PerCapita": 571,  "Public_Debt": 52.2},
#     "NGA": {"GDP_Growth": 3.3, "Inflation": 24.7, "Unemployment": 5.3,  "GDP_PerCapita": 2184, "Public_Debt": 38.8},
#     "RWA": {"GDP_Growth": 8.2, "Inflation": 13.5, "Unemployment": 14.3, "GDP_PerCapita": 930,  "Public_Debt": 72.5},
#     "STP": {"GDP_Growth": 0.5, "Inflation": 18.3, "Unemployment": 12.2, "GDP_PerCapita": 2278, "Public_Debt": 103.1},
#     "SEN": {"GDP_Growth": 4.2, "Inflation": 9.7,  "Unemployment": 19.1, "GDP_PerCapita": 1549, "Public_Debt": 76.1},
#     "SLE": {"GDP_Growth": 3.5, "Inflation": 43.5, "Unemployment": 4.2,  "GDP_PerCapita": 478,  "Public_Debt": 81.3},
#     "SOM": {"GDP_Growth": 3.0, "Inflation": 6.0,  "Unemployment": 14.5, "GDP_PerCapita": 450,  "Public_Debt": 63.1},
#     "ZAF": {"GDP_Growth": 1.9, "Inflation": 6.1,  "Unemployment": 31.9, "GDP_PerCapita": 6001, "Public_Debt": 73.2},
#     "SSD": {"GDP_Growth":-2.3, "Inflation": 30.0, "Unemployment": 12.0, "GDP_PerCapita": 441,  "Public_Debt": 62.3},
#     "SDN": {"GDP_Growth":-0.3, "Inflation": 138.8,"Unemployment": 11.8, "GDP_PerCapita": 648,  "Public_Debt": 212.0},
#     "TZA": {"GDP_Growth": 4.7, "Inflation": 4.3,  "Unemployment": 2.6,  "GDP_PerCapita": 1102, "Public_Debt": 42.3},
#     "TGO": {"GDP_Growth": 5.8, "Inflation": 7.7,  "Unemployment": 3.9,  "GDP_PerCapita": 914,  "Public_Debt": 68.0},
#     "TUN": {"GDP_Growth": 2.4, "Inflation": 9.3,  "Unemployment": 15.2, "GDP_PerCapita": 3807, "Public_Debt": 82.5},
#     "UGA": {"GDP_Growth": 5.3, "Inflation": 7.2,  "Unemployment": 2.8,  "GDP_PerCapita": 883,  "Public_Debt": 52.7},
#     "ZMB": {"GDP_Growth": 4.7, "Inflation": 12.4, "Unemployment": 13.2, "GDP_PerCapita": 1300, "Public_Debt": 138.6},
#     "ZWE": {"GDP_Growth": 5.3, "Inflation": 87.6, "Unemployment": 5.2,  "GDP_PerCapita": 1509, "Public_Debt": 95.1},
#     "SYC": {"GDP_Growth": 4.5, "Inflation": 2.6,  "Unemployment": 3.3,  "GDP_PerCapita": 11234,"Public_Debt": 65.3},
# }

# # ── Data helpers ──────────────────────────────────────────────────────────────
# def _enrich(df):
#     df["Trade_Balance"] = df["Exports_GDP"] - df["Imports_GDP"]
#     df["Era"] = df["Year"].apply(
#         lambda y: "🔴 COVID" if 2020 <= y <= 2021
#         else ("🟡 Post-COVID" if y >= 2022
#         else ("🟢 Growth" if y >= 2010 else "🔵 Early 2000s"))
#     )
#     return df.reset_index(drop=True)

# @st.cache_data(ttl=3600, show_spinner=False)
# def fetch_single_country(iso3: str):
#     try:
#         import wbgapi as wb
#         frames = []
#         for col, code in WB_INDICATORS.items():
#             s = wb.data.DataFrame(code, iso3, mrv=30, numericTimeKeys=True)
#             s = s.T.reset_index()
#             s.columns = ["Year", col]
#             s["Year"] = s["Year"].astype(int)
#             frames.append(s.set_index("Year"))
#         df = pd.concat(frames, axis=1).reset_index()
#         df = df[df["Year"] >= 2000].sort_values("Year")
#         df["GDP_B"] = df["GDP_B"] / 1e9
#         if "GDP_PerCapita" not in df.columns:
#             df["GDP_PerCapita"] = np.nan
#         if "Public_Debt" not in df.columns:
#             df["Public_Debt"] = np.nan
#         return _enrich(df), "live"
#     except Exception:
#         if iso3 == "KEN":
#             return _enrich(pd.DataFrame(KENYA_FALLBACK)), "cached"
#         return None, "unavailable"

# @st.cache_data(ttl=3600, show_spinner=False)
# def fetch_primary_country(iso3: str):
#     return fetch_single_country(iso3)

# def compute_health_score(row):
#     """
#     Economic Health Score (0–100) based on 5 indicators.
#     Higher is better.
#     """
#     score = 50.0  # baseline
#     # GDP Growth: ideal ~5%, penalize negatives
#     gdp_g = row.get("GDP_Growth", np.nan)
#     if not np.isnan(gdp_g):
#         score += min(gdp_g * 2, 20) if gdp_g > 0 else gdp_g * 3

#     # Inflation: ideal <5%, penalize high
#     inf = row.get("Inflation", np.nan)
#     if not np.isnan(inf):
#         if inf <= 5:
#             score += 10
#         elif inf <= 10:
#             score += 5
#         elif inf <= 20:
#             score -= 5
#         else:
#             score -= 15

#     # Unemployment: lower is better
#     unemp = row.get("Unemployment", np.nan)
#     if not np.isnan(unemp):
#         score -= min(unemp * 0.5, 15)

#     # GDP per Capita: log scale bonus
#     gdp_pc = row.get("GDP_PerCapita", np.nan)
#     if not np.isnan(gdp_pc) and gdp_pc > 0:
#         score += min(np.log10(gdp_pc) * 5, 15)

#     # Public Debt: < 40% great, > 100% terrible
#     debt = row.get("Public_Debt", np.nan)
#     if not np.isnan(debt):
#         if debt < 40:
#             score += 10
#         elif debt < 60:
#             score += 5
#         elif debt < 80:
#             score -= 0
#         elif debt < 100:
#             score -= 5
#         else:
#             score -= 15

#     return max(0, min(100, score))

# # ── Gemini AI helper ──────────────────────────────────────────────────────────
# def build_data_summary(df, country_name, year_range):
#     dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()
#     latest = dff.iloc[-1]
#     lines = [
#         f"Country: {country_name}",
#         f"Period: {year_range[0]}–{year_range[1]}",
#         f"Latest Year: {int(latest['Year'])}",
#         f"GDP: ${latest['GDP_B']:.1f}B (growth: {latest['GDP_Growth']:.1f}%)",
#         f"GDP per Capita: ${latest.get('GDP_PerCapita', 'N/A')}",
#         f"Inflation: {latest['Inflation']:.1f}%",
#         f"Unemployment: {latest['Unemployment']:.1f}%",
#         f"Trade Balance: {latest['Trade_Balance']:.1f}% of GDP",
#         f"Public Debt: {latest.get('Public_Debt', 'N/A')}% of GDP",
#         "",
#         "Year-by-year GDP growth (%):",
#         ", ".join([f"{int(r.Year)}: {r.GDP_Growth:.1f}%" for _, r in dff.iterrows() if not pd.isna(r.GDP_Growth)]),
#         "",
#         "Year-by-year Inflation (%):",
#         ", ".join([f"{int(r.Year)}: {r.Inflation:.1f}%" for _, r in dff.iterrows() if not pd.isna(r.Inflation)]),
#         "",
#         f"Avg GDP Growth: {dff['GDP_Growth'].mean():.1f}%",
#         f"Peak Inflation: {dff['Inflation'].max():.1f}% in {int(dff.loc[dff['Inflation'].idxmax(), 'Year'])}",
#         f"Lowest Unemployment: {dff['Unemployment'].min():.1f}% in {int(dff.loc[dff['Unemployment'].idxmin(), 'Year'])}",
#     ]
#     return "\n".join(lines)

# def call_gemini(prompt: str, api_key: str) -> str:
#     try:
#         import google.generativeai as genai
#         genai.configure(api_key=api_key)
#         model = genai.GenerativeModel("gemini-2.0-flash")
#         response = model.generate_content(prompt)
#         return response.text
#     except ImportError:
#         return "❌ google-generativeai not installed. Run: pip install google-generativeai"
#     except Exception as e:
#         return f"❌ Gemini error: {str(e)}"

# # ── Sidebar ───────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("### 🌍 Africa Economic Intelligence")
#     st.markdown("---")

#     st.markdown("**PRIMARY COUNTRY**")
#     primary_code = st.selectbox(
#         "Primary country",
#         options=list(COUNTRY_OPTIONS.keys()),
#         format_func=lambda c: COUNTRY_OPTIONS[c],
#         index=list(COUNTRY_OPTIONS.keys()).index("KEN"),
#         label_visibility="collapsed",
#     )

#     st.markdown("---")
#     st.markdown("**TIME RANGE**")
#     year_range = st.slider("Years", min_value=2000, max_value=2023,
#                            value=(2005, 2023), label_visibility="collapsed")

#     st.markdown("---")
#     st.markdown("**INDICATORS**")
#     show_gdp       = st.checkbox("GDP & Growth",        value=True)
#     show_gdp_pc    = st.checkbox("GDP Per Capita",       value=True)
#     show_inf       = st.checkbox("Inflation",            value=True)
#     show_unemp     = st.checkbox("Unemployment",         value=True)
#     show_trade     = st.checkbox("Trade Balance",        value=True)
#     show_debt      = st.checkbox("Public Debt",          value=True)
#     show_scatter   = st.checkbox("Correlation Analysis", value=True)
#     show_stats     = st.checkbox("Statistical Summary",  value=True)

#     st.markdown("---")
#     st.markdown("**FORECASTING**")
#     show_forecast  = st.checkbox("5-Year Forecast", value=True)
#     forecast_years = st.slider("Horizon (years)", 1, 10, 5, disabled=not show_forecast)
#     forecast_model = st.radio("Model",
#                               ["Linear", "Polynomial (deg 2)", "Polynomial (deg 3)"],
#                               disabled=not show_forecast)

#     st.markdown("---")
#     st.markdown("**AI INSIGHTS**")
#     gemini_key = st.text_input(
#         "Gemini API Key",
#         value=os.getenv("GEMINI_API_KEY", ""),
#         type="password",
#         placeholder="AIzaSy…",
#         help="Get your free key at aistudio.google.com",
#     )

#     st.markdown("---")
#     st.markdown("**DISPLAY**")
#     highlight_covid = st.toggle("Highlight COVID period", value=True)

#     st.markdown("---")
#     st.markdown(
#         f"<small style='color:#3a4f3d'>Source: World Bank Open Data<br>"
#         f"54 African countries · {datetime.now().strftime('%d %b %Y')}</small>",
#         unsafe_allow_html=True,
#     )

# # ── Load primary country ──────────────────────────────────────────────────────
# with st.spinner("Loading data…"):
#     df, data_source = fetch_primary_country(primary_code)

# if df is None:
#     st.error(f"Could not load data for {COUNTRY_OPTIONS[primary_code]}.")
#     st.stop()

# last_year    = int(df["Year"].max())
# country_info = AFRICA_COUNTRIES[primary_code]
# country_name = country_info[0]
# country_flag = country_info[1]
# dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

# # ── Header ────────────────────────────────────────────────────────────────────
# st.markdown(
#     f"<p class='section-label'>AFRICA ECONOMIC INTELLIGENCE DASHBOARD · WORLD BANK · "
#     f"{'LIVE' if data_source == 'live' else 'OFFLINE'}</p>",
#     unsafe_allow_html=True,
# )
# col_h1, col_h2 = st.columns([3, 1])
# with col_h1:
#     st.title(f"🌍 Africa Economic Intelligence Dashboard")
#     st.markdown(f"**{country_flag} {country_name}** — GDP · Inflation · Unemployment · Trade · Debt &nbsp;·&nbsp; {year_range[0]}–{year_range[1]}")
# with col_h2:
#     badge = "badge-live" if data_source == "live" else "badge-cache"
#     label = "🟢 LIVE" if data_source == "live" else "🟡 OFFLINE"
#     st.markdown(f"<div style='padding-top:2rem'><span class='data-badge {badge}'>{label}</span></div>",
#                 unsafe_allow_html=True)
#     if st.button("🔄 Refresh"):
#         st.cache_data.clear()
#         st.rerun()

# st.markdown("---")

# # ── KPI Cards ─────────────────────────────────────────────────────────────────
# latest = dff.iloc[-1]
# prev   = dff.iloc[-2]

# k1, k2, k3, k4, k5, k6 = st.columns(6)
# k1.metric("GDP (Latest)",          f"${latest['GDP_B']:.1f}B",
#           f"{latest['GDP_Growth']:+.1f}% growth")
# k2.metric("GDP Per Capita",
#           f"${latest['GDP_PerCapita']:,.0f}" if not pd.isna(latest.get('GDP_PerCapita', np.nan)) else "N/A",
#           f"{latest['GDP_PerCapita']-prev.get('GDP_PerCapita',latest['GDP_PerCapita']):+.0f} vs prior" if not pd.isna(latest.get('GDP_PerCapita', np.nan)) else "")
# k3.metric("Inflation",             f"{latest['Inflation']:.1f}%",
#           f"{latest['Inflation']-prev['Inflation']:+.1f}pp vs prior year")
# k4.metric("Unemployment",          f"{latest['Unemployment']:.1f}%",
#           f"{latest['Unemployment']-prev['Unemployment']:+.1f}pp vs prior year")
# k5.metric("Trade Balance (% GDP)", f"{latest['Trade_Balance']:.1f}%",
#           f"{latest['Trade_Balance']-prev['Trade_Balance']:+.1f}pp vs prior year")
# k6.metric("Public Debt (% GDP)",
#           f"{latest['Public_Debt']:.1f}%" if not pd.isna(latest.get('Public_Debt', np.nan)) else "N/A",
#           f"{latest['Public_Debt']-prev.get('Public_Debt',latest['Public_Debt']):+.1f}pp" if not pd.isna(latest.get('Public_Debt', np.nan)) else "")

# st.markdown("---")

# # ── Tabs ──────────────────────────────────────────────────────────────────────
# tabs = st.tabs([
#     "📈 GDP", "💰 GDP Per Capita", "🔥 Inflation", "👷 Unemployment",
#     "🌍 Trade", "🏦 Public Debt", "🔗 Correlations", "🔮 Forecast",
#     "🗺️ Africa Map", "🏆 Rankings", "📊 Compare", "🤖 AI Insights", "📋 Statistics",
# ])

# # ── Shared helpers ────────────────────────────────────────────────────────────
# def add_covid_band(fig):
#     if highlight_covid:
#         fig.add_vrect(
#             x0=2019.5, x1=2021.5,
#             fillcolor="rgba(232,93,74,0.08)",
#             line=dict(color="rgba(232,93,74,0.3)", width=1, dash="dot"),
#             annotation_text="COVID", annotation_position="top left",
#             annotation_font=dict(color=COLORS["red"], size=10),
#         )
#     return fig

# def run_forecast(years, values, horizon, model_name):
#     X = np.array(years).reshape(-1, 1)
#     y = np.array(values)
#     if model_name == "Linear":
#         model = LinearRegression()
#     elif model_name == "Polynomial (deg 2)":
#         model = make_pipeline(PolynomialFeatures(2), LinearRegression())
#     else:
#         model = make_pipeline(PolynomialFeatures(3), LinearRegression())
#     model.fit(X, y)
#     future = np.arange(years[-1] + 1, years[-1] + horizon + 1)
#     pred   = model.predict(future.reshape(-1, 1))
#     ci     = 1.96 * np.std(y - model.predict(X)) * np.sqrt(1 + 1 / len(y))
#     return future.tolist(), pred.tolist(), (pred - ci).tolist(), (pred + ci).tolist()

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 1 — GDP
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[0]:
#     if show_gdp:
#         st.subheader(f"GDP — {country_name}")
#         fig = make_subplots(specs=[[{"secondary_y": True}]])
#         fig.add_trace(go.Bar(
#             x=dff["Year"], y=dff["GDP_B"], name="GDP (USD B)",
#             marker=dict(color=COLORS["green"], opacity=0.22,
#                         line=dict(color=COLORS["green"], width=1)),
#         ), secondary_y=False)
#         fig.add_trace(go.Scatter(
#             x=dff["Year"], y=dff["GDP_Growth"], name="GDP Growth %",
#             line=dict(color=COLORS["green"], width=2.5),
#             mode="lines+markers", marker=dict(size=5),
#         ), secondary_y=True)
#         fig.update_layout(**layout(height=380))
#         fig.update_yaxes(title_text="GDP (USD B)", secondary_y=False,
#                          tickprefix="$", ticksuffix="B",
#                          gridcolor=COLORS["border"], linecolor=COLORS["border"])
#         fig.update_yaxes(title_text="Growth %", secondary_y=True,
#                          ticksuffix="%", gridcolor="rgba(0,0,0,0)")
#         fig.update_xaxes(gridcolor=COLORS["border"])
#         add_covid_band(fig)
#         st.plotly_chart(fig, use_container_width=True)

#         c1, c2 = st.columns(2)
#         with c1:
#             dc = dff.copy(); dc["GDP_Change"] = dc["GDP_B"].diff()
#             fig2 = go.Figure(go.Bar(
#                 x=dc["Year"][1:], y=dc["GDP_Change"][1:],
#                 marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
#                               for v in dc["GDP_Change"][1:]],
#                 text=[f"${v:+.1f}B" for v in dc["GDP_Change"][1:]],
#                 textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
#             ))
#             fig2.update_layout(**layout(height=280, yaxis_extra=dict(tickprefix="$", ticksuffix="B")))
#             add_covid_band(fig2)
#             st.plotly_chart(fig2, use_container_width=True)
#         with c2:
#             era_avg = df.groupby("Era")["GDP_Growth"].mean().reset_index()
#             fig3 = go.Figure(go.Bar(
#                 x=era_avg["Era"], y=era_avg["GDP_Growth"],
#                 marker_color=[COLORS["blue"],COLORS["red"],COLORS["green"],COLORS["yellow"]],
#                 text=[f"{v:.1f}%" for v in era_avg["GDP_Growth"]],
#                 textposition="outside", textfont=dict(size=10, color=COLORS["text"]),
#             ))
#             fig3.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
#             st.plotly_chart(fig3, use_container_width=True)

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 2 — GDP Per Capita
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[1]:
#     if show_gdp_pc:
#         st.subheader(f"GDP Per Capita — {country_name}")
#         pc_data = dff.dropna(subset=["GDP_PerCapita"])
#         if pc_data.empty:
#             st.info("GDP per Capita data not available for this country.")
#         else:
#             fig = go.Figure()
#             fig.add_trace(go.Scatter(
#                 x=pc_data["Year"], y=pc_data["GDP_PerCapita"],
#                 name="GDP Per Capita (USD)",
#                 line=dict(color=COLORS["blue"], width=2.5),
#                 mode="lines+markers", marker=dict(size=6),
#                 fill="tozeroy", fillcolor="rgba(74,157,232,0.08)",
#             ))
#             # Add trend line
#             if len(pc_data) > 2:
#                 z = np.polyfit(pc_data["Year"], pc_data["GDP_PerCapita"], 1)
#                 p = np.poly1d(z)
#                 fig.add_trace(go.Scatter(
#                     x=pc_data["Year"], y=p(pc_data["Year"]),
#                     name="Trend", line=dict(color=COLORS["text"], width=1.5, dash="dot"),
#                     mode="lines",
#                 ))
#             fig.update_layout(**layout(height=380,
#                               yaxis_extra=dict(tickprefix="$", title="USD per person")))
#             add_covid_band(fig)
#             st.plotly_chart(fig, use_container_width=True)

#             c1, c2, c3, c4 = st.columns(4)
#             c1.metric("Current GDP/Capita", f"${pc_data.iloc[-1]['GDP_PerCapita']:,.0f}")
#             c2.metric("Peak GDP/Capita",    f"${pc_data['GDP_PerCapita'].max():,.0f}",
#                       f"in {int(pc_data.loc[pc_data['GDP_PerCapita'].idxmax(),'Year'])}")
#             c3.metric("Lowest GDP/Capita",  f"${pc_data['GDP_PerCapita'].min():,.0f}",
#                       f"in {int(pc_data.loc[pc_data['GDP_PerCapita'].idxmin(),'Year'])}")
#             growth_pct = ((pc_data.iloc[-1]['GDP_PerCapita'] / pc_data.iloc[0]['GDP_PerCapita']) - 1) * 100
#             c4.metric("Total Growth",       f"{growth_pct:+.1f}%",
#                       f"since {int(pc_data.iloc[0]['Year'])}")

#             # YoY growth bar chart
#             st.markdown("#### Year-over-Year GDP Per Capita Growth")
#             pc_copy = pc_data.copy()
#             pc_copy["PC_Growth"] = pc_copy["GDP_PerCapita"].pct_change() * 100
#             fig2 = go.Figure(go.Bar(
#                 x=pc_copy["Year"][1:], y=pc_copy["PC_Growth"][1:],
#                 marker_color=[COLORS["blue"] if v >= 0 else COLORS["red"]
#                               for v in pc_copy["PC_Growth"][1:]],
#                 text=[f"{v:+.1f}%" for v in pc_copy["PC_Growth"][1:]],
#                 textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
#             ))
#             fig2.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
#             add_covid_band(fig2)
#             st.plotly_chart(fig2, use_container_width=True)

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 3 — Inflation
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[2]:
#     if show_inf:
#         st.subheader(f"Inflation — {country_name}")
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             x=list(dff["Year"]) + list(dff["Year"])[::-1],
#             y=[7.5]*len(dff) + [2.5]*len(dff),
#             fill="toself", fillcolor="rgba(61,220,110,0.06)",
#             line=dict(color="rgba(0,0,0,0)"), name="Target Band (2.5–7.5%)",
#         ))
#         fig.add_hline(y=7.5, line=dict(color=COLORS["red"], dash="dot", width=1),
#                       annotation_text="Upper 7.5%",
#                       annotation_font=dict(color=COLORS["red"], size=10))
#         fig.add_hline(y=2.5, line=dict(color=COLORS["green"], dash="dot", width=1),
#                       annotation_text="Lower 2.5%",
#                       annotation_font=dict(color=COLORS["green"], size=10))
#         fig.add_trace(go.Scatter(
#             x=dff["Year"], y=dff["Inflation"], name="CPI Inflation",
#             line=dict(color=COLORS["yellow"], width=2.5), mode="lines+markers",
#             marker=dict(size=5, color=[
#                 COLORS["red"] if v > 7.5 else
#                 (COLORS["green"] if v < 2.5 else COLORS["yellow"])
#                 for v in dff["Inflation"]
#             ]),
#             fill="tozeroy", fillcolor="rgba(245,200,66,0.07)",
#         ))
#         fig.update_layout(**layout(height=380, yaxis_extra=dict(ticksuffix="%", title="CPI %")))
#         add_covid_band(fig)
#         st.plotly_chart(fig, use_container_width=True)

#         c1, c2 = st.columns(2)
#         with c1:
#             above  = (dff["Inflation"] > 7.5).sum()
#             within = ((dff["Inflation"] >= 2.5) & (dff["Inflation"] <= 7.5)).sum()
#             below  = (dff["Inflation"] < 2.5).sum()
#             fig2 = go.Figure(go.Pie(
#                 labels=["Above target","Within target","Below target"],
#                 values=[above, within, below], hole=0.55,
#                 marker=dict(colors=[COLORS["red"],COLORS["green"],COLORS["blue"]]),
#                 textfont=dict(color=COLORS["text"]),
#             ))
#             fig2.update_layout(**layout(height=280),
#                                title=dict(text="Years Within Target Band",
#                                           font=dict(color=COLORS["text"])))
#             st.plotly_chart(fig2, use_container_width=True)
#         with c2:
#             fig3 = go.Figure(go.Histogram(
#                 x=dff["Inflation"], nbinsx=10,
#                 marker=dict(color=COLORS["yellow"], opacity=0.7,
#                             line=dict(color=COLORS["bg"], width=1)),
#             ))
#             fig3.add_vline(x=dff["Inflation"].mean(),
#                            line=dict(color=COLORS["text"], dash="dash", width=1.5),
#                            annotation_text=f"Mean: {dff['Inflation'].mean():.1f}%",
#                            annotation_font=dict(color=COLORS["text"], size=10))
#             fig3.update_layout(**layout(height=280,
#                                xaxis_extra=dict(title="Inflation %"),
#                                yaxis_extra=dict(title="Count")))
#             st.plotly_chart(fig3, use_container_width=True)

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 4 — Unemployment
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[3]:
#     if show_unemp:
#         st.subheader(f"Unemployment — {country_name}")
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             x=dff["Year"], y=dff["Unemployment"], name="Unemployment %",
#             line=dict(color=COLORS["red"], width=2.5), mode="lines+markers",
#             marker=dict(size=6), fill="tozeroy", fillcolor="rgba(232,93,74,0.1)",
#         ))
#         dc2 = dff.copy()
#         dc2["MA3"] = dc2["Unemployment"].rolling(3, center=True).mean()
#         fig.add_trace(go.Scatter(
#             x=dc2["Year"], y=dc2["MA3"], name="3-Year Rolling Avg",
#             line=dict(color=COLORS["text"], width=1.5, dash="dot"), mode="lines",
#         ))
#         fig.update_layout(**layout(height=360,
#                           yaxis_extra=dict(ticksuffix="%", title="Unemployment %")))
#         add_covid_band(fig)
#         st.plotly_chart(fig, use_container_width=True)

#         c1, c2, c3 = st.columns(3)
#         c1.metric("Peak",    f"{dff['Unemployment'].max():.1f}%",
#                   f"in {int(dff.loc[dff['Unemployment'].idxmax(),'Year'])}")
#         c2.metric("Lowest",  f"{dff['Unemployment'].min():.1f}%",
#                   f"in {int(dff.loc[dff['Unemployment'].idxmin(),'Year'])}")
#         c3.metric("Average", f"{dff['Unemployment'].mean():.1f}%", "ILO modeled")

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 5 — Trade
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[4]:
#     if show_trade:
#         st.subheader(f"Trade Balance — {country_name}")
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             x=dff["Year"], y=dff["Exports_GDP"], name="Exports % GDP",
#             line=dict(color=COLORS["blue"], width=2.5),
#             mode="lines+markers", marker=dict(size=4),
#         ))
#         fig.add_trace(go.Scatter(
#             x=dff["Year"], y=dff["Imports_GDP"], name="Imports % GDP",
#             line=dict(color=COLORS["yellow"], width=2.5),
#             mode="lines+markers", marker=dict(size=4),
#         ))
#         fig.add_trace(go.Scatter(
#             x=list(dff["Year"]) + list(dff["Year"])[::-1],
#             y=list(dff["Imports_GDP"]) + list(dff["Exports_GDP"])[::-1],
#             fill="toself", fillcolor="rgba(232,93,74,0.08)",
#             line=dict(color="rgba(0,0,0,0)"), name="Trade Deficit",
#         ))
#         fig.update_layout(**layout(height=360, yaxis_extra=dict(ticksuffix="%", title="% of GDP")))
#         add_covid_band(fig)
#         st.plotly_chart(fig, use_container_width=True)

#         fig2 = go.Figure(go.Bar(
#             x=dff["Year"], y=dff["Trade_Balance"],
#             marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
#                           for v in dff["Trade_Balance"]],
#             text=[f"{v:.1f}%" for v in dff["Trade_Balance"]],
#             textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
#         ))
#         fig2.add_hline(y=0, line=dict(color=COLORS["muted"], width=1))
#         fig2.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
#         add_covid_band(fig2)
#         st.plotly_chart(fig2, use_container_width=True)

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 6 — Public Debt
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[5]:
#     if show_debt:
#         st.subheader(f"Public Debt — {country_name}")
#         debt_data = dff.dropna(subset=["Public_Debt"])
#         if debt_data.empty:
#             st.info("Public Debt data not available for this country in this date range.")
#         else:
#             fig = go.Figure()
#             fig.add_hrect(y0=0, y1=40, fillcolor="rgba(61,220,110,0.05)",
#                           line=dict(color="rgba(0,0,0,0)"), annotation_text="Low Debt Zone (< 40%)",
#                           annotation_font=dict(color=COLORS["green"], size=10))
#             fig.add_hrect(y0=60, y1=max(debt_data["Public_Debt"].max()+10, 100),
#                           fillcolor="rgba(232,93,74,0.05)",
#                           line=dict(color="rgba(0,0,0,0)"), annotation_text="High Risk Zone (> 60%)",
#                           annotation_font=dict(color=COLORS["red"], size=10))
#             fig.add_hline(y=60, line=dict(color=COLORS["yellow"], dash="dot", width=1.5),
#                           annotation_text="IMF Threshold 60%",
#                           annotation_font=dict(color=COLORS["yellow"], size=10))
#             fig.add_trace(go.Scatter(
#                 x=debt_data["Year"], y=debt_data["Public_Debt"],
#                 name="Public Debt % GDP",
#                 line=dict(color=COLORS["purple"], width=2.5),
#                 mode="lines+markers", marker=dict(size=6,
#                     color=[COLORS["green"] if v < 40 else
#                            (COLORS["yellow"] if v < 60 else COLORS["red"])
#                            for v in debt_data["Public_Debt"]]),
#                 fill="tozeroy", fillcolor="rgba(167,139,250,0.08)",
#             ))
#             fig.update_layout(**layout(height=400,
#                               yaxis_extra=dict(ticksuffix="%", title="% of GDP")))
#             add_covid_band(fig)
#             st.plotly_chart(fig, use_container_width=True)

#             c1, c2, c3, c4 = st.columns(4)
#             c1.metric("Current Debt",  f"{debt_data.iloc[-1]['Public_Debt']:.1f}%",
#                       "of GDP")
#             c2.metric("Peak Debt",     f"{debt_data['Public_Debt'].max():.1f}%",
#                       f"in {int(debt_data.loc[debt_data['Public_Debt'].idxmax(),'Year'])}")
#             c3.metric("Lowest Debt",   f"{debt_data['Public_Debt'].min():.1f}%",
#                       f"in {int(debt_data.loc[debt_data['Public_Debt'].idxmin(),'Year'])}")
#             risk = "🟢 Sustainable" if debt_data.iloc[-1]["Public_Debt"] < 60 else (
#                    "🟡 Moderate Risk" if debt_data.iloc[-1]["Public_Debt"] < 80 else "🔴 High Risk")
#             c4.metric("Debt Risk",     risk, "IMF framework")

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 7 — Correlations
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[6]:
#     if show_scatter:
#         st.subheader(f"Correlation Analysis — {country_name}")
#         c1, c2 = st.columns(2)
#         with c1:
#             sl, ic, r, p, _ = stats.linregress(dff["GDP_Growth"], dff["Unemployment"])
#             tx = np.linspace(dff["GDP_Growth"].min(), dff["GDP_Growth"].max(), 100)
#             fig = go.Figure()
#             fig.add_trace(go.Scatter(
#                 x=dff["GDP_Growth"], y=dff["Unemployment"],
#                 mode="markers+text", text=dff["Year"],
#                 textposition="top center",
#                 textfont=dict(size=9, color=COLORS["muted"]),
#                 marker=dict(size=10, color=dff["Year"],
#                             colorscale=[[0,COLORS["blue"]],[0.86,COLORS["red"]],[1,COLORS["green"]]],
#                             showscale=True,
#                             colorbar=dict(title="Year", tickfont=dict(color=COLORS["muted"]))),
#                 name="Observations",
#             ))
#             fig.add_trace(go.Scatter(
#                 x=tx, y=sl*tx+ic, mode="lines",
#                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
#                 name=f"Trend (R²={r**2:.2f})",
#             ))
#             fig.update_layout(**layout(height=360,
#                               xaxis_extra=dict(title="GDP Growth %", ticksuffix="%"),
#                               yaxis_extra=dict(title="Unemployment %", ticksuffix="%")))
#             st.plotly_chart(fig, use_container_width=True)
#             st.caption(f"Pearson r = {r:.3f} | R² = {r**2:.3f} | p = {p:.4f}")

#         with c2:
#             sl2, ic2, r2, p2, _ = stats.linregress(dff["Inflation"], dff["GDP_Growth"])
#             tx2 = np.linspace(dff["Inflation"].min(), dff["Inflation"].max(), 100)
#             fig2 = go.Figure()
#             fig2.add_trace(go.Scatter(
#                 x=dff["Inflation"], y=dff["GDP_Growth"],
#                 mode="markers+text", text=dff["Year"],
#                 textposition="top center",
#                 textfont=dict(size=9, color=COLORS["muted"]),
#                 marker=dict(size=10, color=COLORS["yellow"], opacity=0.8),
#                 name="Observations",
#             ))
#             fig2.add_trace(go.Scatter(
#                 x=tx2, y=sl2*tx2+ic2, mode="lines",
#                 line=dict(color=COLORS["text"], dash="dash", width=1.5),
#                 name=f"Trend (R²={r2**2:.2f})",
#             ))
#             fig2.update_layout(**layout(height=360,
#                                xaxis_extra=dict(title="Inflation %", ticksuffix="%"),
#                                yaxis_extra=dict(title="GDP Growth %", ticksuffix="%")))
#             st.plotly_chart(fig2, use_container_width=True)
#             st.caption(f"Pearson r = {r2:.3f} | R² = {r2**2:.3f} | p = {p2:.4f}")

#         corr_cols   = ["GDP_B","GDP_Growth","Inflation","Unemployment",
#                        "Exports_GDP","Imports_GDP","Trade_Balance"]
#         corr_labels = ["GDP (B)","GDP Growth","Inflation","Unemployment",
#                        "Exports","Imports","Trade Bal."]
#         corr = dff[corr_cols].corr().values
#         fig3 = go.Figure(go.Heatmap(
#             z=corr, x=corr_labels, y=corr_labels,
#             colorscale=[[0,COLORS["red"]],[0.5,COLORS["surface"]],[1,COLORS["green"]]],
#             zmid=0, zmin=-1, zmax=1,
#             text=[[f"{v:.2f}" for v in row] for row in corr],
#             texttemplate="%{text}", textfont=dict(size=11, color=COLORS["text"]),
#         ))
#         fig3.update_layout(**layout(height=380))
#         st.plotly_chart(fig3, use_container_width=True)

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 8 — Forecast
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[7]:
#     if show_forecast:
#         st.subheader(f"Forecast — {country_name} · {last_year+1}–{last_year+forecast_years}")
#         st.caption(f"Model: **{forecast_model}** | Trained on {year_range[0]}–{last_year} | Shaded = 95% CI")

#         train = df[(df["Year"] >= year_range[0]) & (df["Year"] <= last_year)].dropna()
#         indicators = [
#             ("GDP_Growth",   "GDP Growth %",     COLORS["green"],  "%",  ""),
#             ("GDP_B",        "GDP (USD Billion)", COLORS["green"],  "B",  "$"),
#             ("Inflation",    "Inflation %",       COLORS["yellow"], "%",  ""),
#             ("Unemployment", "Unemployment %",    COLORS["red"],    "%",  ""),
#             ("GDP_PerCapita","GDP Per Capita",     COLORS["blue"],   "",   "$"),
#             ("Public_Debt",  "Public Debt % GDP", COLORS["purple"], "%",  ""),
#         ]
#         fc1, fc2 = st.columns(2)
#         forecast_results = {}

#         for i, (col, label, color, unit, prefix) in enumerate(indicators):
#             valid = train[["Year", col]].dropna()
#             if len(valid) < 3:
#                 continue
#             fut_yrs, pred, lo, hi = run_forecast(
#                 valid["Year"].tolist(), valid[col].tolist(),
#                 forecast_years, forecast_model,
#             )
#             forecast_results[col] = {"years": fut_yrs, "pred": pred}
#             rh = int(color[1:3],16); rg = int(color[3:5],16); rb = int(color[5:7],16)

#             fig = go.Figure()
#             fig.add_trace(go.Scatter(
#                 x=valid["Year"], y=valid[col], name="Historical",
#                 line=dict(color=color, width=2.5), mode="lines+markers",
#                 marker=dict(size=4),
#             ))
#             fig.add_trace(go.Scatter(
#                 x=fut_yrs + fut_yrs[::-1], y=hi + lo[::-1],
#                 fill="toself", fillcolor=f"rgba({rh},{rg},{rb},0.12)",
#                 line=dict(color="rgba(0,0,0,0)"), name="95% CI",
#             ))
#             fig.add_trace(go.Scatter(
#                 x=fut_yrs, y=pred, name="Forecast",
#                 line=dict(color=color, width=2, dash="dash"),
#                 mode="lines+markers", marker=dict(size=6, symbol="diamond"),
#             ))
#             fig.add_vline(x=last_year + 0.5,
#                           line=dict(color=COLORS["muted"], dash="dot", width=1),
#                           annotation_text="Forecast →",
#                           annotation_font=dict(color=COLORS["muted"], size=9))
#             add_covid_band(fig)
#             tick_suf = "" if col in ("GDP_B","GDP_PerCapita") else unit
#             tick_pre = prefix
#             fig.update_layout(**layout(height=300,
#                               yaxis_extra=dict(title=label, ticksuffix=tick_suf, tickprefix=tick_pre)))
#             with (fc1 if i % 2 == 0 else fc2):
#                 st.plotly_chart(fig, use_container_width=True)

#         if forecast_results:
#             st.markdown("---")
#             st.markdown("**📋 Forecast Summary**")
#             rows = []
#             ref = list(forecast_results.keys())[0]
#             lbl_map = {"GDP_Growth":"GDP Growth %","GDP_B":"GDP (USD B)",
#                        "Inflation":"Inflation %","Unemployment":"Unemployment %",
#                        "GDP_PerCapita":"GDP Per Capita","Public_Debt":"Public Debt %"}
#             for idx, yr in enumerate(forecast_results[ref]["years"]):
#                 row = {"Year": yr}
#                 for col, res in forecast_results.items():
#                     if col in ("GDP_B","GDP_PerCapita"):
#                         fmt = f"${res['pred'][idx]:.1f}" + ("B" if col=="GDP_B" else "")
#                     else:
#                         fmt = f"{res['pred'][idx]:.1f}%"
#                     row[lbl_map.get(col, col)] = fmt
#                 rows.append(row)
#             st.dataframe(pd.DataFrame(rows).set_index("Year"), use_container_width=True)
#     else:
#         st.info("Enable **5-Year Forecast** in the sidebar.")

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 9 — Africa Choropleth Map
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[8]:
#     st.subheader("🗺️ Africa Economic Map")
#     st.caption("Choropleth map showing economic indicators across all 54 African nations")

#     map_col1, map_col2 = st.columns([2, 1])
#     with map_col1:
#         map_indicator = st.selectbox(
#             "Select Indicator",
#             options=["GDP_Growth", "Inflation", "Unemployment", "GDP_PerCapita", "Public_Debt"],
#             format_func=lambda x: {
#                 "GDP_Growth":    "📈 GDP Growth (%)",
#                 "Inflation":     "🔥 Inflation (%)",
#                 "Unemployment":  "👷 Unemployment (%)",
#                 "GDP_PerCapita": "💰 GDP Per Capita (USD)",
#                 "Public_Debt":   "🏦 Public Debt (% of GDP)",
#             }[x],
#             key="map_indicator",
#         )
#     with map_col2:
#         map_colorscale = st.selectbox(
#             "Color Scale",
#             options=["RdYlGn", "RdYlGn_r", "Viridis", "Plasma", "Blues"],
#             index=0,
#             key="map_colorscale",
#         )

#     # Build map dataframe
#     map_rows = []
#     for code, vals in AFRICA_MAP_DATA.items():
#         country_n = AFRICA_COUNTRIES[code][0]
#         val = vals.get(map_indicator, np.nan)
#         map_rows.append({
#             "iso_alpha3": code,
#             "Country": country_n,
#             "Value": val,
#         })
#     map_df = pd.DataFrame(map_rows)

#     # Indicator metadata for display
#     ind_meta = {
#         "GDP_Growth":    ("GDP Growth (%)",       "%",  "RdYlGn",   "Latest GDP Growth Rate"),
#         "Inflation":     ("Inflation (%)",         "%",  "RdYlGn_r", "Latest CPI Inflation Rate"),
#         "Unemployment":  ("Unemployment (%)",      "%",  "RdYlGn_r", "Latest Unemployment Rate"),
#         "GDP_PerCapita": ("GDP Per Capita (USD)",  "$",  "Viridis",  "Latest GDP Per Capita"),
#         "Public_Debt":   ("Public Debt (% GDP)",   "%",  "RdYlGn_r", "Public Debt as % of GDP"),
#     }
#     ind_label, ind_unit, default_cs, ind_title = ind_meta[map_indicator]
#     colorscale_to_use = map_colorscale

#     fig_map = go.Figure(go.Choropleth(
#         locations=map_df["iso_alpha3"],
#         z=map_df["Value"],
#         text=map_df["Country"],
#         customdata=np.stack([
#             map_df["Country"],
#             map_df["Value"].apply(lambda v: f"{ind_unit}{v:,.1f}" if ind_unit=="$" else f"{v:.1f}{ind_unit}")
#         ], axis=-1),
#         hovertemplate="<b>%{customdata[0]}</b><br>" + ind_label + ": %{customdata[1]}<extra></extra>",
#         colorscale=colorscale_to_use,
#         autocolorscale=False,
#         reversescale=False,
#         marker=dict(line=dict(color="#0a0f0d", width=0.5)),
#         colorbar=dict(
#             title=dict(text=ind_label, font=dict(color=COLORS["text"], size=12)),
#             tickfont=dict(color=COLORS["muted"]),
#             bgcolor=COLORS["surface"],
#             bordercolor=COLORS["border"],
#             borderwidth=1,
#             thickness=15,
#             len=0.75,
#         ),
#     ))

#     fig_map.update_layout(
#         title=dict(
#             text=f"Africa — {ind_title}",
#             font=dict(color=COLORS["text"], size=16),
#             x=0.5,
#         ),
#         geo=dict(
#             scope="africa",
#             showframe=False,
#             showcoastlines=True,
#             coastlinecolor=COLORS["border"],
#             showland=True,
#             landcolor="#111812",
#             showocean=True,
#             oceancolor="#0a0f0d",
#             showcountries=True,
#             countrycolor=COLORS["border"],
#             bgcolor=COLORS["bg"],
#             projection_type="mercator",
#             lataxis_range=[-35, 38],
#             lonaxis_range=[-18, 52],
#         ),
#         paper_bgcolor=COLORS["bg"],
#         plot_bgcolor=COLORS["bg"],
#         font=dict(color=COLORS["muted"], family="DM Mono, monospace"),
#         margin=dict(t=60, b=20, l=0, r=0),
#         height=580,
#     )

#     st.plotly_chart(fig_map, use_container_width=True)

#     # Summary stats below map
#     st.markdown("---")
#     mc1, mc2, mc3, mc4, mc5 = st.columns(5)
#     valid_vals = map_df["Value"].dropna()
#     mc1.metric("Continental Average", f"{valid_vals.mean():.1f}{ind_unit}" if ind_unit != "$" else f"${valid_vals.mean():,.0f}")
#     mc2.metric("Highest",
#                f"{map_df.loc[map_df['Value'].idxmax(),'Country']}",
#                f"{map_df['Value'].max():.1f}{ind_unit}" if ind_unit != "$" else f"${map_df['Value'].max():,.0f}")
#     mc3.metric("Lowest",
#                f"{map_df.loc[map_df['Value'].idxmin(),'Country']}",
#                f"{map_df['Value'].min():.1f}{ind_unit}" if ind_unit != "$" else f"${map_df['Value'].min():,.0f}")
#     mc4.metric("Median", f"{valid_vals.median():.1f}{ind_unit}" if ind_unit != "$" else f"${valid_vals.median():,.0f}")
#     mc5.metric("Countries Tracked", f"{len(valid_vals)}", "out of 54")

#     # Top 10 table
#     st.markdown(f"#### Top 10 Countries — {ind_label}")
#     top10 = map_df.dropna(subset=["Value"]).sort_values("Value", ascending=(map_indicator in ["GDP_PerCapita","GDP_Growth"]), key=lambda x: -x).head(10)
#     top10 = map_df.dropna(subset=["Value"]).sort_values("Value", ascending=False).head(10)
#     top10_display = top10.copy()
#     top10_display["Rank"] = range(1, len(top10_display)+1)
#     top10_display[ind_label] = top10_display["Value"].apply(
#         lambda v: f"${v:,.0f}" if ind_unit == "$" else f"{v:.1f}{ind_unit}"
#     )
#     st.dataframe(
#         top10_display[["Rank","Country",ind_label]].set_index("Rank"),
#         use_container_width=True,
#     )

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 10 — Economic Rankings
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[9]:
#     st.subheader("🏆 Africa Economic Rankings")
#     st.caption("Economic Health Score computed from GDP Growth, Inflation, Unemployment, GDP Per Capita & Public Debt")

#     # Compute scores for all countries using static data
#     ranking_rows = []
#     for code, vals in AFRICA_MAP_DATA.items():
#         country_n = AFRICA_COUNTRIES[code][0]
#         flag      = AFRICA_COUNTRIES[code][1]
#         score     = compute_health_score(vals)
#         ranking_rows.append({
#             "Code":            code,
#             "Flag":            flag,
#             "Country":         country_n,
#             "Health Score":    round(score, 1),
#             "GDP Growth (%)":  vals.get("GDP_Growth", np.nan),
#             "Inflation (%)":   vals.get("Inflation", np.nan),
#             "Unemployment (%)":vals.get("Unemployment", np.nan),
#             "GDP/Capita ($)":  vals.get("GDP_PerCapita", np.nan),
#             "Public Debt (%)": vals.get("Public_Debt", np.nan),
#         })

#     rank_df = pd.DataFrame(ranking_rows).sort_values("Health Score", ascending=False).reset_index(drop=True)
#     rank_df.insert(0, "Rank", range(1, len(rank_df)+1))

#     # Score distribution gauge bar chart
#     fig_rank = go.Figure(go.Bar(
#         x=rank_df["Health Score"],
#         y=rank_df["Flag"] + " " + rank_df["Country"],
#         orientation="h",
#         marker=dict(
#             color=rank_df["Health Score"],
#             colorscale=[[0,COLORS["red"]],[0.4,COLORS["yellow"]],[1,COLORS["green"]]],
#             cmin=0, cmax=100,
#             showscale=True,
#             colorbar=dict(
#                 title="Score", tickfont=dict(color=COLORS["muted"]),
#                 bgcolor=COLORS["surface"], bordercolor=COLORS["border"],
#             ),
#         ),
#         text=[f"{v:.1f}" for v in rank_df["Health Score"]],
#         textposition="outside",
#         textfont=dict(size=9, color=COLORS["text"]),
#     ))
#     fig_rank.update_layout(
#         **layout(height=max(700, len(rank_df)*14),
#                  yaxis_extra=dict(autorange="reversed")),
#         title=dict(text="Economic Health Score — All 54 African Nations",
#                    font=dict(color=COLORS["text"])),
#         xaxis=dict(range=[0, 115], tickcolor=COLORS["border"],
#                    gridcolor=COLORS["border"], linecolor=COLORS["border"]),
#     )
#     st.plotly_chart(fig_rank, use_container_width=True)

#     # Medal podium top 3
#     st.markdown("---")
#     st.markdown("### 🥇 Top Performers")
#     pod1, pod2, pod3 = st.columns(3)
#     top3 = rank_df.head(3)

#     for i, (col, medal, color) in enumerate(zip(
#         [pod1, pod2, pod3],
#         ["🥇", "🥈", "🥉"],
#         [COLORS["yellow"], "#c0c0c0", "#cd7f32"]
#     )):
#         row = top3.iloc[i]
#         with col:
#             st.markdown(f"""
#             <div style='background:{COLORS["surface"]};border:1px solid {color};
#                         border-radius:8px;padding:1.2rem;text-align:center;'>
#                 <div style='font-size:2rem'>{medal}</div>
#                 <div style='font-size:1.5rem'>{row['Flag']}</div>
#                 <div style='color:{COLORS["text"]};font-weight:bold;margin:0.3rem 0'>
#                     {row['Country']}</div>
#                 <div style='color:{color};font-size:1.3rem;font-weight:bold'>
#                     {row['Health Score']}</div>
#                 <div style='color:{COLORS["muted"]};font-size:0.7rem'>Health Score</div>
#             </div>
#             """, unsafe_allow_html=True)

#     # Bottom 3
#     st.markdown("### ⚠️ Countries Needing Attention")
#     bot1, bot2, bot3 = st.columns(3)
#     bot3_df = rank_df.tail(3).iloc[::-1]
#     for i, col in enumerate([bot1, bot2, bot3]):
#         row = bot3_df.iloc[i]
#         with col:
#             st.markdown(f"""
#             <div style='background:{COLORS["surface"]};border:1px solid {COLORS["red"]};
#                         border-radius:8px;padding:1.2rem;text-align:center;'>
#                 <div style='font-size:1.5rem'>{row['Flag']}</div>
#                 <div style='color:{COLORS["text"]};font-weight:bold;margin:0.3rem 0'>
#                     {row['Country']}</div>
#                 <div style='color:{COLORS["red"]};font-size:1.3rem;font-weight:bold'>
#                     {row['Health Score']}</div>
#                 <div style='color:{COLORS["muted"]};font-size:0.7rem'>Health Score</div>
#             </div>
#             """, unsafe_allow_html=True)

#     st.markdown("---")
#     # Full ranking table
#     st.markdown("### 📋 Full Economic Ranking Table")
#     display_rank = rank_df.copy()
#     display_rank["GDP Growth (%)"]   = display_rank["GDP Growth (%)"].apply(lambda v: f"{v:+.1f}%" if not np.isnan(v) else "—")
#     display_rank["Inflation (%)"]    = display_rank["Inflation (%)"].apply(lambda v: f"{v:.1f}%" if not np.isnan(v) else "—")
#     display_rank["Unemployment (%)"] = display_rank["Unemployment (%)"].apply(lambda v: f"{v:.1f}%" if not np.isnan(v) else "—")
#     display_rank["GDP/Capita ($)"]   = display_rank["GDP/Capita ($)"].apply(lambda v: f"${v:,.0f}" if not np.isnan(v) else "—")
#     display_rank["Public Debt (%)"]  = display_rank["Public Debt (%)"].apply(lambda v: f"{v:.1f}%" if not np.isnan(v) else "—")
#     display_rank["Country"]          = display_rank["Flag"] + " " + display_rank["Country"]

#     st.dataframe(
#         display_rank[["Rank","Country","Health Score","GDP Growth (%)","Inflation (%)",
#                        "Unemployment (%)","GDP/Capita ($)","Public Debt (%)"]].set_index("Rank"),
#         use_container_width=True,
#     )

#     st.download_button(
#         "⬇️ Download Rankings CSV",
#         data=rank_df.to_csv(index=False).encode("utf-8"),
#         file_name="africa_economic_rankings.csv",
#         mime="text/csv",
#     )

#     st.markdown("""
#     <div class='insight-box'>
#         <h4>ℹ️ About the Economic Health Score</h4>
#         <p>The score (0–100) is a composite index weighted across five indicators:
#         GDP Growth (positive contribution), Inflation (penalized above 10%),
#         Unemployment (penalized), GDP Per Capita (log-scale bonus), and
#         Public Debt (penalized above 60% of GDP). Scores above 70 indicate
#         strong economic health; below 40 indicates significant challenges.</p>
#     </div>
#     """, unsafe_allow_html=True)

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 11 — Country Comparison
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[10]:
#     st.subheader("📊 Country Comparison — All 54 African Nations")
#     st.caption("🟢 = full data · 🟡 = partial · 🔴 = sparse")

#     cc1, cc2, cc3 = st.columns([2, 1, 1])
#     with cc1:
#         compare_codes = st.multiselect(
#             "Select countries (up to 5)",
#             options=list(COUNTRY_OPTIONS.keys()),
#             default=["KEN","NGA","ZAF","ETH","GHA"],
#             format_func=lambda c: COUNTRY_OPTIONS[c],
#             max_selections=5,
#         )
#     with cc2:
#         compare_indicator = st.selectbox(
#             "Indicator",
#             options=["GDP_Growth","GDP_B","GDP_PerCapita","Inflation","Unemployment",
#                      "Exports_GDP","Imports_GDP","Trade_Balance","Public_Debt"],
#             format_func=lambda x: {
#                 "GDP_Growth":"GDP Growth %","GDP_B":"GDP (USD B)",
#                 "GDP_PerCapita":"GDP Per Capita","Inflation":"Inflation %",
#                 "Unemployment":"Unemployment %","Exports_GDP":"Exports % GDP",
#                 "Imports_GDP":"Imports % GDP","Trade_Balance":"Trade Balance % GDP",
#                 "Public_Debt":"Public Debt % GDP",
#             }[x],
#         )
#     with cc3:
#         compare_range = st.slider("Year range", 2000, 2023, (2005, 2023), key="cmp_range")

#     if not compare_codes:
#         st.info("Select at least one country above.")
#     else:
#         country_data = {}
#         load_errors  = []
#         progress = st.progress(0, text="Loading…")
#         for i, code in enumerate(compare_codes):
#             progress.progress((i+1)/len(compare_codes),
#                               text=f"Loading {AFRICA_COUNTRIES[code][0]}…")
#             cdf, _ = fetch_single_country(code)
#             if cdf is not None:
#                 country_data[code] = cdf
#             else:
#                 load_errors.append(AFRICA_COUNTRIES[code][0])
#         progress.empty()

#         if load_errors:
#             st.warning(f"Could not load: {', '.join(load_errors)}")

#         if country_data:
#             ind_labels = {
#                 "GDP_Growth":    ("GDP Growth %",       "%", ""),
#                 "GDP_B":         ("GDP (USD Billion)",  "B", "$"),
#                 "GDP_PerCapita": ("GDP Per Capita",     "",  "$"),
#                 "Inflation":     ("Inflation %",        "%", ""),
#                 "Unemployment":  ("Unemployment %",     "%", ""),
#                 "Exports_GDP":   ("Exports % of GDP",   "%", ""),
#                 "Imports_GDP":   ("Imports % of GDP",   "%", ""),
#                 "Trade_Balance": ("Trade Balance % GDP","%", ""),
#                 "Public_Debt":   ("Public Debt % GDP",  "%", ""),
#             }
#             ind_label, ind_unit, ind_prefix = ind_labels[compare_indicator]
#             tick_suffix = "" if ind_unit in ("B","") else ind_unit

#             st.markdown(f"### {ind_label} — Over Time")
#             fig = go.Figure()
#             for idx, (code, cdf) in enumerate(country_data.items()):
#                 cdf_f = cdf[(cdf["Year"] >= compare_range[0]) &
#                             (cdf["Year"] <= compare_range[1])].dropna(subset=[compare_indicator])
#                 if cdf_f.empty:
#                     continue
#                 color = COUNTRY_PALETTE[idx % len(COUNTRY_PALETTE)]
#                 name  = AFRICA_COUNTRIES[code][0]
#                 fig.add_trace(go.Scatter(
#                     x=cdf_f["Year"], y=cdf_f[compare_indicator], name=name,
#                     line=dict(color=color, width=2.5), mode="lines+markers",
#                     marker=dict(size=5),
#                     hovertemplate=f"<b>{name}</b><br>Year: %{{x}}<br>{ind_label}: %{{y:.1f}}<extra></extra>",
#                 ))
#             fig.update_layout(**layout(height=420,
#                               yaxis_extra=dict(title=ind_label,
#                                                ticksuffix=tick_suffix, tickprefix=ind_prefix)))
#             if highlight_covid:
#                 add_covid_band(fig)
#             st.plotly_chart(fig, use_container_width=True)

#             # Bar chart — latest values
#             st.markdown(f"### Latest Value — {ind_label}")
#             bar_data = []
#             for code, cdf in country_data.items():
#                 valid = cdf.dropna(subset=[compare_indicator])
#                 if not valid.empty:
#                     bar_data.append({
#                         "Country": AFRICA_COUNTRIES[code][0],
#                         "Value":   valid.iloc[-1][compare_indicator],
#                         "Year":    int(valid.iloc[-1]["Year"]),
#                     })
#             if bar_data:
#                 bar_df = pd.DataFrame(bar_data).sort_values("Value", ascending=True)
#                 fig_bar = go.Figure(go.Bar(
#                     x=bar_df["Value"], y=bar_df["Country"], orientation="h",
#                     marker=dict(
#                         color=bar_df["Value"],
#                         colorscale=[[0,COLORS["red"]],[0.5,COLORS["yellow"]],[1,COLORS["green"]]],
#                         showscale=True,
#                         colorbar=dict(title=ind_label, tickfont=dict(color=COLORS["muted"])),
#                     ),
#                     text=[f"{ind_prefix}{v:.1f}{ind_unit if ind_unit not in ('B','') else ('B' if ind_unit=='B' else '')} ({y})"
#                           for v, y in zip(bar_df["Value"], bar_df["Year"])],
#                     textposition="outside",
#                     textfont=dict(size=10, color=COLORS["text"]),
#                 ))
#                 fig_bar.update_layout(**layout(
#                     height=max(250, len(bar_data)*55),
#                     yaxis_extra=dict(title=""),
#                     xaxis_extra=dict(title=ind_label,
#                                      ticksuffix=tick_suffix, tickprefix=ind_prefix),
#                 ))
#                 st.plotly_chart(fig_bar, use_container_width=True)

#             # Summary table
#             st.markdown("### 📋 All Indicators — Latest Values")
#             table_rows = []
#             for code, cdf in country_data.items():
#                 row = {"Country": AFRICA_COUNTRIES[code][0], "Quality": AFRICA_COUNTRIES[code][2]}
#                 for ind, (lbl, unit, pfx) in ind_labels.items():
#                     valid = cdf.dropna(subset=[ind])
#                     if not valid.empty:
#                         v  = valid.iloc[-1][ind]
#                         yr = int(valid.iloc[-1]["Year"])
#                         row[lbl] = f"{pfx}{v:.1f}{unit if unit not in ('B','') else ('B' if unit=='B' else '')} ({yr})"
#                     else:
#                         row[lbl] = "—"
#                 table_rows.append(row)
#             st.dataframe(pd.DataFrame(table_rows).set_index("Country"), use_container_width=True)

#             all_frames = []
#             for code, cdf in country_data.items():
#                 tmp = cdf.copy()
#                 tmp.insert(0, "Country", AFRICA_COUNTRIES[code][0])
#                 tmp.insert(1, "ISO3", code)
#                 all_frames.append(tmp)
#             combined = pd.concat(all_frames, ignore_index=True)
#             st.download_button("⬇️ Download Comparison CSV",
#                                data=combined.to_csv(index=False).encode("utf-8"),
#                                file_name="africa_comparison.csv", mime="text/csv")

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 12 — AI INSIGHTS
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[11]:
#     st.subheader(f"🤖 AI Insights — {country_name}")
#     st.caption("Powered by Google Gemini · Reads your actual loaded data, not hardcoded text")

#     if not gemini_key:
#         st.warning(
#             "**Add your Gemini API key to enable AI Insights.**\n\n"
#             "1. Go to [aistudio.google.com](https://aistudio.google.com) → Get API Key\n"
#             "2. Paste it into the **AI Insights** field in the sidebar\n"
#             "3. Or add `GEMINI_API_KEY=your_key` to your `.env` file"
#         )
#     else:
#         data_summary = build_data_summary(df, country_name, year_range)

#         st.markdown("**Quick Analysis — click any button to generate:**")
#         PRESETS = {
#             "📊 Full Economic Overview": (
#                 f"You are an expert economist specializing in African economies. "
#                 f"Analyze the following economic data for {country_name} and write a "
#                 f"comprehensive 4-paragraph economic overview. Cover: (1) GDP growth trajectory "
#                 f"and key turning points, (2) inflation patterns and monetary policy implications, "
#                 f"(3) unemployment trends and labor market dynamics, (4) trade balance and "
#                 f"structural economic challenges. Be specific — reference actual numbers from the data.\n\n"
#                 f"DATA:\n{data_summary}"
#             ),
#             "📉 COVID Impact Analysis": (
#                 f"Analyze the specific economic impact of COVID-19 (2020–2021) on {country_name} "
#                 f"based on this data. Compare pre-COVID averages (2015–2019) to COVID years and "
#                 f"the recovery period (2022–2023). Quantify the damage and recovery across all "
#                 f"indicators. Write 3 focused paragraphs.\n\nDATA:\n{data_summary}"
#             ),
#             "🔮 Outlook & Risks": (
#                 f"Based on the historical economic trends for {country_name}, write a forward-looking "
#                 f"assessment covering: (1) what the data suggests about growth momentum, "
#                 f"(2) the biggest economic risks and vulnerabilities, (3) structural opportunities "
#                 f"for the economy. Ground every point in the actual data provided.\n\nDATA:\n{data_summary}"
#             ),
#             "🌍 Regional Context": (
#                 f"Place {country_name}'s economic performance in the context of sub-Saharan Africa. "
#                 f"Based on this data, assess whether the country is an outperformer, average, or "
#                 f"underperformer relative to typical African economies. Discuss inflation management, "
#                 f"growth consistency, and trade dynamics. Write 3 concise paragraphs.\n\nDATA:\n{data_summary}"
#             ),
#             "📈 Best & Worst Years": (
#                 f"From the data provided for {country_name}, identify and explain the 3 best and "
#                 f"3 worst economic years. For each year, explain what likely caused the performance "
#                 f"based on the indicators. Reference specific numbers. Write in a clear analytical style.\n\nDATA:\n{data_summary}"
#             ),
#         }

#         cols = st.columns(3)
#         for i, (btn_label, _) in enumerate(PRESETS.items()):
#             with cols[i % 3]:
#                 if st.button(btn_label, use_container_width=True):
#                     st.session_state["ai_prompt"]   = PRESETS[btn_label]
#                     st.session_state["ai_btn_label"] = btn_label

#         st.markdown("---")
#         st.markdown("**Or ask a custom question:**")
#         custom_q = st.text_area(
#             "Your question",
#             placeholder=f"e.g. Why did inflation spike so high in {country_name}? "
#                         f"What does the trade deficit mean for economic growth?",
#             height=80,
#             label_visibility="collapsed",
#         )
#         if st.button("🔍 Ask Gemini", use_container_width=False):
#             if custom_q.strip():
#                 full_prompt = (
#                     f"You are an expert economist. Answer the following question about "
#                     f"{country_name} using the data provided. Be specific and reference "
#                     f"actual numbers.\n\nQUESTION: {custom_q}\n\nDATA:\n{data_summary}"
#                 )
#                 st.session_state["ai_prompt"]   = full_prompt
#                 st.session_state["ai_btn_label"] = f"❓ {custom_q[:60]}…"

#         if "ai_prompt" in st.session_state:
#             st.markdown("---")
#             st.markdown(f"**{st.session_state.get('ai_btn_label', 'Analysis')}**")
#             with st.spinner("Gemini is analyzing the data…"):
#                 response = call_gemini(st.session_state["ai_prompt"], gemini_key)
#             st.markdown(
#                 f"<div class='ai-response'>{response}</div>",
#                 unsafe_allow_html=True,
#             )
#             st.download_button(
#                 "⬇️ Download Analysis",
#                 data=response.encode("utf-8"),
#                 file_name=f"{primary_code}_ai_analysis.txt",
#                 mime="text/plain",
#             )
#             if st.button("🗑️ Clear"):
#                 del st.session_state["ai_prompt"]
#                 del st.session_state["ai_btn_label"]
#                 st.rerun()

# # ═════════════════════════════════════════════════════════════════════════════
# # TAB 13 — Statistics
# # ═════════════════════════════════════════════════════════════════════════════
# with tabs[12]:
#     if show_stats:
#         st.subheader(f"Statistical Summary — {country_name}")
#         summary_cols = ["GDP_Growth","Inflation","Unemployment",
#                         "Exports_GDP","Imports_GDP","Trade_Balance"]
#         # add optional columns
#         for opt_col in ["GDP_PerCapita","Public_Debt"]:
#             if opt_col in dff.columns and not dff[opt_col].isna().all():
#                 summary_cols.append(opt_col)

#         label_map = {
#             "GDP_Growth":"GDP Growth %","Inflation":"Inflation %",
#             "Unemployment":"Unemployment %","Exports_GDP":"Exports % GDP",
#             "Imports_GDP":"Imports % GDP","Trade_Balance":"Trade Balance % GDP",
#             "GDP_PerCapita":"GDP Per Capita ($)","Public_Debt":"Public Debt % GDP",
#         }
#         stats_df = dff[summary_cols].describe().T.round(2)
#         stats_df.index = [label_map.get(i, i) for i in stats_df.index]
#         stats_df.columns = ["Count","Mean","Std Dev","Min",
#                             "25th %ile","Median","75th %ile","Max"]
#         st.dataframe(
#             stats_df.style.background_gradient(subset=["Mean"], cmap="RdYlGn", axis=0)
#                           .format("{:.2f}"),
#             use_container_width=True,
#         )
#         st.markdown("---")
#         disp_cols = ["Year","Era","GDP_B","GDP_Growth","Inflation",
#                      "Unemployment","Exports_GDP","Imports_GDP","Trade_Balance"]
#         disp_names = ["Year","Era","GDP ($B)","GDP Growth %","Inflation %",
#                       "Unemployment %","Exports % GDP","Imports % GDP","Trade Balance %"]
#         for opt_col, opt_name in [("GDP_PerCapita","GDP Per Capita ($)"),("Public_Debt","Public Debt %")]:
#             if opt_col in dff.columns and not dff[opt_col].isna().all():
#                 disp_cols.append(opt_col)
#                 disp_names.append(opt_name)

#         disp = dff[disp_cols].copy()
#         disp.columns = disp_names
#         st.dataframe(disp.set_index("Year"), use_container_width=True)
#         st.download_button("⬇️ Download CSV",
#                            data=disp.to_csv(index=False).encode("utf-8"),
#                            file_name=f"{primary_code}_data.csv", mime="text/csv")

# # ── Footer insights ───────────────────────────────────────────────────────────
# st.markdown("---")
# st.subheader("Key Insights")
# c1, c2, c3, c4 = st.columns(4)
# with c1:
#     st.markdown("""<div class='insight-box'>
#         <h4>📈 Sustained Long-Term Growth</h4>
#         <p>Many African economies have recorded GDP growth of 4–8% annually over two decades,
#         outpacing global averages and demonstrating strong structural development.</p>
#         </div>""", unsafe_allow_html=True)
# with c2:
#     st.markdown("""<div class='insight-box warn'>
#         <h4>🔥 Inflation Pressures</h4>
#         <p>Inflation remains a persistent challenge, amplified by global food and energy
#         shocks in 2008 and 2022 and structural import dependency across the continent.</p>
#         </div>""", unsafe_allow_html=True)
# with c3:
#     st.markdown("""<div class='insight-box danger'>
#         <h4>🌍 Trade Imbalances</h4>
#         <p>Most African economies run persistent trade deficits driven by fuel, machinery,
#         and manufactured goods imports. Export diversification remains a key challenge.</p>
#         </div>""", unsafe_allow_html=True)
# with c4:
#     st.markdown("""<div class='insight-box'>
#         <h4>🏦 Rising Public Debt</h4>
#         <p>Several African nations now carry debt above 80% of GDP, raising concerns
#         about fiscal sustainability and debt servicing costs amid rising global interest rates.</p>
#         </div>""", unsafe_allow_html=True)

# st.markdown(
#     "<br><small style='color:#3a4f3d'>Data: World Bank Open Data · IMF DataMapper · "
#     "54 African countries · All indicators from official national statistics.</small>",
#     unsafe_allow_html=True,
# )

"""
Africa Economic Intelligence Dashboard
Streamlit + Plotly | All Upgrades:
  - Live World Bank API (wbgapi) with offline fallback
  - GDP Per Capita
  - Public Debt
  - Choropleth Map of Africa (indicator-selectable)
  - Economic Ranking Table with Economic Health Score
  - 5-Year Forecasting Panel
  - Country Comparison — all 54 African countries
  - AI Insights Tab — powered by Google Gemini
Data source: World Bank Open Data
"""

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Africa Economic Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0a0f0d; }
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    [data-testid="stSidebar"] { background-color: #111812; border-right: 1px solid #1e2e21; }
    [data-testid="stSidebar"] * { color: #e8f0ea !important; }
    [data-testid="metric-container"] {
        background: #111812; border: 1px solid #1e2e21;
        border-radius: 6px; padding: 1rem 1.2rem;
    }
    [data-testid="stMetricLabel"] { color: #6b7f6e !important; font-size: 0.75rem; }
    [data-testid="stMetricValue"] { color: #e8f0ea !important; }
    [data-testid="stMetricDelta"] { font-size: 0.8rem; }
    h1, h2, h3 { color: #e8f0ea !important; }
    p, li { color: #b0bfb3 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #111812; border-bottom: 1px solid #1e2e21; }
    .stTabs [data-baseweb="tab"] { color: #6b7f6e; }
    .stTabs [aria-selected="true"] { color: #3ddc6e !important; border-bottom-color: #3ddc6e !important; }
    hr { border-color: #1e2e21; }
    .stAlert { background-color: #111812; border-color: #1e2e21; }
    .section-label {
        font-family: monospace; font-size: 0.65rem; letter-spacing: 0.2em;
        color: #3ddc6e; text-transform: uppercase; margin-bottom: 0.25rem;
    }
    .data-badge {
        display: inline-block; font-family: monospace; font-size: 0.62rem;
        letter-spacing: 0.1em; padding: 0.25rem 0.65rem;
        border-radius: 2px; margin-bottom: 1rem;
    }
    .badge-live  { background: rgba(61,220,110,0.15); color: #3ddc6e; border: 1px solid #3ddc6e; }
    .badge-cache { background: rgba(245,200,66,0.15); color: #f5c842; border: 1px solid #f5c842; }
    .insight-box {
        background: #111812; border: 1px solid #1e2e21;
        border-left: 3px solid #3ddc6e; border-radius: 4px;
        padding: 1rem 1.2rem; margin-bottom: 0.75rem;
    }
    .insight-box.warn   { border-left-color: #f5c842; }
    .insight-box.danger { border-left-color: #e85d4a; }
    .insight-box h4 { color: #e8f0ea !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
    .insight-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
    .forecast-box {
        background: rgba(74,157,232,0.06); border: 1px solid rgba(74,157,232,0.25);
        border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
    }
    .forecast-box h4 { color: #4a9de8 !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
    .forecast-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
    .compare-box {
        background: rgba(167,139,250,0.06); border: 1px solid rgba(167,139,250,0.25);
        border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem;
    }
    .compare-box h4 { color: #a78bfa !important; margin: 0 0 0.3rem; font-size: 0.9rem; }
    .compare-box p  { color: #6b7f6e !important; margin: 0; font-size: 0.82rem; line-height: 1.6; }
    .ai-response {
        background: #0d1a0f; border: 1px solid #1e2e21;
        border-left: 3px solid #3ddc6e; border-radius: 4px;
        padding: 1.4rem 1.6rem; margin-top: 1rem;
        font-size: 0.88rem; line-height: 1.8; color: #c8d8cb !important;
        white-space: pre-wrap;
    }
    .rank-gold   { color: #f5c842; font-weight: bold; }
    .rank-silver { color: #c0c0c0; font-weight: bold; }
    .rank-bronze { color: #cd7f32; font-weight: bold; }
    .score-bar {
        background: #1e2e21; border-radius: 3px; height: 8px; width: 100%;
        margin-top: 4px;
    }
    .score-fill {
        border-radius: 3px; height: 8px;
        background: linear-gradient(90deg, #e85d4a, #f5c842, #3ddc6e);
    }
</style>
""", unsafe_allow_html=True)

# ── Colors & layout ───────────────────────────────────────────────────────────
COLORS = {
    "bg": "#0a0f0d", "surface": "#111812", "border": "#1e2e21",
    "green": "#3ddc6e", "yellow": "#f5c842", "red": "#e85d4a",
    "blue": "#4a9de8", "purple": "#a78bfa", "muted": "#6b7f6e", "text": "#e8f0ea",
}
COUNTRY_PALETTE = [
    "#3ddc6e","#4a9de8","#f5c842","#e85d4a","#a78bfa",
    "#f97316","#06b6d4","#ec4899","#84cc16","#fb923c",
]
GRID = dict(gridcolor=COLORS["border"], linecolor=COLORS["border"], tickcolor=COLORS["border"])

def layout(height=360, xaxis_extra=None, yaxis_extra=None, **kwargs):
    return dict(
        paper_bgcolor=COLORS["surface"], plot_bgcolor=COLORS["bg"],
        font=dict(family="DM Mono, monospace", color=COLORS["muted"], size=11),
        xaxis={**GRID, **(xaxis_extra or {})},
        yaxis={**GRID, **(yaxis_extra or {})},
        margin=dict(t=40, b=40, l=55, r=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
        height=height, **kwargs,
    )

# ── All 54 African countries ──────────────────────────────────────────────────
AFRICA_COUNTRIES = {
    "DZA": ("Algeria",              "🇩🇿", "🟢"),
    "AGO": ("Angola",               "🇦🇴", "🟡"),
    "BEN": ("Benin",                "🇧🇯", "🟡"),
    "BWA": ("Botswana",             "🇧🇼", "🟢"),
    "BFA": ("Burkina Faso",         "🇧🇫", "🟡"),
    "BDI": ("Burundi",              "🇧🇮", "🟡"),
    "CPV": ("Cabo Verde",           "🇨🇻", "🟡"),
    "CMR": ("Cameroon",             "🇨🇲", "🟢"),
    "CAF": ("Central African Rep.", "🇨🇫", "🔴"),
    "TCD": ("Chad",                 "🇹🇩", "🟡"),
    "COM": ("Comoros",              "🇰🇲", "🔴"),
    "COD": ("DR Congo",             "🇨🇩", "🟡"),
    "COG": ("Republic of Congo",    "🇨🇬", "🟡"),
    "CIV": ("Côte d'Ivoire",        "🇨🇮", "🟢"),
    "DJI": ("Djibouti",             "🇩🇯", "🟡"),
    "EGY": ("Egypt",                "🇪🇬", "🟢"),
    "GNQ": ("Equatorial Guinea",    "🇬🇶", "🟡"),
    "ERI": ("Eritrea",              "🇪🇷", "🔴"),
    "SWZ": ("Eswatini",             "🇸🇿", "🟡"),
    "ETH": ("Ethiopia",             "🇪🇹", "🟢"),
    "GAB": ("Gabon",                "🇬🇦", "🟡"),
    "GMB": ("Gambia",               "🇬🇲", "🟡"),
    "GHA": ("Ghana",                "🇬🇭", "🟢"),
    "GIN": ("Guinea",               "🇬🇳", "🟡"),
    "GNB": ("Guinea-Bissau",        "🇬🇼", "🔴"),
    "KEN": ("Kenya",                "🇰🇪", "🟢"),
    "LSO": ("Lesotho",              "🇱🇸", "🟡"),
    "LBR": ("Liberia",              "🇱🇷", "🟡"),
    "LBY": ("Libya",                "🇱🇾", "🔴"),
    "MDG": ("Madagascar",           "🇲🇬", "🟡"),
    "MWI": ("Malawi",               "🇲🇼", "🟡"),
    "MLI": ("Mali",                 "🇲🇱", "🟡"),
    "MRT": ("Mauritania",           "🇲🇷", "🟡"),
    "MUS": ("Mauritius",            "🇲🇺", "🟢"),
    "MAR": ("Morocco",              "🇲🇦", "🟢"),
    "MOZ": ("Mozambique",           "🇲🇿", "🟡"),
    "NAM": ("Namibia",              "🇳🇦", "🟢"),
    "NER": ("Niger",                "🇳🇪", "🟡"),
    "NGA": ("Nigeria",              "🇳🇬", "🟢"),
    "RWA": ("Rwanda",               "🇷🇼", "🟢"),
    "STP": ("São Tomé & Príncipe",  "🇸🇹", "🔴"),
    "SEN": ("Senegal",              "🇸🇳", "🟢"),
    "SLE": ("Sierra Leone",         "🇸🇱", "🟡"),
    "SOM": ("Somalia",              "🇸🇴", "🔴"),
    "ZAF": ("South Africa",         "🇿🇦", "🟢"),
    "SSD": ("South Sudan",          "🇸🇸", "🔴"),
    "SDN": ("Sudan",                "🇸🇩", "🔴"),
    "TZA": ("Tanzania",             "🇹🇿", "🟢"),
    "TGO": ("Togo",                 "🇹🇬", "🟡"),
    "TUN": ("Tunisia",              "🇹🇳", "🟢"),
    "UGA": ("Uganda",               "🇺🇬", "🟢"),
    "ZMB": ("Zambia",               "🇿🇲", "🟢"),
    "ZWE": ("Zimbabwe",             "🇿🇼", "🟡"),
    "SYC": ("Seychelles",           "🇸🇨", "🟡"),
}
COUNTRY_OPTIONS = {
    code: f"{info[2]} {info[1]} {info[0]}"
    for code, info in sorted(AFRICA_COUNTRIES.items(), key=lambda x: x[1][0])
}

# ── World Bank indicators ─────────────────────────────────────────────────────
WB_INDICATORS = {
    "GDP_B":         "NY.GDP.MKTP.CD",
    "GDP_Growth":    "NY.GDP.MKTP.KD.ZG",
    "GDP_PerCapita": "NY.GDP.PCAP.CD",
    "Inflation":     "FP.CPI.TOTL.ZG",
    "Unemployment":  "SL.UEM.TOTL.ZS",
    "Exports_GDP":   "NE.EXP.GNFS.ZS",
    "Imports_GDP":   "NE.IMP.GNFS.ZS",
    "Public_Debt":   "GC.DOD.TOTL.GD.ZS",
}

# ── Kenya fallback ────────────────────────────────────────────────────────────
KENYA_FALLBACK = {
    "Year":          list(range(2000, 2024)),
    "GDP_B":         [12.7,13.3,13.4,14.0,15.1,18.7,22.5,27.2,30.6,29.5,
                      32.2,34.0,41.1,47.6,60.9,63.4,70.5,79.3,87.8,95.5,
                      98.8,99.2,110.4,107.9],
    "GDP_Growth":    [0.6,4.5,0.3,2.9,4.6,5.9,6.5,6.9,1.5,2.7,
                      8.4,6.1,4.6,5.9,5.4,5.7,5.9,4.9,6.3,5.4,
                      -0.3,7.6,4.8,5.6],
    "GDP_PerCapita": [381,394,393,404,426,515,604,713,780,738,
                      789,816,972,1104,1378,1402,1517,1672,1818,1939,
                      1965,1944,2121,2043],
    "Inflation":     [10.0,5.8,2.0,9.8,11.6,10.3,6.0,4.3,26.2,10.5,
                      4.0,14.0,9.4,5.7,6.9,6.6,6.3,8.0,4.7,5.2,
                      5.3,6.1,9.1,6.3],
    "Unemployment":  [9.8,9.8,9.8,9.8,9.8,9.3,8.7,8.1,7.4,6.7,
                      6.1,5.5,4.9,4.4,3.9,3.5,2.8,3.5,4.3,5.0,
                      5.6,5.7,5.7,5.6],
    "Exports_GDP":   [25.2,24.8,23.6,23.0,24.0,23.8,23.0,24.5,24.1,20.4,
                      21.2,21.0,19.5,18.3,16.9,15.7,14.6,13.8,13.9,13.5,
                      12.4,13.5,14.2,13.8],
    "Imports_GDP":   [33.1,32.5,31.6,30.5,32.0,31.8,33.0,37.2,42.4,36.3,
                      36.1,40.0,38.5,37.3,34.5,32.5,30.6,29.8,31.9,29.5,
                      26.7,28.0,32.6,31.2],
    "Public_Debt":   [53.2,51.8,49.0,46.5,44.2,42.0,40.1,38.5,36.8,42.0,
                      43.5,44.9,43.1,43.2,44.5,48.2,52.4,55.1,58.3,62.1,
                      68.4,70.1,69.3,71.2],
}

# ── Static data for Africa map (latest values) ────────────────────────────────
# Approximate latest values for choropleth (used when API unavailable)
AFRICA_MAP_DATA = {
    "DZA": {"GDP_Growth": 3.5, "Inflation": 9.3, "Unemployment": 11.7, "GDP_PerCapita": 3691, "Public_Debt": 57.8},
    "AGO": {"GDP_Growth": 1.1, "Inflation": 13.2, "Unemployment": 7.7,  "GDP_PerCapita": 1987, "Public_Debt": 87.3},
    "BEN": {"GDP_Growth": 6.0, "Inflation": 2.7,  "Unemployment": 1.4,  "GDP_PerCapita": 1321, "Public_Debt": 53.5},
    "BWA": {"GDP_Growth": 5.5, "Inflation": 8.5,  "Unemployment": 17.6, "GDP_PerCapita": 7370, "Public_Debt": 20.1},
    "BFA": {"GDP_Growth": 1.5, "Inflation": 14.1, "Unemployment": 4.9,  "GDP_PerCapita": 833,  "Public_Debt": 61.2},
    "BDI": {"GDP_Growth": 1.8, "Inflation": 28.1, "Unemployment": 1.1,  "GDP_PerCapita": 265,  "Public_Debt": 68.3},
    "CPV": {"GDP_Growth": 4.8, "Inflation": 7.1,  "Unemployment": 11.3, "GDP_PerCapita": 3861, "Public_Debt": 128.7},
    "CMR": {"GDP_Growth": 3.8, "Inflation": 7.4,  "Unemployment": 3.6,  "GDP_PerCapita": 1620, "Public_Debt": 47.3},
    "CAF": {"GDP_Growth": 1.0, "Inflation": 5.6,  "Unemployment": 6.8,  "GDP_PerCapita": 492,  "Public_Debt": 48.9},
    "TCD": {"GDP_Growth": 3.3, "Inflation": 4.0,  "Unemployment": 1.7,  "GDP_PerCapita": 696,  "Public_Debt": 42.1},
    "COM": {"GDP_Growth": 2.0, "Inflation": 11.1, "Unemployment": 4.0,  "GDP_PerCapita": 1387, "Public_Debt": 29.5},
    "COD": {"GDP_Growth": 8.3, "Inflation": 18.2, "Unemployment": 4.5,  "GDP_PerCapita": 565,  "Public_Debt": 14.6},
    "COG": {"GDP_Growth": 1.4, "Inflation": 3.0,  "Unemployment": 8.1,  "GDP_PerCapita": 2074, "Public_Debt": 93.5},
    "CIV": {"GDP_Growth": 6.7, "Inflation": 4.2,  "Unemployment": 3.4,  "GDP_PerCapita": 2286, "Public_Debt": 56.8},
    "DJI": {"GDP_Growth": 6.5, "Inflation": 4.0,  "Unemployment": 26.0, "GDP_PerCapita": 3460, "Public_Debt": 43.0},
    "EGY": {"GDP_Growth": 3.8, "Inflation": 29.8, "Unemployment": 7.1,  "GDP_PerCapita": 3201, "Public_Debt": 95.8},
    "GNQ": {"GDP_Growth":-5.0, "Inflation": 4.8,  "Unemployment": 8.6,  "GDP_PerCapita": 6732, "Public_Debt": 43.1},
    "ERI": {"GDP_Growth": 2.9, "Inflation": 6.3,  "Unemployment": 5.8,  "GDP_PerCapita": 598,  "Public_Debt": 175.2},
    "SWZ": {"GDP_Growth": 2.4, "Inflation": 4.8,  "Unemployment": 22.7, "GDP_PerCapita": 4156, "Public_Debt": 41.1},
    "ETH": {"GDP_Growth": 6.1, "Inflation": 33.9, "Unemployment": 3.3,  "GDP_PerCapita": 925,  "Public_Debt": 55.0},
    "GAB": {"GDP_Growth": 2.3, "Inflation": 3.4,  "Unemployment": 19.0, "GDP_PerCapita": 7562, "Public_Debt": 65.4},
    "GMB": {"GDP_Growth": 4.3, "Inflation": 11.9, "Unemployment": 9.1,  "GDP_PerCapita": 756,  "Public_Debt": 79.9},
    "GHA": {"GDP_Growth": 2.9, "Inflation": 38.1, "Unemployment": 4.5,  "GDP_PerCapita": 2390, "Public_Debt": 88.1},
    "GIN": {"GDP_Growth": 4.7, "Inflation": 10.5, "Unemployment": 5.1,  "GDP_PerCapita": 1093, "Public_Debt": 35.8},
    "GNB": {"GDP_Growth": 4.2, "Inflation": 7.4,  "Unemployment": 3.1,  "GDP_PerCapita": 757,  "Public_Debt": 78.2},
    "KEN": {"GDP_Growth": 5.6, "Inflation": 6.3,  "Unemployment": 5.6,  "GDP_PerCapita": 2043, "Public_Debt": 71.2},
    "LSO": {"GDP_Growth": 2.0, "Inflation": 6.3,  "Unemployment": 24.0, "GDP_PerCapita": 1038, "Public_Debt": 55.8},
    "LBR": {"GDP_Growth": 4.8, "Inflation": 7.6,  "Unemployment": 2.8,  "GDP_PerCapita": 650,  "Public_Debt": 61.5},
    "LBY": {"GDP_Growth": 17.9,"Inflation": 3.9,  "Unemployment": 19.6, "GDP_PerCapita": 6888, "Public_Debt": 5.9},
    "MDG": {"GDP_Growth": 4.0, "Inflation": 9.7,  "Unemployment": 1.8,  "GDP_PerCapita": 519,  "Public_Debt": 54.6},
    "MWI": {"GDP_Growth": 0.9, "Inflation": 26.6, "Unemployment": 5.7,  "GDP_PerCapita": 598,  "Public_Debt": 82.1},
    "MLI": {"GDP_Growth": 2.0, "Inflation": 9.7,  "Unemployment": 7.8,  "GDP_PerCapita": 876,  "Public_Debt": 54.4},
    "MRT": {"GDP_Growth": 5.2, "Inflation": 9.5,  "Unemployment": 10.7, "GDP_PerCapita": 1771, "Public_Debt": 60.4},
    "MUS": {"GDP_Growth": 7.0, "Inflation": 10.8, "Unemployment": 8.0,  "GDP_PerCapita": 10267,"Public_Debt": 81.0},
    "MAR": {"GDP_Growth": 3.0, "Inflation": 6.6,  "Unemployment": 12.9, "GDP_PerCapita": 3442, "Public_Debt": 70.2},
    "MOZ": {"GDP_Growth": 5.0, "Inflation": 9.8,  "Unemployment": 3.2,  "GDP_PerCapita": 502,  "Public_Debt": 99.6},
    "NAM": {"GDP_Growth": 4.2, "Inflation": 6.2,  "Unemployment": 19.9, "GDP_PerCapita": 4852, "Public_Debt": 68.4},
    "NER": {"GDP_Growth": 7.3, "Inflation": 3.6,  "Unemployment": 0.5,  "GDP_PerCapita": 571,  "Public_Debt": 52.2},
    "NGA": {"GDP_Growth": 3.3, "Inflation": 24.7, "Unemployment": 5.3,  "GDP_PerCapita": 2184, "Public_Debt": 38.8},
    "RWA": {"GDP_Growth": 8.2, "Inflation": 13.5, "Unemployment": 14.3, "GDP_PerCapita": 930,  "Public_Debt": 72.5},
    "STP": {"GDP_Growth": 0.5, "Inflation": 18.3, "Unemployment": 12.2, "GDP_PerCapita": 2278, "Public_Debt": 103.1},
    "SEN": {"GDP_Growth": 4.2, "Inflation": 9.7,  "Unemployment": 19.1, "GDP_PerCapita": 1549, "Public_Debt": 76.1},
    "SLE": {"GDP_Growth": 3.5, "Inflation": 43.5, "Unemployment": 4.2,  "GDP_PerCapita": 478,  "Public_Debt": 81.3},
    "SOM": {"GDP_Growth": 3.0, "Inflation": 6.0,  "Unemployment": 14.5, "GDP_PerCapita": 450,  "Public_Debt": 63.1},
    "ZAF": {"GDP_Growth": 1.9, "Inflation": 6.1,  "Unemployment": 31.9, "GDP_PerCapita": 6001, "Public_Debt": 73.2},
    "SSD": {"GDP_Growth":-2.3, "Inflation": 30.0, "Unemployment": 12.0, "GDP_PerCapita": 441,  "Public_Debt": 62.3},
    "SDN": {"GDP_Growth":-0.3, "Inflation": 138.8,"Unemployment": 11.8, "GDP_PerCapita": 648,  "Public_Debt": 212.0},
    "TZA": {"GDP_Growth": 4.7, "Inflation": 4.3,  "Unemployment": 2.6,  "GDP_PerCapita": 1102, "Public_Debt": 42.3},
    "TGO": {"GDP_Growth": 5.8, "Inflation": 7.7,  "Unemployment": 3.9,  "GDP_PerCapita": 914,  "Public_Debt": 68.0},
    "TUN": {"GDP_Growth": 2.4, "Inflation": 9.3,  "Unemployment": 15.2, "GDP_PerCapita": 3807, "Public_Debt": 82.5},
    "UGA": {"GDP_Growth": 5.3, "Inflation": 7.2,  "Unemployment": 2.8,  "GDP_PerCapita": 883,  "Public_Debt": 52.7},
    "ZMB": {"GDP_Growth": 4.7, "Inflation": 12.4, "Unemployment": 13.2, "GDP_PerCapita": 1300, "Public_Debt": 138.6},
    "ZWE": {"GDP_Growth": 5.3, "Inflation": 87.6, "Unemployment": 5.2,  "GDP_PerCapita": 1509, "Public_Debt": 95.1},
    "SYC": {"GDP_Growth": 4.5, "Inflation": 2.6,  "Unemployment": 3.3,  "GDP_PerCapita": 11234,"Public_Debt": 65.3},
}

# ── Data helpers ──────────────────────────────────────────────────────────────
def _enrich(df):
    df["Trade_Balance"] = df["Exports_GDP"] - df["Imports_GDP"]
    df["Era"] = df["Year"].apply(
        lambda y: "🔴 COVID" if 2020 <= y <= 2021
        else ("🟡 Post-COVID" if y >= 2022
        else ("🟢 Growth" if y >= 2010 else "🔵 Early 2000s"))
    )
    return df.reset_index(drop=True)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_single_country(iso3: str):
    try:
        import wbgapi as wb
        frames = []
        for col, code in WB_INDICATORS.items():
            s = wb.data.DataFrame(code, iso3, mrv=30, numericTimeKeys=True)
            s = s.T.reset_index()
            s.columns = ["Year", col]
            s["Year"] = s["Year"].astype(int)
            frames.append(s.set_index("Year"))
        df = pd.concat(frames, axis=1).reset_index()
        df = df[df["Year"] >= 2000].sort_values("Year")
        df["GDP_B"] = df["GDP_B"] / 1e9
        if "GDP_PerCapita" not in df.columns:
            df["GDP_PerCapita"] = np.nan
        if "Public_Debt" not in df.columns:
            df["Public_Debt"] = np.nan
        return _enrich(df), "live"
    except Exception:
        if iso3 == "KEN":
            return _enrich(pd.DataFrame(KENYA_FALLBACK)), "cached"
        return None, "unavailable"

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_primary_country(iso3: str):
    return fetch_single_country(iso3)

def compute_health_score(row):
    """
    Economic Health Score (0–100) based on 5 indicators.
    Higher is better.
    """
    score = 50.0  # baseline
    # GDP Growth: ideal ~5%, penalize negatives
    gdp_g = row.get("GDP_Growth", np.nan)
    if not np.isnan(gdp_g):
        score += min(gdp_g * 2, 20) if gdp_g > 0 else gdp_g * 3

    # Inflation: ideal <5%, penalize high
    inf = row.get("Inflation", np.nan)
    if not np.isnan(inf):
        if inf <= 5:
            score += 10
        elif inf <= 10:
            score += 5
        elif inf <= 20:
            score -= 5
        else:
            score -= 15

    # Unemployment: lower is better
    unemp = row.get("Unemployment", np.nan)
    if not np.isnan(unemp):
        score -= min(unemp * 0.5, 15)

    # GDP per Capita: log scale bonus
    gdp_pc = row.get("GDP_PerCapita", np.nan)
    if not np.isnan(gdp_pc) and gdp_pc > 0:
        score += min(np.log10(gdp_pc) * 5, 15)

    # Public Debt: < 40% great, > 100% terrible
    debt = row.get("Public_Debt", np.nan)
    if not np.isnan(debt):
        if debt < 40:
            score += 10
        elif debt < 60:
            score += 5
        elif debt < 80:
            score -= 0
        elif debt < 100:
            score -= 5
        else:
            score -= 15

    return max(0, min(100, score))

# ── Gemini AI helper ──────────────────────────────────────────────────────────
def build_data_summary(df, country_name, year_range):
    dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()
    latest = dff.iloc[-1]
    lines = [
        f"Country: {country_name}",
        f"Period: {year_range[0]}–{year_range[1]}",
        f"Latest Year: {int(latest['Year'])}",
        f"GDP: ${latest['GDP_B']:.1f}B (growth: {latest['GDP_Growth']:.1f}%)",
        f"GDP per Capita: ${latest.get('GDP_PerCapita', 'N/A')}",
        f"Inflation: {latest['Inflation']:.1f}%",
        f"Unemployment: {latest['Unemployment']:.1f}%",
        f"Trade Balance: {latest['Trade_Balance']:.1f}% of GDP",
        f"Public Debt: {latest.get('Public_Debt', 'N/A')}% of GDP",
        "",
        "Year-by-year GDP growth (%):",
        ", ".join([f"{int(r.Year)}: {r.GDP_Growth:.1f}%" for _, r in dff.iterrows() if not pd.isna(r.GDP_Growth)]),
        "",
        "Year-by-year Inflation (%):",
        ", ".join([f"{int(r.Year)}: {r.Inflation:.1f}%" for _, r in dff.iterrows() if not pd.isna(r.Inflation)]),
        "",
        f"Avg GDP Growth: {dff['GDP_Growth'].mean():.1f}%",
        f"Peak Inflation: {dff['Inflation'].max():.1f}% in {int(dff.loc[dff['Inflation'].idxmax(), 'Year'])}",
        f"Lowest Unemployment: {dff['Unemployment'].min():.1f}% in {int(dff.loc[dff['Unemployment'].idxmin(), 'Year'])}",
    ]
    return "\n".join(lines)

def call_gemini(prompt: str, api_key: str) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except ImportError:
        return "❌ google-generativeai not installed. Run: pip install google-generativeai"
    except Exception as e:
        return f"❌ Gemini error: {str(e)}"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌍 Africa Economic Intelligence")
    st.markdown("---")

    st.markdown("**PRIMARY COUNTRY**")
    primary_code = st.selectbox(
        "Primary country",
        options=list(COUNTRY_OPTIONS.keys()),
        format_func=lambda c: COUNTRY_OPTIONS[c],
        index=list(COUNTRY_OPTIONS.keys()).index("KEN"),
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**TIME RANGE**")
    year_range = st.slider("Years", min_value=2000, max_value=2023,
                           value=(2005, 2023), label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**INDICATORS**")
    show_gdp       = st.checkbox("GDP & Growth",        value=True)
    show_gdp_pc    = st.checkbox("GDP Per Capita",       value=True)
    show_inf       = st.checkbox("Inflation",            value=True)
    show_unemp     = st.checkbox("Unemployment",         value=True)
    show_trade     = st.checkbox("Trade Balance",        value=True)
    show_debt      = st.checkbox("Public Debt",          value=True)
    show_scatter   = st.checkbox("Correlation Analysis", value=True)
    show_stats     = st.checkbox("Statistical Summary",  value=True)

    st.markdown("---")
    st.markdown("**FORECASTING**")
    show_forecast  = st.checkbox("5-Year Forecast", value=True)
    forecast_years = st.slider("Horizon (years)", 1, 10, 5, disabled=not show_forecast)
    forecast_model = st.radio("Model",
                              ["Linear", "Polynomial (deg 2)", "Polynomial (deg 3)"],
                              disabled=not show_forecast)

    st.markdown("---")
    st.markdown("**AI INSIGHTS**")
    gemini_key = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        placeholder="AIzaSy…",
        help="Get your free key at aistudio.google.com",
    )

    st.markdown("---")
    st.markdown("**DISPLAY**")
    highlight_covid = st.toggle("Highlight COVID period", value=True)

    st.markdown("---")
    st.markdown(
        f"<small style='color:#3a4f3d'>Source: World Bank Open Data<br>"
        f"54 African countries · {datetime.now().strftime('%d %b %Y')}</small>",
        unsafe_allow_html=True,
    )

# ── Load primary country ──────────────────────────────────────────────────────
with st.spinner("Loading data…"):
    df, data_source = fetch_primary_country(primary_code)

if df is None:
    st.error(f"Could not load data for {COUNTRY_OPTIONS[primary_code]}.")
    st.stop()

last_year    = int(df["Year"].max())
country_info = AFRICA_COUNTRIES[primary_code]
country_name = country_info[0]
country_flag = country_info[1]
dff = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f"<p class='section-label'>AFRICA ECONOMIC INTELLIGENCE DASHBOARD · WORLD BANK · "
    f"{'LIVE' if data_source == 'live' else 'OFFLINE'}</p>",
    unsafe_allow_html=True,
)
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title(f"🌍 Africa Economic Intelligence Dashboard")
    st.markdown(f"**{country_flag} {country_name}** — GDP · Inflation · Unemployment · Trade · Debt &nbsp;·&nbsp; {year_range[0]}–{year_range[1]}")
with col_h2:
    badge = "badge-live" if data_source == "live" else "badge-cache"
    label = "🟢 LIVE" if data_source == "live" else "🟡 OFFLINE"
    st.markdown(f"<div style='padding-top:2rem'><span class='data-badge {badge}'>{label}</span></div>",
                unsafe_allow_html=True)
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
latest = dff.iloc[-1]
prev   = dff.iloc[-2]

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("GDP (Latest)",          f"${latest['GDP_B']:.1f}B",
          f"{latest['GDP_Growth']:+.1f}% growth")
k2.metric("GDP Per Capita",
          f"${latest['GDP_PerCapita']:,.0f}" if not pd.isna(latest.get('GDP_PerCapita', np.nan)) else "N/A",
          f"{latest['GDP_PerCapita']-prev.get('GDP_PerCapita',latest['GDP_PerCapita']):+.0f} vs prior" if not pd.isna(latest.get('GDP_PerCapita', np.nan)) else "")
k3.metric("Inflation",             f"{latest['Inflation']:.1f}%",
          f"{latest['Inflation']-prev['Inflation']:+.1f}pp vs prior year")
k4.metric("Unemployment",          f"{latest['Unemployment']:.1f}%",
          f"{latest['Unemployment']-prev['Unemployment']:+.1f}pp vs prior year")
k5.metric("Trade Balance (% GDP)", f"{latest['Trade_Balance']:.1f}%",
          f"{latest['Trade_Balance']-prev['Trade_Balance']:+.1f}pp vs prior year")
k6.metric("Public Debt (% GDP)",
          f"{latest['Public_Debt']:.1f}%" if not pd.isna(latest.get('Public_Debt', np.nan)) else "N/A",
          f"{latest['Public_Debt']-prev.get('Public_Debt',latest['Public_Debt']):+.1f}pp" if not pd.isna(latest.get('Public_Debt', np.nan)) else "")

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📈 GDP", "💰 GDP Per Capita", "🔥 Inflation", "👷 Unemployment",
    "🌍 Trade", "🏦 Public Debt", "🔗 Correlations", "🔮 Forecast",
    "🗺️ Africa Map", "🏆 Rankings", "📊 Compare", "🤖 AI Insights", "📋 Statistics",
])

# ── Shared helpers ────────────────────────────────────────────────────────────
def add_covid_band(fig):
    if highlight_covid:
        fig.add_vrect(
            x0=2019.5, x1=2021.5,
            fillcolor="rgba(232,93,74,0.08)",
            line=dict(color="rgba(232,93,74,0.3)", width=1, dash="dot"),
            annotation_text="COVID", annotation_position="top left",
            annotation_font=dict(color=COLORS["red"], size=10),
        )
    return fig

def run_forecast(years, values, horizon, model_name):
    X = np.array(years).reshape(-1, 1)
    y = np.array(values)
    if model_name == "Linear":
        model = LinearRegression()
    elif model_name == "Polynomial (deg 2)":
        model = make_pipeline(PolynomialFeatures(2), LinearRegression())
    else:
        model = make_pipeline(PolynomialFeatures(3), LinearRegression())
    model.fit(X, y)
    future = np.arange(years[-1] + 1, years[-1] + horizon + 1)
    pred   = model.predict(future.reshape(-1, 1))
    ci     = 1.96 * np.std(y - model.predict(X)) * np.sqrt(1 + 1 / len(y))
    return future.tolist(), pred.tolist(), (pred - ci).tolist(), (pred + ci).tolist()

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — GDP
# ═════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    if show_gdp:
        st.subheader(f"GDP — {country_name}")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=dff["Year"], y=dff["GDP_B"], name="GDP (USD B)",
            marker=dict(color=COLORS["green"], opacity=0.22,
                        line=dict(color=COLORS["green"], width=1)),
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=dff["Year"], y=dff["GDP_Growth"], name="GDP Growth %",
            line=dict(color=COLORS["green"], width=2.5),
            mode="lines+markers", marker=dict(size=5),
        ), secondary_y=True)
        fig.update_layout(**layout(height=380))
        fig.update_yaxes(title_text="GDP (USD B)", secondary_y=False,
                         tickprefix="$", ticksuffix="B",
                         gridcolor=COLORS["border"], linecolor=COLORS["border"])
        fig.update_yaxes(title_text="Growth %", secondary_y=True,
                         ticksuffix="%", gridcolor="rgba(0,0,0,0)")
        fig.update_xaxes(gridcolor=COLORS["border"])
        add_covid_band(fig)
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            dc = dff.copy(); dc["GDP_Change"] = dc["GDP_B"].diff()
            fig2 = go.Figure(go.Bar(
                x=dc["Year"][1:], y=dc["GDP_Change"][1:],
                marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
                              for v in dc["GDP_Change"][1:]],
                text=[f"${v:+.1f}B" for v in dc["GDP_Change"][1:]],
                textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
            ))
            fig2.update_layout(**layout(height=280, yaxis_extra=dict(tickprefix="$", ticksuffix="B")))
            add_covid_band(fig2)
            st.plotly_chart(fig2, use_container_width=True)
        with c2:
            era_avg = df.groupby("Era")["GDP_Growth"].mean().reset_index()
            fig3 = go.Figure(go.Bar(
                x=era_avg["Era"], y=era_avg["GDP_Growth"],
                marker_color=[COLORS["blue"],COLORS["red"],COLORS["green"],COLORS["yellow"]],
                text=[f"{v:.1f}%" for v in era_avg["GDP_Growth"]],
                textposition="outside", textfont=dict(size=10, color=COLORS["text"]),
            ))
            fig3.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
            st.plotly_chart(fig3, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — GDP Per Capita
# ═════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    if show_gdp_pc:
        st.subheader(f"GDP Per Capita — {country_name}")
        pc_data = dff.dropna(subset=["GDP_PerCapita"])
        if pc_data.empty:
            st.info("GDP per Capita data not available for this country.")
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=pc_data["Year"], y=pc_data["GDP_PerCapita"],
                name="GDP Per Capita (USD)",
                line=dict(color=COLORS["blue"], width=2.5),
                mode="lines+markers", marker=dict(size=6),
                fill="tozeroy", fillcolor="rgba(74,157,232,0.08)",
            ))
            # Add trend line
            if len(pc_data) > 2:
                z = np.polyfit(pc_data["Year"], pc_data["GDP_PerCapita"], 1)
                p = np.poly1d(z)
                fig.add_trace(go.Scatter(
                    x=pc_data["Year"], y=p(pc_data["Year"]),
                    name="Trend", line=dict(color=COLORS["text"], width=1.5, dash="dot"),
                    mode="lines",
                ))
            fig.update_layout(**layout(height=380,
                              yaxis_extra=dict(tickprefix="$", title="USD per person")))
            add_covid_band(fig)
            st.plotly_chart(fig, use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Current GDP/Capita", f"${pc_data.iloc[-1]['GDP_PerCapita']:,.0f}")
            c2.metric("Peak GDP/Capita",    f"${pc_data['GDP_PerCapita'].max():,.0f}",
                      f"in {int(pc_data.loc[pc_data['GDP_PerCapita'].idxmax(),'Year'])}")
            c3.metric("Lowest GDP/Capita",  f"${pc_data['GDP_PerCapita'].min():,.0f}",
                      f"in {int(pc_data.loc[pc_data['GDP_PerCapita'].idxmin(),'Year'])}")
            growth_pct = ((pc_data.iloc[-1]['GDP_PerCapita'] / pc_data.iloc[0]['GDP_PerCapita']) - 1) * 100
            c4.metric("Total Growth",       f"{growth_pct:+.1f}%",
                      f"since {int(pc_data.iloc[0]['Year'])}")

            # YoY growth bar chart
            st.markdown("#### Year-over-Year GDP Per Capita Growth")
            pc_copy = pc_data.copy()
            pc_copy["PC_Growth"] = pc_copy["GDP_PerCapita"].pct_change() * 100
            fig2 = go.Figure(go.Bar(
                x=pc_copy["Year"][1:], y=pc_copy["PC_Growth"][1:],
                marker_color=[COLORS["blue"] if v >= 0 else COLORS["red"]
                              for v in pc_copy["PC_Growth"][1:]],
                text=[f"{v:+.1f}%" for v in pc_copy["PC_Growth"][1:]],
                textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
            ))
            fig2.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
            add_covid_band(fig2)
            st.plotly_chart(fig2, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — Inflation
# ═════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    if show_inf:
        st.subheader(f"Inflation — {country_name}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(dff["Year"]) + list(dff["Year"])[::-1],
            y=[7.5]*len(dff) + [2.5]*len(dff),
            fill="toself", fillcolor="rgba(61,220,110,0.06)",
            line=dict(color="rgba(0,0,0,0)"), name="Target Band (2.5–7.5%)",
        ))
        fig.add_hline(y=7.5, line=dict(color=COLORS["red"], dash="dot", width=1),
                      annotation_text="Upper 7.5%",
                      annotation_font=dict(color=COLORS["red"], size=10))
        fig.add_hline(y=2.5, line=dict(color=COLORS["green"], dash="dot", width=1),
                      annotation_text="Lower 2.5%",
                      annotation_font=dict(color=COLORS["green"], size=10))
        fig.add_trace(go.Scatter(
            x=dff["Year"], y=dff["Inflation"], name="CPI Inflation",
            line=dict(color=COLORS["yellow"], width=2.5), mode="lines+markers",
            marker=dict(size=5, color=[
                COLORS["red"] if v > 7.5 else
                (COLORS["green"] if v < 2.5 else COLORS["yellow"])
                for v in dff["Inflation"]
            ]),
            fill="tozeroy", fillcolor="rgba(245,200,66,0.07)",
        ))
        fig.update_layout(**layout(height=380, yaxis_extra=dict(ticksuffix="%", title="CPI %")))
        add_covid_band(fig)
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            above  = (dff["Inflation"] > 7.5).sum()
            within = ((dff["Inflation"] >= 2.5) & (dff["Inflation"] <= 7.5)).sum()
            below  = (dff["Inflation"] < 2.5).sum()
            fig2 = go.Figure(go.Pie(
                labels=["Above target","Within target","Below target"],
                values=[above, within, below], hole=0.55,
                marker=dict(colors=[COLORS["red"],COLORS["green"],COLORS["blue"]]),
                textfont=dict(color=COLORS["text"]),
            ))
            fig2.update_layout(**layout(height=280),
                               title=dict(text="Years Within Target Band",
                                          font=dict(color=COLORS["text"])))
            st.plotly_chart(fig2, use_container_width=True)
        with c2:
            fig3 = go.Figure(go.Histogram(
                x=dff["Inflation"], nbinsx=10,
                marker=dict(color=COLORS["yellow"], opacity=0.7,
                            line=dict(color=COLORS["bg"], width=1)),
            ))
            fig3.add_vline(x=dff["Inflation"].mean(),
                           line=dict(color=COLORS["text"], dash="dash", width=1.5),
                           annotation_text=f"Mean: {dff['Inflation'].mean():.1f}%",
                           annotation_font=dict(color=COLORS["text"], size=10))
            fig3.update_layout(**layout(height=280,
                               xaxis_extra=dict(title="Inflation %"),
                               yaxis_extra=dict(title="Count")))
            st.plotly_chart(fig3, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — Unemployment
# ═════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    if show_unemp:
        st.subheader(f"Unemployment — {country_name}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dff["Year"], y=dff["Unemployment"], name="Unemployment %",
            line=dict(color=COLORS["red"], width=2.5), mode="lines+markers",
            marker=dict(size=6), fill="tozeroy", fillcolor="rgba(232,93,74,0.1)",
        ))
        dc2 = dff.copy()
        dc2["MA3"] = dc2["Unemployment"].rolling(3, center=True).mean()
        fig.add_trace(go.Scatter(
            x=dc2["Year"], y=dc2["MA3"], name="3-Year Rolling Avg",
            line=dict(color=COLORS["text"], width=1.5, dash="dot"), mode="lines",
        ))
        fig.update_layout(**layout(height=360,
                          yaxis_extra=dict(ticksuffix="%", title="Unemployment %")))
        add_covid_band(fig)
        st.plotly_chart(fig, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Peak",    f"{dff['Unemployment'].max():.1f}%",
                  f"in {int(dff.loc[dff['Unemployment'].idxmax(),'Year'])}")
        c2.metric("Lowest",  f"{dff['Unemployment'].min():.1f}%",
                  f"in {int(dff.loc[dff['Unemployment'].idxmin(),'Year'])}")
        c3.metric("Average", f"{dff['Unemployment'].mean():.1f}%", "ILO modeled")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 5 — Trade
# ═════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    if show_trade:
        st.subheader(f"Trade Balance — {country_name}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dff["Year"], y=dff["Exports_GDP"], name="Exports % GDP",
            line=dict(color=COLORS["blue"], width=2.5),
            mode="lines+markers", marker=dict(size=4),
        ))
        fig.add_trace(go.Scatter(
            x=dff["Year"], y=dff["Imports_GDP"], name="Imports % GDP",
            line=dict(color=COLORS["yellow"], width=2.5),
            mode="lines+markers", marker=dict(size=4),
        ))
        fig.add_trace(go.Scatter(
            x=list(dff["Year"]) + list(dff["Year"])[::-1],
            y=list(dff["Imports_GDP"]) + list(dff["Exports_GDP"])[::-1],
            fill="toself", fillcolor="rgba(232,93,74,0.08)",
            line=dict(color="rgba(0,0,0,0)"), name="Trade Deficit",
        ))
        fig.update_layout(**layout(height=360, yaxis_extra=dict(ticksuffix="%", title="% of GDP")))
        add_covid_band(fig)
        st.plotly_chart(fig, use_container_width=True)

        fig2 = go.Figure(go.Bar(
            x=dff["Year"], y=dff["Trade_Balance"],
            marker_color=[COLORS["green"] if v >= 0 else COLORS["red"]
                          for v in dff["Trade_Balance"]],
            text=[f"{v:.1f}%" for v in dff["Trade_Balance"]],
            textposition="outside", textfont=dict(size=9, color=COLORS["muted"]),
        ))
        fig2.add_hline(y=0, line=dict(color=COLORS["muted"], width=1))
        fig2.update_layout(**layout(height=280, yaxis_extra=dict(ticksuffix="%")))
        add_covid_band(fig2)
        st.plotly_chart(fig2, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 6 — Public Debt
# ═════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    if show_debt:
        st.subheader(f"Public Debt — {country_name}")
        debt_data = dff.dropna(subset=["Public_Debt"])
        if debt_data.empty:
            st.info("Public Debt data not available for this country in this date range.")
        else:
            fig = go.Figure()
            fig.add_hrect(y0=0, y1=40, fillcolor="rgba(61,220,110,0.05)",
                          line=dict(color="rgba(0,0,0,0)"), annotation_text="Low Debt Zone (< 40%)",
                          annotation_font=dict(color=COLORS["green"], size=10))
            fig.add_hrect(y0=60, y1=max(debt_data["Public_Debt"].max()+10, 100),
                          fillcolor="rgba(232,93,74,0.05)",
                          line=dict(color="rgba(0,0,0,0)"), annotation_text="High Risk Zone (> 60%)",
                          annotation_font=dict(color=COLORS["red"], size=10))
            fig.add_hline(y=60, line=dict(color=COLORS["yellow"], dash="dot", width=1.5),
                          annotation_text="IMF Threshold 60%",
                          annotation_font=dict(color=COLORS["yellow"], size=10))
            fig.add_trace(go.Scatter(
                x=debt_data["Year"], y=debt_data["Public_Debt"],
                name="Public Debt % GDP",
                line=dict(color=COLORS["purple"], width=2.5),
                mode="lines+markers", marker=dict(size=6,
                    color=[COLORS["green"] if v < 40 else
                           (COLORS["yellow"] if v < 60 else COLORS["red"])
                           for v in debt_data["Public_Debt"]]),
                fill="tozeroy", fillcolor="rgba(167,139,250,0.08)",
            ))
            fig.update_layout(**layout(height=400,
                              yaxis_extra=dict(ticksuffix="%", title="% of GDP")))
            add_covid_band(fig)
            st.plotly_chart(fig, use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Current Debt",  f"{debt_data.iloc[-1]['Public_Debt']:.1f}%",
                      "of GDP")
            c2.metric("Peak Debt",     f"{debt_data['Public_Debt'].max():.1f}%",
                      f"in {int(debt_data.loc[debt_data['Public_Debt'].idxmax(),'Year'])}")
            c3.metric("Lowest Debt",   f"{debt_data['Public_Debt'].min():.1f}%",
                      f"in {int(debt_data.loc[debt_data['Public_Debt'].idxmin(),'Year'])}")
            risk = "🟢 Sustainable" if debt_data.iloc[-1]["Public_Debt"] < 60 else (
                   "🟡 Moderate Risk" if debt_data.iloc[-1]["Public_Debt"] < 80 else "🔴 High Risk")
            c4.metric("Debt Risk",     risk, "IMF framework")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 7 — Correlations
# ═════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    if show_scatter:
        st.subheader(f"Correlation Analysis — {country_name}")
        c1, c2 = st.columns(2)
        with c1:
            sl, ic, r, p, _ = stats.linregress(dff["GDP_Growth"], dff["Unemployment"])
            tx = np.linspace(dff["GDP_Growth"].min(), dff["GDP_Growth"].max(), 100)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dff["GDP_Growth"], y=dff["Unemployment"],
                mode="markers+text", text=dff["Year"],
                textposition="top center",
                textfont=dict(size=9, color=COLORS["muted"]),
                marker=dict(size=10, color=dff["Year"],
                            colorscale=[[0,COLORS["blue"]],[0.86,COLORS["red"]],[1,COLORS["green"]]],
                            showscale=True,
                            colorbar=dict(title="Year", tickfont=dict(color=COLORS["muted"]))),
                name="Observations",
            ))
            fig.add_trace(go.Scatter(
                x=tx, y=sl*tx+ic, mode="lines",
                line=dict(color=COLORS["text"], dash="dash", width=1.5),
                name=f"Trend (R²={r**2:.2f})",
            ))
            fig.update_layout(**layout(height=360,
                              xaxis_extra=dict(title="GDP Growth %", ticksuffix="%"),
                              yaxis_extra=dict(title="Unemployment %", ticksuffix="%")))
            st.plotly_chart(fig, use_container_width=True)
            st.caption(f"Pearson r = {r:.3f} | R² = {r**2:.3f} | p = {p:.4f}")

        with c2:
            sl2, ic2, r2, p2, _ = stats.linregress(dff["Inflation"], dff["GDP_Growth"])
            tx2 = np.linspace(dff["Inflation"].min(), dff["Inflation"].max(), 100)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=dff["Inflation"], y=dff["GDP_Growth"],
                mode="markers+text", text=dff["Year"],
                textposition="top center",
                textfont=dict(size=9, color=COLORS["muted"]),
                marker=dict(size=10, color=COLORS["yellow"], opacity=0.8),
                name="Observations",
            ))
            fig2.add_trace(go.Scatter(
                x=tx2, y=sl2*tx2+ic2, mode="lines",
                line=dict(color=COLORS["text"], dash="dash", width=1.5),
                name=f"Trend (R²={r2**2:.2f})",
            ))
            fig2.update_layout(**layout(height=360,
                               xaxis_extra=dict(title="Inflation %", ticksuffix="%"),
                               yaxis_extra=dict(title="GDP Growth %", ticksuffix="%")))
            st.plotly_chart(fig2, use_container_width=True)
            st.caption(f"Pearson r = {r2:.3f} | R² = {r2**2:.3f} | p = {p2:.4f}")

        corr_cols   = ["GDP_B","GDP_Growth","Inflation","Unemployment",
                       "Exports_GDP","Imports_GDP","Trade_Balance"]
        corr_labels = ["GDP (B)","GDP Growth","Inflation","Unemployment",
                       "Exports","Imports","Trade Bal."]
        corr = dff[corr_cols].corr().values
        fig3 = go.Figure(go.Heatmap(
            z=corr, x=corr_labels, y=corr_labels,
            colorscale=[[0,COLORS["red"]],[0.5,COLORS["surface"]],[1,COLORS["green"]]],
            zmid=0, zmin=-1, zmax=1,
            text=[[f"{v:.2f}" for v in row] for row in corr],
            texttemplate="%{text}", textfont=dict(size=11, color=COLORS["text"]),
        ))
        fig3.update_layout(**layout(height=380))
        st.plotly_chart(fig3, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 8 — Forecast
# ═════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    if show_forecast:
        st.subheader(f"Forecast — {country_name} · {last_year+1}–{last_year+forecast_years}")
        st.caption(f"Model: **{forecast_model}** | Trained on {year_range[0]}–{last_year} | Shaded = 95% CI")

        train = df[(df["Year"] >= year_range[0]) & (df["Year"] <= last_year)].dropna()
        indicators = [
            ("GDP_Growth",   "GDP Growth %",     COLORS["green"],  "%",  ""),
            ("GDP_B",        "GDP (USD Billion)", COLORS["green"],  "B",  "$"),
            ("Inflation",    "Inflation %",       COLORS["yellow"], "%",  ""),
            ("Unemployment", "Unemployment %",    COLORS["red"],    "%",  ""),
            ("GDP_PerCapita","GDP Per Capita",     COLORS["blue"],   "",   "$"),
            ("Public_Debt",  "Public Debt % GDP", COLORS["purple"], "%",  ""),
        ]
        fc1, fc2 = st.columns(2)
        forecast_results = {}

        for i, (col, label, color, unit, prefix) in enumerate(indicators):
            valid = train[["Year", col]].dropna()
            if len(valid) < 3:
                continue
            fut_yrs, pred, lo, hi = run_forecast(
                valid["Year"].tolist(), valid[col].tolist(),
                forecast_years, forecast_model,
            )
            forecast_results[col] = {"years": fut_yrs, "pred": pred}
            rh = int(color[1:3],16); rg = int(color[3:5],16); rb = int(color[5:7],16)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=valid["Year"], y=valid[col], name="Historical",
                line=dict(color=color, width=2.5), mode="lines+markers",
                marker=dict(size=4),
            ))
            fig.add_trace(go.Scatter(
                x=fut_yrs + fut_yrs[::-1], y=hi + lo[::-1],
                fill="toself", fillcolor=f"rgba({rh},{rg},{rb},0.12)",
                line=dict(color="rgba(0,0,0,0)"), name="95% CI",
            ))
            fig.add_trace(go.Scatter(
                x=fut_yrs, y=pred, name="Forecast",
                line=dict(color=color, width=2, dash="dash"),
                mode="lines+markers", marker=dict(size=6, symbol="diamond"),
            ))
            fig.add_vline(x=last_year + 0.5,
                          line=dict(color=COLORS["muted"], dash="dot", width=1),
                          annotation_text="Forecast →",
                          annotation_font=dict(color=COLORS["muted"], size=9))
            add_covid_band(fig)
            tick_suf = "" if col in ("GDP_B","GDP_PerCapita") else unit
            tick_pre = prefix
            fig.update_layout(**layout(height=300,
                              yaxis_extra=dict(title=label, ticksuffix=tick_suf, tickprefix=tick_pre)))
            with (fc1 if i % 2 == 0 else fc2):
                st.plotly_chart(fig, use_container_width=True)

        if forecast_results:
            st.markdown("---")
            st.markdown("**📋 Forecast Summary**")
            rows = []
            ref = list(forecast_results.keys())[0]
            lbl_map = {"GDP_Growth":"GDP Growth %","GDP_B":"GDP (USD B)",
                       "Inflation":"Inflation %","Unemployment":"Unemployment %",
                       "GDP_PerCapita":"GDP Per Capita","Public_Debt":"Public Debt %"}
            for idx, yr in enumerate(forecast_results[ref]["years"]):
                row = {"Year": yr}
                for col, res in forecast_results.items():
                    if col in ("GDP_B","GDP_PerCapita"):
                        fmt = f"${res['pred'][idx]:.1f}" + ("B" if col=="GDP_B" else "")
                    else:
                        fmt = f"{res['pred'][idx]:.1f}%"
                    row[lbl_map.get(col, col)] = fmt
                rows.append(row)
            st.dataframe(pd.DataFrame(rows).set_index("Year"), use_container_width=True)
    else:
        st.info("Enable **5-Year Forecast** in the sidebar.")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 9 — Africa Choropleth Map
# ═════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    st.subheader("🗺️ Africa Economic Map")
    st.caption("Choropleth map showing economic indicators across all 54 African nations")

    map_col1, map_col2 = st.columns([2, 1])
    with map_col1:
        map_indicator = st.selectbox(
            "Select Indicator",
            options=["GDP_Growth", "Inflation", "Unemployment", "GDP_PerCapita", "Public_Debt"],
            format_func=lambda x: {
                "GDP_Growth":    "📈 GDP Growth (%)",
                "Inflation":     "🔥 Inflation (%)",
                "Unemployment":  "👷 Unemployment (%)",
                "GDP_PerCapita": "💰 GDP Per Capita (USD)",
                "Public_Debt":   "🏦 Public Debt (% of GDP)",
            }[x],
            key="map_indicator",
        )
    with map_col2:
        map_colorscale = st.selectbox(
            "Color Scale",
            options=["RdYlGn", "RdYlGn_r", "Viridis", "Plasma", "Blues"],
            index=0,
            key="map_colorscale",
        )

    # Build map dataframe
    map_rows = []
    for code, vals in AFRICA_MAP_DATA.items():
        country_n = AFRICA_COUNTRIES[code][0]
        val = vals.get(map_indicator, np.nan)
        map_rows.append({
            "iso_alpha3": code,
            "Country": country_n,
            "Value": val,
        })
    map_df = pd.DataFrame(map_rows)

    # Indicator metadata for display
    ind_meta = {
        "GDP_Growth":    ("GDP Growth (%)",       "%",  "RdYlGn",   "Latest GDP Growth Rate"),
        "Inflation":     ("Inflation (%)",         "%",  "RdYlGn_r", "Latest CPI Inflation Rate"),
        "Unemployment":  ("Unemployment (%)",      "%",  "RdYlGn_r", "Latest Unemployment Rate"),
        "GDP_PerCapita": ("GDP Per Capita (USD)",  "$",  "Viridis",  "Latest GDP Per Capita"),
        "Public_Debt":   ("Public Debt (% GDP)",   "%",  "RdYlGn_r", "Public Debt as % of GDP"),
    }
    ind_label, ind_unit, default_cs, ind_title = ind_meta[map_indicator]
    colorscale_to_use = map_colorscale

    fig_map = go.Figure(go.Choropleth(
        locations=map_df["iso_alpha3"],
        z=map_df["Value"],
        text=map_df["Country"],
        customdata=np.stack([
            map_df["Country"],
            map_df["Value"].apply(lambda v: f"{ind_unit}{v:,.1f}" if ind_unit=="$" else f"{v:.1f}{ind_unit}")
        ], axis=-1),
        hovertemplate="<b>%{customdata[0]}</b><br>" + ind_label + ": %{customdata[1]}<extra></extra>",
        colorscale=colorscale_to_use,
        autocolorscale=False,
        reversescale=False,
        marker=dict(line=dict(color="#0a0f0d", width=0.5)),
        colorbar=dict(
            title=dict(text=ind_label, font=dict(color=COLORS["text"], size=12)),
            tickfont=dict(color=COLORS["muted"]),
            bgcolor=COLORS["surface"],
            bordercolor=COLORS["border"],
            borderwidth=1,
            thickness=15,
            len=0.75,
        ),
    ))

    fig_map.update_layout(
        title=dict(
            text=f"Africa — {ind_title}",
            font=dict(color=COLORS["text"], size=16),
            x=0.5,
        ),
        geo=dict(
            scope="africa",
            showframe=False,
            showcoastlines=True,
            coastlinecolor=COLORS["border"],
            showland=True,
            landcolor="#111812",
            showocean=True,
            oceancolor="#0a0f0d",
            showcountries=True,
            countrycolor=COLORS["border"],
            bgcolor=COLORS["bg"],
            projection_type="mercator",
            lataxis_range=[-35, 38],
            lonaxis_range=[-18, 52],
        ),
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["bg"],
        font=dict(color=COLORS["muted"], family="DM Mono, monospace"),
        margin=dict(t=60, b=20, l=0, r=0),
        height=580,
    )

    st.plotly_chart(fig_map, use_container_width=True)

    # Summary stats below map
    st.markdown("---")
    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    valid_vals = map_df["Value"].dropna()
    mc1.metric("Continental Average", f"{valid_vals.mean():.1f}{ind_unit}" if ind_unit != "$" else f"${valid_vals.mean():,.0f}")
    mc2.metric("Highest",
               f"{map_df.loc[map_df['Value'].idxmax(),'Country']}",
               f"{map_df['Value'].max():.1f}{ind_unit}" if ind_unit != "$" else f"${map_df['Value'].max():,.0f}")
    mc3.metric("Lowest",
               f"{map_df.loc[map_df['Value'].idxmin(),'Country']}",
               f"{map_df['Value'].min():.1f}{ind_unit}" if ind_unit != "$" else f"${map_df['Value'].min():,.0f}")
    mc4.metric("Median", f"{valid_vals.median():.1f}{ind_unit}" if ind_unit != "$" else f"${valid_vals.median():,.0f}")
    mc5.metric("Countries Tracked", f"{len(valid_vals)}", "out of 54")

    # Top 10 table
    st.markdown(f"#### Top 10 Countries — {ind_label}")
    top10 = map_df.dropna(subset=["Value"]).sort_values("Value", ascending=(map_indicator in ["GDP_PerCapita","GDP_Growth"]), key=lambda x: -x).head(10)
    top10 = map_df.dropna(subset=["Value"]).sort_values("Value", ascending=False).head(10)
    top10_display = top10.copy()
    top10_display["Rank"] = range(1, len(top10_display)+1)
    top10_display[ind_label] = top10_display["Value"].apply(
        lambda v: f"${v:,.0f}" if ind_unit == "$" else f"{v:.1f}{ind_unit}"
    )
    st.dataframe(
        top10_display[["Rank","Country",ind_label]].set_index("Rank"),
        use_container_width=True,
    )

# ═════════════════════════════════════════════════════════════════════════════
# TAB 10 — Economic Rankings
# ═════════════════════════════════════════════════════════════════════════════
with tabs[9]:
    st.subheader("🏆 Africa Economic Rankings")
    st.caption("Economic Health Score computed from GDP Growth, Inflation, Unemployment, GDP Per Capita & Public Debt")

    # Compute scores for all countries using static data
    ranking_rows = []
    for code, vals in AFRICA_MAP_DATA.items():
        country_n = AFRICA_COUNTRIES[code][0]
        flag      = AFRICA_COUNTRIES[code][1]
        score     = compute_health_score(vals)
        ranking_rows.append({
            "Code":            code,
            "Flag":            flag,
            "Country":         country_n,
            "Health Score":    round(score, 1),
            "GDP Growth (%)":  vals.get("GDP_Growth", np.nan),
            "Inflation (%)":   vals.get("Inflation", np.nan),
            "Unemployment (%)":vals.get("Unemployment", np.nan),
            "GDP/Capita ($)":  vals.get("GDP_PerCapita", np.nan),
            "Public Debt (%)": vals.get("Public_Debt", np.nan),
        })

    rank_df = pd.DataFrame(ranking_rows).sort_values("Health Score", ascending=False).reset_index(drop=True)
    rank_df.insert(0, "Rank", range(1, len(rank_df)+1))

    # Score distribution gauge bar chart
    fig_rank = go.Figure(go.Bar(
        x=rank_df["Health Score"],
        y=rank_df["Flag"] + " " + rank_df["Country"],
        orientation="h",
        marker=dict(
            color=rank_df["Health Score"],
            colorscale=[[0,COLORS["red"]],[0.4,COLORS["yellow"]],[1,COLORS["green"]]],
            cmin=0, cmax=100,
            showscale=True,
            colorbar=dict(
                title="Score", tickfont=dict(color=COLORS["muted"]),
                bgcolor=COLORS["surface"], bordercolor=COLORS["border"],
            ),
        ),
        text=[f"{v:.1f}" for v in rank_df["Health Score"]],
        textposition="outside",
        textfont=dict(size=9, color=COLORS["text"]),
    ))
    fig_rank.update_layout(
        **layout(height=max(700, len(rank_df)*14),
                 yaxis_extra=dict(autorange="reversed"),
                 xaxis_extra=dict(range=[0, 115], tickcolor=COLORS["border"],
                                  gridcolor=COLORS["border"], linecolor=COLORS["border"])),
        title=dict(text="Economic Health Score — All 54 African Nations",
                   font=dict(color=COLORS["text"])),
    )
    st.plotly_chart(fig_rank, use_container_width=True)

    # Medal podium top 3
    st.markdown("---")
    st.markdown("### 🥇 Top Performers")
    pod1, pod2, pod3 = st.columns(3)
    top3 = rank_df.head(3)

    for i, (col, medal, color) in enumerate(zip(
        [pod1, pod2, pod3],
        ["🥇", "🥈", "🥉"],
        [COLORS["yellow"], "#c0c0c0", "#cd7f32"]
    )):
        row = top3.iloc[i]
        with col:
            st.markdown(f"""
            <div style='background:{COLORS["surface"]};border:1px solid {color};
                        border-radius:8px;padding:1.2rem;text-align:center;'>
                <div style='font-size:2rem'>{medal}</div>
                <div style='font-size:1.5rem'>{row['Flag']}</div>
                <div style='color:{COLORS["text"]};font-weight:bold;margin:0.3rem 0'>
                    {row['Country']}</div>
                <div style='color:{color};font-size:1.3rem;font-weight:bold'>
                    {row['Health Score']}</div>
                <div style='color:{COLORS["muted"]};font-size:0.7rem'>Health Score</div>
            </div>
            """, unsafe_allow_html=True)

    # Bottom 3
    st.markdown("### ⚠️ Countries Needing Attention")
    bot1, bot2, bot3 = st.columns(3)
    bot3_df = rank_df.tail(3).iloc[::-1]
    for i, col in enumerate([bot1, bot2, bot3]):
        row = bot3_df.iloc[i]
        with col:
            st.markdown(f"""
            <div style='background:{COLORS["surface"]};border:1px solid {COLORS["red"]};
                        border-radius:8px;padding:1.2rem;text-align:center;'>
                <div style='font-size:1.5rem'>{row['Flag']}</div>
                <div style='color:{COLORS["text"]};font-weight:bold;margin:0.3rem 0'>
                    {row['Country']}</div>
                <div style='color:{COLORS["red"]};font-size:1.3rem;font-weight:bold'>
                    {row['Health Score']}</div>
                <div style='color:{COLORS["muted"]};font-size:0.7rem'>Health Score</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    # Full ranking table
    st.markdown("### 📋 Full Economic Ranking Table")
    display_rank = rank_df.copy()
    display_rank["GDP Growth (%)"]   = display_rank["GDP Growth (%)"].apply(lambda v: f"{v:+.1f}%" if not np.isnan(v) else "—")
    display_rank["Inflation (%)"]    = display_rank["Inflation (%)"].apply(lambda v: f"{v:.1f}%" if not np.isnan(v) else "—")
    display_rank["Unemployment (%)"] = display_rank["Unemployment (%)"].apply(lambda v: f"{v:.1f}%" if not np.isnan(v) else "—")
    display_rank["GDP/Capita ($)"]   = display_rank["GDP/Capita ($)"].apply(lambda v: f"${v:,.0f}" if not np.isnan(v) else "—")
    display_rank["Public Debt (%)"]  = display_rank["Public Debt (%)"].apply(lambda v: f"{v:.1f}%" if not np.isnan(v) else "—")
    display_rank["Country"]          = display_rank["Flag"] + " " + display_rank["Country"]

    st.dataframe(
        display_rank[["Rank","Country","Health Score","GDP Growth (%)","Inflation (%)",
                       "Unemployment (%)","GDP/Capita ($)","Public Debt (%)"]].set_index("Rank"),
        use_container_width=True,
    )

    st.download_button(
        "⬇️ Download Rankings CSV",
        data=rank_df.to_csv(index=False).encode("utf-8"),
        file_name="africa_economic_rankings.csv",
        mime="text/csv",
    )

    st.markdown("""
    <div class='insight-box'>
        <h4>ℹ️ About the Economic Health Score</h4>
        <p>The score (0–100) is a composite index weighted across five indicators:
        GDP Growth (positive contribution), Inflation (penalized above 10%),
        Unemployment (penalized), GDP Per Capita (log-scale bonus), and
        Public Debt (penalized above 60% of GDP). Scores above 70 indicate
        strong economic health; below 40 indicates significant challenges.</p>
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 11 — Country Comparison
# ═════════════════════════════════════════════════════════════════════════════
with tabs[10]:
    st.subheader("📊 Country Comparison — All 54 African Nations")
    st.caption("🟢 = full data · 🟡 = partial · 🔴 = sparse")

    cc1, cc2, cc3 = st.columns([2, 1, 1])
    with cc1:
        compare_codes = st.multiselect(
            "Select countries (up to 5)",
            options=list(COUNTRY_OPTIONS.keys()),
            default=["KEN","NGA","ZAF","ETH","GHA"],
            format_func=lambda c: COUNTRY_OPTIONS[c],
            max_selections=5,
        )
    with cc2:
        compare_indicator = st.selectbox(
            "Indicator",
            options=["GDP_Growth","GDP_B","GDP_PerCapita","Inflation","Unemployment",
                     "Exports_GDP","Imports_GDP","Trade_Balance","Public_Debt"],
            format_func=lambda x: {
                "GDP_Growth":"GDP Growth %","GDP_B":"GDP (USD B)",
                "GDP_PerCapita":"GDP Per Capita","Inflation":"Inflation %",
                "Unemployment":"Unemployment %","Exports_GDP":"Exports % GDP",
                "Imports_GDP":"Imports % GDP","Trade_Balance":"Trade Balance % GDP",
                "Public_Debt":"Public Debt % GDP",
            }[x],
        )
    with cc3:
        compare_range = st.slider("Year range", 2000, 2023, (2005, 2023), key="cmp_range")

    if not compare_codes:
        st.info("Select at least one country above.")
    else:
        country_data = {}
        load_errors  = []
        progress = st.progress(0, text="Loading…")
        for i, code in enumerate(compare_codes):
            progress.progress((i+1)/len(compare_codes),
                              text=f"Loading {AFRICA_COUNTRIES[code][0]}…")
            cdf, _ = fetch_single_country(code)
            if cdf is not None:
                country_data[code] = cdf
            else:
                load_errors.append(AFRICA_COUNTRIES[code][0])
        progress.empty()

        if load_errors:
            st.warning(f"Could not load: {', '.join(load_errors)}")

        if country_data:
            ind_labels = {
                "GDP_Growth":    ("GDP Growth %",       "%", ""),
                "GDP_B":         ("GDP (USD Billion)",  "B", "$"),
                "GDP_PerCapita": ("GDP Per Capita",     "",  "$"),
                "Inflation":     ("Inflation %",        "%", ""),
                "Unemployment":  ("Unemployment %",     "%", ""),
                "Exports_GDP":   ("Exports % of GDP",   "%", ""),
                "Imports_GDP":   ("Imports % of GDP",   "%", ""),
                "Trade_Balance": ("Trade Balance % GDP","%", ""),
                "Public_Debt":   ("Public Debt % GDP",  "%", ""),
            }
            ind_label, ind_unit, ind_prefix = ind_labels[compare_indicator]
            tick_suffix = "" if ind_unit in ("B","") else ind_unit

            st.markdown(f"### {ind_label} — Over Time")
            fig = go.Figure()
            for idx, (code, cdf) in enumerate(country_data.items()):
                cdf_f = cdf[(cdf["Year"] >= compare_range[0]) &
                            (cdf["Year"] <= compare_range[1])].dropna(subset=[compare_indicator])
                if cdf_f.empty:
                    continue
                color = COUNTRY_PALETTE[idx % len(COUNTRY_PALETTE)]
                name  = AFRICA_COUNTRIES[code][0]
                fig.add_trace(go.Scatter(
                    x=cdf_f["Year"], y=cdf_f[compare_indicator], name=name,
                    line=dict(color=color, width=2.5), mode="lines+markers",
                    marker=dict(size=5),
                    hovertemplate=f"<b>{name}</b><br>Year: %{{x}}<br>{ind_label}: %{{y:.1f}}<extra></extra>",
                ))
            fig.update_layout(**layout(height=420,
                              yaxis_extra=dict(title=ind_label,
                                               ticksuffix=tick_suffix, tickprefix=ind_prefix)))
            if highlight_covid:
                add_covid_band(fig)
            st.plotly_chart(fig, use_container_width=True)

            # Bar chart — latest values
            st.markdown(f"### Latest Value — {ind_label}")
            bar_data = []
            for code, cdf in country_data.items():
                valid = cdf.dropna(subset=[compare_indicator])
                if not valid.empty:
                    bar_data.append({
                        "Country": AFRICA_COUNTRIES[code][0],
                        "Value":   valid.iloc[-1][compare_indicator],
                        "Year":    int(valid.iloc[-1]["Year"]),
                    })
            if bar_data:
                bar_df = pd.DataFrame(bar_data).sort_values("Value", ascending=True)
                fig_bar = go.Figure(go.Bar(
                    x=bar_df["Value"], y=bar_df["Country"], orientation="h",
                    marker=dict(
                        color=bar_df["Value"],
                        colorscale=[[0,COLORS["red"]],[0.5,COLORS["yellow"]],[1,COLORS["green"]]],
                        showscale=True,
                        colorbar=dict(title=ind_label, tickfont=dict(color=COLORS["muted"])),
                    ),
                    text=[f"{ind_prefix}{v:.1f}{ind_unit if ind_unit not in ('B','') else ('B' if ind_unit=='B' else '')} ({y})"
                          for v, y in zip(bar_df["Value"], bar_df["Year"])],
                    textposition="outside",
                    textfont=dict(size=10, color=COLORS["text"]),
                ))
                fig_bar.update_layout(**layout(
                    height=max(250, len(bar_data)*55),
                    yaxis_extra=dict(title=""),
                    xaxis_extra=dict(title=ind_label,
                                     ticksuffix=tick_suffix, tickprefix=ind_prefix),
                ))
                st.plotly_chart(fig_bar, use_container_width=True)

            # Summary table
            st.markdown("### 📋 All Indicators — Latest Values")
            table_rows = []
            for code, cdf in country_data.items():
                row = {"Country": AFRICA_COUNTRIES[code][0], "Quality": AFRICA_COUNTRIES[code][2]}
                for ind, (lbl, unit, pfx) in ind_labels.items():
                    valid = cdf.dropna(subset=[ind])
                    if not valid.empty:
                        v  = valid.iloc[-1][ind]
                        yr = int(valid.iloc[-1]["Year"])
                        row[lbl] = f"{pfx}{v:.1f}{unit if unit not in ('B','') else ('B' if unit=='B' else '')} ({yr})"
                    else:
                        row[lbl] = "—"
                table_rows.append(row)
            st.dataframe(pd.DataFrame(table_rows).set_index("Country"), use_container_width=True)

            all_frames = []
            for code, cdf in country_data.items():
                tmp = cdf.copy()
                tmp.insert(0, "Country", AFRICA_COUNTRIES[code][0])
                tmp.insert(1, "ISO3", code)
                all_frames.append(tmp)
            combined = pd.concat(all_frames, ignore_index=True)
            st.download_button("⬇️ Download Comparison CSV",
                               data=combined.to_csv(index=False).encode("utf-8"),
                               file_name="africa_comparison.csv", mime="text/csv")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 12 — AI INSIGHTS
# ═════════════════════════════════════════════════════════════════════════════
with tabs[11]:
    st.subheader(f"🤖 AI Insights — {country_name}")
    st.caption("Powered by Google Gemini · Reads your actual loaded data, not hardcoded text")

    if not gemini_key:
        st.warning(
            "**Add your Gemini API key to enable AI Insights.**\n\n"
            "1. Go to [aistudio.google.com](https://aistudio.google.com) → Get API Key\n"
            "2. Paste it into the **AI Insights** field in the sidebar\n"
            "3. Or add `GEMINI_API_KEY=your_key` to your `.env` file"
        )
    else:
        data_summary = build_data_summary(df, country_name, year_range)

        st.markdown("**Quick Analysis — click any button to generate:**")
        PRESETS = {
            "📊 Full Economic Overview": (
                f"You are an expert economist specializing in African economies. "
                f"Analyze the following economic data for {country_name} and write a "
                f"comprehensive 4-paragraph economic overview. Cover: (1) GDP growth trajectory "
                f"and key turning points, (2) inflation patterns and monetary policy implications, "
                f"(3) unemployment trends and labor market dynamics, (4) trade balance and "
                f"structural economic challenges. Be specific — reference actual numbers from the data.\n\n"
                f"DATA:\n{data_summary}"
            ),
            "📉 COVID Impact Analysis": (
                f"Analyze the specific economic impact of COVID-19 (2020–2021) on {country_name} "
                f"based on this data. Compare pre-COVID averages (2015–2019) to COVID years and "
                f"the recovery period (2022–2023). Quantify the damage and recovery across all "
                f"indicators. Write 3 focused paragraphs.\n\nDATA:\n{data_summary}"
            ),
            "🔮 Outlook & Risks": (
                f"Based on the historical economic trends for {country_name}, write a forward-looking "
                f"assessment covering: (1) what the data suggests about growth momentum, "
                f"(2) the biggest economic risks and vulnerabilities, (3) structural opportunities "
                f"for the economy. Ground every point in the actual data provided.\n\nDATA:\n{data_summary}"
            ),
            "🌍 Regional Context": (
                f"Place {country_name}'s economic performance in the context of sub-Saharan Africa. "
                f"Based on this data, assess whether the country is an outperformer, average, or "
                f"underperformer relative to typical African economies. Discuss inflation management, "
                f"growth consistency, and trade dynamics. Write 3 concise paragraphs.\n\nDATA:\n{data_summary}"
            ),
            "📈 Best & Worst Years": (
                f"From the data provided for {country_name}, identify and explain the 3 best and "
                f"3 worst economic years. For each year, explain what likely caused the performance "
                f"based on the indicators. Reference specific numbers. Write in a clear analytical style.\n\nDATA:\n{data_summary}"
            ),
        }

        cols = st.columns(3)
        for i, (btn_label, _) in enumerate(PRESETS.items()):
            with cols[i % 3]:
                if st.button(btn_label, use_container_width=True):
                    st.session_state["ai_prompt"]   = PRESETS[btn_label]
                    st.session_state["ai_btn_label"] = btn_label

        st.markdown("---")
        st.markdown("**Or ask a custom question:**")
        custom_q = st.text_area(
            "Your question",
            placeholder=f"e.g. Why did inflation spike so high in {country_name}? "
                        f"What does the trade deficit mean for economic growth?",
            height=80,
            label_visibility="collapsed",
        )
        if st.button("🔍 Ask Gemini", use_container_width=False):
            if custom_q.strip():
                full_prompt = (
                    f"You are an expert economist. Answer the following question about "
                    f"{country_name} using the data provided. Be specific and reference "
                    f"actual numbers.\n\nQUESTION: {custom_q}\n\nDATA:\n{data_summary}"
                )
                st.session_state["ai_prompt"]   = full_prompt
                st.session_state["ai_btn_label"] = f"❓ {custom_q[:60]}…"

        if "ai_prompt" in st.session_state:
            st.markdown("---")
            st.markdown(f"**{st.session_state.get('ai_btn_label', 'Analysis')}**")
            with st.spinner("Gemini is analyzing the data…"):
                response = call_gemini(st.session_state["ai_prompt"], gemini_key)
            st.markdown(
                f"<div class='ai-response'>{response}</div>",
                unsafe_allow_html=True,
            )
            st.download_button(
                "⬇️ Download Analysis",
                data=response.encode("utf-8"),
                file_name=f"{primary_code}_ai_analysis.txt",
                mime="text/plain",
            )
            if st.button("🗑️ Clear"):
                del st.session_state["ai_prompt"]
                del st.session_state["ai_btn_label"]
                st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# TAB 13 — Statistics
# ═════════════════════════════════════════════════════════════════════════════
with tabs[12]:
    if show_stats:
        st.subheader(f"Statistical Summary — {country_name}")
        summary_cols = ["GDP_Growth","Inflation","Unemployment",
                        "Exports_GDP","Imports_GDP","Trade_Balance"]
        # add optional columns
        for opt_col in ["GDP_PerCapita","Public_Debt"]:
            if opt_col in dff.columns and not dff[opt_col].isna().all():
                summary_cols.append(opt_col)

        label_map = {
            "GDP_Growth":"GDP Growth %","Inflation":"Inflation %",
            "Unemployment":"Unemployment %","Exports_GDP":"Exports % GDP",
            "Imports_GDP":"Imports % GDP","Trade_Balance":"Trade Balance % GDP",
            "GDP_PerCapita":"GDP Per Capita ($)","Public_Debt":"Public Debt % GDP",
        }
        stats_df = dff[summary_cols].describe().T.round(2)
        stats_df.index = [label_map.get(i, i) for i in stats_df.index]
        stats_df.columns = ["Count","Mean","Std Dev","Min",
                            "25th %ile","Median","75th %ile","Max"]
        st.dataframe(
            stats_df.style.background_gradient(subset=["Mean"], cmap="RdYlGn", axis=0)
                          .format("{:.2f}"),
            use_container_width=True,
        )
        st.markdown("---")
        disp_cols = ["Year","Era","GDP_B","GDP_Growth","Inflation",
                     "Unemployment","Exports_GDP","Imports_GDP","Trade_Balance"]
        disp_names = ["Year","Era","GDP ($B)","GDP Growth %","Inflation %",
                      "Unemployment %","Exports % GDP","Imports % GDP","Trade Balance %"]
        for opt_col, opt_name in [("GDP_PerCapita","GDP Per Capita ($)"),("Public_Debt","Public Debt %")]:
            if opt_col in dff.columns and not dff[opt_col].isna().all():
                disp_cols.append(opt_col)
                disp_names.append(opt_name)

        disp = dff[disp_cols].copy()
        disp.columns = disp_names
        st.dataframe(disp.set_index("Year"), use_container_width=True)
        st.download_button("⬇️ Download CSV",
                           data=disp.to_csv(index=False).encode("utf-8"),
                           file_name=f"{primary_code}_data.csv", mime="text/csv")

# ── Footer insights ───────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Key Insights")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""<div class='insight-box'>
        <h4>📈 Sustained Long-Term Growth</h4>
        <p>Many African economies have recorded GDP growth of 4–8% annually over two decades,
        outpacing global averages and demonstrating strong structural development.</p>
        </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class='insight-box warn'>
        <h4>🔥 Inflation Pressures</h4>
        <p>Inflation remains a persistent challenge, amplified by global food and energy
        shocks in 2008 and 2022 and structural import dependency across the continent.</p>
        </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class='insight-box danger'>
        <h4>🌍 Trade Imbalances</h4>
        <p>Most African economies run persistent trade deficits driven by fuel, machinery,
        and manufactured goods imports. Export diversification remains a key challenge.</p>
        </div>""", unsafe_allow_html=True)
with c4:
    st.markdown("""<div class='insight-box'>
        <h4>🏦 Rising Public Debt</h4>
        <p>Several African nations now carry debt above 80% of GDP, raising concerns
        about fiscal sustainability and debt servicing costs amid rising global interest rates.</p>
        </div>""", unsafe_allow_html=True)

st.markdown(
    "<br><small style='color:#3a4f3d'>Data: World Bank Open Data · IMF DataMapper · "
    "54 African countries · All indicators from official national statistics.</small>",
    unsafe_allow_html=True,
)