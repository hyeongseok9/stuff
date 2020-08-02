package main

import (
	//	"time"
	"fmt"
	"math"

	"github.com/golang/protobuf/proto"

	"github.com/namhs9/measure"
	"github.com/zeromq/goczmq"
)

var (
	conn *goczmq.Sock
)

func getSession() (*goczmq.Sock, error) {
	if conn == nil {
		fmt.Println("trying to connect")
		dealer, err := goczmq.NewReq("tcp://localhost:5555")
		fmt.Println("connected ", err)
		if err != nil {
			return nil, err
		}
		conn = dealer
	}
	return conn, nil
}

func upload(buf []byte) {
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
	_, _, _ = dealer.RecvFrame()
}

func summary(tags map[string]string, reqc <-chan *[]float32) {
	precision := 2
	for {
		bufclone := <-reqc
		fmt.Println("Preparing send")
		reduce := map[string]int32{}
		total := 0
		for _, val := range *bufclone {
			val := fmt.Sprint(math.Floor(float64(val*float32(math.Pow10(precision)))) / math.Pow10(precision))
			if _, ok := reduce[val]; !ok {
				reduce[val] = 0
			}
			reduce[val] += 1
			total++
		}

		mp := measure.MeasurePayload{}
		for k, v := range tags {
			mp.Tags = append(mp.Tags, &measure.Tag{Key: k, Value: v})
		}
		for k, v := range reduce {
			mp.FloatFields = append(mp.FloatFields, &measure.FloatField{Key: k, Value: 100 * float32(v) / float32(total)})
		}

		out, err := proto.Marshal(&mp)
		if err == nil {
			fmt.Println("Sending ", len(out))
			upload(out)
			fmt.Println("Send Complete ")
		} else {
			fmt.Println(err)
		}
	}

}
