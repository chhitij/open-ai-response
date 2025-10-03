📘 Document 1: Malaria – Developing Drugs for Treatment

59901823dft_malaria_developing_…

What is the difference between clinical cure and radical cure in malaria treatment?

Why is P. vivax more challenging to treat compared to P. falciparum?

What are the key inclusion criteria for uncomplicated malaria clinical trials?

In severe or complicated malaria trials, what is the primary efficacy endpoint?

What are the FDA’s recommendations for handling reinfection vs. recrudescence in trial outcomes?

What safety database size does the FDA recommend for malaria drug development?

What role do Controlled Human Malaria Infection (CHMI) studies play in early clinical development?

📘 Document 2: Summary of Benefits and Coverage – Sample

sbc-completed-sample

What is the overall deductible for an individual under this plan?

How much does a patient pay for a generic drug prescription if using a participating provider?

What services are not included in the out-of-pocket limit?

If a participant uses a non-participating hospital for an overnight stay costing $1,500, what extra cost may they face due to balance billing?

What is the copay for a primary care visit to treat an illness or injury?

List at least two services excluded from coverage under this plan.

In the coverage example of having a baby (normal delivery), how much does the patient pay out-of-pocket in total?

📘 Document 3: U.S. Benefits Brochure 2024

U.S._Benefits_Brochure_2024

What are the two types of medical plans offered, and how do they differ?

What percentage of salary does Short-Term and Long-Term Disability cover?

How much does the company match for the 401(k) Plan, and when do employees become fully vested?

What financial assistance is available for adoption, and how does it differ for full-time vs. part-time employees?

How many paid holidays are observed each year in the U.S.?

What is the paid parental leave policy for new parents?

What resource provides up to 10 free counseling sessions per person per year?

## Run the simple web UI

A minimal single-page UI is included at `static/index.html` so you can ask questions from a browser.

1. Create and activate a virtual environment (zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

2. Install the package (this will install dependencies from `pyproject.toml`):

```bash
pip install -e .
```

3. Set required environment variables in your shell (replace with your real tokens):

```bash
export OPENAI_API_KEY="sk-..."
export RENDER_OPEN_AI_AUTH_TOKEN="your-ui-token"
```

4. Run the FastAPI app with uvicorn:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

5. Open the UI in your browser:

http://127.0.0.1:8000/

Enter your question and the auth token you set in `RENDER_OPEN_AI_AUTH_TOKEN` and click Ask.

Notes:
- The app expects a valid OpenAI key in `OPENAI_API_KEY` and a UI auth token in `RENDER_OPEN_AI_AUTH_TOKEN`.
- If `RENDER_OPEN_AI_AUTH_TOKEN` is left as the default `changeme`, the server will reject requests; set it before running.


FOR WNINDOW:

.\.venv\Scripts\activate
