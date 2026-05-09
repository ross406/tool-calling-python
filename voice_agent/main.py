import asyncio
from urllib import response
from dotenv import load_dotenv
import speech_recognition as sr
from openai import OpenAI
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()
client = OpenAI()
async_client = AsyncOpenAI()

async def tts(speech:str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Speak in a chearful and friendly tone.",
        input=speech,
        response_format="pcm",
    )as response:
        player = LocalAudioPlayer()
        await player.play(response)




def main():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        print("Speak Somthing...")
        audio = r.listen(source)
        print("Recognizing...")
        stt = r.recognize_google(audio, language='en-in')
        print("You said: ", stt)

        SYSTEM_PROMPT = """You are an expert voice agent.
       You will be given a voice input, and you need to understand the intent and respond accordingly.
       If the user is asking a question, provide a concise and accurate answer.
       whatever you speak will be converted back to audio and played back to the user, so keep your responses short and to the point.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": stt}
            ]
        )

        print("Agent: ", response.choices[0].message.content)
        asyncio.run(tts(speech=response.choices[0].message.content))

main()