import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-proba',
  templateUrl: './proba.component.html',
  styleUrls: ['./proba.component.css']
})
export class ProbaComponent implements OnInit {
  message: string = '';
  messages: string[] = [];

  constructor(private socket: Socket) { }

  ngOnInit() {
    // Ova logika se izvršava kada se komponenta inicijalizuje
    this.socket.on('proba', (msg: string) => {
      this.messages.push(msg);
    });
  }

  sendMessage() {
    // Ova funkcija se poziva kada korisnik pošalje poruku
    this.socket.emit('message', this.message);
    this.message = ''; // Resetujemo polje za unos
  }
}
