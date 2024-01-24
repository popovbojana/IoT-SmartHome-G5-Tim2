import { Component, OnInit } from '@angular/core';
import { Button } from '../devices/button';
import { DHT } from '../devices/dht';
import { DUS } from '../devices/dus';
import { Gyro } from '../devices/gyro';
import { LCD } from '../devices/lcd';
import { PIR } from '../devices/pir';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-pi2',
  templateUrl: './pi2.component.html',
  styleUrls: ['./pi2.component.css']
})
export class Pi2Component  implements OnInit{

  constructor(private socket: Socket) { }

  ds2: Button = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    door_unlocked: false,
    code: ''
  }

  dus2: DUS = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    distance: 0
  }

  dpir2: PIR = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    motion_detected: false
  }

  gdht: DHT = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    humidity: 0,
    temperature: 0
  }

  glcd: LCD = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    display: '',
  }

  gsg: Gyro = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    rotation: 0,
    acceleration: 0
  }

  rpir3: PIR = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    motion_detected: false
  }

  rdht3: DHT = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    humidity: 0,
    temperature: 0
  }

  ngOnInit() {
    this.socket.on('DS2', (response: Button) => {
      this.ds2 = response;
    });

    this.socket.on('DUS2', (response: DUS) => {
      this.dus2 = response;
    });

    this.socket.on('DPIR2', (response: PIR) => {
      this.dpir2 = response;
    }); 

    this.socket.on('GDHT', (response: DHT) => {
      this.gdht = response;
    });

    this.socket.on('GLCD', (response: LCD) => {
      this.glcd = response;
    });

    this.socket.on('GSG', (response: Gyro) => {
      this.gsg = response;
    });

    this.socket.on('RPIR3', (response: PIR) => {
      this.rpir3 = response;
    }); 

    this.socket.on('RDH3', (response: DHT) => {
      this.rdht3 = response;
    });

  }
}
