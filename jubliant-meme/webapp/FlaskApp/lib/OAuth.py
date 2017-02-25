#!/usr/bin/env python

import json
from manageCredentials import createEncryptionObject
from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        authKey = current_app.config.get('oauth_credentials', None)
        createEncryptionObject.unleashEncoder()
        credentials = createEncryptionObject.unsealCredentials(
            createEncryptionObject.encoder, authKey
        )
        oAuthCredentials = credentials.get(self.provider_name, None)

        if oAuthCredentials:
            self.consumer_id = oAuthCredentials.get('id')
            self.consumer_secret = oAuthCredentials.get('secret')

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for(
            'wapi.oauth_callback',
            provider=self.provider_name,
            _external=True
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('Facebook')
        self.service = OAuth2Service(
            name='Facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    # def authorize(self):
    #     return redirect(self.service.get_authorize_url(
    #         scope='email',
    #         response_type='code',
    #         redirect_uri=self.get_callback_url())
    #     )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}
        )
        me = oauth_session.get('me?fields=id,email').json()
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],
            me.get('email')
        )


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('Google')
        self.service = OAuth2Service(
            name='Google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            base_url='https://www.googleapis.com/oauth2/v1/'
        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url(),
                },
            decoder=json.loads
        )
        me = oauth_session.get(
                'https://www.googleapis.com/oauth2/v1/userinfo'
            ).json()
        return (
            'google$' + me['id'],
            me.get('email').split('@')[0],
            me.get('email')
        )
