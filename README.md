# Concept Explainer (ELI5) · PS 23

Complex concepts can be hard to understand when explanations assume too much or too little background. This app displays the same concept at three levels: **Kid**, **Student**, and **Expert**.

## Run on Windows

Extract `Code.zip`, open PowerShell in the extracted folder containing `app.py`, and run:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Use **Demo** mode with one of the five example topics. Click a topic to fill in the input, then click **Explain**. Demo answers are built in and are not live AI output.

### Enable Live AI

Create a key at [Google AI Studio](https://aistudio.google.com/apikey) if eligible, then set it in the same PowerShell window. Stop the running app with Ctrl+C first. The value below is a placeholder, not a key:

```powershell
$env:GEMINI_API_KEY = 'replace-with-your-key'
py -m streamlit run app.py
```

The app starts in Live AI mode when a key is set. Keep the key private. Never include it in source, screenshots, your ZIP, or GitHub. The default model is `gemini-3.5-flash-lite`; if needed, set `GEMINI_MODEL` to a compatible model available to your key. Live mode sends the entered topic to Gemini and needs internet access. Demo mode needs no key or API connection once dependencies are installed.

## How it works

`app.py` validates the topic and displays the UI. `explainer.py` makes one Gemini API request with one prompt specifying the audience, depth, and output format. It checks that the response has exactly three nonempty fields: `kid`, `student`, and `expert`. Each field goes into its own tab. No model training or dataset is used.

## Tests and submission

```powershell
py -m unittest -v test_explainer
```

The automated tests use built-in examples and a simulated API response; they do not contact Gemini. For real results, try the prompt in Google AI Studio on 3–5 topics, then run at least five concepts through **Live AI** (e.g. gravity, photosynthesis, inflation, recursion, and black holes). For each, check that all three tabs are complete, the explanations get progressively more technical, and the core facts agree. Save 3–5 actual output screenshots; add 1–2 to both the report and the public repository README as required by the assignment.

The report should describe the work you actually did, including a prompt improvement you tried and the observed results. The public repository should be named `llm-ps23-<RollNo>`; place its real URL in `github_link.txt` after creating it. Do not include the environment, venv, or API key when packaging or uploading source.
