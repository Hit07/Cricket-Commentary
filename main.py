from google.cloud import texttospeech


def split_voice(text):
    audio_clips = []
    curr_clip = []

    for line in text:
        line = line.strip()
        if line:
            curr_clip.append(line)
        else:
            if curr_clip:
                audio_clips.append('\n'.join(curr_clip))
                curr_clip = []

    if curr_clip:
        audio_clips.append('\n'.join(curr_clip))
    return audio_clips


def gcp_convert_text_to_speech(text, speech_output_file):
    user = texttospeech.TextToSpeechClient()
    chunks = split_voice(text)

    with open(speech_output_file, 'wb') as file:
        for chunk in chunks:
            if '(Male Voice)' in chunk:
                chunk = chunk.replace('Commentator 1 (Male Voice)','').strip()
                voice_params = texttospeech.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.SsmlVoiceGender.MALE
                )
            elif '(Female Voice)' in chunk:
                chunk = chunk.replace('Commentator 2 (Female Voice)','').strip()
                voice_params = texttospeech.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
                )
            else:
                voice_params = texttospeech.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
                )


            synthesis_input = texttospeech.SynthesisInput(text=chunk)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

            response = user.synthesize_speech(
                input=synthesis_input,
                voice=voice_params,
                audio_config=audio_config
            )

            file.write(response.audio_content)

    print(f"Audio content written to {speech_output_file}")


if __name__ == '__main__':
    with open('text_file.txt', 'r') as file:
        text = file.readlines()

    speech_output_file = 'worldcup_cricket_commentary.mp3'
    gcp_convert_text_to_speech(text, speech_output_file)
