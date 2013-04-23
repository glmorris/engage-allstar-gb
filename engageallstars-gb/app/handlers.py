import jinja2

# set default template directory
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('app/templates'))

# load custom libraries
from lib.basehandler import BaseHandler


class LanguageEntryHandler(BaseHandler):

    def get(self, language):

        """ Set language for the session based on language code appended to url """

        BaseHandler.set_language(self, language)
        self.redirect_to('home')


class GateHandler(BaseHandler):

    def get(self):

        """Display page to enter access code"""

        # if valid session, then redirect to welcome page
        # only perform this check if we're in not debug mode
        # if webapp2.get_app().debug is not True:
        #     if 'valid_user' in self.session:
        #         if self.session['valid_user'] is True:
        #             return self.redirect('/')

        # get language content for Enter page
        l10n = BaseHandler.get_page_content(self, 'enter')

        template_values = {
            'cur_page': 'gate',
            'l10n': l10n,
            'csrf_token': BaseHandler.generate_csrf_token(self),
            'language_code': BaseHandler.get_language(self)
        }

        template = jinja_env.get_template('enter.html')
        self.response.out.write(template.render(template_values))

    def post(self):

        """Process access code entry"""

        # if webapp2.get_app().debug is not True:
            # if 'valid_user' in self.session:
            #     if self.session['valid_user'] is True:
            #         return self.redirect('/')

        # get language content for Enter page
        l10n = BaseHandler.get_page_content(self, 'enter')

        template_values = {
            'cur_page': 'gate',
            'l10n': l10n,
            'code_attempted': True,
            'csrf_token': BaseHandler.generate_csrf_token(self),
            'language_code': BaseHandler.get_language(self)
        }

        is_valid = BaseHandler.validate_access_code(self, self.request.get('c'))

        if is_valid is True:
            return self.redirect_to('home')

        # re-display access code entry form
        template = jinja_env.get_template('enter.html')
        self.response.out.write(template.render(template_values))


class HomeHandler(BaseHandler):
    def get(self):

        """Display the Home page"""

        # get language content for page
        l10n = BaseHandler.get_page_content(self, 'home')

        user_type = BaseHandler.get_user_type(self)

        template_values = {
            'cur_page': 'home',
            'l10n': l10n,
            'user_type': user_type,
            'language_code': BaseHandler.get_language(self)
        }

        # load the welcome page template
        template = jinja_env.get_template('home.html')

        # display page
        self.response.out.write(template.render(template_values))


class PrizesHandler(BaseHandler):
    def get(self):

        """Display the Prizes page"""

        # get language content for page
        l10n = BaseHandler.get_page_content(self, 'prizes')

        user_type = BaseHandler.get_user_type(self)

        template_values = {
            'cur_page': 'prizes',
            'l10n': l10n,
            'user_type': user_type,
            'language_code': BaseHandler.get_language(self)
        }

        # load the welcome page template
        template = jinja_env.get_template('prizes.html')

        # display page
        self.response.out.write(template.render(template_values))


class ResourcesHandler(BaseHandler):
    def get(self):

        """Display the Resources page"""

        # get language content for page
        l10n = BaseHandler.get_page_content(self, 'resources')

        user_type = BaseHandler.get_user_type(self)

        template_values = {
            'cur_page': 'resources',
            'l10n': l10n,
            'user_type': user_type,
            'language_code': BaseHandler.get_language(self)
        }

        # load the welcome page template
        template = jinja_env.get_template('resources.html')

        # display page
        self.response.out.write(template.render(template_values))


class RulesHandler(BaseHandler):
    def get(self):

        """Display the Rules page"""

        # get language content for page
        l10n = BaseHandler.get_page_content(self, 'rules')

        user_type = BaseHandler.get_user_type(self)

        template_values = {
            'cur_page': 'rules',
            'l10n': l10n,
            'user_type': user_type,
            'language_code': BaseHandler.get_language(self)
        }

        # load the welcome page template
        template = jinja_env.get_template('rules.html')

        # display page
        self.response.out.write(template.render(template_values))


class ChangeLanguageHandler(BaseHandler):
    def get(self):

        """Change the site language"""

        new_language = self.request.get('lang')

        BaseHandler.set_language(self, new_language)

        # redirect user back to their previous page
        self.redirect(self.request.referer)
