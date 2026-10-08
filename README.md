# Radar Junior

What skills do companies ask from junior candidates in Argentina?

This project collects entry-level remote job posts open to Argentina
from the Himalayas public API, to measure which skills come up most.

## Stage 1: collecting the data

- `bajar_avisos.py` downloads every entry-level job post, page by page
- Results are saved in `avisos.json` (not tracked: it is generated data)
- 530 posts from 287 companies on the first run

## How to run it

```
pip install requests
python bajar_avisos.py
```

## Next stages

2. Store the posts and query them with SQL
3. A small dashboard to explore the data
4. Tests, and a weekly automatic update

## Stage 2: asking the data

- `crear_base.py` loads the posts into a SQLite database (`avisos.db`)
- `consultas.py` answers three questions: who posts the most, which skills
  come up, and how many posts publish a salary in USD

### A note on how reliable these numbers are

Counting skills with `LIKE "%AI%"` gives 503 out of 530 posts, which is clearly
wrong. The pattern also matches *maintain*, *detail*, *email* and *training*.
The same happens with `%Excel%` matching *excellent*, and `%Git%` matching
*digital*.

Searching for the word surrounded by spaces drops AI to 154, and Excel from
230 to 29. That is closer to the truth, but still imperfect: it misses "AI,"
with a comma, and posts that start a sentence with it. The real figure is
somewhere between the two, closer to the lower one.

Both counts are printed side by side on purpose.

## Stage 5: letting an AI read the postings

Counting keywords only finds what I already thought to look for. If "CRM" is not
on my list, I will never learn that 13% of these jobs ask for it.

- `leer_con_ia.py` sends each posting to Google's Gemini API and asks what skills
  it requires, with no predefined list
- 501 of the 530 postings were read this way
- The result: **1,019 distinct skills**, against the 6 the keyword search could see

### What it found

The most requested skills are not technical:

| skill | share of postings |
|---|---|
| communication | 55% |
| English | 32% |
| organization | 28% |
| problem solving | 19% |
| attention to detail | 19% |
| customer service | 17% |
| teamwork | 16% |
| data analysis | 14% |
| CRM | 13% |
| AI | 10% |

CRM, prospecting and negotiation never showed up before, because they were not on
my list. Meanwhile English lands at 32% here and 45% with the keyword count: two
independent methods pointing at the same place, which is the best sign a number
can be trusted.

### How reliable this is

**The prompt had to be rewritten once.** The first version let the model answer in
whatever language it chose, so `communication skills` and `comunicación` were
counted as two different things. Asking explicitly for short Spanish terms fixed
it. The tool did exactly what it was told; the instruction was the problem. The
same thing that had happened with `LIKE` in stage 2.

**Three models were used, not one.** Google's free tier allows 500 requests per
day per model. Two earlier runs (one with a badly chosen model, one with the first
prompt) burned through the quota, so the batch was finished across
`gemini-3.1-flash-lite`, `gemini-flash-latest` and `gemini-3.5-flash-lite`. Their
output was compared on the same postings before mixing the results: same language,
same casing, same style.

**29 postings are missing.** They failed on retry and were left out. At 501 of 530
the percentages do not move meaningfully.

### Running it

```
pip install requests
python leer_con_ia.py
```

Needs a `GEMINI_API_KEY` in a `.env` file at the project root. That file is in
`.gitignore` and never leaves the machine.
