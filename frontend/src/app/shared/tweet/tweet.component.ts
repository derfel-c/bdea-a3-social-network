import { AfterViewInit, Component, Input } from '@angular/core';
import { Tweet } from 'src/app/api/models/tweet.interface';
import { QueryService } from 'src/app/query/services/query.service';

@Component({
  selector: 'app-tweet',
  templateUrl: './tweet.component.html',
  styleUrls: ['./tweet.component.scss'],
})
export class TweetComponent implements AfterViewInit {
  @Input() public tweet?: Tweet;

  constructor(private readonly _queryService: QueryService) {}

  public ngAfterViewInit(): void {
    if (this.tweet && !this.tweet.user && this.tweet.post._key) {
      this._queryService
        .getUserByTweetId(this.tweet?.post._key)
        .subscribe((user) => {
          if (user && this.tweet) {
            this.tweet.user = user;
          }
        });
    }
  }
}
