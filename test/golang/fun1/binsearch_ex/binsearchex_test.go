package binsearch_ex

import (
	"bufio"
	"bytes"
	"encoding/binary"
	"encoding/csv"
	"encoding/gob"
	"fmt"
	"io"
	"os"
	"strconv"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func setup() (*os.File, *os.File, error) {
	// testArr := []DummyElem{
	// 	DummyElem{index: 1, msg: "one"},
	// 	DummyElem{index: 2, msg: "two"},
	// 	DummyElem{index: 3, msg: "three"},
	// 	DummyElem{index: 4, msg: "four"},
	// 	DummyElem{index: 5, msg: "five"},
	// 	DummyElem{index: 6, msg: "six"},
	// 	DummyElem{index: 7, msg: "seven"},
	// 	DummyElem{index: 8, msg: "eight"},
	// 	DummyElem{index: 9, msg: "nine"},
	// }

	fIndex, err := os.Create("gob.encoded.idx")
	if err != nil {
		return nil, nil, err
	}
	//defer fIndex.Close()

	datafile, err := os.Create("gob.encoded.dat")
	if err != nil {
		return nil, nil, err
	}
	enc := gob.NewEncoder(datafile)

	csvfile, _ := os.Open("./CSV.csv")
	defer csvfile.Close()
	// csv reader 생성
	rdr := csv.NewReader(bufio.NewReader(csvfile))

	// csv 내용 모두 읽기
	rows, _ := rdr.ReadAll()

	// 행,열 읽기
	for i, row := range rows {
		if i == 0 {
			continue
		}
		priceDate, err := time.Parse("2006-01-02", row[0])
		if err != nil {
			fmt.Println("time parse error ", row[0])
			return nil, nil, err
		}
		open, _ := strconv.ParseFloat(row[1], 32)
		high, _ := strconv.ParseFloat(row[1], 32)
		low, _ := strconv.ParseFloat(row[1], 32)
		close, _ := strconv.ParseFloat(row[1], 32)
		adjClose, _ := strconv.ParseFloat(row[1], 32)
		volume, _ := strconv.ParseInt(row[1], 10, 32)

		s := StockPrice{
			Date:     priceDate,
			Open:     float32(open),
			High:     float32(high),
			Low:      float32(low),
			Close:    float32(close),
			AdjClose: float32(adjClose),
			Volume:   int32(volume),
		}
		posBefore, err := datafile.Seek(0, io.SeekCurrent)
		if err != nil {
			return nil, nil, err
		}
		enc.Encode(s)
		posAfter, err := datafile.Seek(0, io.SeekCurrent)
		if err != nil {
			return nil, nil, err
		}
		length := posAfter - posBefore
		binary.Write(fIndex, binary.BigEndian, posBefore)
		binary.Write(fIndex, binary.BigEndian, length)
		if i == 629 {
			fmt.Println("Writing priceDate:", priceDate, " pos:", posBefore, " length:", length)
		}
	}

	idxFileSize, _ := fIndex.Seek(0, io.SeekEnd)
	fmt.Println("idxFileSize:", idxFileSize)

	return datafile, fIndex, nil
}

func TestBinSearchFilebased(t *testing.T) {
	testdata, idxdata, err := setup()
	if err != nil {
		assert.Fail(t, fmt.Sprint(err))
		return
	}
	expectedIndex, _ := time.Parse("2006-01-02", "2017-02-02")
	expected := float32(26.0)
	actual, err := searchBinary(testdata, idxdata, expectedIndex)
	if err != nil {
		assert.Fail(t, fmt.Sprint(err))
		return
	}

	assert.Equal(t, expected, actual.Open, "not expected")
}

func TestWriteIndex(t *testing.T) {
	fIndex, err := os.Create("test.idx")
	if err != nil {
		assert.Fail(t, fmt.Sprint(err))
		return
	}

	posBefore := int64(10000)
	binary.Write(fIndex, binary.BigEndian, posBefore)
	// binary.Write(fIndex, binary.BigEndian, length)
	pos, _ := fIndex.Seek(0, io.SeekEnd)
	fmt.Println("single int64 bytes:", pos)
	fIndex.Close()

}

func TestSerialIndex(t *testing.T) {

	fIndex, err := os.Create("test2.idx")
	if err != nil {
		assert.Fail(t, fmt.Sprint(err))
		return
	}
	defer fIndex.Close()

	var buf bytes.Buffer

	priceDate := time.Now()
	open := float32(1)
	high := float32(1)
	low := float32(1)
	close := float32(1)
	adjClose := float32(1)
	volume := float32(1)

	s := StockPrice{
		Date:     priceDate,
		Open:     float32(open),
		High:     float32(high),
		Low:      float32(low),
		Close:    float32(close),
		AdjClose: float32(adjClose),
		Volume:   int32(volume),
	}

	enc := gob.NewEncoder(&buf)
	err = enc.Encode(&StockPrice{})
	if err != nil {
		assert.Fail(t, "readStockPrice step -4", err)
		return
	}
	var readbuf bytes.Buffer
	readbuf.Write(buf.Bytes())
	// fmt.Println(hex.EncodeToString(headerBytes))

	sizearray := [][]int64{[]int64{0, 0}, []int64{0, 0}, []int64{0, 0}, []int64{0, 0}}
	for i := 0; i < 4; i++ {
		posBefore, _ := fIndex.Seek(0, io.SeekCurrent)
		buf.Reset()

		enc.Encode(s)
		fIndex.Write(buf.Bytes())
		posAfter, _ := fIndex.Seek(0, io.SeekCurrent)
		sizearray[i][0] = posBefore
		sizearray[i][1] = posAfter - posBefore

	}

	sp := StockPrice{}

	r := bufio.NewReader(&readbuf)
	dec := gob.NewDecoder(r)

	err = dec.Decode(&sp)
	if err != nil {
		assert.Fail(t, "readStockPrice step -5", err)
		return
	}

	targetIndex := 2

	fIndex.Seek(sizearray[targetIndex][0], io.SeekStart)
	readbytes := make([]byte, sizearray[targetIndex][1])
	fIndex.Read(readbytes)
	readbuf.Reset()
	readbuf.Write(readbytes)

	err = dec.Decode(&sp)
	if err != nil {
		assert.Fail(t, "readStockPrice step -6", err)
		return
	}
	fmt.Println("Stock Price: ", sp)
}
