import os
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types
import pyaudio
from .tasks import share_screen, send_live_video,send_realtime_audio,listen_to_audio,receive_response_from_ai,play_ai_audio
from .tools import WHITEBOARD_TOOL_MAP, tools
from .tools import draw_on_board,write_on_board,delete_item,clear_board

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Missing API KEY")

client = genai.Client(api_key=api_key,http_options={"api_version": "v1alpha"})
import os

# this is for the system instruction
#Gets the directory where live_agent.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2Join it with the filename
prompt_path = os.path.join(current_dir, "prompt.md")

# 3. Open using the full path
with open(prompt_path, 'r', encoding='utf-8') as f:
    system_message = f.read()



# defines the gemini model we are using
MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"

CONFIG =types.LiveConnectConfig(
    response_modalities = ["AUDIO"],
    system_instruction = system_message, 
    speech_config = {
        "voice_config": {"prebuilt_voice_config": {"voice_name": "Kore"}}},
    tools = [tools,{'google_search': {}}]
)

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
                tg.create_task(receive_response_from_ai(live_session))

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
    


