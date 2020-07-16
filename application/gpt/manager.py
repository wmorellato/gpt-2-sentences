import os
import json
import time
import traceback
from ..util import *
from ..sentences import models
from .generator import Generator
from threading import Thread
from colorama import Fore, init

init(autoreset=True)

import tracemalloc

class Manager:
    def __init__(self, app):
        self.app = app
        self.threads = []
        self.generators = {}

        self.app.logger.info(Fore.GREEN + "initializing manager")        
        self.load_model_config()
        self.download_checkpoints()
        self.init_gen_threads()


    def load_model_config(self):
        with open(os.path.join(self.app.base_path, 'gpt_models.json')) as f:
            try:
                self.model_config = json.loads(f.read())
            except:
                self.app.logger.exception('No model config file')
                self.model_config = {}
        
        for k in self.model_config.keys():
            genre = self.app.db_session.query(models.Genre).filter_by(name=k).first()
            self.app.logger.info("%s %s", k, genre)

            if genre is None:
                genre = models.Genre(name=k)

                self.app.db_session.add(genre)
                self.app.db_session.flush()

            self.model_config[k]['id'] = genre.id

        self.app.db_session.commit()


    def download_checkpoints(self):
        self.app.logger.info("verifying checkpoints")
        
        for k in self.model_config.keys():
            try:
                descriptor = self.model_config[k]

                version = descriptor['version']
                model_path = os.path.join(self.app.base_path, 'assets', k, 'v' + str(version))
                self.app.logger.info(model_path)

                if not os.path.exists(model_path):
                    self.app.logger.info(Fore.RED + 'checkpoint for {} not found, downloading'.format(k))
                    os.makedirs(model_path)
                    download_file_with_progress(descriptor['url'], model_path)
            except Exception as e:
                # ugly as fuck
                self.app.logger.exception('could not verify %s checkpoint\nreason:\n%s', k, e)


    def init_gen_threads(self):
        genres = self.model_config.keys()

        for g in genres:
            t = Thread(target=self.generation_thread, args=(g,), daemon=True)
            self.threads.append(t)
            t.start()


    def generation_thread(self, genre):
        self.app.logger.debug(Fore.GREEN + 'initializing thread for %s' % genre)

        if not genre in self.model_config:
            self.app.logger.error('no model descriptor found for genre %s', genre)
            return

        descriptor = self.model_config[genre]
        self.generators[genre] = Generator(self.app, genre, descriptor)

        while True:
            sentences = self.generators[genre].generate(descriptor['num_samples'], length=256)
            split_sentences = self.treat_sentences(sentences)

            self.save_to_database(genre, split_sentences)

            time.sleep(10)
    

    def treat_sentences(self, sentences):
        split_sentences = []

        for s in sentences:
            lines = s.split('\n')
            split_sentences += lines
        
        return split_sentences


    def save_to_database(self, genre, sentences):
        self.app.logger.debug('saving %d %s sentences to database', len(sentences), genre)
        descriptor = self.model_config[genre]

        for s in sentences:
            sentence_item = models.Sentence(
                genre=descriptor['id'],
                text=s,
                rating=0,
                modelVersion=descriptor['version']
            )

            self.app.db_session.add(sentence_item)
        
        self.app.db_session.commit()