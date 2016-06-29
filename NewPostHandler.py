"""Handler for new posts created."""
from BaseHandler import Handler
from models import Posts
from models import blog_key
import bleach


class NewPost(Handler):
    """Handler for new blog post page."""

    def render_page(self, post_title="",
                    post_body="",
                    error_message=""):
        self.render("newpost.html",
                    post_title=post_title,
                    post_body=post_body,
                    error_message=error_message)

    def get(self):
        self.render_page()

    def post(self):
        post_title = bleach.clean(self.request.get("post-title"), strip=True)
        post_body = bleach.clean(self.request.get("post-body"), strip=True)

        if post_title and post_body:
            post = Posts(parent=blog_key(),
                         post_title=post_title,
                         post_body=post_body)
            post.put()

            self.redirect("/blog/%s" % str(post.key.id()))

        else:
            # Bootstrap alert error
            error_message = """<div class="alert alert-danger" role="alert" class="error-message">Please enter a post title and a post body.</div>"""
            self.render_page(error_message=error_message,
                             post_title=post_title, post_body=post_body)