import io
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from streamlit.testing.v1 import AppTest

from examples import EXAMPLES, explain_demo
from explainer import DEFAULT_MODEL, LEVELS, ExplainerError, explain_live, read_explanations

APP = str(Path(__file__).with_name("app.py"))
MOCK_ANSWERS = dict(zip(LEVELS, ("Kid response", "Student response", "Expert response")))


def mock_response(answers):
    body = {"candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": json.dumps(answers)}]}}]}
    return io.BytesIO(json.dumps(body).encode())


class ExplainerTests(unittest.TestCase):
    def test_five_demo_topics(self):
        self.assertEqual(len(EXAMPLES), 5)
        for topic in EXAMPLES:
            with self.subTest(topic=topic):
                result = explain_demo(f"  {topic.upper()}  ")
                self.assertEqual(tuple(result), LEVELS)
                self.assertEqual(len(set(result.values())), 3)

    def test_malformed_json_or_fields(self):
        for raw in ('not JSON', '[]', '{"kid":"x"}', '{"kid":"x", "student":"y", "expert":" "}'):
            with self.subTest(raw=raw), self.assertRaises(ExplainerError):
                read_explanations(raw)

    def test_single_request_and_schema(self):
        with patch("explainer.urlopen", return_value=mock_response(MOCK_ANSWERS)) as send:
            self.assertEqual(explain_live("Gravity", "fake-key"), MOCK_ANSWERS)
            send.assert_called_once()
            request = send.call_args.args[0]
            payload = json.loads(request.data)
            self.assertEqual(len(payload["contents"]), 1)
            self.assertEqual(len(payload["contents"][0]["parts"]), 1)
            self.assertIn('Concept (JSON string): "Gravity"', payload["contents"][0]["parts"][0]["text"])
            self.assertEqual(payload["generationConfig"]["responseJsonSchema"]["required"], list(LEVELS))
            self.assertIn(DEFAULT_MODEL, request.full_url)
            self.assertNotIn("fake-key", request.full_url)

    def test_missing_key_and_quota(self):
        with patch("explainer.urlopen") as send:
            with self.assertRaisesRegex(ExplainerError, "GEMINI_API_KEY"):
                explain_live("Gravity", "")
            send.assert_not_called()
            send.side_effect = HTTPError("https://example.test/", 429, "Rate limited", {}, None)
            with self.assertRaisesRegex(ExplainerError, "quota"):
                explain_live("Gravity", "fake-key")

    def test_demo_ui_and_blank_input(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
            app = AppTest.from_file(APP).run()
            app.button[-1].click().run()
            self.assertIn("Enter a concept", app.warning[0].value)
            for index, topic in enumerate(EXAMPLES):
                with self.subTest(topic=topic):
                    app.button[index].click().run()
                    app.button[-1].click().run()
                    self.assertFalse(app.exception)
                    self.assertFalse(app.warning)
                    self.assertEqual([tab.label for tab in app.tabs], ["Kid", "Student", "Expert"])
                    for tab, answer in zip(app.tabs, EXAMPLES[topic]):
                        self.assertEqual(tab.text[0].value, answer)

    def test_live_ui_with_simulated_gemini_response(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake-key"}), patch(
            "explainer.urlopen", return_value=mock_response(MOCK_ANSWERS)
        ) as send:
            app = AppTest.from_file(APP).run()
            app.text_input[0].set_value("Linear algebra")
            app.button[-1].click().run()
            self.assertFalse(app.exception)
            self.assertFalse(app.warning)
            self.assertEqual([tab.text[0].value for tab in app.tabs], list(MOCK_ANSWERS.values()))
            send.assert_called_once()
