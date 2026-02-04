import discord
from openai import OpenAI
from pypdf import PdfReader
import os

# ================= CONFIG =================

DISCORD_TOKEN = ""
OPENAI_API_KEY = ""

PDF_PATH = "PDF"

ALLOWED_CHANNEL_ID = 1467253854780264664
TICKET_CHANNEL_ID = 1467253854096588825

ALLOWED_ROLE_IDS = [
    1467253851642921000,
]

MODEL_NAME = "gpt-5-mini"

FALLBACK_MESSAGE = (
    "I'm not sure. Please wait for staff to assist you or open a support ticket in "
    f"<#{TICKET_CHANNEL_ID}>."
)


client_ai = OpenAI(api_key=)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def load_pdf_text():
    reader = PdfReader(PDF_PATH)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


PDF_TEXT = load_pdf_text()


def user_has_role(member):
    return any(role.id in ALLOWED_ROLE_IDS for role in member.roles)


@client.event
async def on_ready():
    print(f" Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != :
        return

    if not user_has_role(message.author):
        return

    try:
        prompt = f"""
You are Swills AI Support Bot.

Answer the user's question ONLY using the information from the PDF below.
Answers should not be big and should be easy to understand.
Give answer only from the PDF and do not use your knowledge.
It must leave a line after each . in the sentences.
If the answer is not found in the PDF, reply ONLY with the word UNKNOWN.

PDF CONTENT:
{PDF_TEXT}

USER QUESTION:
{message.content}
"""

        response = client_ai.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Answer strictly from the PDF."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content.strip()

        if not answer or answer.upper() == "UNKNOWN":
            await message.channel.send(FALLBACK_MESSAGE)
        else:
            await message.channel.send(answer)

    except Exception as e:
        print("ERROR:", e)
        await message.channel.send(FALLBACK_MESSAGE)


client.run(DISCORD_TOKEN)
