import asyncio
import cv2
from PIL import Image
import mss
from google.genai import types
from google import genai
import pyaudio
import io
from .tools  import tools_handler

# --- pyaudio config ---
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

pya = pyaudio.PyAudio()


audio_queue_output = asyncio.Queue()
audio_queue_mic = asyncio.Queue(maxsize=5)
audio_stream = None



# this function uses my microphone to listen to audio which will be sent to gemini
async def listen_to_audio():
    """Listens for audio and puts it into the mic audio queue."""
    global audio_stream
    mic_info = pya.get_default_input_device_info()
    audio_stream = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=SEND_SAMPLE_RATE,
        input=True,
        input_device_index=mic_info["index"],
        frames_per_buffer=CHUNK_SIZE,
    )
    kwargs = {"exception_on_overflow": False} if __debug__ else {}
    while True:
        data = await asyncio.to_thread(audio_stream.read, CHUNK_SIZE, **kwargs)
        await audio_queue_mic.put({"data": data, "mime_type": "audio/pcm"})

# this function send my audio to gemini
async def send_realtime_audio(session):
    """Sends audio from the mic audio queue to the GenAI session."""
    while True:
        msg = await audio_queue_mic.get()
        await session.send_realtime_input(audio=msg)

        
# this functions get the voice and the tool response from AI
async def receive_response_from_ai(session, client_id):
    """Receives responses including tool call from GenAI and puts audio data into the speaker audio queue."""
    while True:
        turn = session.receive()
        async for response in turn:
            if (response.server_content and response.server_content.model_turn):
                for part in response.server_content.model_turn.parts:
                    if part.inline_data and isinstance(part.inline_data.data, bytes):
                        audio_queue_output.put_nowait(part.inline_data.data)

            # A. HANDLE TOOLS (Whiteboard/Agentic Actions)
            if response.tool_call:
                # We call your tools_handler here
                await tools_handler(client_id,session, response.tool_call)
                print(f"🎨 handling task for {client_id}")
            

        # Empty the queue on interruption to stop playback
        while not audio_queue_output.empty():
            audio_queue_output.get_nowait()

# this function plays the audio from gemini 
async def play_ai_audio():
    """Plays audio from the speaker audio queue."""
    stream = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=RECEIVE_SAMPLE_RATE,
        output=True,
    )
    while True:
        bytestream = await audio_queue_output.get()
        await asyncio.to_thread(stream.write, bytestream)

# this function uses my camera and sends my video to gemini

async def send_live_video(session):
    # Initialize the camera (0 is usually the default webcam)
    cap = cv2.VideoCapture(0)
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 1. Resize or process frame (Optional: 768x768 is ideal)
            frame = cv2.resize(frame, (768, 768))

            # 2. Encode the frame as a JPEG
            success, buffer = cv2.imencode('.jpg', frame)
            if success:
                # 3. Send the encoded bytes to the Gemini session
                await session.send_realtime_input(
                    media=types.Blob(
                        data=buffer.tobytes(),
                        mime_type="image/jpeg"
                    )
                )
            
            # 4. Maintain 1 frame per second to meet API constraints
            await asyncio.sleep(1.0)
            
    finally:
        cap.release()

# this function shares my screen

async def share_screen(session):
    with mss.mss() as sct:
        # Select the monitor to capture (usually monitors[1] is the primary)
        monitor = sct.monitors[1]
        
        while True:
            # 1. Capture the screen
            sct_img = sct.grab(monitor)
            
            # 2. Convert to PIL Image for easy resizing/encoding
            # Note: sct_img is in BGRA format
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # 3. Optimization: Resize to 768x768 (API sweet spot)
            img.thumbnail((768, 768))
            
            # 4. Encode to JPEG bytes
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=80)
            frame_bytes = buffer.getvalue()
            
            # 5. Send to Gemini session
            await session.send_realtime_input(
                video=types.Blob(
                    data=frame_bytes,
                    mime_type="image/jpeg"
                )
            )
            
            # 6. Strict 1 FPS limit
            await asyncio.sleep(1.0)
