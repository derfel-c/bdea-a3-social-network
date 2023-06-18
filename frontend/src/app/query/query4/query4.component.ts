import { Component } from '@angular/core';
import { filter, map, switchMap, BehaviorSubject, tap } from 'rxjs';
import { QueryService } from '../services/query.service';
import { User } from 'src/app/api/models/user.interface';

@Component({
  selector: 'app-query4',
  templateUrl: './query4.component.html',
  styleUrls: ['./query4.component.scss'],
})
export class Query4Component {
  public userId$ = this._queryService.user$.pipe(
    filter((userId: number) => !!userId || userId <= 0)
  );

  private readonly _user$ = new BehaviorSubject<User | undefined>(undefined);
  public user$ = this._user$.asObservable();

  public following$ = this.userId$.pipe(
    switchMap((userId: number) =>
      this._queryService.getCountOfUsersUserFollows(userId.toString())
    ),
    tap((x) => x.length > 0 ? this._user$.next(x[0].user) : null),
    map((x) => x.length > 0 ? x[0].following_count : 0)
  );

  public followers$ = this.userId$.pipe(
    switchMap((userId: number) =>
      this._queryService.getFollowerCountOfUser(userId.toString())
    ),
    tap((x) => x.length > 0 ? this._user$.next(x[0].user) : null),
    map((x) => x.length > 0 ? x[0].follower_count : 0)
  );

  public top25RecentTweets$ = this.userId$.pipe(
    switchMap((userId: number) =>
      this._queryService.getTop25RecentTweets(userId.toString())
    ),
    map((x) => x.map((post) => ({post: post}))),
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
