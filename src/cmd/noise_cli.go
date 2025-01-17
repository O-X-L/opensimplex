package main

import (
	"encoding/json"
	"flag"
	"log"
	"math"
	"os"
	"time"

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

func (n *simplexNoise) get_extended_2d_array(size int64, pos_x float64, pos_y float64, silent bool) ([]float32, float32) {
	if !silent {
		log.Println("Generate 2D array..")
	}
	d := []float32{}
	m := float32(0)

	for x := range size {
		for y := range size {
			xa := float64(x) + pos_x
			ya := float64(y) + pos_y
			h := n.get_extended_2d(xa, ya)
			d = append(d, float32(xa), float32(ya), h)
			if h > m {
				m = h
			}
		}
	}

	return d, m
}

type noiseArrayJSON struct {
	Data []float32 `json:"data"`
	Max  float32   `json:"max"`
}

func export_to_json(d []float32, m float32, o string, silent bool) {
	n := noiseArrayJSON{Data: d, Max: m}
	json, err := json.Marshal(n)
	if err != nil {
		log.Fatalf("Error encoding data: %v\n", err)
	}
	err = os.WriteFile(o, json, 0644)
	if err != nil {
		log.Fatalf("Error writing data: %v\n", err)
	}
	if !silent {
		log.Printf("Data written to file: %v\n", o)
	}
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
	size := flag.Int64("size", 1000, "Map Size")
	pos_x := flag.Float64("x", 0, "Position X")
	pos_y := flag.Float64("y", 0, "Position Y")
	// pos_z := flag.Float64("z", 0, "Position Z")
	// pos_w := flag.Float64("w", 0, "Position W")
	out_file := flag.String("out", "/tmp/map.json", "Map Output File")

	silent := flag.Bool("silent", false, "Do not show output")

	flag.Parse()

	if *dimensions != 2 {
		log.Fatalln("Currently only 2D arrays are supported by this CLI")
	}

	if *seed == -1 {
		t := time.Now().UnixMilli()
		seed = &t
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

	m, d := noise.get_extended_2d_array(*size, *pos_x, *pos_y, *silent)
	export_to_json(m, d, *out_file, *silent)
}
