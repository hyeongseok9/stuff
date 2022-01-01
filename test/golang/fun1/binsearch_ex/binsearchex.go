package binsearch_ex

import (
	"bufio"
	"bytes"
	"encoding/binary"
	"encoding/gob"
	"fmt"
	"io"
	"os"
	"time"
)

func getIndexSize(file *os.File) (int64, error) {
	pos, err := file.Seek(0, io.SeekEnd)
	indexSize := pos / 16
	return indexSize, err
}

func readStockPrice(src *os.File, fIndex *os.File, idx int64) (StockPrice, error) {
	var sp StockPrice
	//dec := gob.NewEncoder(src)

	blocksize := 8 * 2
	idxPos := idx * int64(blocksize)
	_, err := fIndex.Seek(idxPos, io.SeekStart)
	fmt.Println("readStockPrice step -1", idx, idxPos, err)
	if err != nil {
		// fmt.Println("readStockPrice step -1", idx, idxPos, err)
		return sp, err
	}
	var pos, length int64
	err = binary.Read(fIndex, binary.BigEndian, &pos)
	if err != nil {
		fmt.Println("readStockPrice step -2", err)
		return sp, err
	}
	binary.Read(fIndex, binary.BigEndian, &length)
	if err != nil {
		fmt.Println("readStockPrice step -3", err)
		return sp, err
	}

	_, err = src.Seek(pos, io.SeekStart)
	if err != nil {
		fmt.Println("readStockPrice step -3.1", err)
		return sp, err
	}
	buf := make([]byte, length)
	nbytethistime, err := src.Read(buf)
	fmt.Println("readStockPrice step -4 pos:", pos,"size:", nbytethistime, " idx:", idx)
	if int64(nbytethistime) != length {

		return sp, fmt.Errorf("cannot read sp block size:%d actual:%d", length, nbytethistime)
	}
	if err != nil {
		fmt.Println("readStockPrice step -5", err)
		return sp, err
	}
	r := bufio.NewReader(bytes.NewBuffer(buf))

	dec := gob.NewDecoder(r)

	err = dec.Decode(&sp)
	if err != nil {
		fmt.Println("readStockPrice step -6", err)
		return sp, err
	}

	return sp, nil
}

func searchBinary(src *os.File, idx *os.File, target time.Time) (StockPrice, error) {
	var sp StockPrice

	n, err := getIndexSize(idx)
	if err != nil {
		return sp, err
	}
	l := int64(0)
	r := n - 1

	var i, m int64
	for i = 1; l <= r && i < n; i++ {
		m = (l + r) / 2
		// fmt.Println("try ", i, " th m:", m)
		sp, err = readStockPrice(src, idx, m)
		if err != nil {
			fmt.Println("searchBinary step -1")
			return sp, err
		}
		if sp.Date.Before(target) {
			l = m + 1
		} else if sp.Date.After(target) {
			r = m - 1
		} else {
			// fmt.Println("search complete in ", i)
			fmt.Println("searchBinary step -2")
			return sp, nil
		}
	}

	return sp, fmt.Errorf("not found")
}
