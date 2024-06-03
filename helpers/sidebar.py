import streamlit as st


def show() -> None:
	with st.sidebar:
		st.markdown(f"""
			<a href="/" style="color:black;text-decoration: none;">
				<div style="display:table;margin-top:-17rem;margin-left:0%;">
					<img src="/app/static/Ducky-logo2.png" width="80">
					<span style="font-size: 0.8em; color: grey">&nbsp;&nbsp;v0.1.0</span>
					<br>
				</div>
			</a>
			<br>
				""", unsafe_allow_html=True)

		reload_button = st.button("↪︎  Reload Page")
		if reload_button:
			st.session_state.clear()
			st.experimental_rerun()

