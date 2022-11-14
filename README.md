# RedditMining

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
