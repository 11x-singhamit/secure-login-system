import time


class AttackDetector:

    def __init__(self):

        self.failed_attempts = {}

        self.locked_until = {}

        self.max_attempts = 5

        self.lockout_duration = 120   # seconds



    def record_failed_attempt(self, username):

        self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1

        if self.failed_attempts[username] >= self.max_attempts:

            self.locked_until[username] = time.time() + self.lockout_duration



    def reset_attempts(self, username):

        self.failed_attempts[username] = 0



    def is_locked(self, username):

        if username not in self.locked_until:

            return False

        return time.time() < self.locked_until[username]



    def get_remaining_lockout(self, username):

        if username not in self.locked_until:

            return 0

        remaining = int(self.locked_until[username] - time.time())

        return max(0, remaining)



    def get_attempt_count(self, username):

        return self.failed_attempts.get(username, 0)
