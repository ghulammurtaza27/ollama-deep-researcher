import streamlit as st
from assistant.graph import graph

def main():
    st.title("Interactive Learning Assistant")
    
    topic = st.text_input("What would you like to learn today?")
    if topic:
        config = {
            "difficulty_level": st.selectbox("Select level", ["elementary", "high_school", "college"]),
            "output_format": st.radio("Preferred format", ["text", "visual", "audio"])
        }
        
        with st.spinner("Building learning path..."):
            response = graph.invoke({"learning_topic": topic}, config)
            
            st.subheader("Explanation")
            st.markdown(response["explanation"])
            
            if "quiz" in response:
                st.subheader("Check Understanding")
                render_quiz(response["quiz"])
                
            if "recommendations" in response:
                st.subheader("Next Steps")
                show_recommendations(response["recommendations"]) 