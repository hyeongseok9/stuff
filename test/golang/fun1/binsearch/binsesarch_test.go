package binsearch

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestBinSearch(t *testing.T) {
	testArr := []DummyElem{
		DummyElem{index: 1, msg: "one"},
		DummyElem{index: 2, msg: "two"},
		DummyElem{index: 3, msg: "three"},
		DummyElem{index: 4, msg: "four"},
		DummyElem{index: 5, msg: "five"},
		DummyElem{index: 6, msg: "six"},
		DummyElem{index: 7, msg: "seven"},
		DummyElem{index: 8, msg: "eight"},
		DummyElem{index: 9, msg: "nine"},
	}
	expectedIndex := 8
	expected := "eight"
	actual, err := searchBinary(testArr, expectedIndex)
	if err != nil {
		assert.Fail(t, fmt.Sprint(err))
		return
	}

	assert.Equal(t, expected, actual, "not expected")
}

func TestRangeSearch(t *testing.T) {
	testArr := []DummyElem{
		DummyElem{index: 10, msg: "ten"},
		DummyElem{index: 20, msg: "twenty"},
		DummyElem{index: 30, msg: "thirty"},
		DummyElem{index: 40, msg: "fourty"},
		DummyElem{index: 50, msg: "fifty"},
		DummyElem{index: 60, msg: "sixty"},
		DummyElem{index: 70, msg: "seventy"},
		DummyElem{index: 80, msg: "eighty"},
		DummyElem{index: 90, msg: "ninety"},
	}
	startIndex := 11
	endIndex := 55

	elemCheck := map[int]bool{}
	err := searchBinaryRange(testArr, startIndex, endIndex, func(d DummyElem) {
		assert.True(t, d.index >= startIndex && d.index <= endIndex, fmt.Sprint("overshoot ", d.index))
		elemCheck[d.index] = true
		// fmt.Println("found ", d.index, d.msg)
	})
	if err != nil {
		assert.Fail(t, fmt.Sprint(err))
		return
	}
	assert.Equal(t, 4, len(elemCheck), "target count not match ")
	for _, index := range []int{20, 30, 40, 50} {
		_, ok := elemCheck[index]
		assert.True(t, ok, fmt.Sprint("elem ", index, " not found"))
	}
}

func TestRangeSearch2(t *testing.T) {
	testArr := []DummyElem{
		DummyElem{index: 10, msg: "ten"},
		DummyElem{index: 20, msg: "twenty"},
		DummyElem{index: 30, msg: "thirty"},
		DummyElem{index: 40, msg: "fourty"},
		DummyElem{index: 50, msg: "fifty"},
		DummyElem{index: 60, msg: "sixty"},
		DummyElem{index: 70, msg: "seventy"},
		DummyElem{index: 80, msg: "eighty"},
		DummyElem{index: 90, msg: "ninety"},
	}
	startIndex := 1
	endIndex := 55

	elemCheck := map[int]bool{}
	err := searchBinaryRange(testArr, startIndex, endIndex, func(d DummyElem) {
		assert.True(t, d.index >= startIndex && d.index <= endIndex, fmt.Sprint("overshoot ", d.index))
		elemCheck[d.index] = true
		// fmt.Println("found ", d.index, d.msg)
	})
	if err != nil {
		assert.Fail(t, fmt.Sprint(err))
		return
	}
	assert.Equal(t, 5, len(elemCheck), "target count not match ")
	for _, index := range []int{10, 20, 30, 40, 50} {
		_, ok := elemCheck[index]
		assert.True(t, ok, fmt.Sprint("elem ", index, " not found"))
	}
}

func TestRangeSearch3(t *testing.T) {
	testArr := []DummyElem{
		DummyElem{index: 10, msg: "ten"},
		DummyElem{index: 20, msg: "twenty"},
		DummyElem{index: 30, msg: "thirty"},
		DummyElem{index: 40, msg: "fourty"},
		DummyElem{index: 50, msg: "fifty"},
		DummyElem{index: 60, msg: "sixty"},
		DummyElem{index: 70, msg: "seventy"},
		DummyElem{index: 80, msg: "eighty"},
		DummyElem{index: 90, msg: "ninety"},
	}
	startIndex := 77
	endIndex := 91

	elemCheck := map[int]bool{}
	err := searchBinaryRange(testArr, startIndex, endIndex, func(d DummyElem) {
		assert.True(t, d.index >= startIndex && d.index <= endIndex, fmt.Sprint("overshoot ", d.index))
		elemCheck[d.index] = true
		// fmt.Println("found ", d.index, d.msg)
	})
	if err != nil {
		assert.Fail(t, fmt.Sprint(err))
		return
	}
	assert.Equal(t, 2, len(elemCheck), "target count not match ")
	for _, index := range []int{80, 90} {
		_, ok := elemCheck[index]
		assert.True(t, ok, fmt.Sprint("elem ", index, " not found"))
	}
}
