# RedditMining

# Currently Used.
## V0.3.
- `n0_3.py`.
  - Main program.
  - API-based miner.
  - Uses Redis for control-based navigation inside the implicit Reddit graph.
- `n0_3_stats.py`.
  - Terminal-based dashboard.
  - Show the number of subreddits, submissions and users found.
- `Dashboard_M03_SubPicker`.
  - Interactive dashboard.
  - NextJS and Style-Component.
  - Frontend job.
  - Changes information with a Python-FastAPI server.
  - Receives and sends list of subreddits and their current status.
  - Interactive clicking for status changing.
  - Interactive filter - without lowercase restrictions - for finding subreddits.
- `server_m03_subpicker.py`.
  - FastaAPI based served.
  - Middleware between redis and nextjs frontend.
  - Receives information from both sides, processess it and give it the respective usage.
    - Two pipelines.
    - Redis -> Transform -> NextJS.
    - NextJS -> Transform -> Redis.
  - Creates a file containing information about the subreddits and its option to mine or not to mine.
    - Location. `ConfigFiles/subreddits2mine.json`.

# Reformed Tag.
- `miner0_0_EDA.py`.
  - Ad hoc miner for testing overall settings.
  - Ad hoc data gathering for structure inference.
  - Used as backbone for testing.

- `miner0_1.py`.
  - Redis for control.
  - Files for saving data.
  - Pros.
    - Faster than `miner0_2.py`.
  - Cons.
    - AdHoc building mechanism.
    - File system can become clutered.
    - Only works for subreddits and submissions.

- `miner0_2.py`.
  - Redis for control.
  - MongoDB for data saving.
  - Pros.
    - Can mine both subreddits, submissions and users.
    - Full database integration.
  - Problems.
    - Kinda slow compared with `miner0_1.py`.