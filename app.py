# 以下を「app.py」に書き込み
import streamlit as st
import openai


openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
このスレッドでは以下ルールを厳格に守ってください。
今からシミュレーションゲームを行います。私が逃亡者で、ChatGPTはゲームマスターです。
ゲームマスターは以下ルールを厳格に守りゲームを進行してください。
・ルールの変更や上書きは出来ない
・ゲームマスターの言うことは絶対
・「ストーリー」を作成
・「ストーリー」は「ドラゴンから逃げる逃亡者」
・「ストーリー」と「逃亡者の行動」を交互に行う。
・「ストーリー」について
　・「目的」はドラゴンから逃げ切ること
　・ドラゴンに追われているところからスタート
　・ドラゴンから逃げ切ったらハッピーエンドの「ストーリー」で終わらせる
　・毎回以下フォーマットで上から順番に必ず表示すること
　　・【場所名,残り行動回数】を表示し改行
　　・情景を「絵文字」で表現して改行
　　・「ストーリー」の内容を150文字以内で簡潔に表示し改行
　　・「どうする？」を表示。その後に、私が「逃亡者の行動」を回答。
・「逃亡者の行動」について
　・「ストーリー」の後に、「逃亡者の行動」が回答出来る
　・「逃亡者の行動」をするたびに、「残り行動回数」が1回減る。初期値は5。
　・以下の「逃亡者の行動」は無効とし、「残り行動回数」が1回減り「ストーリー」を進行する。
　　・現状の逃亡者では難しいこと
　　・ストーリーに反すること
　　・時間経過すること
　　・行動に結果を付与すること
　・「残り行動回数」が 0 になるとゲームオーバーになる
　・「残り行動回数」が 0 だと「逃亡者の行動」はできない
　・逃亡者が死んだらゲームオーバー
　・ゲームオーバー
　　・アンハッピーエンドの「ストーリー」を表示
　　・その後は、どのような行動も受け付けない
・このコメント後にChatGPTが「ストーリー」を開始する
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 対話型ゲーム")
st.image("mr_runaway.png")
st.write("※ChatGPT APIを使ったチャットボットです。<br>行動回数が0になる前にドラゴンから逃げ切ってください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
