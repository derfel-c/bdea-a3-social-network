import { Component } from '@angular/core';
import { QueryService } from '../services/query.service';
import { BehaviorSubject, filter, map, switchMap, tap, share } from 'rxjs';

@Component({
  selector: 'app-query1',
  templateUrl: './query1.component.html',
  styleUrls: ['./query1.component.scss'],
})
export class Query1Component {
  public user$ = this._queryService.user$;

  public tweets$ = this.user$.pipe(
    filter((userId: number) => !!userId || userId <= 0),
    switchMap((userId: number) =>
      this._queryService.getTweets(userId.toString())
    )
  );

  constructor(private readonly _queryService: QueryService) {}

  public getRandomUser() {
    this._queryService.getRandomUser();
  }

  public getRandomUserWithTweets() {
    this._queryService.getRandomUserWithTweets();
  }
}
