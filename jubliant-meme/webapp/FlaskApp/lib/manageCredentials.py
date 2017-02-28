#!/usr/bin/env python

import os
import ConfigParser
from encryptedpickle import encryptedpickle


def parseConfiguration():
    """ Parse the config contents of secretfile
    """
    secrets = {}
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    basedir = os.path.abspath(os.path.dirname(__file__))
    configFile = os.path.join(basedir, "../config/secret.ini")
    try:
        config.read(configFile)
        for section in config.sections():
            for option in config.options(section):
                secrets[option] = config.get(section, option)
    except Exception as err:
        raise Exception(err)

    return secrets


class createEncryptionObject(object):
    secrets = parseConfiguration()
    sigPassPhrase = secrets.get('sigPassPhrase')
    encryptionPassPhrase = secrets.get('encryptionPassPhrase')
    encoder = None

    @classmethod
    def sigPhrase(cls):
        return cls.sigPassPhrase

    @classmethod
    def encryptionPhrase(cls):
        return cls.encryptionPassPhrase

    @classmethod
    def unleashEncoder(cls):
        passPhrase = {0: cls.sigPhrase()}
        encryption = {0: cls.encryptionPhrase()}

        cls.encoder = encryptedpickle.EncryptedPickle(passPhrase, encryption)

        encryptionAlgorithm = {
            255: {
                'algorithm': 'aes-256-cbc',
                'salt_size': 32,
                'pbkdf2_algorithm': 'sha256',
                'pbkdf2_iterations': 10,
            },
        }

        cls.encoder.set_algorithms(encryption=encryptionAlgorithm)

        options = {
            'encryption_algorithm_id': 255,
            'compression_algorithm_id': 1,
            'flags': {
                    'timestamp': True,
                },
            }
        cls.encoder.set_options(options)

    @staticmethod
    def sealCredentials(encoder, credentials):
        return encoder.seal(credentials)

    @staticmethod
    def unsealCredentials(encoder, key):
        return encoder.unseal(key)


if __name__ == "__main__":
    data = {'Google': {
                    'secret': 'lpIdV0orZN7Iheq9aKLR0lpq',
                    'id': '1018986531748-scj7iu2qorn97iop18fr336rdcbebqn7.apps.googleusercontent.com'
                },
            'Facebook': {
                    'secret': '00d8ed891309b8195951eea5ad10fc55',
                    'id': 1649427608686391
                    }
            }
    createEncryptionObject.unleashEncoder()
    key = createEncryptionObject.sealCredentials(
        createEncryptionObject.encoder, data
    )

    value = createEncryptionObject.unsealCredentials(
        createEncryptionObject.encoder, key
    )

    import pprint

    pprint.pprint(key)
    pprint.pprint(value)
