import json
import traceback

from gpslocationsharer.utils import (
    path_equals,
    format_response,
    share_location_route,
)


def lambda_handler(event, context):
    try:
        print(json.dumps(event.get("headers")))  # Only logging headers, I don't want to log people's GPS location passed in "body"
        result = route(event)
        print(result)
        return result
    except Exception:
        traceback.print_exc()
        return format_response(event=event, http_code=500, body="Internal server error")


# Only using POST because I want to prevent CORS preflight checks, and setting a
# custom header counts as "not a simple request" or whatever, so I need to pass
# in the CSRF token (don't want to pass as a query parameter), so that really
# only leaves POST as an option, as GET has its body removed by AWS somehow
#
# see https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests
def route(event):
    if path_equals(event=event, method="POST", path="/share"):
        return share_location_route(event)
    return format_response(event=event, http_code=403, body={"message": "Forbidden"})
