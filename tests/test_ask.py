from types import SimpleNamespace

from app import ask


def test_chat_sends_follow_up_questions_to_the_same_session(monkeypatch, capsys):
    sent_questions = []

    class FakeSession:
        def send_message(self, question):
            sent_questions.append(question)
            return SimpleNamespace(text=f"回答: {question}", usage_metadata=None)

    session = FakeSession()
    client = SimpleNamespace(chats=SimpleNamespace(create=lambda **kwargs: session))
    monkeypatch.setattr(ask.genai, "Client", lambda **kwargs: client)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    questions = iter(["続きの質問", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(questions))

    ask.chat("最初の質問")

    assert sent_questions == ["最初の質問", "続きの質問"]
    assert "回答: 続きの質問" in capsys.readouterr().out