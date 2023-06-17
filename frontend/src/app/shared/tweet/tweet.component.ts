import { Component, Input } from '@angular/core';
import { Tweet } from 'src/app/api/models/tweet.interface';

@Component({
  selector: 'app-tweet',
  templateUrl: './tweet.component.html',
  styleUrls: ['./tweet.component.scss']
})
export class TweetComponent {
  @Input() public tweet?: Tweet;
}
