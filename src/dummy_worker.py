import schedule
from typing import Dict, List, Optional

from worker_bunch.dispatcher import Dispatcher
from worker_bunch.notification import Notification
from worker_bunch.worker.worker import Worker


class DummyWorkerConfKey:
    DUMMY_TEXT = "dummy_text"


DUMMY_WORKER_JSONSCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        DummyWorkerConfKey.DUMMY_TEXT: {"type": "string", "minLength": 1, "description": "Dummy text"},
    },
    "required": [DummyWorkerConfKey.DUMMY_TEXT]
}


class DummyWorker(Worker):

    def __init__(self, name: str):
        super().__init__(name)

        self._dummy_text = ""

    def set_extra_settings(self, extra_settings: Optional[Dict[str, any]]):
        """Called by the framework with the partial settings."""
        super().set_extra_settings(extra_settings)

        self._dummy_text = self._extra_settings.get(DummyWorkerConfKey.DUMMY_TEXT)

    def get_partial_settings_schema(self) -> Optional[Dict[str, any]]:
        """Overwrite and provide your partial JSON schema for extra setting."""
        return DUMMY_WORKER_JSONSCHEMA

    def make_partial_settings_required(self) -> bool:
        """Overwrite and True to force the existence of partial JSON schema."""
        return True

    def set_last_will(self):
        """Set the last will at mqtt client. Explicitly triggered before the mqtt client connects. Kind of:
        ```
        if self._topic and self._last_will:
            self._mqtt_proxy.set_last_will(topic, payload)
        ```
        """
    def subscribe_notifications(self, dispatcher: Dispatcher):
        """
        subscribe for notifications via:

        timer_job = schedule.every(14 * 60).to(16 * 60).seconds  # type: schedule.Job
        dispatcher.subscribe_timer(self, timer_job, "keyword-timer")

        self._dispatcher.subscribe_cron("* * * * *", self, "cron-every-minute")

        self._dispatcher.subscribe_topics(self, ["mqtt/topic"],
        """
        timer_job = schedule.every(5).to(7).seconds  # type: schedule.Job
        dispatcher.subscribe_timer(self, timer_job, "keyword-timer")

        dispatcher.subscribe_cron(self, "* * * * *", "cron-every-minute")

        # dispatcher.subscribe_mqtt_topics(self, self._mqtt_topics_in, 0.2)

        self._logger.info("subscribe")

    def _work(self, notifications: List[Notification]):
        for notification in notifications:
            self._logger.info("notified: %s", notification)

        self._logger.info(self._dummy_text)

        # message = f"dummy message: {notification.topic}"
        # self._mqtt_proxy.queue(topic=self._mqtt_topic_out, payload=message, retain=self._mqtt_retain)

    def _final_work(self):
        """
        E.g.: You may send explicitly the last will(s) here (as a normal message). Kind of:
        ```
        if self._topic and self._last_will:
            self._mqtt_proxy.publish(self._topic, self._last_will)
        ```
        """
