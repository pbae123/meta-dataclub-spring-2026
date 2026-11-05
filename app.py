import streamlit as st

from ui import bootstrap_feed, render_create_panel, render_post_card, seed_posts


def main() -> None:
    st.set_page_config(
        page_title="Meta Well-Being Post Scanner",
        page_icon="🧠",
        layout="wide",
    )

    bootstrap_feed()

    if "posts" not in st.session_state:
        st.session_state.posts = seed_posts()

    st.markdown('<div class="header">Meta Well-Being Post Scanner</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Mock social media UI for post risk detection</div>', unsafe_allow_html=True)

    feed_col, div_col, create_col = st.columns([1.45, 0.03, 1.15], gap="small")

    with feed_col:
        st.markdown("<div class='section-title'>Community Feed</div>", unsafe_allow_html=True)
        for post in st.session_state.posts:
            render_post_card(post)

    with div_col:
        st.markdown(
            '<div style="border-left: 2px solid #bdd4f5; min-height: 600px; margin: 0 auto;"></div>',
            unsafe_allow_html=True,
        )

    with create_col:
        render_create_panel()


if __name__ == "__main__":
    main()
