import { Component } from '@angular/core';
import { Buzzer } from '../devices/buzzer';
import { DHT } from '../devices/dht';
import { FDSS } from '../devices/fdss';
import { IR } from '../devices/ir';
import { PIR } from '../devices/pir';
import { RGB } from '../devices/rgb';
import { OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-pi3',
  templateUrl: './pi3.component.html',
  styleUrls: ['./pi3.component.css']
})
export class Pi3Component implements OnInit{

  constructor(private socket: Socket) { }

  rpir4: PIR = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    motion_detected: false
  }

  rdht4: DHT = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    humidity: 0,
    temperature: 0
  }

  bb: Buzzer = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    pitch: 0,
    duration: 0
  }

  b4sd: FDSS = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    alarm_time: '',
    binary: 0
  }

  bir: IR = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    button: ''
  }

  brgb: RGB = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    state: ''
  }

  ngOnInit() {
    this.socket.on('RPIR4', (response: PIR) => {
      this.rpir4 = response;
    });

    this.socket.on('RDHT4', (response: DHT) => {
      this.rdht4 = response;
    });

    this.socket.on('BB', (response: Buzzer) => {
      this.bb = response;
    }); 

    this.socket.on('B4SD', (response: FDSS) => {
      this.b4sd = response;
    });

    this.socket.on('BIR', (response: IR) => {
      this.bir = response;
    });

    this.socket.on('BRGB', (response: RGB) => {
      this.brgb = response;
    });
  }
}