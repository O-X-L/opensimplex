package main

import (
	"C"

	opensimplex_noise "github.com/ojrac/opensimplex-go"
)
import (
	"log"
	"math"
)

var n opensimplex_noise.Noise32

//export set_seed
func set_seed(seed int64) {
	n = opensimplex_noise.New32(seed)
}

//export get_2d
func get_2d(x float32, y float32) float32 {
	return n.Eval2(x, y)
}

//export get_3d
func get_3d(x float32, y float32, z float32) float32 {
	return n.Eval3(x, y, z)
}

//export get_4d
func get_4d(x float32, y float32, z float32, w float32) float32 {
	return n.Eval4(x, y, z, w)
}

func main() {}
