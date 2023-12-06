DROP SCHEMA IF EXISTS part1 CASCADE;

CREATE SCHEMA part1;

SET search_path TO part1;

CREATE TABLE input_sections (key text, value text);
CREATE TABLE seeds (seed bigint);
CREATE TABLE maps (map text, dest_rng_start bigint, src_rng_start bigint, rng_len bigint);

-- populate input_sections
INSERT INTO input_sections
SELECT
  split_part(section, ':', 1) as key,
  split_part(section, ':', 2) as value
FROM
  unnest(
    regexp_split_to_array(
      pg_read_file('/Users/darren/Projects/advent-of-code/2023/05/input.txt'),
      '\n\n'
    )
  ) AS x(section);


-- populate seeds
INSERT INTO seeds
SELECT regexp_split_to_table(trim(value), '\s+')::bigint
FROM input_sections WHERE key = 'seeds';

-- populate maps
WITH i AS (
  SELECT
    key as key,
    unnest(
      array_remove(
        regexp_split_to_array(trim(value), '\n'),
        ''
      )
    ) as rs
  FROM input_sections WHERE key LIKE '%map'
)
INSERT INTO maps
SELECT
  key as map,
  split_part(rs, ' ', 1)::bigint as dest_rng_start,
  split_part(rs, ' ', 2)::bigint as src_rng_start,
  split_part(rs, ' ', 3)::bigint as rng_len
FROM i;

-- lookup in map
CREATE FUNCTION lookup(m text, input bigint) RETURNS bigint AS $$
DECLARE
  result bigint;
BEGIN
  SELECT 
    dest_rng_start + (input - src_rng_start)
  INTO result
  FROM maps
  WHERE
    map = m and
    src_rng_start <= input and
    input <= src_rng_start + rng_len
  LIMIT 1;

  IF result IS NULL THEN
    result := input;
  END IF;

  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- find result
WITH locations AS (
  SELECT
    seed,
    lookup(
      'humidity-to-location map',
      lookup(
        'temperature-to-humidity map',
        lookup(
          'light-to-temperature map',
          lookup(
            'water-to-light map',
            lookup(
              'fertilizer-to-water map',
              lookup(
                'soil-to-fertilizer map',
                lookup('seed-to-soil map', seed)
              )
            )
          )
        )
      )
    ) as location
  FROM seeds
)
SELECT MIN(location) AS "lowest location number" FROM locations;
