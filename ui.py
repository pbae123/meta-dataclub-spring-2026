from datetime import datetime, timezone
from typing import Any

import streamlit as st

from config import LABEL_COLS
from inference import analyze_text


def bootstrap_feed() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #e9f0fb;
                color: #0f172a;
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            .block-container {
                max-width: 1440px;
                padding-top: 1.2rem;
                padding-left: 1.2rem;
                padding-right: 1.2rem;
            }

            .header {
                font-size: 1.65rem;
                font-weight: 900;
                margin-bottom: 0.1rem;
                color: #000000;
            }

            .subheader {
                color: #4b6fa8;
                margin-bottom: 0.85rem;
            }

            .section-title {
                font-size: 1.18rem;
                font-weight: 800;
                margin-bottom: 0.7rem;
                color: #000000;
            }

            [data-testid="stAlert"] p {
                color: #111827 !important;
                font-weight: 600;
            }

            [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] > div {
                border-radius: 12px !important;
                border-color: #bdd4f5 !important;
            }

            .feed-card {
                background: #ffffff;
                border: 1px solid #bdd4f5;
                border-radius: 12px;
                padding: 10px;
                margin-bottom: 8px;
            }

            .name-line {
                font-weight: 700;
                color: #0f172a;
            }

            .handle-line {
                color: #4b6fa8;
                font-size: 0.88rem;
            }

            [data-testid="InputInstructions"] {
                display: none !important;
            }

            .stTextArea label {
                color: #000000 !important;
                font-weight: 600;
            }

            .stTextArea [data-baseweb="textarea"] {
                border: 3px solid #0866ff !important;
                border-radius: 6px !important;
                background-color: #eef4fd !important;
                box-shadow: none !important;
                overflow: hidden !important;
            }

            .stTextArea textarea {
                min-height: 180px !important;
                background-color: #eef4fd !important;
                color: #0f172a !important;
                caret-color: #000000 !important;
                border: none !important;
                border-radius: 0 !important;
                outline: none !important;
                box-shadow: none !important;
                resize: none !important;
            }

            .stTextArea textarea::placeholder {
                color: #000000 !important;
                opacity: 1 !important;
            }

            [data-testid="stButton"] > button[kind="primary"] {
                background-color: #0866ff;
                border: none;
                color: #ffffff;
            }

            [data-testid="stButton"] > button[kind="primary"]:hover {
                background-color: #0553d4;
                border: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def seed_posts() -> list[dict[str, Any]]:
    return [
        # Thread 1 — sleepless anxiety night
        {
            "username": "Sofia",
            "handle": "@sofia.m",
            "content": "Stressful test tomorrow and I can't sleep 😓",
            "likes": 34,
            "profile_pic": "https://i.pravatar.cc/80?img=47",
            "image_url": "",
            "replies": [
                {
                    "username": "Jake",
                    "handle": "@jake.r",
                    "content": "Same, been up since 3am running through everything that could go wrong.",
                    "likes": 8,
                    "profile_pic": "https://i.pravatar.cc/80?img=15",
                },
                {
                    "username": "Maya",
                    "handle": "@maya.writes",
                    "content": "I can't get to sleep without medication anymore — too busy replaying every mistake I made during the day.",
                    "likes": 21,
                    "profile_pic": "https://i.pravatar.cc/80?img=9",
                },
            ],
        },
        {
            "username": "Ariana",
            "handle": "@ariana.dev",
            "content": "Built a tiny agent benchmark this morning. GPT + retrieval cut response time by ~18% 🚀",
            "likes": 143,
            "profile_pic": "https://i.pravatar.cc/80?img=32",
            "image_url": "https://images.unsplash.com/photo-1518773553398-650c184e0bb3?auto=format&fit=crop&w=1000&q=80",
        },
        {
            "username": "Miguel",
            "handle": "@migs",
            "content": "If your eval set is static, your AI app is already behind. Rotate fresh data weekly.",
            "likes": 87,
            "profile_pic": "https://i.pravatar.cc/80?img=12",
            "image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1000&q=80",
        },
        {
            "username": "Sana",
            "handle": "@sana.codes",
            "content": "Prompt engineering is good, but pipeline reliability is what saves production demos.",
            "likes": 66,
            "profile_pic": "https://i.pravatar.cc/80?img=5",
            "image_url": "",
        },
        {
            "username": "Leo",
            "handle": "@leo.ai",
            "content": "New vision model can read whiteboards shockingly well. Testing OCR + summarization next.",
            "likes": 119,
            "profile_pic": "https://i.pravatar.cc/80?img=56",
            "image_url": "https://images.unsplash.com/photo-1527430253228-e93688616381?auto=format&fit=crop&w=1000&q=80",
        },
        {
            "username": "Jordan",
            "handle": "@jordan.k",
            "content": "I'm in such a weird mood right now. I'm sad, but also want to punch things, but also anxious, but also want to cuddle. And I'm irritated about the whole thing. Why, brain? Why do you do this?",
            "likes": 204,
            "profile_pic": "https://i.pravatar.cc/80?img=22",
            "image_url": "",
        },
    ]


def _render_card_body(post: dict[str, Any]) -> None:
    avatar_col, text_col = st.columns([0.1, 0.9], gap="small")
    with avatar_col:
        st.image(post.get("profile_pic") or "https://i.pravatar.cc/80", width=44)
    with text_col:
        st.markdown(f"<div class='name-line'>{post['username']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='handle-line'>{post['handle']}</div>", unsafe_allow_html=True)
        st.write(post["content"])
        if post.get("image_upload") is not None:
            st.image(post["image_upload"], width=500)
        elif post.get("image_url"):
            st.image(post["image_url"], width=500)
        st.caption(f"❤️ {post['likes']}  •  💬 Reply  •  🔁 Repost")


def render_post_card(post: dict[str, Any]) -> None:
    with st.container(border=True):
        _render_card_body(post)

    for reply in post.get("replies", []):
        line_col, reply_col = st.columns([0.04, 0.96], gap="small")
        with line_col:
            st.markdown(
                '<div style="border-right: 2px solid #bdd4f5; min-height: 110px; height: 100%;"></div>',
                unsafe_allow_html=True,
            )
        with reply_col:
            with st.container(border=True):
                _render_card_body(reply)


def render_analysis(result: dict) -> None:
    tier = result["tier"]
    alert_line = f"{result['emoji']} {result['message']}  (score: {result['weighted_score']:.3f})"

    if tier == "RED":
        st.error(alert_line)
    elif tier == "ORANGE":
        st.warning(alert_line)
    else:
        st.success(alert_line)

    if result["flagged_labels"]:
        st.markdown(f"**Flagged:** {', '.join(result['flagged_labels'])}")

    for combo in result["triggered_combos"]:
        st.markdown(f"⚠️ {combo}")

    st.markdown("**Label probabilities:**")
    for lbl in LABEL_COLS:
        prob = result["label_probabilities"][lbl]
        flag = " ← flagged" if lbl in result["flagged_labels"] else ""
        st.progress(prob, text=f"{lbl}: {prob:.3f}{flag}")

    st.caption(f"Analyzed at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")


def render_create_panel() -> None:
    st.markdown("<div class='section-title'>Create Post</div>", unsafe_allow_html=True)

    content = st.text_area(
        "Write your post",
        placeholder="What's happening?",
        max_chars=500,
        height=180,
    )

    if st.button("Analyze Post", type="primary", use_container_width=True):
        if not content.strip():
            st.warning("Please enter post text before analysis.")
        else:
            result = analyze_text(content)
            render_analysis(result)
