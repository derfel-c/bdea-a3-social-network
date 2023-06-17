import { Component, Input } from '@angular/core';
import { User } from 'src/app/api/models/user.interface';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
export class UserComponent {
  @Input() public user?: User;
  @Input() public follower?: number;
  @Input() public following?: number;
}
