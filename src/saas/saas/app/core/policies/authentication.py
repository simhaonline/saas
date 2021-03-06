import logging
log = logging.getLogger(__name__)

from zope.interface import implementer
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import Everyone, Authenticated

@implementer(IAuthenticationPolicy)
class AuthenticationPolicy(object):
    def __init__(self, userStore):
        self.userStore = userStore

    def authenticated_userid(self, request):
        log.debug('//todo AuthenticationPolicy::authenticated_userid()')
        session = request.session
        email = session['email'] if 'email' in session else None
        if email != '':
            user = self.userStore.userByEmail(email)
            return user[0]

        return None

    def unauthenticated_userid(self, request):
        log.debug('//todo AuthenticationPolicy::unauthenticated_userid()')
        session = request.session
        email = session['email'] if 'email' in session else None
        return email

    def effective_principals(self, request):
        session = request.session
        email = session['email'] if 'email' in session else None
        client_id = session['client'] if 'client' in session else None

        if email is not None and self.userStore.emailExists(email):
            user = self.userStore.userByEmail(email)
            user_id = user[0]

            principal = {
                'client_id': client_id,
                'user_id': user_id
            }

            return [Everyone, Authenticated, principal]
        else:
            return None


    def remember(self, request, userid, **kw):
        try: 
            session = request.session
            session['email'] = userid
            for k, v in kw.items():
                if k != 'email':
                    session[k] = v
        except Exception as e:
            log.error(e)
            raise e
        return None

    def forget(self, request):
        session = request.session
        session.invalidate()

        return None