import os
import time
import gpt_2_simple as gpt2

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, checkpoint_dir='./application/sentences/assets/scifi_checkpoint')

def generate(n, length=256, temperature=0.8):
    print('[+] generating %d sentences, max length of %d tokens, temperature=%f' % (n, length, temperature))

    start = time.time()
    print('[+] cwd:', os.getcwd())

    items = gpt2.generate(sess,
                        nsamples=n,
                        checkpoint_dir='./application/sentences/assets/scifi_checkpoint',
                        length=length,
                        prefix='The red moon',
                        temperature=temperature,
                        return_as_list=True)

    print('[*] generated in %d seconds' % (time.time() - start))
    
    with open('output.txt', 'w') as f:
        for i in items:
            f.write('\n'.join(i.split('\\n')))
    
    return items

# def split_generated_text():
#     pass

# print(generate(5))