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
