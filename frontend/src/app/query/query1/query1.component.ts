import { Component } from '@angular/core';
import { QueryService } from '../services/query.service';
import { BehaviorSubject, filter, map, switchMap, tap } from 'rxjs';

@Component({
  selector: 'app-query1',
  templateUrl: './query1.component.html',
  styleUrls: ['./query1.component.scss']
})
export class Query1Component {

  public user$ = this._queryService.user$;

  public tweets$ = this.user$.pipe(
    filter((userId: number) => !!userId || userId <= 0),
    switchMap((userId: number) => this._queryService.getTweets(userId.toString())),
    map((tweets) => tweets?.length > 0 ? tweets : null),
    tap(() => this._isLoading$$.next(false))
  );

  private readonly _isLoading$$ = new BehaviorSubject<boolean>(false);
  public readonly isLoading$ = this._isLoading$$.asObservable();

  constructor(private readonly _queryService: QueryService) {
    this.tweets$.subscribe(console.log);
  }

  public getRandomUser() {
    this._isLoading$$.next(true);
    this._queryService.getRandomUser();
  }

  public getRandomUserWithTweets() {
    this._isLoading$$.next(true);
    this._queryService.getRandomUserWithTweets();
  }
}
