class LoginAttempt:
    """Represents a login attempt"""

    def __init__(self, data: Dict[str, Any]):
        # {
        #     "kind": "identitytoolkit#VerifyPasswordResponse",
        #     "localId": "12345",
        #     "email": "FOO@OO",
        #     "displayName": "",
        #     "registered": true,
        #     "mfaPendingCredential": "123445",
        #     "mfaInfo": [{
        #         "phoneInfo": "+********1234",
        #         "mfaEnrollmentId": "1234",
        #         "displayName": "",
        #         "enrolledAt": "2025-01-01T01:00:00.000000Z"
        #     }]
        # }

        # {
        #     "idToken": "1234",
        #     "expiresIn": "1234",
        #     "refreshToken": "1234"
        # }

        id_token
        self.ppid: int = data.get('ppid', None)
        self.connected_components: List[str] = data.get('connectedComponents', [])

        self.evses: List[Evse] = []
        for evse in data.get('evses', []):
            self.evses.append(Evse(data=evse))