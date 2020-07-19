package osinfo

import (
	"container/ring"
	"fmt"
	"math"
	"runtime/pprof"
	"sync"
	"time"
	"whatap/util/singleton"

	"net/http"

	"github.com/gorilla/mux"
	"github.com/shirou/gopsutil/cpu"
	"github.com/wcharczuk/go-chart" //exposes "chart"
)

var (
	calculator *RunningStatsCalculator
)

func CpuUsagePercent() (result float64) {
	cpus, _ := cpu.Percent(0, false)
	if cpus != nil && len(cpus) > 0 {
		result = cpus[0]
	}
	return
}

var Thread = singleton.NewSingletonTimer(
	calcStdDev,
	func() int32 {
		return 50
	})

type RunningStatsCalculator struct {
	count    uint32
	mean     float32
	dSquared float32
	calcLock sync.Mutex
	buf      *ring.Ring
}

func (self *RunningStatsCalculator) Init() {
	self.calcLock = sync.Mutex{}
	self.buf = ring.New(1200)
}

type ClockValue struct {
	clock time.Time
	val   float32
}

func (self *RunningStatsCalculator) Update(newValue float32) {
	self.calcLock.Lock()
	defer self.calcLock.Unlock()

	self.count++

	meanDifferential := (newValue - self.mean) / float32(self.count)

	newMean := self.mean + meanDifferential

	dSquaredIncrement :=
		(newValue - newMean) * (newValue - self.mean)

	newDSquared := self.dSquared + dSquaredIncrement

	self.mean = newMean

	self.dSquared = newDSquared
	self.buf.Value = ClockValue{clock: time.Now(), val: newValue}
	self.buf = self.buf.Next()
}

func (self *RunningStatsCalculator) Variance() float32 {

	return self.dSquared / float32(self.count)
}

func (self *RunningStatsCalculator) Stdev() float32 {

	return float32(math.Sqrt(float64(self.Variance())))
}

func (self *RunningStatsCalculator) Reset() {
	self.calcLock.Lock()
	defer self.calcLock.Unlock()

	self.count = 0
	self.mean = 0
	self.dSquared = 0
}

func GetInstance() *RunningStatsCalculator {
	if calculator == nil {
		calculator = &RunningStatsCalculator{}
		calculator.Init()
		Thread.Start()
		go debugroutine()
	}

	return calculator
}

func calcStdDev() {
	newValue := CpuUsagePercent()
	calculator.Update(float32(newValue))
}

func GetSTDDev() (result float32) {
	result = GetInstance().Stdev()
	GetInstance().Reset()
	return
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
	if calculator != nil {
		xvalues := make([]time.Time, calculator.buf.Len())
		yvalues := make([]float64, calculator.buf.Len())
		i := 0
		calculator.buf.Do(func(v interface{}) {
			if v != nil {
				clockvalue := v.(ClockValue)
				xvalues[i] = clockvalue.clock
				yvalues[i] = float64(clockvalue.val)

				i++
			}

		})
		graph := chart.Chart{
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

}

func debugGoroutineHandler(w http.ResponseWriter, req *http.Request) {
	contentType := "text/plain"
	w.Header().Add("Content-Type", contentType)
	p := pprof.Lookup("goroutine")
	p.WriteTo(w, 1)
}
