package main

import (
	"C"

	opensimplex_noise "github.com/ojrac/opensimplex-go"
)

//export get_2d
func get_2d(seed int64, x float32, y float32) float32 {
	return opensimplex_noise.New32(seed).Eval2(x, y)
}

//export get_3d
func get_3d(seed int64, x float32, y float32, z float32) float32 {
	return opensimplex_noise.New32(seed).Eval3(x, y, z)
}

//export get_4d
func get_4d(seed int64, x float32, y float32, z float32, w float32) float32 {
	return opensimplex_noise.New32(seed).Eval4(x, y, z, w)
}

func main() {}
