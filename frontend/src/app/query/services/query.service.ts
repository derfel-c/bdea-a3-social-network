import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, retry } from 'rxjs';
import { ApiService } from 'src/app/api/api.service';
import { Post } from 'src/app/api/models/post.interface';
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

  public getRandomUserWithFollowersWithTweets() {
    return this._apiService.getRandomUserWithFollowersWithTweets().subscribe((userId: number) => {
      this._user$$.next(userId);
    });
  }

  public getTweets(userId: string): Observable<Tweet[]> {
    return this._apiService.getPostById(userId);
  }

  public getTop100UsersWithMostFollowers(): Observable<{count: number, user: User}[]> {
    return this._apiService.getTop100UsersWithMostFollowers().pipe(
      retry()
    );
  }

  public getTop100UsersFollowingTop100Users(): Observable<{count: number, user: User}[]> {
    return this._apiService.getTop100UsersFollowingTop100Users().pipe(
      retry()
    );
  }

  public getCountOfUsersUserFollows(userKey: string): Observable<{following_count: number, user: User}[]> {
    return this._apiService.getCountOfUsersUserFollows(userKey);
  }

  public getFollowerCountOfUser(userKey: string): Observable<{follower_count: number, user: User}[]> {
    return this._apiService.getFollowerCountOfUser(userKey);
  }

  public getTop25RecentTweets(userKey: string): Observable<Post[]> {
    return this._apiService.getTop25NewestTweetsForUser(userKey);
  }

  public getTweetsForUserFromCache(userKey: string): Observable<Post[]> {
    return this._apiService.getTweetsForUserFromCache(userKey);
  }

  public getTop25PostsContainingWords(words: string): Observable<Post[]> {
    return this._apiService.getTop25PostsContainingWords(words);
  }
}
