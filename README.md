<p align=center>
  <img height="222px" src="https://github.com/aurimas13/MIT_CS_Application/blob/main/Public/MIT_CS_1.png"/>
</p>
<h1 align="center"> Simple LLM Price Identification 🚀 </h1>
<p align="center"> Identify Lowesrt Prices for the products. </p>
<p align="center"> Featuring <b> Notebooks </b> to Modules to <b> Infrastructure in Azure </b> & more. </p>
<br>
<p align=center>
  <a href="https://img.shields.io/github/last-commit/aurimas13/LLM-Price-Agent"><img alt="lastcommit" src="https://img.shields.io/github/last-commit/aurimas13/LLM-Price-Agent?style=social"/></a>
  <a href="https://img.shields.io/github/stars/aurimas13/LLM-Price-Agent"><img alt="stars" src="https://img.shields.io/github/stars/aurimas13/LLM-Price-Agent?style=social"/></a>
  <!-- <a href="https://img.shields.io/github/forks/aurimas13/MIT_CS_Application"><img alt="twitter" src="https://img.shields.io/github/forks/aurimas13/MIT_CS_Application?style=social"/> -->
  <a href="https://twitter.com/aanausedas"><img alt="twitter" src="https://img.shields.io/twitter/follow/aanausedas?style=social"/></a>

**Hello and welcome!** 

End-To-End application of an LLM agent that takes the details of the product characteristics and returns a list of suggested products with lowest prices at the top and descriptions. LLM agent that sold the goods using Open AI - ChatGPT - can be inspected through [Simple LLM Python module](https://github.com/aurimas13/LLM-Price-Agent/blob/main/LLM_Goods.py) or a newer Python module that is still under work by 21st of February [here](https://github.com/aurimas13/LLM-Price-Agent/blob/main/modules/LLM_Goods_Final.py) or a newer Jupyter Notebook [here](https://github.com/aurimas13/LLM-Price-Agent/blob/main/notebooks/LLM_Goods_Final.ipynb) while `FastAPI` found [here](https://github.com/aurimas13/LLM-Price-Agent/blob/main/app/main.py), `Docker`- [here](https://github.com/aurimas13/LLM-Price-Agent/blob/main/Dockerfile) & `Terraform` - [here](https://github.com/aurimas13/LLM-Price-Agent/blob/main/terraform-fastapi/main.tf) implementations are built for the [older Python module](https://github.com/aurimas13/LLM-Price-Agent/blob/main/LLM_Goods.py) based on [older Jupyter notebook](https://github.com/aurimas13/LLM-Price-Agent/blob/main/notebooks/LLM_Goods.ipynb) that is ought to be remade by 21st of February as PostgreSQl database is not yet implemented but under work as found [here](https://github.com/aurimas13/LLM-Price-Agent/blob/main/app/database.py).

### 📊 TODO if not DONE by 21st of Feruary:

**DONE** 1. Update the description of the solved problem with what is expected.

**DONE** 2. Ensure the app is not getting blocked or over-engineering the solution, by starting from Jupyter Notebook and making the agent work.

**DONE** 3. Wrap up in Fast API and expose the POST endpoint to perform chat. Will assume that there is one user.

**DONE** 4. Wrap up the solution in docker-compose (+) to ensure we can spin it up quickly for validation. 

*Still under work* 5. Use great_expectations for validation.

**DONE** 6. Document the edge cases, tradeoffs, and assumptions made during an implementation and providing directions to remediate and solve those cases as found [here](https://github.com/aurimas13/LLM-Price-Agent/blob/main/public/Edges%2C%20Tradeoffs%2C%20Assumptions.md).

**DONE** 7. Create a Terraform script to host the solution in the Azure. 

*Still under work* 8. Document Terraform implemetation in README.

*Still under work* 9. Provide a list of limitations and potential scalability issues for the final implementation and options to overcome them.

*Still under work* 10. Update README.md with the latest information and provide a link to the deployed solution on Azure.

1. Create a Virtual Ebvironemnt

`python3 -m venv venv`

2. Activate the Virtual Environment

- On macOS and Linux:

```bash
source venv/bin/activate
```

- On Windows:
`.\venv\Scripts\activate`

3. Install the dependencies

`pip install -r requirements.txt`

4. Run the application

5. Deactivate the Virtual Environment

`deactivate`
