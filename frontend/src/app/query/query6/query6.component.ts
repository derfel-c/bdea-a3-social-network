import { Component } from '@angular/core';
import { Subject, debounceTime, distinctUntilChanged, filter, map, switchMap } from 'rxjs';
import { QueryService } from '../services/query.service';

@Component({
  selector: 'app-query6',
  templateUrl: './query6.component.html',
  styleUrls: ['./query6.component.scss']
})
export class Query6Component {
  private _userInput$$ = new Subject<string>();
  public userInput$ = this._userInput$$.pipe(
    debounceTime(200),
    distinctUntilChanged(),
    filter((query) => !!query),
  );

  public tweets$ = this.userInput$.pipe(
    switchMap((query) =>
      this._queryService.getTop25PostsContainingWords(query)
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

  public updateQuery(query: string) {
    this._userInput$$.next(query);
  }
}
