import streamlit as st
import requests
import json

# Page Setting
st.set_page_config(page_title="change audio to text",
                   page_icon="😄😄😄")

st.title("Change Audio to Text")

st.write("upload an audio format and change it to text")


c1, c2, c3 = st.columns([1,4,1])

with c2:
    with st.form(key="my_form"):
        # upload audio
        f = st.file_uploader("upload an audio format(.wav)", type=[".wav"])
        # submit
        submit_button = st.form_submit_button(label="Start")

    # if upload success
    if f is not None:
        st.audio(f, format="wav") # show player
        # audio name
        path_in = f.name
        st.write(f"file path: {path_in}")
        # catch format size
        getsize = f.tell()
        getsize = round((getsize / 1000000), 1) # calculate size

        if getsize < 100: # if size < 100MB

            bytes_value = f.getvalue()
            # catch huggingface token
            api_token = "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"
            # API key
            headers = {"Authorization": f"Bearer {api_token}"}
            API_URL = ("https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h")

            def query(data):
                # request
                response = requests.request("POST",
                                            API_URL,
                                            headers=headers,
                                            data=data)
                return json.loads(response.content.decode("utf-8"))

            # request audio to text
            data = query(bytes_value)

            # get text
            result = data.values()
            text_value = next(iter(result)).lower()
            st.markdown("- **Text:**")
            st.info(text_value)

            # download text
            st.download_button(
                "Download Text",
                text_value,
                file_name="speech_to_text_result.txt"
            )
        else:
            st.warning(
                "Warning⚠️: Please upload audio minimize 100MB"
            )
    else:
        st.stop()




