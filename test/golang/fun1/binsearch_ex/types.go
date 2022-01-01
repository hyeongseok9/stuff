package binsearch_ex

import "time"

type DummyElem struct {
	index int
	msg   string
}

/*
Date	Open	High	Low	Close	Adj Close	Volume
2016-12-30	28.719999	28.83	28.459999	28.639999	26.909061	56000

*/
type StockPrice struct {
	Date     time.Time
	Open     float32
	High     float32
	Low      float32
	Close    float32
	AdjClose float32
	Volume   int32
}
