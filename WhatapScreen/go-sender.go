package main
import(
	"time"
	"fmt"
	"math"
	"measure"
	"github.com/golang/protobuf/proto"

	"github.com/zeromq/goczmq"
)

var (
	conn *goczmq.Sock
)

func getSession()(*goczmq.Sock, error){
	if conn ==nil{
		dealer, err := goczmq.NewDealer("tcp://127.0.0.1:5555")
		if err != nil {
			return nil, err
		}
		conn = dealer 
	}
	return conn, nil
}

func upload(buf []byte){
	dealer, err := getSession()
	if err != nil {
		fmt.Println(err)
		return
	}
	
	err = dealer.SendFrame(buf, goczmq.FlagNone)
	if err != nil {
		fmt.Println(err)
		return
	}


}

func summary(tags map[string]string, reqc <- chan *[]float32){
	
	for{
		bufclone := <- reqc
		now := time.Now()
		reduce := map[string]int32{}
		for _, val := range *bufclone{
			val := fmt.Sprint(math.Floor(float64(val*float32(math.Pow10(precision)))) / math.Pow10(precision))
			if _, ok := reduce[val]; !ok {
				reduce[val] = 0
			}
			reduce[val] += 1
		}
		

		mp := measure.MeasurePayload()
		for k, v:= range tags{
			mp.Tags = append(mp.Tags, measure.IntField{Key: k, Value: v})
		}
		for k, v := range reduce{
			mp.FloatFields = append(mp.FloatField, measure.FloatField{Key: k, Value: v})
		}

		out, err := proto.Marshal(mp)
		if err == nil {
			send(out)			
		}else{
			fmt.Println(err)
		}
	}

}