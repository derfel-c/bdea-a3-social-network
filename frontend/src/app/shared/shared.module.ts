import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TweetComponent } from './tweet/tweet.component';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { UserComponent } from './user/user.component';

@NgModule({
  declarations: [TweetComponent, UserComponent],
  imports: [CommonModule, MatCardModule, MatIconModule],
  exports: [TweetComponent, UserComponent],
})
export class SharedModule {}
