import sys
import types

# Stub out optional dependencies used in main during import
sys.modules.setdefault("openai", types.SimpleNamespace(OpenAI=lambda *a, **k: None))

module = types.ModuleType("dotenv")
module.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", module)

from main import postprocess_reply


def test_remove_think_block():
    text = "Hello<think>secret</think>World"
    assert postprocess_reply(text) == "HelloWorld"
    assert "<think>" not in postprocess_reply(text)


def test_drop_starting_think():
    text = "<think>I should not be seen"
    assert postprocess_reply(text) == ""


def test_strip_whitespace():
    text = "  Hello world  "
    assert postprocess_reply(text) == "Hello world"
