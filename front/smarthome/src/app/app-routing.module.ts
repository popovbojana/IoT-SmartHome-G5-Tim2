import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { Pi1Component } from './pi1/pi1.component';
import { Pi2Component } from './pi2/pi2.component';
import { Pi3Component } from './pi3/pi3.component';
import { ProbaComponent } from './proba/proba.component';

const routes: Routes = [
  {path: "", component: HomeComponent},
  {path: "home", component: HomeComponent},
  {path: "pi1", component: Pi1Component},
  {path: "pi2", component: Pi2Component},
  {path: "pi3", component: Pi3Component},
  {path: "proba", component: ProbaComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
