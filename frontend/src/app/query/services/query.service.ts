import { Injectable } from '@angular/core';
import {
  BehaviorSubject,
  Observable,
  filter,
  from,
  groupBy,
  map,
  mergeMap,
  retry,
  share,
  switchMap,
  toArray,
} from 'rxjs';
import { ApiService } from 'src/app/api/api.service';
import { Post } from 'src/app/api/models/post.interface';
import { Tweet } from 'src/app/api/models/tweet.interface';
import { User } from 'src/app/api/models/user.interface';

@Injectable({
  providedIn: 'root',
})
export class QueryService {
  private readonly _userId$$ = new BehaviorSubject<number>(NaN);
  public readonly user$ = this._userId$$.pipe(
    filter((userId) => !!userId || userId <= 0),
    switchMap((userId) => this.getUsers(userId.toString())),
    share()
  );

  constructor(private readonly _apiService: ApiService) {}

  public getRandomUser() {
    return this._apiService.getRandomUser().subscribe((userId: number) => {
      this._userId$$.next(userId);
    });
  }

  public getRandomUserWithTweets() {
    return this._apiService
      .getRandomUserWithTweets()
      .subscribe((userId: number) => {
        this._userId$$.next(userId);
      });
  }

  public getRandomUserWithFollowersWithTweets() {
    return this._apiService
      .getRandomUserWithFollowersWithTweets()
      .subscribe((userId: number) => {
        this._userId$$.next(userId);
      });
  }

  public getTweets(userId: string): Observable<Tweet[]> {
    return this._apiService.getPostById(userId);
  }

  public getUsers(userId: string): Observable<User> {
    return this._apiService.getUserById(userId);
  }

  public getUserByTweetId(tweetId: string): Observable<User> {
    return this._apiService.getUserByTweetId(tweetId);
  }

  public getTop100UsersWithMostFollowers(): Observable<
    { count: number; user: User }[]
  > {
    return this._apiService.getTop100UsersWithMostFollowers().pipe(retry());
  }

  public getTop100UsersFollowingTop100Users(): Observable<
    { count: number; user: User }[]
  > {
    return this._apiService.getTop100UsersFollowingTop100Users().pipe(retry());
  }

  public getCountOfUsersUserFollows(
    userKey: string
  ): Observable<{ following_count: number; user: User }[]> {
    return this._apiService.getCountOfUsersUserFollows(userKey);
  }

  public getFollowerCountOfUser(
    userKey: string
  ): Observable<{ follower_count: number; user: User }[]> {
    return this._apiService.getFollowerCountOfUser(userKey);
  }

  public getTop25RecentTweets(userKey: string): Observable<Post[]> {
    return this._apiService.getTop25NewestTweetsForUser(userKey);
  }

  public getTop25PopularTweetsForUser(userKey: string): Observable<Post[]> {
    return this._apiService.getTop25PopularTweetsForUser(userKey);
  }

  public getTweetsForUserFromCache(userKey: string): Observable<Post[]> {
    return this._apiService.getTweetsForUserFromCache(userKey);
  }

  public getTop25PostsContainingWords(words: string): Observable<Post[]> {
    return this._apiService.getTop25PostsContainingWords(words);
  }

  public postTweetsForUserFromCache(userKey: string, post: Omit<Post, '_id'|'_key'|'_rev'|'id'>): Observable<any> {
    return this._apiService.postTweetsForUserFromCache(userKey, post);
  }
}
