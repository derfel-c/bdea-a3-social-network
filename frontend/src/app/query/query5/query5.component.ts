import { Component } from '@angular/core';
import { QueryService } from '../services/query.service';
import { filter, map, switchMap } from 'rxjs';

@Component({
  selector: 'app-query5',
  templateUrl: './query5.component.html',
  styleUrls: ['./query5.component.scss']
})
export class Query5Component {
  public user$ = this._queryService.user$;

  public tweets$ = this.user$.pipe(
    filter((userId: number) => !!userId || userId <= 0),
    switchMap((userId: number) =>
      this._queryService.getTweetsForUserFromCache(userId.toString())
    ),
    map((x) => x.map((post) => ({post: post})))
  );

  constructor(private readonly _queryService: QueryService) {}

  public getRandomUser() {
    this._queryService.getRandomUser();
  }

  public getRandomUserWithTweets() {
    this._queryService.getRandomUserWithTweets();
  }
}
