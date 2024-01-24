import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { MatIconModule } from '@angular/material/icon';
import { HomeComponent } from './home/home.component';
import { MatCardModule } from '@angular/material/card';
import { MatExpansionModule } from '@angular/material/expansion';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { Pi1Component } from './pi1/pi1.component';
import { Pi2Component } from './pi2/pi2.component';
import { Pi3Component } from './pi3/pi3.component';
import { ProbaComponent } from './proba/proba.component';
import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { HttpClientModule } from '@angular/common/http';

const config: SocketIoConfig = { url: '127.0.0.1:5000', options: {} };

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HomeComponent,
    Pi1Component,
    Pi2Component,
    Pi3Component,
    ProbaComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatIconModule,
    MatCardModule,
    MatExpansionModule,
    BrowserAnimationsModule,
    MatButtonModule,
    FormsModule,
    SocketIoModule.forRoot(config),
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }