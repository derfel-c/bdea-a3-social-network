import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: 'query', loadChildren: () => import('./query/query.module').then(m => m.QueryModule) },
  { path: '', redirectTo: 'query/1', pathMatch: 'full'},
  { path: '**', redirectTo: 'query/1', pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
