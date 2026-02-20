class AttackDetector:

    def classify_attack(self, failed_attempts, time_interval=0):

        if failed_attempts >= 5:
            return "BRUTE FORCE ATTACK"

        elif failed_attempts >= 3:
            return "SUSPICIOUS LOGIN ATTEMPTS"

        elif failed_attempts > 0:
            return "FAILED LOGIN ATTEMPT"

        else:
            return "NORMAL ACTIVITY"


    def get_risk(self, failed_attempts):

        if failed_attempts >= 5:
            return "CRITICAL"

        elif failed_attempts >= 3:
            return "HIGH"

        elif failed_attempts >= 1:
            return "MEDIUM"

        return "LOW"
