import { Component } from '@angular/core';
import { BehaviorSubject, Observable, map, switchMap, tap } from 'rxjs';
import { Tweet } from 'src/app/api/models/tweet.interface';
import { QueryService } from '../services/query.service';

@Component({
  selector: 'app-query4',
  templateUrl: './query4.component.html',
  styleUrls: ['./query4.component.scss'],
})
export class Query4Component {
  public user$ = this._queryService.user$;

  public following$ = this.user$.pipe(
    switchMap((user) =>
      this._queryService.getCountOfUsersUserFollows(user._key)
    ),
    map((x) => x.length > 0 ? x[0].following_count : 0)
  );

  public followers$ = this.user$.pipe(
    switchMap((user) =>
      this._queryService.getFollowerCountOfUser(user._key)
    ),
    map((x) => x.length > 0 ? x[0].follower_count : 0)
  );

  public top25RecentTweets$: Observable<Tweet[]> = this.user$.pipe(
    switchMap((user) =>
      this._queryService.getTop25RecentTweets(user._key)
    ),
    map((x) => x.map((y) => ({post: y} as Tweet))),
    tap(() => this._loading$$.next(false))
  );

  public top25PopularTweets$ = this.user$.pipe(
    switchMap((user) =>
      this._queryService.getTop25PopularTweetsForUser(user._key)
    ),
    map((x) => x.map((y) => ({post: y} as Tweet))),
    tap(() => this._loading$$.next(false))
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
