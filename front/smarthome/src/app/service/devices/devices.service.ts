import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { DMS } from 'src/app/devices/dms';
import { IR } from 'src/app/devices/ir';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DevicesService {

  constructor(private http: HttpClient) { }

  dms(dmsDTO: DMS): Observable<any> {
    return this.http.post<any>(environment.apiHost + "dms", dmsDTO);
  }

  ir(irDTO: IR): Observable<any> {
    return this.http.post<any>(environment.apiHost + "ir", irDTO);
  }

  alarmClock(alarmClockDTO: AlarmClock): Observable<any> {
    return this.http.post<any>(environment.apiHost + "alarm-clock-pi", alarmClockDTO);
  }
}

export interface AlarmClock{
  time: string,
  action: string
}