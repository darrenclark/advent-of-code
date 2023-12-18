package main

import (
	"fmt"
	"os"
	"strings"
)

type posAndDir struct {
	x  int
	y  int
	dx int
	dy int
}

type contraption struct {
	grid      []string
	visited   map[posAndDir]bool
	energized [][]bool
	width     int
	height    int
}

func newContraption(input []string) contraption {
	width := len(input[0])
	height := len(input)

	energized := make([][]bool, height)
	for i := 0; i < height; i++ {
		energized[i] = make([]bool, width)
	}

	return contraption{
		grid:      input,
		visited:   make(map[posAndDir]bool),
		energized: energized,
		width:     width,
		height:    height,
	}
}

func (c *contraption) castBeam(x, y, dx, dy int) {
	if x < 0 || x >= c.width || y < 0 || y >= c.height {
		return
	}

	p := posAndDir{x: x, y: y, dx: dx, dy: dy}
	if c.visited[p] == true {
		return
	}

	c.visited[p] = true
	c.energized[y][x] = true

	ch := c.grid[y][x]
	if ch == '/' {
		if dx != 0 {
			dy = -dx
			dx = 0
		} else {
			dx = -dy
			dy = 0
		}
		c.castBeam(x+dx, y+dy, dx, dy)
	} else if ch == '\\' {
		if dx != 0 {
			dy = dx
			dx = 0
		} else {
			dx = dy
			dy = 0
		}
		c.castBeam(x+dx, y+dy, dx, dy)
	} else if ch == '|' && dx != 0 {
		c.castBeam(x, y+1, 0, 1)
		c.castBeam(x, y-1, 0, -1)
	} else if ch == '-' && dy != 0 {
		c.castBeam(x+1, y, 1, 0)
		c.castBeam(x-1, y, -1, 0)
	} else {
		c.castBeam(x+dx, y+dy, dx, dy)
	}
}

func (c *contraption) countEnergized() int {
	count := 0

	for _, row := range c.energized {
		for _, e := range row {
			if e {
				count += 1
			}
		}
	}

	return count
}

func (c *contraption) reset() {
	c.visited = make(map[posAndDir]bool)
	for row := 0; row < c.height; row++ {
		for col := 0; col < c.width; col++ {
			c.energized[row][col] = false
		}
	}
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("usage: go run main.go path/to/input.txt")
		os.Exit(1)
	}

	bytes, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	input := strings.Split(strings.Trim(string(bytes), "\n"), "\n")

	c := newContraption(input)
	c.castBeam(0, 0, 1, 0)

	fmt.Printf("[PART 1] Number of energized tiles: %d\n", c.countEnergized())

	largest := 0

	for row := 0; row < c.height; row++ {
		// start on left side
		c.reset()
		c.castBeam(0, row, 1, 0)
		res := c.countEnergized()
		largest = max(largest, res)

		// start on right side
		c.reset()
		c.castBeam(c.width-1, row, -1, 0)
		res = c.countEnergized()
		largest = max(largest, res)
	}

	for col := 0; col < c.height; col++ {
		// start on top side
		c.reset()
		c.castBeam(col, 0, 1, 0)
		res := c.countEnergized()
		largest = max(largest, res)

		// start on bottom side
		c.reset()
		c.castBeam(col, c.height-1, -1, 0)
		res = c.countEnergized()
		largest = max(largest, res)
	}

	fmt.Printf("[PART 2] Number of energized tiles: %d\n", largest)
}
