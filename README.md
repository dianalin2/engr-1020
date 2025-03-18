# Engineering 1020 Project

The solution involves a desktop frontend where the user uploads infrastructure information into a database. An on-premises LLM generates SysML models based on the information provided through the database. This model could then be viewed in a SysML visualizer. This solution allows for dynamic generation of SysML models that are tailored to the inventoried hardware. 

We are using Electron for the desktop frontend.

We are using MongoDB for the database because it stores data in “documents,” which allows for components to be stored in a flexible JSON-like hierarchal model. This document model is more aligned with a SysML model than other SQL database alternatives. 

We are using Llama for our LLM. Llama can be deployed on-premises, which reduces the security overheads of using LLMs because it does not access external servers. While the computing power needed for this solution is much higher than an externally provided LLM, this is not a restriction for our client, as mentioned in a previous client interview. 

<p align="center">
  <img src="https://github.com/dianalin2/engr-1020/blob/main/docs/flowchart.jpg?raw=true" />
</p>
