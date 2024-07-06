import os

# import dotenv

# dotenv.load_dotenv()

SPARKAI_APP_ID = os.environ["SPARKAI_APP_ID"]
SPARKAI_API_SECRET = os.environ["SPARKAI_API_SECRET"]
SPARKAI_API_KEY = os.environ["SPARKAI_API_KEY"]


import gradio as gr

import zhiguai.events
import zhiguai.models
import zhiguai.prompts

with gr.Blocks() as demo:

    config = zhiguai.models.Config(
        SPARKAI_APP_ID,
        SPARKAI_API_SECRET,
        SPARKAI_API_KEY,
    )

    chat_model = zhiguai.models.ChatModel(config)

    chat_prompt = zhiguai.prompts.VILLAGER_CHAT_PROMPT_TEMPLATE

    critic_model = zhiguai.models.CriticModel(config)

    critic_prompt = zhiguai.prompts.VILLAGER_CRITIC_PROMPT_TEMPLATE

    # TODO: Implement Dropdown
    npc = gr.Dropdown(
        choices=[
            "老妪花姑",
        ],
        value="老妪花姑",
        multiselect=False,
        label="NPC",
        info="Select NPC.",
    )

    if not npc.value:
        raise gr.Error("Please select NPC.")

    role = "桃源村村民"
    name = "老妪花姑"
    appearance = "一个头戴头巾身着麻衣的年长女性"
    voice = ""
    backstory = "你非常迷信，自幼受到母亲的影响，深信鬼神之说，家中常年供奉神像和香火。你的丈夫早逝，你认为是鬼怪作祟。你现今独居。"
    relationships = ""
    response = ""
    memory = []
    action = "继续谈话"
    action_space = ["开门", "关门", "继续谈话"]

    # TODO: Implement Dropdown
    your_appearance = gr.Dropdown(
        choices=[
            "书生",
        ],
        value="书生",
        multiselect=False,
        label="Your Appearance",
        info="Select your appearance.",
    )

    if not your_appearance.value:
        raise gr.Error("Please select your appearance.")

    observation = (
        "一个身背书篓的青年游学书生，虽然贫寒潦倒，但是潇洒俊逸，自带书生意气"
    )

    npc = zhiguai.events.NPC(
        role=role,
        name=name,
        appearance=appearance,
        voice=voice,
        backstory=backstory,
        relationships=relationships,
        observation=observation,
        response=response,
        memory=memory,
        action=action,
        action_space=action_space,
        chat_model=chat_model,
        chat_prompt=chat_prompt,
        critic_model=critic_model,
        critic_prompt=critic_prompt,
    )

    chatbot = gr.Chatbot([], elem_id="chatbox", label="Dialogue")

    query = gr.Textbox(
        label="Your Turn", placeholder="Directly press 'Submit' button to start"
    )

    submit = gr.Button("Submit", visible=True)

    submit.click(
        fn=npc.responde,
        inputs=[query, chatbot],
        outputs=[query, chatbot],
    )

    print("[Info]", npc.react())

    if npc.react() == "开门":
        gr.Info("Succeed!")
    elif npc.react() == "关门":
        gr.Info("Failed!")

if __name__ == "__main__":
    demo.queue().launch()
