import { Post } from "./post.interface";
import { User } from "./user.interface";

export interface Tweet {
  user: User;
  post: Post;
}
