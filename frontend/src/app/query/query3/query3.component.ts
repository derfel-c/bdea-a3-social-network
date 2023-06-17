import { Component } from '@angular/core';
import { QueryService } from '../services/query.service';
import { share } from 'rxjs/operators';

@Component({
  selector: 'app-query3',
  templateUrl: './query3.component.html',
  styleUrls: ['./query3.component.scss']
})
export class Query3Component {
  public top100Users$ = this._queryService
    .getTop100UsersFollowingTop100Users()
    .pipe(share());

  constructor(private readonly _queryService: QueryService) {}
}
