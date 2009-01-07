# Printing options. Change 'PRINT_VOTES' to true if you wish to vote. 'PRINTER'
# is the name of a printer accessible by the command `lpr'.
PRINT = {'PRINT_VOTES': False, 'PRINTER': 'ML-3051ND'}

# Do not touch the following unless you know what your are doing.
AUTH_PROFILE_MODULE = 'vote.Voter'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'vote.backends.VoterBackend',
)
