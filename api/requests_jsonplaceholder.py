import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


class Comment:
    def __init__(
        self,
        post_id: int,
        comment_id: int | None,
        name: str,
        email: str,
        body: str,
    ):
        self.post_id = post_id
        self.comment_id = comment_id
        self.name = name
        self.email = email
        self.body = body

    # classmethod means this method is called on the class itself and uses `cls`
    # to build and return a Comment instance from API response data.
    @classmethod
    def from_dict(cls, data: dict) -> "Comment":
        return cls(
            post_id=data["postId"],
            comment_id=data.get("id"),
            name=data["name"],
            email=data["email"],
            body=data["body"],
        )

    def to_dict(self) -> dict:
        return {
            "postId": self.post_id,
            "name": self.name,
            "email": self.email,
            "body": self.body,
        }

    def __repr__(self) -> str:
        return (
            f"Comment(post_id={self.post_id}, comment_id={self.comment_id}, "
            f"name={self.name!r})"
        )


class JSONPlaceholderClient:
    def __init__(self, base_url: str = BASE_URL, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _get(self, endpoint_path: str, params: dict | None = None) -> dict | list:
        url = f"{self.base_url}/{endpoint_path.lstrip('/')}"

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            raise RuntimeError(f"GET request failed for {url}: {exc}") from exc

    def _post(self, endpoint_path: str, payload: dict) -> dict:
        url = f"{self.base_url}/{endpoint_path.lstrip('/')}"

        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            raise RuntimeError(f"POST request failed for {url}: {exc}") from exc

    def get_comment(self, comment_id: int) -> Comment:
        data = self._get(f"comments/{comment_id}")
        return Comment.from_dict(data)

    def get_comments(self, limit: int = 5) -> list[Comment]:
        data = self._get("comments")
        comments = [Comment.from_dict(comment_data) for comment_data in data]
        return comments[:limit]

    def create_comment(self, comment: Comment) -> Comment:
        data = self._post("comments", comment.to_dict())
        return Comment.from_dict(data)


def main() -> None:
    client = JSONPlaceholderClient()

    print("GET one comment")
    comment = client.get_comment(1)
    print(comment)
    print(comment.name)
    print(comment.email)
    print(comment.body)

    print("\nGET many comments")
    comments = client.get_comments(limit=3)
    for current_comment in comments:
        print(current_comment)

    print("\nPOST create a new comment")
    new_comment = Comment(
        post_id=1,
        comment_id=None,
        name="Practice requests example",
        email="practice@example.com",
        body="This is a sample JSONPlaceholder comment POST request.",
    )
    created_comment = client.create_comment(new_comment)
    print(created_comment)
    print(created_comment.name)


if __name__ == "__main__":
    main()
