import { Component } from '@angular/core';
import { share } from 'rxjs';
import { QueryService } from '../services/query.service';

@Component({
  selector: 'app-query2',
  templateUrl: './query2.component.html',
  styleUrls: ['./query2.component.scss'],
})
export class Query2Component {
  public top100Users$ = this._queryService
    .getTop100UsersWithMostFollowers()
    .pipe(share());

  constructor(private readonly _queryService: QueryService) {}
}
