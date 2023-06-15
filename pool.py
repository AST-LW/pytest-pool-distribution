import json
import os


class DataPointError(Exception):
    pass


class Pooling:

    DATA_DIR = "./data"

    @staticmethod
    def __segregate_pool_data(worker_count):
        """
        product_pool_data.py
            [
                {
                    "product_id": "1",
                    "product_name": "Table"
                },
                ...
            ]

        user_pool_data.py
            [
                {
                    "user_name": "James",
                    "user_email": "james@email.com"
                },
                ...
            ]
        ... 

        Returns:

        {
            "0": {
                "product": {
                    "product_id": "1",
                    "product_name": "Table"
                },
                "user": {
                    "user_name": "James",
                    "user_email": "james@email.com"
                }
            },
            ... 
        }

        """
        segregated_pool_data = {}

        data_files_list = os.listdir(Pooling.DATA_DIR)

        for worker_index in range(worker_count):
            temp = {}
            for data_file in data_files_list:
                # Error will be thrown if the data points are less than the specified parallel instance
                # 3 data points in data files -> 4 instances started 
                # throw error that ./gw3.json is not found ... it again can be handled .. How.. left to user choice
                with open(f"{Pooling.DATA_DIR}/{data_file}", "r") as file:
                    data = json.load(file)
                    key = data_file.split("_")[0]
                    try:
                        temp[key] = data[worker_index]
                    except:
                        # Throwing the error when the data points count in all the data files does not equal with instances specified...
                        raise DataPointError("Data point count is not matched")
            segregated_pool_data[worker_index] = temp
        return segregated_pool_data

    @staticmethod
    def create_pool_template(session_request):
        """
        Creating the the instance file based on number of instances...

        pytest -n 2 - gw0.json gw1.json

        pytest -n 3 - gw0.json gw1.json gw2.json

        and also dumps the segregated data into respective files ( Assured that number of instances == number of instance files == split of data )

        This method should be executed in "session" scope
        """
        try:
            worker_count = int(
                session_request.config.workerinput["workercount"])

            segregated_pool_data = Pooling.__segregate_pool_data(worker_count)

            for worker_index in range(worker_count):
                with open(f"./gw{worker_index}.json", "w") as file:
                    file.write(json.dumps(segregated_pool_data[worker_index]))

        except:
            # continue as this is not a parallel execution
            pass

    @staticmethod
    def create_instance_reference(function_request):
        """
        Now when the test case runs, we get there instance on which it is going to be executed... like gw0 or gw1 or gw2 ...

        Hence this method does the same by storing the information in the Environment variable called INSTANCE_INFO

        This method is executed in "function" scope
        """
        try:
            os.environ[f"INSTANCE"] = str({
                "instance": str(function_request.config.workerinput["workerid"]),
                "test_case": str(function_request.node.nodeid)
            })
        except:
            # continue as this is not a parallel execution
            pass

    @staticmethod
    def get_pool_data(key):
        """
        This method fetches the respective data point using key which points to keys in respective instance files

        Test case - T0
        Running on - gw0
        Fetch - gw0.json file
        Retrieve - <json-data>["product"]
        Returns - 
            {
                "product_id": "1",
                "product_name": "Table"
            }
        """

        instance_info = eval(os.environ.get(f"INSTANCE"))

        with open(f"./{instance_info['instance']}.json", "r") as file:
            json_data = json.load(file)

            # This can be used to check the execution as in pytest xdist does not allow printing on console...
            with open(f"./debug.txt", "a") as file:
                file.write(
                    f"Instance - {str(instance_info['instance'])}; Test case - {str(instance_info['test_case'])}; Data Retrieved - {json_data[key]}" + "\n")

            return json_data[key]
