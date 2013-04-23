from webapp2_extras.routes import RedirectRoute
import handlers

# TODO: uncomment the 'enter_with_language' route once we start supporting multiple languages

_routes = [
    RedirectRoute('/enter', handlers.GateHandler, name='enter', strict_slash=True),
    RedirectRoute('/prizes', handlers.PrizesHandler, name='prizes', strict_slash=True),
    RedirectRoute('/resources', handlers.ResourcesHandler, name='resources', strict_slash=True),
    RedirectRoute('/rules', handlers.RulesHandler, name='rules', strict_slash=True),
    RedirectRoute('/change-language', handlers.ChangeLanguageHandler, name='change_language', strict_slash=True),
    # RedirectRoute('/<language:(en|mx|ar|latam|la|au)>', handlers.LanguageEntryHandler, name='enter_with_language', strict_slash=True),
    RedirectRoute('/', handlers.HomeHandler, name='home', strict_slash=True)
]


def get_routes():
    return _routes


def add_routes(app):
    for r in _routes:
        app.router.add(r)
