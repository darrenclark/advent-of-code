DROP SCHEMA IF EXISTS part2 CASCADE;

CREATE SCHEMA part2;

SET search_path TO part2;

CREATE TYPE map AS ENUM (
  'humidity-to-location map',
  'temperature-to-humidity map',
  'light-to-temperature map',
  'water-to-light map',
  'fertilizer-to-water map',
  'soil-to-fertilizer map',
  'seed-to-soil map'
);

CREATE UNLOGGED TABLE input_sections (key text, value text);
CREATE UNLOGGED TABLE seeds (seed_start bigint, seed_end bigint);
CREATE UNLOGGED TABLE maps (map map, dest_rng_start bigint, src_rng_start bigint, src_rng_end bigint);

CREATE INDEX maps_map_src_rng ON maps (map, src_rng_start, src_rng_end) INCLUDE (dest_rng_start);

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
DO $$
DECLARE
  input text[];
  elem text;
  range_start bigint;
  range_len bigint;
BEGIN

  SELECT regexp_split_to_array(trim(value), '\s+')
  INTO input
  FROM input_sections WHERE key = 'seeds';

  FOREACH elem IN ARRAY input
  LOOP
    IF range_start IS NULL THEN
      range_start := elem::bigint;
    ELSE
      range_len := elem::bigint;

      INSERT INTO seeds (seed_start, seed_end)
      VALUES (range_start, range_start + range_len - 1);

      range_start := NULL;
      range_len := NULL;
    END IF;

  END LOOP;
END;
$$ LANGUAGE plpgsql;

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
  key::map as map,
  split_part(rs, ' ', 1)::bigint as dest_rng_start,
  split_part(rs, ' ', 2)::bigint as src_rng_start,
  (split_part(rs, ' ', 2)::bigint + split_part(rs, ' ', 3)::bigint - 1) as src_rng_end
FROM i;

-- lookup in map
CREATE FUNCTION lookup(m map, input bigint) RETURNS bigint AS $$
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
    input <= src_rng_end
  LIMIT 1;

  IF result IS NULL THEN
    result := input;
  END IF;

  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- command to execute
CREATE FUNCTION run(_seed_start bigint) RETURNS bigint AS $$
DECLARE
  result bigint;
  _seed_end bigint;
BEGIN

  SET search_path TO part2;

  SELECT seed_end
  INTO _seed_end
  FROM seeds
  WHERE seed_start = _seed_start;

  IF _seed_end IS NULL THEN
    RAISE NOTICE 'could not find seed range starting with %', _seed_start;
    RETURN -1;
  END IF;

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
    FROM generate_series(_seed_start, _seed_end) seed
  )
  SELECT MIN(location)
  INTO result
  FROM locations;

  RETURN result;
END;
$$ LANGUAGE plpgsql;

SELECT
  'psql postgres -c "SELECT part2.run(' || seed_start::text || ');"' AS "commands to run"
FROM seeds;
