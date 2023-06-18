import { Component } from '@angular/core';
import { BehaviorSubject, map, switchMap, tap } from 'rxjs';
import { Tweet } from 'src/app/api/models/tweet.interface';
import { QueryService } from '../services/query.service';

@Component({
  selector: 'app-query5',
  templateUrl: './query5.component.html',
  styleUrls: ['./query5.component.scss']
})
export class Query5Component {
  public user$ = this._queryService.user$;

  public tweets$ = this.user$.pipe(
    switchMap((user) =>
      this._queryService.getTweetsForUserFromCache(user._key)
    ),
    map((x) => x.map((y) => ({post: y} as Tweet))),
    tap(() => this._loading$$.next(false)),
  );

  private _loading$$ = new BehaviorSubject<boolean>(false);
  public loading$ = this._loading$$.asObservable();

  constructor(private readonly _queryService: QueryService) {}

  public getRandomUser() {
    this._loading$$.next(true);
    this._queryService.getRandomUser();
  }

  public getRandomUserWithFollowersWithTweets() {
    this._loading$$.next(true);
    this._queryService.getRandomUserWithFollowersWithTweets();
  }
}
