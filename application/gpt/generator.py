import os
import json
import time
import gpt_2_simple as gpt2

class Generator:
    def __init__(self, app, genre, model_descriptor):
        self.app = app
        self.genre = genre
        self.descriptor = model_descriptor
        self.checkpoint_dir = os.path.join(self.app.base_path, 'assets', genre, 'v' + str(self.descriptor['version']), 'checkpoint')

        try:
            self.app.logger.info('loading model for %s sentences, version %s' % (self.genre, self.descriptor['version']))

            self.sess = gpt2.start_tf_sess(threads=1)
            gpt2.load_gpt2(self.sess, checkpoint_dir=self.checkpoint_dir)
        except Exception as e:
            self.app.logger.exception('could not load %s model\nreason:\n%s', genre, e)
    

    def reset_generator(self):
        self.app.logger.info('resetting %s session', self.genre)
        self.sess = gpt2.reset_session(self.sess, threads=1)
        gpt2.load_gpt2(self.sess, checkpoint_dir=self.checkpoint_dir)


    def generate(self, num_sentences, length=256, temperature=0.8, prefix=''):
        self.app.logger.info('generating %d batch(es), max length of %d tokens, temperature=%f and prefix %s' % (num_sentences, length, temperature, prefix))

        start = time.time()

        try:
            items = gpt2.generate(self.sess,
                                checkpoint_dir=self.checkpoint_dir,
                                nsamples=num_sentences,
                                length=length,
                                prefix=prefix,
                                temperature=temperature,
                                return_as_list=True)
        except Exception as e:
            self.app.logger.exception('error generating sentences: %s', e)
            return []

        self.app.logger.info('generation took %d seconds' % (time.time() - start))

        self.reset_generator()
                
        return items