from datetime import datetime

class Firewall:
    def __init__(self, max_requests_timedelta, timedelta) -> None:
        self.max_requests_timedelta = max_requests_timedelta # Maximum requests in timedelta
        self.timedelta = timedelta
        self.request_history = {} # map user -> list of timestamps of requests

    def request_incoming_is_spam(self, user_id) -> bool:
        """Answers question: 'Is the ammount of requests generated by this user considered spam?' """
        if user_id in self.request_history:
            # check if not too many requests in too short time, delete requests sent before minute
            now = datetime.now()
            self.request_history[user_id].append(now)
            for r in self.request_history[user_id]:
                if self.timedelta < now - r:
                    self.request_history[user_id].pop(0) 
                else:
                    # beacuse that means that every timestamp forward will be in the timedelta
                    break
            
            return len(self.request_history[user_id]) > self.max_requests_timedelta

        self.request_history[user_id] = [datetime.now()]
        return False



