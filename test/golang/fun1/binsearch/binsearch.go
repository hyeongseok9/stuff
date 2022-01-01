package binsearch

import (
	"fmt"
)

func searchBinary(src []DummyElem, target int) (string, error) {
	n := len(src)
	l := 0
	r := n - 1

	var i, m int
	for i = 1; l <= r && i < n; i++ {
		m = (l + r) / 2
		// fmt.Println("try ", i, " th m:", m)
		if src[m].index < target {
			l = m + 1
		} else if src[m].index > target {
			r = m - 1
		} else {
			// fmt.Println("search complete in ", i)
			return src[m].msg, nil
		}
	}

	return "", fmt.Errorf("not found for %d th try  m:%d", i, m)
}

func getPosition(src []DummyElem, target int) (int, error) {
	n := len(src)
	l := 0
	r := n - 1
	about := 0

	var i, m int
	for i = 1; l <= r && i < n; i++ {
		m = (l + r) / 2
		// fmt.Println("try ", i, " th m:", m, " l:", l, " r:", r)
		if src[m].index < target {
			l = m + 1
			about = l
		} else if src[m].index > target {
			r = m - 1
			about = l
		} else {
			// fmt.Println("search complete in ", i)
			return m, nil
		}
	}

	return about, fmt.Errorf("not found for %d th try  m:%d", i, m)
}

func searchBinaryRange(src []DummyElem, startIndex int, endIndex int, h1 func(DummyElem)) error {
	n := len(src)

	if startIndex > endIndex {
		return fmt.Errorf("invalid startIndex %d endIndex %d", startIndex, endIndex)
	}

	var startPos int
	if src[0].index > startIndex {
		startPos = 0
	} else {
		startPos, _ = getPosition(src, startIndex)
	}

	var i, m int
	for m, i = startPos, 0; m < n && i < n; i, m = i+1, m+1 {
		index := src[m].index
		// fmt.Println("index: ", index, " m:", m)
		if index >= startIndex && index <= endIndex {
			h1(src[m])
		} else {
			break
		}

	}

	return nil
}
