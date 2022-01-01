package fun1


import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestFun1(t *testing.T){
	expected :=1
	actual := 0
	hello()
	assert.Equal(t, expected, actual , "not expected")
}