"""A LinkController Module."""

from masonite.request import Request
from masonite.response import Response
from masonite.validation import Validator
from masonite.controllers import Controller
from masonite.view import View
from app.Links import Links

class LinkController(Controller):

    def __init__(self, request: Request):
        self.request = request

    def store(self, validator: Validator):

        '''
            Validations
                - Not empty
                - Unique alias
                - Domain valid
        '''

        errors = self.request.validate(

            validator.required('alias'),
            validator.required('redirect_to'),

            validator.active_domain('redirect_to'),
            
            validator.isnt(
                validator.is_in('alias', Links.all().lists('alias'),
                messages = {'alias': 'Already exists an alias with this name. Please choose other.'})
            )

        )

        if errors:

            self.request.status(400)
            return {'error': True, 'errors': errors}

        else:

            shortned_link = Links()
            shortned_link.alias = self.request.input('alias')

            redirect_to = self.request.input('redirect_to')

            if not redirect_to.startswith('http://'):
                redirect_to = 'http://' + redirect_to

            shortned_link.redirect_to = redirect_to
            shortned_link.save()

            self.request.status(200)
            
            return {
                "url_shortned": env('APP_URL') + "/" + shortned_link.alias
            }

    def redirect(self, response: Response):

        link = Links.where('alias', self.request.param('alias')).first()

        if link:

            link.total_access += 1
            link.save()

            return response.redirect(link.redirect_to)

        else:

            # Show the default 404 error page instead json with error

            self.request.status(400)
            return { 'error': True, 'errors': 'Alias not found.'}