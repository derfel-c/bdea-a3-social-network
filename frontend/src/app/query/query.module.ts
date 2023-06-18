import { ScrollingModule } from '@angular/cdk/scrolling';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTabsModule } from '@angular/material/tabs';
import { SharedModule } from '../shared/shared.module';
import { QueryRoutingModule } from './query-routing.module';
import { Query1Component } from './query1/query1.component';
import { Query2Component } from './query2/query2.component';
import { Query3Component } from './query3/query3.component';
import { Query4Component } from './query4/query4.component';
import { Query5Component } from './query5/query5.component';
import { Query6Component } from './query6/query6.component';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    Query1Component,
    Query2Component,
    Query3Component,
    Query4Component,
    Query5Component,
    Query6Component,
  ],
  imports: [
    CommonModule,
    FormsModule,
    QueryRoutingModule,
    MatButtonModule,
    MatDividerModule,
    MatCardModule,
    MatProgressSpinnerModule,
    SharedModule,
    ScrollingModule,
    MatTabsModule,
    MatInputModule,
  ],
})
export class QueryModule {}
