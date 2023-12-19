class Lagoon
  BLANK = '.'
  DUG = '#'
  DUG_FILL = 'I'
  DUG_CHARS = "#I"

  def initialize
    @grid = ["#"]
    @x = 0
    @y = 0
    @row_count = 1
    @col_count = 1
  end

  def dig(direction, count)
    case direction
    when "U"
      do_dig(0, -count)
    when "D"
      do_dig(0, count)
    when "L"
      do_dig(-count, 0)
    when "R"
      do_dig(count, 0)
    else
      raise "unknown direction: #{direction}"
    end
  end

  def fill
    for y in 1...(@row_count - 1)
      inside = false
      for x in 0...(@col_count - 1)
        @grid[y][x] = 'I' if inside and @grid[y][x] == BLANK

        inside = !inside if vertical_edge?(x, y)
      end
    end
  end

  def count_dug
    @grid.sum do |row|
      row.count DUG_CHARS
    end
  end

  def print
    @grid.each { |row| puts row }
  end

  private

  def do_dig(dx, dy)
    expand_if_needed(dx, dy)

    while dx > 0
      @x += 1
      dx -= 1
      @grid[@y][@x] = '#'
    end
    while dx < 0
      @x -= 1
      dx += 1
      @grid[@y][@x] = '#'
    end
    while dy > 0
      @y += 1
      dy -= 1
      @grid[@y][@x] = '#'
    end
    while dy < 0
      @y -= 1
      dy += 1
      @grid[@y][@x] = '#'
    end
  end

  def expand_if_needed(dx, dy)
    dest_x = @x + dx
    dest_y = @y + dy

    if dest_y >= @row_count
      to_add = (dest_y+1) - @row_count
      to_add.times { |_| @grid.insert(@grid.length, BLANK * @col_count) }
      @row_count += to_add
    elsif dest_y < 0
      to_add = -dest_y
      to_add.times { |_| @grid.insert(0, BLANK * @col_count) }
      @row_count += to_add
      @y += to_add
    end

    if dest_x >= @col_count
      to_add = (dest_x+1) - @col_count
      to_add.times do |_|
        @grid.each { |row| row.insert(row.length, BLANK) }
      end
      @col_count += to_add
    elsif dest_x < 0
      to_add = -dest_x
      to_add.times do |_|
        @grid.each { |row| row.insert(0, BLANK) }
      end
      @col_count += to_add
      @x += to_add
    end
  end

  def vertical_edge?(x, y)
    @grid[y][x] == DUG && @grid[y-1][x] == DUG
  end
end

def part1
  input = ARGF.read.split("\n").map do |l|
    parts = l.split

    {direction: parts[0], count: parts[1].to_i}
  end

  lagoon = Lagoon.new

  input.each { |step| lagoon.dig(step[:direction], step[:count]) }

  lagoon.fill

  puts "[PART 1] Cubic meters: #{lagoon.count_dug}"
end

part1
