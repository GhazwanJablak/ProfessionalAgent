import gradio as gr
import json
import os
from pypdf import PdfReader
from openai import OpenAI
from pathlib import Path
from tools import handle_tool_calls
from schemas import user_details_schema, unknown_question_schema

tools = [{"type": "function", "function": user_details_schema},
        {"type": "function", "function": unknown_question_schema}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Ghazwan Namou Jablak"
        reader = PdfReader("LinkedIn_Profile.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
            particularly questions related to {self.name}'s career, background, skills and experience. \
                Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
                    You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
                        Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
                            If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
                                If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = handle_tool_calls(tool_calls)
                messages.append(message)
                messages.extend(results)
                response = OpenAI.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            else:
                done = True
        return response.choices[0].message.content

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()