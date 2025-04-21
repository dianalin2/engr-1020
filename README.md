# Engineering 1020 Project

## The Problem

The solution involves a desktop frontend where the user uploads infrastructure information into a database. An on-premises LLM generates SysML models based on the information provided through the database. This model could then be viewed in a SysML visualizer. This solution allows for dynamic generation of SysML models that are tailored to the inventoried hardware. 

## Technologies

We are using Electron for the desktop frontend.

We are using MongoDB for the database because it stores data in “documents,” which allows for components to be stored in a flexible JSON-like hierarchal model. This document model is more aligned with a SysML model than other SQL database alternatives. 

We are using Llama for our LLM. Llama can be deployed on-premises, which reduces the security overheads of using LLMs because it does not access external servers. While the computing power needed for this solution is much higher than an externally provided LLM, this is not a restriction for our client, as mentioned in a previous client interview. 

A diagram of how the application works is shown below:

<p align="center">
  <img src="https://github.com/dianalin2/engr-1020/blob/main/docs/flowchart.png?raw=true" />
</p>

## Deployment

### Prerequisites

- Python 3.7+
- Node.js
- Docker and Docker Compose (for on-premises database and SysML viewer deployment)

### Instructions

1. Create a Python virtual environment with the following command: `virtualenv venv/`, activate the environment, and run `pip intall -r requirements.txt` in the root directory of the repository to install Python dependencies.

2. Create a Hugging Face account, request access for the [Llama 3.2](https://huggingface.co/collections/meta-llama/metas-llama-32-language-models-and-evals-675bfd70e574a62dd0e40586) models, and generate an [access token](https://huggingface.co/settings/tokens) for your HuggingFace account.

3. Deploy a MongoDB database. For more in-depth directions, see [Database Deployment](#database-deployment).

4. Set the following environment variables:
    - `PYTHON_PATH=<your python command>`
    - `HF_TOKEN=<your generated access token>`
    - `DB_uri=<your database connection url>`
  Alternatively, create a [`.env` file](https://dotenvx.com/docs/env-file#format) with the above environment variable values. 

5. Deploy a SysML viewer. To easily deploy a SysML viewer on-premises, install [Docker](http://www.docker.com) and Docker Compose on your machine. Then, run `docker compose up app` in the root directory.

6. In the command line, ensure you are in the `./gui` folder. Then install dependences with `npm install` and run the application with `npm run start`. Your GUI should now launch.

## Database Deployment

### Off-Premises Deployment

To deploy a database off-premises, we recommend [MongoDB Atlas](https://www.mongodb.com). Simply follow the instructions to deploy a database expressly and use the generated database URL to connect to the database.

### On-Premises Deployment

To deploy a dataase on-premises, first install [Docker](https://www.docker.com) and Docker Compose on the machine you want to deploy the database on. For development, this machine is likely your personal machine.

In the command line, ensure you are in the root directory of the repository and start the database with Docker Compose:

```sh
docker compose up mongo
```

The database should start, and you can now connect to the database at `mongodb://root:example@localhost:27017`.
