#API Endpoints
*Posts (/api/posts/):

-GET /: Retrieve a list of all posts. Supports pagination (?page=...) and searching (?search=...).

-POST /: Create a new post. (Requires authentication)

-GET /<id>/: Retrieve a specific post.

-PUT/PATCH /<id>/: Update a specific post. (Author only)

-DELETE /<id>/: Delete a specific post. (Author only)

*Comments (/api/posts/<post_id>/comments/):

-GET /: List all comments for a specific post. Supports pagination.

-POST /: Create a new comment on a post. (Requires authentication)

-GET /<comment_id>/: Retrieve a specific comment.

-PUT/PATCH /<comment_id>/: Update a specific comment. (Author only)

-DELETE /<comment_id>/: Delete a specific comment. (Author only)