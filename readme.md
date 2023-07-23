# House

House is a debate simulation between multiple participants, which can be represented by different large language models (LLMs) from OpenAI, Azure OpenAI and Google Vertex AI. Each debate participant can take on a different persona and represents a different viewpoint. The participants can also choose to search on the Internet for information.

House is an experiment to use LLMs to debate and discuss a topic and get views from multiple perspectives.

## Setup

After you have cloned the repo, rename the `.env.example` file to `.env` and provide the necessary API key and other information from your provider.

Then set up the packages needed to run House with pip.

```
$ pip install -r requirements.txt
```

You can consider setting up its own environment using Conda or pyenv or any of these similar tools.


## How to run your own house debates

Go into `specs.py` file. There are some default House participants which you can use directly, or you can create your own participants. For example, this one takes on the Socrates persona and uses OpenAI's `text-davinci-003` model.

```python
socrates = Specification(
    provider = "openai",
    model_name = "text-davinci-003",
    persona="Socrates",
    context = house_rules + "You are Socrates, a Greek philosopher from Athens who is \
        credited as the founder of Western philosophy and among the first moral philosophers \
        of the ethical tradition of thought."
)
   
```

The final list of participants you want to use is in the `house_specs` variable.

Next, go into the `house.py` file and change the question you want the house to debate on. You can also change the number of rounds the participants will debate.

```python
question = "Should AI be regulated?"
number_of_rounds = 2
```

Then you can run the app by doing this at the command line:

```
$ python house.py
```

You should see how the house is running. When the house debate ends, the content is written to a markdown file, and a summary is also generated. 

Here's an [example of the conversation file](conversation-should-ai-be-regulated-7284.md).

Here's an [example of a summary file](summary-should-ai-be-regulated-7284.md).

## Google VertexAI

House can also work with Google Cloud Platform (GCP) Vertex AI PaLM. GCP offers an enterprise version of PaLM through Vertex AI. The following instructions assume you already have an account that has the necessary credentials to use Vertex AI. 

To use Google Cloud Platform Vertex AI PaLM you can do the following:

1. If you don't already have the `gcloud` command-line interface (CLI), you can install it by following the instructions here https://cloud.google.com/sdk/docs/install
2. Once you have `gcloud`, run this command in the command line

```
$ gcloud auth application-default login
```

3. This will open up a browser for you to log into the account with the credentials to access Vertex AI. Follow the instructions and click through to login and approve.
4. Once you you're done, an `application_default_credentials.json` file wil be created at the default location. House will know how to locate this file (it's just using Google's default location to find it) to log into Vertex. 
