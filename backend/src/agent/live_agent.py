import os
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types
import pyaudio
from tasks import share_screen, send_live_video,send_realtime_audio,listen_to_audio,receive_audio_from_ai,play_ai_audio


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Missing API KEY")

client = genai.Client(api_key=api_key)

#system_prompt  = open("prompt.md", "r") 
#print(system_prompt)

MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "You are a helpful and friendly AI assistant.",
    "speech_config": {
        "voice_config": {"prebuilt_voice_config": {"voice_name": "Kore"}}}
}

pya = pyaudio.PyAudio()


audio_queue_output = asyncio.Queue()
audio_queue_mic = asyncio.Queue(maxsize=5)
audio_stream = None

async def agent():
    """Main function to run the agent"""
    try:
        async with client.aio.live.connect(
            model=MODEL, config= CONFIG
        ) as live_session:
            print("Connected to Gemini. Start Speaking!")
            async with asyncio.TaskGroup() as tg:
                tg.create_task(listen_to_audio())
                tg.create_task(send_live_video(live_session))
                tg.create_task(send_realtime_audio(live_session))
                tg.create_task(receive_audio_from_ai(live_session))
                tg.create_task(play_ai_audio())
                tg.create_task(share_screen(live_session))
    except asyncio.CancelledError:
        pass

    finally:
        if audio_stream:
            audio_stream.close()
        pya.terminate()
        print("\nConnection closed.")



if __name__ == "__main__":
    try:
        asyncio.run(agent())
    except KeyboardInterrupt:
        print("Interrupted by user.")
    


