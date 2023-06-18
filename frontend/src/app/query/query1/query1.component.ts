import { Component } from '@angular/core';
import { BehaviorSubject, switchMap, tap } from 'rxjs';
import { QueryService } from '../services/query.service';

@Component({
  selector: 'app-query1',
  templateUrl: './query1.component.html',
  styleUrls: ['./query1.component.scss'],
})
export class Query1Component {
  public user$ = this._queryService.user$;

  public tweets$ = this.user$.pipe(
    switchMap((user) =>
      this._queryService.getTweets(user._key),
    ),
    tap(() => this._loading$$.next(false))
  );

  private _loading$$ = new BehaviorSubject<boolean>(false);
  public loading$ = this._loading$$.asObservable();

  constructor(private readonly _queryService: QueryService) {}

  public getRandomUser() {
    this._loading$$.next(true);
    this._queryService.getRandomUser();
  }

  public getRandomUserWithTweets() {
    this._loading$$.next(true);
    this._queryService.getRandomUserWithTweets();
  }
}
