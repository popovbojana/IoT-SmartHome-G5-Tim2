import { Component } from '@angular/core';
import { Button } from '../devices/button';
import { DHT } from '../devices/dht';
import { DUS } from '../devices/dus';
import { Gyro } from '../devices/gyro';
import { LCD } from '../devices/lcd';
import { PIR } from '../devices/pir';

@Component({
  selector: 'app-pi2',
  templateUrl: './pi2.component.html',
  styleUrls: ['./pi2.component.css']
})
export class Pi2Component {

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
}
