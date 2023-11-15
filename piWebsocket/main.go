package main

import (
	"fmt"
	"log"
	"time"

	"periph.io/x/conn/v3/gpio"
	"periph.io/x/conn/v3/gpio/gpioreg"
	"periph.io/x/host/v3"
)

var (
	pulseChan      chan struct{}
	lastUpdateTime time.Time
)

func main() {
	if _, err := host.Init(); err != nil {
		log.Fatal(err)
	}

	pin := gpioreg.ByName("GPIO14")
	if pin == nil {
		log.Fatal("Failed to find GPIO14")
	}

	if err := pin.In(gpio.PullUp, gpio.BothEdges); err != nil {
		log.Fatal(err)
	}

	pulseChan = make(chan struct{}, 1000) // Buffered channel

	go readPulses(pin)

	for {
		calculateRPMAndHorsepower()
		time.Sleep(1 * time.Second)
	}
}

func readPulses(pin gpio.PinIO) {
	for {
		pin.WaitForEdge(-1)
		pulseChan <- struct{}{}
	}
}

func calculateRPMAndHorsepower() {
	currentTime := time.Now()
	elapsedTime := currentTime.Sub(lastUpdateTime).Seconds()

	pulseCount := 0
	empty := false
	for !empty {
		select {
		case <-pulseChan:
			pulseCount++
		default:
			empty = true
		}
	}

	rpm := float64(pulseCount) / elapsedTime / 7 * 60

	lastUpdateTime = currentTime

	const torque = 14
	horsepower := (torque * rpm) / 5252

	fmt.Printf("RPM: %.2f, Horsepower: %.2f\n", rpm, horsepower)
}
