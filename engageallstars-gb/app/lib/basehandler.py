import webapp2
from webapp2_extras import sessions

from app.lib import utils


class BaseHandler(webapp2.RequestHandler):
    """
        BaseHandler for all requests

        Holds the session properties so they
        are reachable for all requests
    """

    def dispatch(self):
        """
            Get a session store for this request.
        """
        self.session_store = sessions.get_store(request=self.request)

        route_name = self.request.route.name

        # if this is not the access code entry page,
        # check to see if this is a valid user session

        # TODO: replace the following if statement with the commented version below
        # once we start supporting multiple languages
        # if route_name != 'enter' and route_name != 'enter_with_language':
        if route_name != 'enter':

            if 'valid_user' not in self.session:
                return self.redirect('/enter')

            if self.session['valid_user'] is not True:
                return self.redirect('/enter')

        try:
            # csrf protection
            if self.request.method == "POST":
                token = self.session.get('_csrf_token')
                if not token or token != self.request.get('_csrf_token'):
                    self.abort(403)

            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def generate_csrf_token(self):
        # session = sessions.get_store().get_session()
        # if '_csrf_token' not in self.session:
        self.session['_csrf_token'] = utils.random_string()
        return self.session['_csrf_token']

    def validate_access_code(self, access_code):

        access_code = access_code.lower()

        if (access_code == 'unmanaged' or access_code == 'u327!us' or access_code == '866262'):
            user_type = 'unmanaged'
        elif (access_code == 'silver1' or access_code == 's327!us' or access_code == '745837'):
            user_type = 'silver'
        elif (access_code == 'gold1' or access_code == 'g327!us' or access_code == '465362'):
            user_type = 'gold'
        else:
            return False

        self.session['valid_user'] = True
        self.session['user_type'] = user_type
        return True

    """ Get object with sit content that corresponds to the language for this session """
    def get_page_content(self, page):

        from itertools import chain

        language = self.get_language()

        base_content = webapp2.import_string('app.l10n.' + language + '.base')
        page_content = webapp2.import_string('app.l10n.' + language + '.' + page)

        content = dict(chain(base_content.l10n.items(), page_content.l10n.items()))

        return content

    """ Get the type of user for this session """
    def get_user_type(self):
        return self.session['user_type']

    """ Set new language for this session """
    def set_language(self, selected_language):

        new_language = ''

        valid_languages = [
            'mx',
            'ar',
            'latam',
            'la',
            'au'
        ]

        # Make sure selected language is valid, otherwise set to English US
        for language in valid_languages:
            if selected_language == language:
                new_language = language
                break

        if new_language is None:
            new_language = 'en'

        self.session['user_language'] = new_language

    """ Return currently selected language """
    def get_language(self):

        if self.session.get('user_language'):
            language = self.session['user_language']
        else:
            language = 'en'
            self.set_language(language)

        return language
