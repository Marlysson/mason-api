"""A LinkController Module."""

from masonite.request import Request
from masonite.response import Response
from masonite.validation import Validator
from masonite.controllers import Controller
from masonite.view import View
from slugify import slugify

from app.Links import Links

class LinkController(Controller):

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    def store(self, validator: Validator):

        '''
            Validations
                - Not empty
                - Unique alias
                - Domain valid
                - Slugfy alias
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

            errors_message = [error for errors_by_input in errors.values() for error in errors_by_input]
            return self.response.json({'errors': errors_message}, status=400)

        else:

            shortned_link = Links()
            shortned_link.alias = slugify(self.request.input('alias'))

            redirect_to = self.request.input('redirect_to')

            if not redirect_to.startswith('http://'):
                redirect_to = 'http://' + redirect_to

            shortned_link.redirect_to = redirect_to
            shortned_link.save()
            
            return self.response.json({"url_shortned": env('APP_URL') + "/" + shortned_link.alias}, status=201)

    def redirect(self):

        link = Links.where('alias', self.request.param('alias')).first()

        if link:

            link.total_access += 1
            link.save()

            return self.response.redirect(link.redirect_to)

        else:

            # Show the default 404 error page instead json with error

            self.request.status(400)
            return self.response.json({'errors': 'Alias not found.'})