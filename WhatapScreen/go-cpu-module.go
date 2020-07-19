package main

import (
	"container/ring"
	"fmt"
	"runtime/pprof"
	"time"

	"net/http"

	"github.com/gorilla/mux"
	"github.com/shirou/gopsutil/cpu"
	"github.com/wcharczuk/go-chart" //exposes "chart"
)

const (
	INTERVAL = 50
	BUFSIZE  = 300 * 20
)

var (
	buf     = ring.New(BUFSIZE)
	counter = int32(0)
)

type ClockValue struct {
	clock time.Time
	val   float32
}

func CpuUsagePercent() (result float64) {
	cpus, _ := cpu.Percent(0, false)
	if cpus != nil && len(cpus) > 0 {
		result = cpus[0]
	}
	return
}

func Update(newValue float32) {
	buf.Value = ClockValue{clock: time.Now(), val: newValue}
	buf = buf.Next()
	counter++
}

func Collect() {
	var lastUpdate time.Time
	for {
		now := time.Now()
		if now.Sub(lastUpdate) > time.Millisecond*INTERVAL {
			Update(float32(CpuUsagePercent()))
			lastUpdate = now
		}

		time.Sleep(10 * time.Millisecond)
	}
}

func debugroutine() {
	port := 6801
	r := mux.NewRouter()
	r.HandleFunc("/debug/goroutine", debugGoroutineHandler)
	r.HandleFunc("/debug/cpu/chart.png", debugCpuChartHandler)

	srv := &http.Server{
		Addr:    fmt.Sprintf(":%d", port),
		Handler: r,
	}
	srv.ListenAndServe()

}

func debugCpuChartHandler(w http.ResponseWriter, req *http.Request) {
	contentType := "image/png"
	w.Header().Add("Content-Type", contentType)

	xvalues := make([]time.Time, buf.Len())
	yvalues := make([]float64, buf.Len())
	i := 0
	buf.Do(func(v interface{}) {
		if v != nil {
			clockvalue := v.(ClockValue)
			xvalues[i] = clockvalue.clock
			yvalues[i] = float64(clockvalue.val)

			i++
		}
	})
	graph := chart.Chart{
		Width:  1920 * 10,
		Height: 1080,
		XAxis: chart.XAxis{
			ValueFormatter: func(v interface{}) string {
				if clock, isFloat := v.(float64); isFloat {
					return time.Unix(int64(clock)/1000000000, int64(clock)-(int64(clock)/1000000000)*1000000000).Format("15:04:05.999")
				}
				return ""
			},
		},
		Series: []chart.Series{
			chart.TimeSeries{
				XValues: xvalues,
				YValues: yvalues,
			},
		},
	}

	// buffer := bytes.NewBuffer([]byte{})
	graph.Render(chart.PNG, w)

}

func debugGoroutineHandler(w http.ResponseWriter, req *http.Request) {
	contentType := "text/plain"
	w.Header().Add("Content-Type", contentType)
	p := pprof.Lookup("goroutine")
	p.WriteTo(w, 1)
}

func main() {
	go Collect()

	for counter < BUFSIZE {
		fmt.Println("counter:", counter)
		time.Sleep(1 * time.Second)
	}
	debugroutine()
}
