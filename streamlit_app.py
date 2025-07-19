import streamlit as st
import requests
import json

st.set_page_config(layout="wide", page_title="Climate Solver with AI Output")

st.title("🌍 Submit Climate Problem")

user_problem = st.text_area("Describe your issue...", height=100, key="problem_input")

WEBHOOK_URL = 'https://hook.relay.app/api/v1/playbook/cmd8s79ao15ew0qm2glcshoxa/trigger/MZbiivKx0fGxhrH0kPUEZg'

if st.button("Get Solutions"):
    if not user_problem.strip():
        st.warning("Please enter a problem.")
    else:
        st.info("Processing your request...")
        payload = {"user_problem": user_problem}

        try:
            res = requests.post(WEBHOOK_URL, json=payload)
            res.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            data = res.json()

            st.subheader("✅ Results")
            st.markdown(f"**Category:** {data.get('category', 'N/A')}")
            st.markdown("---")

            st.markdown("#### Solution 1:")
            st.code(data.get('solution1', 'N/A'), language="text")

            st.markdown("#### Details:")
            st.code(
                f"""Location: {data.get('preciseLocation', 'N/A')}
Authority: {data.get('governmentAuthority', 'N/A')}
Phone: {data.get('contactNumber', 'N/A')}
Toll-free: {data.get('tollFreeNumber', 'N/A')}
Email: {data.get('email', 'N/A')}
Website: {data.get('website', 'N/A')}""",
                language="text"
            )
            st.markdown("---")

            st.markdown("#### What *you* should do:")
            st.code(data.get('solution2', 'N/A'), language="text")

        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the webhook: {e}")
        except json.JSONDecodeError:
            st.error("Error decoding JSON response from the webhook.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
