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
