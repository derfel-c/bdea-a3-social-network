import { Component } from '@angular/core';
import { QueryService } from '../services/query.service';
import { share } from 'rxjs/operators';

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
