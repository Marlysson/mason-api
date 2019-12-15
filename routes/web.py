"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [
    Post('/links', 'LinkController@store'),
    Get('/@alias', 'LinkController@redirect')
]
