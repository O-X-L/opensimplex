package internal

import (
	"encoding/json"
	"log"
	"os"
)

type noiseArrayJSON struct {
	Data []float32 `json:"data"`
	Max  float32   `json:"max"`
	Min  float32   `json:"min"`
}

func ExportToJSON(d []float32, max float32, min float32, o string, silent bool) {
	n := noiseArrayJSON{Data: d, Max: max, Min: min}
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

func UpdateSinkDown(d []float32, min float32, max float32, silent bool, dimensions int) ([]float32, float32, float32) {
	if !silent {
		log.Println("Sinking noise-map..")
	}
	var ih int
	md := dimensions + 1
	for i := range len(d) / md {
		ih = i*md + dimensions
		d[ih] = d[ih] - min
	}
	max -= min
	min = 0
	return d, max, min
}

func UpdateLowerBy(d []float32, min float32, max float32, lower float32, silent bool, dimensions int) ([]float32, float32, float32) {
	if !silent {
		log.Println("Lowering noise-map..")
	}
	var ih int
	md := dimensions + 1
	for i := range len(d) / md {
		ih = i*md + dimensions
		d[ih] -= lower
		if d[ih] < 0 {
			d[ih] = 0
		}
	}
	max -= lower
	if max < 0 {
		max = 0
	}
	min -= lower
	if min < 0 {
		min = 0
	}
	return d, max, min
}

func UpdateStripCoords(d []float32, silent bool, dimensions int) []float32 {
	if !silent {
		log.Println("Stripping coords..")
	}
	var ih int
	var d2 []float32
	md := dimensions + 1
	for i := range len(d) / md {
		ih = i*md + dimensions
		d2 = append(d2, d[ih])
	}
	return d2
}

func updateMirrorX(d []float32, dimensions int, size int64) []float32 {
	// todo: test with 3D/4D
	var src, dst, s, hi int
	d2 := make([]float32, len(d))
	copy(d2, d)
	s = int(size)
	md := dimensions + 1
	f := s * s * md

	for x := range s {
		for y := range s {
			hi = y*md + dimensions
			// begin: at first value of last row
			src = (f - ((x + 1) * s * md)) + hi
			// begin: at first value of first row
			dst = (x * s * md) + hi
			d2[dst] = d[src]
		}
	}

	return d2
}

func updateMirrorY(d []float32, dimensions int, size int64) []float32 {
	// todo: test with 3D/4D
	var src, dst, s int
	d2 := make([]float32, len(d))
	copy(d2, d)
	s = int(size)
	md := dimensions + 1

	for y := range s {
		for x := range s {
			// begin: at last value of first row
			src = ((y + 1) * s * md) - (x*md + 1)
			// begin: at first value of first row
			dst = (y * s * md) + (x*md + dimensions)
			d2[dst] = d[src]
		}
	}

	return d2
}

func UpdateMirrorY(d []float32, silent bool, dimensions int, size int64) []float32 {
	if !silent {
		log.Println("Mirroring on Y-axis..")
	}
	return updateMirrorY(d, dimensions, size)
}

func UpdateMirrorX(d []float32, silent bool, dimensions int, size int64) []float32 {
	// todo: test with 3D/4D
	if !silent {
		log.Println("Mirroring on X-axis..")
	}
	return updateMirrorX(d, dimensions, size)
}

func UpdateMirrorXY(d []float32, silent bool, dimensions int, size int64) []float32 {
	if !silent {
		log.Println("Mirroring on X- & Y-axis..")
	}
	d = updateMirrorX(d, dimensions, size)
	return updateMirrorY(d, dimensions, size)
}

func updateRotate90CW(d []float32, dimensions int, size int64) []float32 {
	// todo: test with 3D/4D
	var src, dst, s int
	d2 := make([]float32, len(d))
	copy(d2, d)
	s = int(size)
	md := dimensions + 1

	for x := range s {
		for y := range s {
			// begin: first value of last row; end: first value of first row
			src = ((s - (y + 1)) * s * md) + (x*md + dimensions)
			// begin: first value of first row; end: last value of first row
			dst = (x * s * md) + (y*md + dimensions)
			d2[dst] = d[src]
		}
	}

	return d2
}

func UpdateRotate90CW(d []float32, silent bool, dimensions int, size int64) []float32 {
	if !silent {
		log.Println("Rotating 90° clockwise..")
	}
	return updateRotate90CW(d, dimensions, size)
}

func UpdateRotate180(d []float32, silent bool, dimensions int, size int64) []float32 {
	if !silent {
		log.Println("Rotating 180°..")
	}
	d = updateRotate90CW(d, dimensions, size)
	return updateRotate90CW(d, dimensions, size)
}

func UpdateRotate90CCW(d []float32, silent bool, dimensions int, size int64) []float32 {
	if !silent {
		log.Println("Rotating 90° counter-clockwise..")
	}
	// todo: test with 3D/4D
	var src, dst, s int
	d2 := make([]float32, len(d))
	copy(d2, d)
	s = int(size)
	md := dimensions + 1

	for x := range s {
		for y := range s {
			// begin: first value of first row; end: last value of first row
			src = (x * s * md) + (y*md + dimensions)
			// begin: first value of last row; end: first value of first row
			dst = ((s - (y + 1)) * s * md) + (x*md + dimensions)
			d2[dst] = d[src]
		}
	}

	return d2
}
