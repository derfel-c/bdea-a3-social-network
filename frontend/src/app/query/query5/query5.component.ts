import { Component } from '@angular/core';
import {
  BehaviorSubject,
  Subject,
  combineLatest,
  from,
  groupBy,
  map,
  mergeMap,
  share,
  startWith,
  switchMap,
  tap,
  toArray,
} from 'rxjs';
import { Post } from 'src/app/api/models/post.interface';
import { Tweet } from 'src/app/api/models/tweet.interface';
import { User } from 'src/app/api/models/user.interface';
import { QueryService } from '../services/query.service';

const contents = [
  'Feeling blessed to be alive today!',
  'Never underestimate the power of a kind word.',
  'Coffee is my spirit animal.',
  'Just finished a 5K run. Feeling fantastic!',
  'Anyone else excited about the game tonight?',
  'Beautiful sunrise this morning. Grateful for another day.',
  'Just tried cooking a new recipe, it was delicious!',
  'Has anyone read any good books lately?',
  "Weekend vibes! Can't wait to relax.",
  "Sometimes, it's okay not to be okay. #MentalHealth",
  'Embracing my flaws and feeling confident!',
  'Having a movie marathon tonight. Any suggestions?',
  'Workout done! Remember to take care of your body.',
  'Remember, success is a journey, not a destination.',
  "I love my pet! They're the best companion.",
  'Throwback to an amazing vacation! #Travel',
  'Spending time in nature is so therapeutic.',
  "Feeling creative today! Let's paint something.",
  'Just finished a great podcast. Highly recommend it!',
  'Always be kind. You never know what someone is going through.',
  'Pursue what sets your soul on fire.',
  "A simple smile can make someone's day. #Positivity",
  'Working from home - love the flexibility!',
  'Finally Friday! Anyone else excited for the weekend?',
  'Remember to hydrate! #Health',
  'Family dinner tonight. Nothing beats homemade food!',
  'Looking forward to trying a new workout tomorrow.',
  'Enjoy the little things in life. They matter the most.',
  'Just baked some cookies. The house smells amazing!',
  'Grateful for friends who make life better.',
  "I love reading. It's like traveling without moving.",
  'Feeling inspired to make some positive changes.',
  'Laughter is the best medicine.',
  'Who else loves a quiet morning with a cup of coffee?',
  'Remember to take time for yourself today.',
  'Just finished cleaning. A tidy home is a happy home.',
  'Never forget to tell your loved ones how much they mean to you.',
  'Appreciating the beautiful weather today.',
  'Always learning, always growing.',
  'Excited for a day of adventures tomorrow!',
  'Feeling so loved and appreciated today.',
  'Who else is a night owl?',
  "I can't be the only one who loves rainy days.",
  "There's no place like home.",
  "Remember, it's okay to take a break.",
  'Happy for a new day full of possibilities.',
  'Feeling motivated to reach my goals!',
  'Who else loves the smell of fresh flowers?',
  'Never too old to learn something new.',
  'Practice gratitude every day.',
  'Self-care Sunday is my favorite day of the week.',
];

@Component({
  selector: 'app-query5',
  templateUrl: './query5.component.html',
  styleUrls: ['./query5.component.scss'],
})
export class Query5Component {
  public user$ = this._queryService.user$;
  private _triggerReload$$ = new Subject<void>();

  public tweets$ = combineLatest([
    this.user$,
    this._triggerReload$$.pipe(startWith(void 0)),
  ]).pipe(
    switchMap(([user]) =>
      this._queryService.getTweetsForUserFromCache(user._key).pipe(
        mergeMap((posts: Post[]) => from(posts)),
        groupBy((post) => post.author),
        mergeMap((group$) =>
          group$.pipe(
            toArray(),
            mergeMap((posts: Post[]) =>
              this._queryService
                .getUserByTweetId(posts[0]._key)
                .pipe(
                  map((user: User) => posts.map((post) => ({ post, user })))
                )
            ),
            mergeMap((posts) => posts)
          )
        ),
        toArray()
      )
    ),
    tap(() => this._loading$$.next(false)),
    share()
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

  public generateTweet(tweets: Tweet[]) {
    this._loading$$.next(true);
    const tweet = tweets[Math.floor(Math.random() * tweets.length)];
    const post = this._getRandomPost(tweet.post);
    this._queryService
      .postTweetsForUserFromCache(tweet.user._key, post)
      .subscribe(() => this._triggerReload$$.next());
  }

  private _getRandomPost(
    post: Post
  ): Omit<Post, '_id' | '_key' | '_rev' | 'id'> {
    return {
      author: post.author,
      content: contents[Math.floor(Math.random() * contents.length)],
      country: post.country,
      date_time: Math.floor(Date.now() / 1000),
      language: post.language,
      latitude: post.latitude,
      longitude: post.longitude,
      number_of_likes: Math.floor(Math.random() * 1000),
      number_of_shares: Math.floor(Math.random() * 500),
    };
  }
}
