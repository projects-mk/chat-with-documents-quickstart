### Deployment options
<details>
<summary>Docker</summary>
- Go to docker dir and then to cpu-only or gpu and run `docker compose up -d`
</details>

<details>
<summary>Kubernetes</summary>
- Not yet supported
</details>

<br>
Just remember to add necessary api keys for example if you want to use OpenAI models, provide OPENAI api key in docker-compose file

<br>

<details>
<summary>Usage</summary>

1. Check if everything is connected correctly in **`Resources`** tab
    ![image](imgs/resources.png)

2. Upload PDF document
    ![image](imgs/upload_and_embed.png)

3. Create new chat
    ![image](imgs/start_chat.png)

4. Start Chatting, in this case using smallest possible llm (zephyr3b)
    ![image](imgs/example_query.png)

</details>

### More advanced configuration

Local LLM models inference is done using [Ollama]('https://ollama.ai/'). So any model listed in [here](https://ollama.ai/library) is supported.

<br>

#### Adding additional LLMs

<details>
<summary>Downloading Open Source models is done in a Resources Tab</summary>

![image](imgs/resources-models.png)
</details>

<br>

#### Enabling prompt monitoring

<details>
<summary>Connecting monitoring service (Langfuse server) is done in Resources Tab</summary>

![image](imgs/resources-monitoring.png)
</details>
By default Langfuse URL will point to url defined as a MONITORING_SERVER_URL, so if you are deploying this app with docker compose, there is no need to change anything here.

You can of cource provide URL pointing to Langfuse cloud as well.

<details>
<summary>Setting up monitoring server</summary>

1. Go to app_url:3000 and create account
    ![image](imgs/lf-signup.png)

2. Log in and create new project
    ![image](imgs/lf-new-project.png)

3. Create a pair of API keys
    ![image](imgs/lf-api-keys.png)

4. Pass those keys into corresponding places in Resources Tab
</details>
