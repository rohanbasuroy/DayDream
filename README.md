# DayDream: Executing Dynamic Scientific Workflows on Serverless Platforms with Hot Starts
## Description
Daydream uses serverless computing to execute dynamic scientific workflows, expressed as directed acyclic graphs (DAGs). DayDream learns about invocation and execution characteristics of components in a dynamic DAG. This helps DayDream to optimally shcedule the components of a DAG to jointly minimize both execution time and cost. DayDream introduces a novel concept called "hot start" of serverless function instances using a probabilistic model to speed up DAG execution on a two-tier (high-end and low-end) serverless platform. 

## Evaluated Applications
DayDream is evaluated with the scientific workflows: [ExaFEL] (cctbx-workflow)(https://www.exascaleproject.org/research-project/exafel/), [Cosmoscout-VR](https://github.com/cosmoscout/cosmoscout-vr), and [CCL](https://github.com/LSSTDESC/CCL). These workflows are widely used by the HPC community and are parts of major HPC projects. They represent significant variation in terms of compute characteristics and have all significant components of scientific workflows.

## Implementation Details
DayDream is implemented in Python3.6 using AWS Lambda in Amazon Cloud as the serverless platform. However, it can be easily ported across other commercial serverless platforms, like Google Cloud Functions in Google Cloud and Azure Functions in Microsoft Cloud.  It utilizes properties of commercial serverless platforms such as cold starts. DayDream has three major components in its design: (1) A system level DAG scheduler, (2) a back-end storage server, and (3) a serverless function pool. The system level DAG scheduler hot starts serverless function instances to execute components of a DAG. The back-end storage server is used by the different serverless functions to exchange messages during their execution. Now, as the application execution starts, the DAG scheduler connects to the back-end storage server and instructs which components corresponding to the current phase should be executed. Depending upon the instructions from the DAG scheduler, function instances for the execution of components of a phase are hot started. 

## Nomenclature Used
DayDream executes applications in form of dynamic DAGs. In a DAG, individual units of execution are called **components**. The components which can run in parallel form a **phase**. Each component is executed by a serverless function, *i.e.,* a AWS Lambda. **Phase time** is the time to complete each phase of the DAG. *The sum of all phase times is the total execution time of the DAG.* **Service Time** of a serverless function is the total end-to-end time of execution of a function which includes the compute and I/O times, as well as the cold start time or hot start time and the wait time (if applicable). Each DAG can run using different component and phase structures, each of which is referred to as a **run**. DayDream is evaluated with *50 runs* of each of the three applications. 

## Setup DayDream

DayDream executes the components of DAGs on AWS Lambda. However, the controller of DayDream runs on a *local computer*, which invokes functions, hot starts functions, and performs all other scheduling decisions. This *local computer* can be any Linux based system which can run **python subprocess**, **python threading**, and can install **aws command line interface (CLI)**. In our experimentation we used a 20-core machine with Ubuntu 18.04 LTS operating system. 
On this *local computer*, perform the following actions to setup DayDream:

(1) *Install the required libraries and AWS CLI* 
   
        pip3 install awscli
        pip3 install numpy
        pip3 install scipy
       

(2) *Configure AWS CLI* 

        aws configure
        
Then follow the prompts to enter your AWS credentials to link the local computer to your AWS account.
        
(3) *Clone this repository in the local computer* </br>
This directory contains three folders *CCL-daydream*, *cctx-workflow-daydream*, and *cosmoscout-vr-daydream*. Each of these folders contains all scripts, executables and experimental data of the application DAGs.

(4) *Set up AWS execution role* </br>
Login to AWS Web portal. Set up an execution role from AWS dashboard with full access of Lambda to S3. This execution role id should start with "arn:aws:iam:.." followed by numericals. Copy this execution role id. 

From the root directory of this repository go to *"cd CCL-daydream/build/"*. Open the **create.py** python file and find two lines which says *command = "aws lambda create-function..."*. In these two lines replace the *--role* parameter with the execution role id which you just created before. Perform the same action, by changing the **create.py** files for both the other applications by going into their respective *build* directories (*"cd cosmoscout-vr-daydream/build/"*, and *cd cctbx-workflow-daydream/build*). </br> 

This completes the setup of setup of DayDream. 

## Run DayDream

(1) **Run CCL** 
  
        cd ./CCL-daydream/build
        python3 main.py
This is the one and only line required to execute all 50 runs of CCL with DayDream as the controller. It sets up CCL in AWS Lambda, sends its executables to AWS, hot starts functions, executes functions on high-end (AWS Lambda with 10 GB memory) and low-end (AWS Lambda with 5 GB memory) AWS Lambdas, and does all other scheduling decisions that DayDream performs. It takes approximately **158 minutes** to complete all the 50 runs. The *run-1* to *run-50* folders are inside *./CCL-daydream/* directory. After the completion of each run, 3 output files are generated in the corresponding *run* directories: (a) **phase_time.txt** (time to complete each phase of the DAG, the sum of which is the total execution time of the DAG). (b) **function_service_time.txt**  (contains the service time of all individual components in all the phases). (c) **execution_cost.txt** (the cost incurred to the cloud provider for each individual components, the sum of which is the total execution cost of the DAG). 

(2) **Run cctbx-workflow** 
  
        cd ./cctbx-workflow-daydream/build
        python3 main.py
This is the one and only line required to execute all 50 runs of cctbx-workflow with DayDream as the controller. It sets up cctbx-workflow in AWS Lambda, sends its executables to AWS, hot starts functions, executes functions on high-end (AWS Lambda with 10 GB memory) and low-end (AWS Lambda with 5 GB memory) AWS Lambdas, and does all other scheduling decisions that DayDream performs. It takes approximately **531 minutes** to complete all the 50 runs. The *run-1* to *run-50* folders are inside *./cctbx-workflow-daydream/* directory. After the completion of each run, all the 3 output files are generated inside the corresponding *run* directories, similar to CCL.  

(3) **Run cosmoscout-vr** 
  
        cd ./cosmoscout-vr-daydream/build
        python3 main.py
This is the one and only line required to execute all 50 runs of cosmoscout-vr with DayDream as the controller. It sets up cosmoscout-vr in AWS Lambda, sends its executables to AWS, hot starts functions, executes functions on high-end (AWS Lambda with 10 GB memory) and low-end (AWS Lambda with 5 GB memory) AWS Lambdas, and does all other scheduling decisions that DayDream performs. It takes approximately **585 minutes** to complete all the 50 runs. The *run-1* to *run-50* folders are inside *./cosmoscout-vr-daydream/* directory. After the completion of each run, all the 3 output files are generated inside the corresponding *run* directories, similar to CCL. 

## Reproduce Results

Each run folder under ./application-name-daydream/ has three **baseline** files (*execution_cost-baseline.txt*, *function_service_time-baseline.txt*, and *phase_time-baseline.txt*). These baseline files are the data generated during the experimentation of DayDream and are used in the paper. If the data in the corresponding generated files (*execution_cost.txt*, *function_service_time.txt*, and *phase_time.txt*) matches with the data from the baseline files, with a less than 10% error bound, then the results of DayDream are successfully reproduced. 
   
## Code Structure

The **main.py** script under ./application-name-daydream/build/ is the main controller of DayDream. It has the following main functions: (a) *define_application* -- it generates the DAG for the particular run and maps the executables (**.exe files**) with the different components. (b) *predict_hot_start* -- it predicts the number of serverless functions to hot start in each phase based on a Weibull distribution fit. (c) *hot_start* -- it actually invokes and hot starts Lambdas in AWS (d) *execute* -- when a component is invoked, this function hot starts them if functions are available or cold starts them if hot started functions are not available. (e) *delete_container* -- it deletes serverless functions after the completion of the run. (f) *generate_output* -- it generates the output files of each run. 

The *main.py* access three other python scripts: *create.py*, *invoke.py*, and *delete.py* to create, invoke, and delete serverless functions, respectively. 

The *test.zip* folder inside /application-name-daydream/build/ contains the package with executables and AWS Lambda function which is shipped to AWS by *main.py* to create serverless Lambda functions.

```./<application_name>/my_test/``` : records the profiling data of each components in a DAG. It includes the concurrency per phase, cpu utilization, memory utilization, and I/O bandwidth utilization.


## Evaluation Metrics
We compare the performance of DayDream in terms of DAG execution time (summation of all phase times) and execution cost. 
