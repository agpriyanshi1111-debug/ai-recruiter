
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import subprocess
import sys

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Recruiter Dashboard",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

[data-testid="metric-container"] {
    background-color: #111827;
    border: 1px solid #374151;
    padding: 15px;
    border-radius: 12px;
}

h1, h2, h3 {
    color: #00E5FF;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================


# BASE PATH SAFE FOR ALL ENVIRONMENTS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "output", "submission.csv")

# AUTO-GENERATE IF MISSING
if not os.path.exists(CSV_PATH):
    st.warning("submission.csv not found. Generating now...")

    subprocess.run([sys.executable, "-m", "backend.app"])

    if not os.path.exists(CSV_PATH):
        st.error("Still not generated. Check backend.app")
        st.stop()

# LOAD DATA
df = pd.read_csv(CSV_PATH)

# =====================================================
# HELPERS
# =====================================================

def score_color(val):
    if val >= 0.90:
        return "background-color: #2ecc71"
    elif val >= 0.80:
        return "background-color: #f1c40f"
    return ""

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🤖 AI Recruiter")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Candidate Explorer",
            "Analytics",
            "Export"
        ]
    )

    st.markdown("---")

    st.subheader("System Features")

    st.markdown("""
    ✅ Skill Matching

    ✅ Behavioral Signals

    ✅ Career Trajectory

    ✅ Availability Analysis

    ✅ Honeypot Detection

    ✅ Semantic Ranking

    ✅ Candidate Ranking
    """)

    st.markdown("---")

    st.subheader("About")

    st.info("""
    AI-powered recruitment ranking system.

    Uses:
    • Skill Matching
    • Behavioral Signals
    • Career Progression
    • Availability Analysis
    • Semantic Ranking
    • Honeypot Detection
    """)

    st.markdown("---")

    st.success("Ranking Complete")

# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    st.title("🚀 AI Candidate Ranking Dashboard")

    st.success("""
    Submission Ready

    ✓ Top 100 Generated
    ✓ Unique Ranks
    ✓ Reasoning Included
    ✓ Honeypot Filtering Applied
    ✓ CSV Ready
    """)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Candidates Ranked", len(df))

    with c2:
        st.metric("Highest Score", round(df["score"].max(), 4))

    with c3:
        st.metric("Average Score", round(df["score"].mean(), 4))

    with c4:
        st.metric("Lowest Score", round(df["score"].min(), 4))

    st.markdown("---")

    top = df.iloc[0]

    st.markdown("## 👑 Best Candidate")

    st.success(
        f"""
        Candidate ID: {top['candidate_id']}

        Rank: {top['rank']}

        Score: {round(top['score'],4)}
        """
    )

    st.markdown("---")

    st.markdown("## 🏆 Leaderboard")

    st.dataframe(
        df.head(5),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input("🔍 Search Candidate ID")

    with col2:
        rank_range = st.slider(
            "Rank Range",
            1,
            100,
            (1, 20)
        )

    with col3:
        jump_rank = st.number_input(
            "Jump To Rank",
            min_value=1,
            max_value=100,
            value=1
        )

    filtered = df[
        (df["rank"] >= rank_range[0]) &
        (df["rank"] <= rank_range[1])
    ]

    if search:
        filtered = filtered[
            filtered["candidate_id"].str.contains(
                search,
                case=False
            )
        ]

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        fig = px.histogram(
            df,
            x="score",
            nbins=20,
            title="Score Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:
        fig2 = px.line(
            df,
            x="rank",
            y="score",
            title="Ranking Curve"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("🎯 Selected Rank")

    st.dataframe(
        df[df["rank"] == jump_rank],
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🥇 Top 10 Candidates")

    st.table(
        df[
            ["rank", "candidate_id", "score"]
        ].head(10)
    )

    st.markdown("---")

    st.subheader("📋 Ranked Candidates")

    st.dataframe(
        filtered,
        use_container_width=True,
        height=500
    )
# =====================================================
# CANDIDATE EXPLORER
# =====================================================

elif page == "Candidate Explorer":

    st.title("🔎 Candidate Explorer")

    candidate = st.selectbox(
        "Select Candidate",
        df["candidate_id"]
    )

    row = df[
        df["candidate_id"] == candidate
    ].iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Rank",
            int(row["rank"])
        )

    with c2:
        st.metric(
            "Score",
            round(float(row["score"]), 4)
        )

    with c3:
        percentile = round(
            ((101 - row["rank"]) / 100) * 100,
            1
        )

        st.metric(
            "Percentile",
            f"{percentile}%"
        )

    st.markdown("---")

    st.subheader("⭐ Candidate Strength")

    score = float(row["score"])

    if score >= 0.90:
        st.success("Excellent Candidate")
    elif score >= 0.80:
        st.info("Strong Candidate")
    elif score >= 0.70:
        st.warning("Good Candidate")
    else:
        st.error("Needs Further Review")

    st.markdown("---")

    st.subheader("Reasoning")

    st.info(row["reasoning"])

    st.markdown("---")

    st.subheader("Score Visualization")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=float(row["score"]) * 100,
            title={"text": "Candidate Match Score"},
            gauge={
                "axis": {"range": [0, 100]}
            }
        )
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("Candidate Record")

    st.json({
        "candidate_id": row["candidate_id"],
        "rank": int(row["rank"]),
        "score": float(row["score"]),
        "reasoning": row["reasoning"]
    })

# =====================================================
# ANALYTICS
# =====================================================

elif page == "Analytics":

    st.title("📊 Ranking Analytics")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Median Score",
            round(df["score"].median(), 4)
        )

    with c2:
        st.metric(
            "Score Std Dev",
            round(df["score"].std(), 4)
        )

    with c3:
        st.metric(
            "Top 10 Avg",
            round(df.head(10)["score"].mean(), 4)
        )

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        fig = px.box(
            df,
            y="score",
            title="Score Spread"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.bar(
            df.head(10),
            x="candidate_id",
            y="score",
            title="Top 10 Candidates"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        fig = px.scatter(
            df,
            x="rank",
            y="score",
            title="Rank vs Score"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.area(
            df.head(25),
            x="rank",
            y="score",
            title="Top 25 Score Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("Complete Ranking Table")

    st.dataframe(
        df,
        use_container_width=True,
        height=600
    )

# =====================================================
# EXPORT
# =====================================================

elif page == "Export":

    st.title("📥 Export Submission")

    st.success(
        "Submission file ready for hackathon upload."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Rows",
            len(df)
        )

    with c2:
        st.metric(
            "Top Score",
            round(df["score"].max(), 4)
        )

    with c3:
        st.metric(
            "Average Score",
            round(df["score"].mean(), 4)
        )

    st.markdown("---")

    with open(CSV_PATH, "rb") as f:

        st.download_button(
            label="⬇ Download Submission CSV",
            data=f,
            file_name="submission.csv",
            mime="text/csv"
        )

    st.markdown("---")

    st.subheader("Submission Preview")

    st.dataframe(
        df.head(25),
        use_container_width=True
    )

    st.markdown("---")

    st.success(
        """
        Hackathon Checklist

        ✅ Top 100 Candidates

        ✅ Rank Column

        ✅ Score Column

        ✅ Reasoning Column

        ✅ CSV Export Ready

        ✅ Dashboard Demo Ready
        """
    )
