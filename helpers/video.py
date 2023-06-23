import os
import re
import uuid
from abc import ABC, abstractmethod

import allure
from _pytest.fixtures import SubRequest
from allure import attachment_type
from playwright.sync_api import BrowserContext
from helpers.configs import BASE_DIR


class AllureVideoSettings(ABC):
    record_video_dir = str(BASE_DIR / 'video')
    record_video_size = {"width": 1600, "height": 900}
    video_path_list = []
    har_path = f"{record_video_dir}{uuid.uuid4()}.har"
    har_url_filter = re.compile('https://.*?(api/rest/|/jrpc/)')

    @abstractmethod
    def attach_to_allure(self, request: SubRequest):
        pass

    def set_video_path_list(self, context: BrowserContext):
        '''
        если
        browser.new_context(
            record_video_dir=None
        )
        playwright уходит в бесконечный цикл при вызове
        page.video.path()
        '''
        if self.record_video_dir is not None:
            for page in context.pages:
                self.video_path_list.append(page.video.path())

    def remove_artifacts(self):
        for videopath in self.video_path_list:
            try:
                os.remove(videopath)
            except FileNotFoundError:
                pass

    def attach_video(self, request):
        for i, video_path in enumerate(self.video_path_list):
            try:
                with open(video_path, 'rb') as videofile:
                    videodata = videofile.read()
            except FileNotFoundError:
                videodata = None
            if videodata is not None:
                allure.attach(
                    videodata,
                    name=f"{request.node.name} - {i}",
                    attachment_type=attachment_type.WEBM)


class VideoAlwaysKeepNoAttach(AllureVideoSettings):
    '''
    сохраняет видеофайл с именеи теста в папке video/
    '''
    record_video_size = {"width": 1600, "height": 900}

    def attach_to_allure(self, request: SubRequest):
        for i, videopath in enumerate(self.video_path_list):
            try:
                os.replace(videopath, f'{self.record_video_dir}{request.node.name}_{i}.webm')
            except FileNotFoundError:
                pass


class VideoNoKeepAlwaysAttach(AllureVideoSettings):
    '''
    всегда добавляет видео к отчету
    '''
    def attach_to_allure(self, request: SubRequest):
        self.attach_video(request)
        self.remove_artifacts()


class VideoNoKeepOnFailAttach(AllureVideoSettings):
    '''
    добавляет видео к отчету при падении теста
    '''
    def attach_to_allure(self, request: SubRequest):
        if getattr(request.node, 'rep_call', None) and request.node.rep_call.failed:
            self.attach_video(request)

        self.remove_artifacts()


class VideoNoKeepNoAttach(AllureVideoSettings):
    '''
    Отключает добавление артефактов в отчет
    '''
    record_video_dir = None
    record_video_size = None
    video_path_list = []
    har_path = None
    har_url_filter = None

    def attach_to_allure(self, *args, **kwargs):
        self.remove_artifacts()

    def set_video_path_list(self, *args, **kwargs):
        return None


class VideoSettingsStrategy:
    '''
    стратегия для выбора типа AllureAttacher
    '''
    attachers = {
        'ALWAYS_KEEP_NO_ATTACH': VideoAlwaysKeepNoAttach,
        'NO_KEEP_ALWAYS_ATTACH': VideoNoKeepAlwaysAttach,
        'NO_KEEP_ON_FAIL': VideoNoKeepOnFailAttach,
        'NO_KEEP_NO_ATTACH': VideoNoKeepNoAttach,
    }

    def get(self, strategy: str = None) -> AllureVideoSettings:
        return self.attachers.get(str(strategy).upper(), VideoNoKeepNoAttach)()
