import { Injectable } from '@angular/core';
import { BehaviorSubject, share, take, Observable } from 'rxjs';
import { ApiService } from 'src/app/api/api.service';
import { Tweet } from 'src/app/api/models/tweet.interface';
import { User } from 'src/app/api/models/user.interface';

@Injectable({
  providedIn: 'root'
})
export class QueryService {
  private readonly _user$$ = new BehaviorSubject<number>(NaN);
  public readonly user$ = this._user$$.asObservable();

  constructor(private readonly _apiService: ApiService) {}

  public getRandomUser() {
    return this._apiService.getRandomUser().subscribe((userId: number) => {
      this._user$$.next(userId);
    });
  }

  public getRandomUserWithTweets() {
    return this._apiService.getRandomUserWithTweets().subscribe((userId: number) => {
      this._user$$.next(userId);
    });
  }

  public getTweets(userId: string): Observable<Tweet[]> {
    return this._apiService.getPostById(userId);
  }

  public getTop100UsersWithMostFollowers(): Observable<{count: number, user: User}[]> {
    return this._apiService.getTop100UsersWithMostFollowers();
  }

  public getTop100UsersFollowingTop100Users(): Observable<{count: number, user: User}[]> {
    return this._apiService.getTop100UsersFollowingTop100Users();
  }
}
