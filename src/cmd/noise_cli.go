package main

import (
	"flag"
	"log"
	"math"
	"time"

	"github.com/O-X-L/python-opensimplex/internal"
	opensimplex_noise "github.com/ojrac/opensimplex-go"
)

const A = 0.5

type simplexNoise struct {
	// seed           int
	persistence    float64
	scale          float64
	octaves        int
	lacunarity     float64
	exponentiation float64
	height         float64
	generator      opensimplex_noise.Noise32
}

func (n *simplexNoise) get_2d(x float32, y float32) float32 {
	return n.generator.Eval2(x, y)
}

/*
func (n *simplexNoise) get_3d(x float64, y float64, z float64) float64 {
	return n.generator.Eval3(x, y, z)
}

func (n *simplexNoise) get_4d(x float64, y float64, z float64, w float64) float64 {
	return n.generator.Eval4(x, y, z, w)
}
*/

// based on: https://github.com/simondevyoutube/ProceduralTerrain_Part10/blob/main/src/noise.js#L15
func (n *simplexNoise) get_extended_2d(x float64, y float64) float32 {
	xs := float32(x / n.scale)
	ys := float32(y / n.scale)
	g := float32(math.Pow(2.0, -n.persistence))
	amplitude := float32(1.0)
	frequency := float32(1.0)
	normalization := float32(0)
	total := float32(0)
	var v float32

	for range n.octaves {
		v = n.get_2d(
			xs*frequency,
			ys*frequency,
		)*A + A
		total += v * amplitude
		normalization += amplitude
		amplitude *= g
		frequency *= float32(n.lacunarity)
	}

	total /= normalization
	if total < 0 {
		total = total * -1
	}
	return float32(math.Pow(float64(total), n.exponentiation) * n.height)
}

func (n *simplexNoise) get_extended_2d_array(size int64, pos_x float64, pos_y float64, silent bool) ([]float32, float32, float32) {
	if !silent {
		log.Println("Generate 2D array..")
	}
	d := []float32{}
	max := float32(0)
	min := float32(100000)

	for x := range size {
		for y := range size {
			xa := float64(x) + pos_x
			ya := float64(y) + pos_y
			h := n.get_extended_2d(xa, ya)
			d = append(d, float32(xa), float32(ya), h)
			if h > max {
				max = h
			}
			if h < min {
				min = h
			}
		}
	}

	return d, max, min
}

func main() {
	seed := flag.Int64("seed", -1, "Seed")
	persistence := flag.Float64("persistence", 0.7, "Persistence")
	scale := flag.Float64("scale", 50.0, "Scale")
	octaves := flag.Int("octaves", 10, "Octaves")
	lacunarity := flag.Float64("lacunarity", 1.5, "Lacunarity")
	exponentiation := flag.Float64("exponentiation", 5.0, "Exponentiation")
	height := flag.Float64("height", 135.0, "Height")

	dimensions := flag.Int("dimensions", 2, "Dimensions")
	size := flag.Int64("size", 1000, "Map size")
	pos_x := flag.Float64("x", 0, "Map offset dimension-X")
	pos_y := flag.Float64("y", 0, "Map offset dimension-Y")
	// pos_z := flag.Float64("z", 0, "Map offset dimension-Z")
	// pos_w := flag.Float64("w", 0, "Map offset dimension-W")

	sink_down := flag.Bool("sink", false, "If the whole noise-map should be sunk-down so the lowest point is 0")
	lower_by := flag.Float64("lower", -1, "Lower each height by this value - negatives are clamped to 0")
	out_file := flag.String("out", "/tmp/map.json", "Map output file")
	silent := flag.Bool("silent", false, "Do not show output")
	export_no_coords := flag.Bool("no-coords", false, "If enabled the coords will be omitted from the data-export")
	mirror := flag.String("mirror", "", "To mirror the values set this to one of: 'x', 'y', 'xy', 'reverse'")
	rotate := flag.String("rotate", "", "To rotate the values set this to one of: '90cw', '90ccw', '180'")

	flag.Parse()

	if *dimensions != 2 {
		log.Fatalln("Currently only 2D arrays are supported by this CLI")
	}

	if *seed == -1 {
		t := time.Now().UnixMilli()
		seed = &t
	}

	if !*silent {
		log.Println("Seed: ", *seed)
	}

	noise := simplexNoise{
		persistence:    *persistence,
		scale:          *scale,
		octaves:        *octaves,
		lacunarity:     *lacunarity,
		exponentiation: *exponentiation,
		height:         *height,
		generator:      opensimplex_noise.New32(*seed),
	}

	d, max, min := noise.get_extended_2d_array(*size, *pos_x, *pos_y, *silent)
	if *sink_down {
		d, max, min = internal.UpdateSinkDown(d, min, max, *silent, *dimensions)
	}
	if *lower_by != -1 {
		d, max, min = internal.UpdateLowerBy(d, min, max, float32(*lower_by), *silent, *dimensions)
	}

	if *mirror == "xy" || *mirror == "reverse" {
		d = internal.UpdateMirrorX(d, *silent, *dimensions, *size)
		d = internal.UpdateMirrorY(d, *silent, *dimensions, *size)
	} else if *mirror == "x" {
		d = internal.UpdateMirrorX(d, *silent, *dimensions, *size)
	} else if *mirror == "y" {
		d = internal.UpdateMirrorY(d, *silent, *dimensions, *size)
	}

	if *rotate == "90cw" {
		d = internal.UpdateRotate90CW(d, *silent, *dimensions, *size)
	} else if *rotate == "90ccw" {
		d = internal.UpdateRotate90CCW(d, *silent, *dimensions, *size)
	} else if *rotate == "180" {
		d = internal.UpdateRotate180(d, *silent, *dimensions, *size)
	}

	if *export_no_coords {
		d = internal.UpdateStripCoords(d, *silent, *dimensions)
	}
	internal.ExportToJSON(d, max, min, *out_file, *silent)
}
