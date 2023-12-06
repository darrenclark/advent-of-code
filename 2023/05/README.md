# 2023 Day 5

https://adventofcode.com/2023/day/5

To run:

```sh
# Install Postgres & start it locally
/opt/homebrew/opt/postgresql@14/bin/postgres -D /opt/homebrew/var/postgresql@14

# update part1.sql and part2.sql to have correct path to input text files
vim *.sql

# part1
psql postgres -f ./part1.sql

# part2:

# 1. Setup database
psql postgres -f ./part1.sql
# 2. Run the outputted psql commands in 10 new terminal windows (yay parallelism)
# 3. Wait a long time...
# 4. Copy paste each individual result in to the command below:
psql postgres -c 'SELECT MIN(x) FROM UNNEST(ARRAY[102613525, 566602517, 624704155, 228214335, 1048225358, 52510809, 123535055, 4153786415, 2658982616, 56651838]) x'
```
