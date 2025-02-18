from django.core.mail.backends.smtp import EmailBackend


class FixedEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        self.connection = self.connection_class(
            self.host, self.port, timeout=self.timeout
        )
        self.connection.set_debuglevel(getattr(self, 'debug_level', 0))

        # Explicitly call starttls() **without
        # keyfile/certfile** for Python 3.12+
        if self.use_tls:
            self.connection.starttls()  # No keyfile or certfile arguments

        self.connection.login(self.username, self.password)
        return True
