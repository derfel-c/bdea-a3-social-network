import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  apiUrl = 'http://localhost:5000/api/v1';

  constructor(private http: HttpClient) {}

  getPostOfFollowedUsers(userKey: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/posts/followedUsers/${userKey}`);
  }

  getPostById(userKey: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/posts/${userKey}`);
  }

  getTop100UsersWithMostFollowers(): Observable<any> {
    return this.http.get(`${this.apiUrl}/followers/top100`);
  }

  getTop100UsersFollowingTop100Users(): Observable<any> {
    return this.http.get(`${this.apiUrl}/followers/top100FollowingTop100`);
  }

  getFollowerCountOfUser(userKey: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/followers/count/${userKey}`);
  }

  getCountOfUsersUserFollows(userKey: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/follows/count/${userKey}`);
  }

  getRandomUser(): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/random`);
  }

  getRandomUserWithTweets(): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/randomWithTweets`);
  }

  getTop25NewestTweetsForUser(userKey: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/posts/top25NewestFor/${userKey}`);
  }

  getTweetsForUserFromCache(userKey: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/cache/${userKey}`);
  }

  postTweetsForUserFromCache(userKey: string, post: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/cache/${userKey}`, post);
  }

  getTop25PostsContainingWords(words: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/posts/contains/${words}`);
  }
}
