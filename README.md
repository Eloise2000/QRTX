# Real-Time Experimentation (RTX)

![Banner](https://raw.githubusercontent.com/Starofall/RTX/master/banner.PNG)


### Description
Q-learning Real-Time Experimentation (QRTX) tool allows for self-adaptation with optimization strategies based on real-time (streaming) data analysis. We provide Q-learning for self-optimization, which can discover optimal system configurations at runtime for each distinct situation that is also dynamically identified at runtime. QRTX is particularly useful in analyzing operational data in a Big Data environement.


### Minimal Setup
* Download the RTX code
* Run `python setup.py install` to download all dependencies 
* To run example experiments, first install [CrowdNav](https://github.com/Starofall/CrowdNav)
* To use Spark as a PreProcessor you also need to install Spark and set SPARK_HOME

### Getting Started Guide
1. First run Kafka in Docker:
   `docker run --name kafka --hostname kafka -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=kafka --env ADVERTISED_PORT=9092 spotify/kafka`
2. Start CrowdNav and run SUMO locally:
   `python run.py`
3. Run QRTX execution strategies

For more details, you can refer to [RTX & CrowdNav Getting Started Guide](https://github.com/Starofall/RTX/wiki/RTX-&-CrowdNav-Getting-Started-Guide)

### Abstractions
RTX has the following abstractions that can be implemented for any given service:
* PreProcessor - To handle Big Data volumes of data, this is used to reduce the volume
    * Example: Spark   
* DataProviders - A source of data to be used in an experiment
    * Example: KafkaDataProvider, HTTPRequestDataProvider
* ChangeProviders - Communicates experiment knobs/variables to the target system
    * Example: KafkaChangeProvider, HTTPRequestChangeProvider
* ExecutionStrategy - Define the process of an experiment
    * Example: Sequential, Gauss-Process-Self-Optimizing, Linear 
* ExperimentDefinition - A experiment is defined in a python file 
    * See `./experiment-specification/experiment.py`

### Supported execution strategies
* Start training process:
  * `python qrtx.py start Qlib`
  * You can further change the training parameter in `/QRTX/Qlib/qworkflow.py`
* Start testing using trained q-table:
  `python qrtx.py test Qlib [q_table csv file]`