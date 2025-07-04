import abc
from typing import Dict, Any

class AlertSenderBase(abc.ABC):
    @abc.abstractmethod
    def send_alert(self, alert: Dict[str, Any]):
        """
        Send an alert to the configured destination.
        """
        pass 