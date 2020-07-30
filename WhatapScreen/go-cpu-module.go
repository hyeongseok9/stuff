package main

import (
	"container/ring"
	"fmt"
	"math"
	"runtime/pprof"
	"sort"
	"strconv"
	"time"
	"os"
	"net"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/shirou/gopsutil/cpu"
	"github.com/wcharczuk/go-chart" //exposes "chart"
//	"github.com/namhs9/measure"
)

const (
	INTERVAL    = 50
	MEASURE_MIN = 1
	BUFSIZE     = 6 * MEASURE_MIN * 60 * (1000 / INTERVAL)
)

var (
	buf     = ring.New(BUFSIZE)
	bufclone  = make([]float32,BUFSIZE)
	counter = int32(0)
	reqc = make(chan *[]float32)

)

type ClockValue struct {
	clock time.Time
	val   float32
}

func CpuUsagePercent() (result []float64) {
	cpus, _ := cpu.Percent(0, true)
	if cpus != nil && len(cpus) > 0 {
		result = cpus
	}
	return
}

func Update(newValue float32) {
	buf.Value = ClockValue{clock: time.Now(), val: newValue}
	buf = buf.Next()
	counter++
	if counter > 0 && counter % BUFSIZE == 0{
		i := int32(0)
		buf.Do(func(v interface{}) {
			if v != nil {
				clockvalue := v.(ClockValue)
				bufclone[i%BUFSIZE] = clockvalue.val
				i += 1
			}
		})
		reqc <- &bufclone	
	}
}

func Collect() {
	var lastUpdate time.Time
	for {
		now := time.Now()
		if now.Sub(lastUpdate) > time.Millisecond*INTERVAL {
			for _, cpuPct := range CpuUsagePercent() {
				Update(float32(cpuPct))
			}

			lastUpdate = now
		}

		time.Sleep(10 * time.Millisecond)
	}
}

func debugroutine() {
	port := 6801
	r := mux.NewRouter()
	r.HandleFunc("/debug/goroutine", debugGoroutineHandler)
	r.HandleFunc("/debug/cpu/history.png", debugCpuHistoryHandler)
	r.HandleFunc("/debug/cpu/pie.png", debugCpuPieHandler)
	r.HandleFunc("/debug/cpu/bar.png", debugCpuBarHandler)
	r.HandleFunc("/debug/cpu/pie.csv", debugCpuCSVHandler)

	srv := &http.Server{
		Addr:    fmt.Sprintf(":%d", port),
		Handler: r,
	}
	srv.ListenAndServe()

}

func debugCpuPieHandler(w http.ResponseWriter, req *http.Request) {
	vars := mux.Vars(req)
	strprecision := vars["prec"]
	precision := 2
	if len(strprecision) > 0 {
		i, err := strconv.ParseInt(strprecision, 10, 64)
		if err == nil {
			precision = int(i)
		}
	}
	contentType := "image/png"
	w.Header().Add("Content-Type", contentType)

	reduce := map[string]int32{}
	buf.Do(func(v interface{}) {
		if v != nil {
			clockvalue := v.(ClockValue)
			val := fmt.Sprint(math.Floor(float64(clockvalue.val*float32(math.Pow10(precision)))) / math.Pow10(precision))
			fmt.Println(val, clockvalue.val, math.Pow10(precision))
			if _, ok := reduce[val]; !ok {
				reduce[val] = 0
			}
			reduce[val] += 1
		}
	})

	var keys []string
	for k := range reduce {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	var values []chart.Value
	for _, k := range keys {
		key := k
		v := reduce[key]
		values = append(values, chart.Value{Value: float64(v), Label: fmt.Sprint(key)})
	}
	graph := chart.PieChart{
		Width:  1920,
		Height: 1080,
		Values: values,
	}

	graph.Render(chart.PNG, w)
}

func debugCpuBarHandler(w http.ResponseWriter, req *http.Request) {
	vars := mux.Vars(req)
	strprecision := vars["prec"]
	precision := 2
	if len(strprecision) > 0 {
		i, err := strconv.ParseInt(strprecision, 10, 64)
		if err == nil {
			precision = int(i)
		}
	}
	contentType := "image/png"
	w.Header().Add("Content-Type", contentType)

	reduce := map[float32]int32{}
	buf.Do(func(v interface{}) {
		if v != nil {
			clockvalue := v.(ClockValue)
			val := float32(math.Floor(float64(clockvalue.val*float32(math.Pow10(precision)))) / math.Pow10(precision))
			fmt.Println(val, clockvalue.val, math.Pow10(precision))
			if _, ok := reduce[val]; !ok {
				reduce[val] = 0
			}
			reduce[val] += 1
		}
	})

	var keys []float64
	for _, k := range reduce {
		keys = append(keys, float64(k))
	}
	sort.Float64s(keys)

	var values []chart.Value
	for _, k := range keys {
		key := float32(k)
		v := reduce[key]
		values = append(values, chart.Value{Value: float64(v), Label: fmt.Sprint(key)})
	}
	graph := chart.BarChart{
		Width:  1920,
		Height: 1080,
		Bars:   values,
	}

	graph.Render(chart.PNG, w)
}
func debugCpuHistoryHandler(w http.ResponseWriter, req *http.Request) {
	contentType := chart.ContentTypePNG
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

func debugCpuCSVHandler(w http.ResponseWriter, req *http.Request) {
	vars := mux.Vars(req)
	strprecision := vars["prec"]
	precision := 2
	if len(strprecision) > 0 {
		i, err := strconv.ParseInt(strprecision, 10, 64)
		if err == nil {
			precision = int(i)
		}
	}
	contentType := "plain/text"
	w.Header().Add("Content-Type", contentType)

	reduce := map[float32]int32{}
	buf.Do(func(v interface{}) {
		if v != nil {
			clockvalue := v.(ClockValue)
			val := float32(math.Floor(float64(clockvalue.val*float32(math.Pow10(precision)))) / math.Pow10(precision))
			fmt.Println(val, clockvalue.val, math.Pow10(precision))
			if _, ok := reduce[val]; !ok {
				reduce[val] = 0
			}
			reduce[val] += 1
		}
	})

	var keys []float64
	for k := range reduce {
		keys = append(keys, float64(k))
	}
	sort.Float64s(keys)

	for _, k := range keys {
		key := float32(k)
		v := reduce[key]
		w.Write([]byte(fmt.Sprint(key, ",", v, "\n")))
	}

}

func debugGoroutineHandler(w http.ResponseWriter, req *http.Request) {
	contentType := "text/plain"
	w.Header().Add("Content-Type", contentType)
	p := pprof.Lookup("goroutine")
	p.WriteTo(w, 1)
}

func getIp()string{
	ifaces, _ := net.Interfaces()
// handle err
	for _, i := range ifaces {
		addrs, _ := i.Addrs()
		// handle err
		for _, addr := range addrs {
			var ip net.IP
			switch v := addr.(type) {
			case *net.IPNet:
					ip = v.IP
			case *net.IPAddr:
					ip = v.IP
			}
			if ip != nil{
				return ip.String()
			}
		}
	}

	return ""
}

func main() {
	tags := map[string]string{}
	tags["ip"]= getIp()
	hostname, _ := os.Hostname()
	tags["hostname"]= hostname
	go summary(tags, reqc)
	go Collect()

	for counter < BUFSIZE {
		fmt.Println("counter:", counter)
		time.Sleep(1 * time.Second)
	}
	debugroutine()
}
