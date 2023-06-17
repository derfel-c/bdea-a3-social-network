import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Query1Component } from './query1/query1.component';
import { Query2Component } from './query2/query2.component';
import { Query4Component } from './query4/query4.component';
import { Query3Component } from './query3/query3.component';

const routes: Routes = [
  { path: '1', component: Query1Component },
  { path: '2', component: Query2Component },
  { path: '3', component: Query3Component },
  { path: '4', component: Query4Component },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class QueryRoutingModule {}
