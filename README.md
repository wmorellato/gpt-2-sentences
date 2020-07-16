# GPT2 Sentences API

A simple Flask app that generates sentences using [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple). I decided to build this API to use with [Babel](https://github.com/wmorellato/babel), a VSCode extension for writing I built a while ago, to provide short writing scripts. As a result, this code has not comments at all. If people start using it, I'll clean it up.

Sentences are classified according to their genre (more on that below), and the checkpoints for each genre are download at initialization. This app was structured to easily swap between checkpoints using a configuration file.

## Examples

`"At first, I looked into his face, but could not tell how, as there was so much tear and rage in it."`

`This way was given to a man named Raymond, whose hands were like the plumes of a cat's, with each hand differently marked.`

`"Besides, I don't care to be asked a question." "You don't care to be asked a question?" asked K.`

## Demo

Not yet :(. I'm planning to upload this to Google Cloud Run.

## Training

The retraining was made using books taken from two bookshelves of Gutenberg: [Science Fiction (Bookshelf)](https://www.gutenberg.org/wiki/Science_Fiction_(Bookshelf)) and [Horror Bookshelf](https://www.gutenberg.org/wiki/Horror_(Bookshelf)). For each genre I selected 35000 sentences (due to time restrictions) to generate separate models.

## Usage

The application does not generate sentences when a request is made. Instead it periodically generates batches of sentences and store them in a database. On requests, `n` sentences are selected at random from this database and returned. Below is a quick description of the available API methods. You can find more detailed documentation in [docs](/docs).

HTTP request | Description
------------- | -------------
**GET** /sentences/rating/ | List sentences based on their rating.
**GET** /sentences/{genre} | Get a list of generated sentences by genre.
**POST** /sentences/rating/ | Rate the quality of a sentence. The criteria for rating is subjective.

So if you want scifi sentences, you would send a request to:

`http://localhost:5000/v1/sentences/scifi`

> :warning: **Note**: the name of the genre must match the genre key in `gpt_models.json`

The response is a JSON array with Sentence objects:

```json
[
  {
    "created": "Sun, 12 Jul 2020 19:06:58 GMT", 
    "genre": "scifi", 
    "id": 567, 
    "modelVersion": 1, 
    "rating": 0, 
    "text": "This is the place to store the vampyre hides, as well as other valuables."
  }, 
  {
    "created": "Sun, 12 Jul 2020 19:11:59 GMT", 
    "genre": "scifi", 
    "id": 717, 
    "modelVersion": 1, 
    "rating": 0, 
    "text": "And the Panic of the Gods had died away, and it came again and again to my waking; and the Detective thought to himself how he should handle it."
  }, 
  {
    "created": "Sun, 12 Jul 2020 19:30:05 GMT", 
    "genre": "scifi", 
    "id": 904, 
    "modelVersion": 1, 
    "rating": 0, 
    "text": "And in a while, it did be very sly and easy; but yet somewhat naughty, to say the least; and she to put her hand upon me, and I to be but a child."
  }, 
  {
    "created": "Mon, 13 Jul 2020 08:57:41 GMT", 
    "genre": "scifi", 
    "id": 1008, 
    "modelVersion": 1, 
    "rating": 0, 
    "text": "No man's life was without its value, so he took a concierge at once, and rather than be driven mad, he went on raving in the same way."
  }, 
  {
    "created": "Mon, 13 Jul 2020 08:58:57 GMT", 
    "genre": "scifi", 
    "id": 1046, 
    "modelVersion": 1, 
    "rating": 0, 
    "text": "Un point de l'autre qui se serait de la Morgue, je suis presque sur l'antieux, mais le coeur est une apporterne."
  }
]
```

## Updating models

The configuration file [gpt_models.json](gpt_models.json) enables you to easily update and specify models for sentence generation. For example, if you would like to include the new genre *fantasy*, you include a new key in the JSON, specifying the version of the model (1) and the URL for the tar file. Also, if you came up with a better model for *scifi* sentences, you increment the version under *scifi* key and provide the URL containing the new model.

```json
{
    "scifi": {
        "version": 2,
        "num_samples": 5,
        "url": "https://drive.google.com/uc?id=brandNewModel"
    },
    {
    "fantasy": {
        "version": 1,
        "num_samples": 5,
        "url": "https://drive.google.com/uc?id=1zipBVixMM-8NmvewdvrhQpI9mXF9mki1&export=download&confirm=x-Y-"
    }
}
```

## Providing custom models

> :warning: **Read this if you want to use your owm models.**

I used this Google Colab [Notebook](https://colab.research.google.com/drive/1VLG8e7YSEwypxU-noRNhsv5dW4NfTGce), also provided by [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple), to train the model using a GPU. After training, you can save a checkpoint to your Google Drive archived in a tar file. The tar file has the structure below:

```
checkpoint/run1/
checkpoint/run1/model-1000.index
checkpoint/run1/model-1000.meta
checkpoint/run1/hparams.json
checkpoint/run1/counter
checkpoint/run1/model-1000.data-00000-of-00001
checkpoint/run1/encoder.json
checkpoint/run1/checkpoint
checkpoint/run1/events.out.tfevents.1593185414.80e6482fdd30
checkpoint/run1/vocab.bpe
```

If you use the Notebook above, the saved tar file will be like this already, but if you want to use a custom file, you *must* provide an archive file (either tar, zip, 7z, whatever) with this structure inside.

## Running with Docker

To run the server on a Docker container, execute the following from the root directory:

```bash
docker build -t gpt-2-sentences .
docker run -dp 5000:5000 gpt-2-sentences
```

If you want to use a GPU to generate the sentences, you will need to uncomment lines 9-33 in the Dockerfile to install additional dependencies. It will take some time though and require a lot of space.