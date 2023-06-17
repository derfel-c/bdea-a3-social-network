import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Query1Component } from './query1/query1.component';
import { QueryRoutingModule } from './query-routing.module';
import { Query2Component } from './query2/query2.component';
import { Query3Component } from './query3/query3.component';
import { Query4Component } from './query4/query4.component';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCardModule } from '@angular/material/card';
import { SharedModule } from '../shared/shared.module';
import {ScrollingModule} from '@angular/cdk/scrolling';
import {MatTabsModule} from '@angular/material/tabs';

@NgModule({
  declarations: [
    Query1Component,
    Query2Component,
    Query3Component,
    Query4Component,
  ],
  imports: [
    CommonModule,
    QueryRoutingModule,
    MatButtonModule,
    MatDividerModule,
    MatCardModule,
    MatProgressSpinnerModule,
    SharedModule,
    ScrollingModule,
    MatTabsModule,
  ],
})
export class QueryModule {}
