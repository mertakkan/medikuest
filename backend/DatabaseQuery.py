#DatabaseQuery.py

import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import random


class MedicalDatabase:
    minmaxSensitivities = {"Age":100, "Height":250, "Weight":100, "BMI":35, "Temperature":20, "HeartRate": 40, 
                           "BloodPressure": 50, "Cholesterol": 130}
    #avgSensitivities = {"Age":50, "Height":100, "Weight":52.5, "BMI":17, "Temperature":10, "HeartRate": 20, 
    #                       "BloodPressure": 25, "Cholesterol": 65}
    avgSensitivities = {"Age":100, "Height":250, "Weight":100, "BMI":35, "Temperature":20, "HeartRate": 40, 
                           "BloodPressure": 50, "Cholesterol": 130}
    exponentialBloodSensitivity = 1
    def __init__(self):
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="MertAkkanPass123",
            auth_plugin='mysql_native_password',
            database='medicaldatabase'  # Add the database name
        )
        self.connection = db_connection
        self.cursor = self.connection.cursor()

    def DiscreteSelection(self, discreteDataType, input_value, personal_epsilon):
        # Implement different functions based on discreteDataType
        if discreteDataType == "blood":
            return self.bloodTypeTotalNum(input_value, personal_epsilon, 1)
        elif discreteDataType == "smoke":
            return self.smokeTypeTotalNum(input_value, personal_epsilon, 1)
        elif discreteDataType == "diabetes":
            return self.diabetesTypeTotalNum(input_value, personal_epsilon, 1)

    def laplaceMechanism(self, personal_epsilon, sensitivity):
        mean = 0
        scale = sensitivity / personal_epsilon
        return np.random.laplace(loc=mean, scale=scale, size=1)[0]

    def exponentialMechanism(self, personal_epsilon, sensitivity, input_list, discreteDataType):
        totalSize = len(input_list)

        Qfs = [0] * totalSize
        for j in range(totalSize):
            Qfs[j] = self.DiscreteSelection(discreteDataType, input_list[j], personal_epsilon)

        max_Qfs = max(Qfs)

        # Subtract the maximum value to prevent overflow
        exp_terms = [np.exp((personal_epsilon * (q - max_Qfs)) / (2 * sensitivity)) for q in Qfs]

        denominator = np.sum(exp_terms)

        exponentialResult = [exp_term / denominator for exp_term in exp_terms]

        selectedIndex = random.choices(range(totalSize), weights=exponentialResult, k=1)[0]

        return input_list[selectedIndex]

    def maxGeneral(self, attribute, personal_epsilon):
        max_query = f"SELECT MAX({attribute}) FROM patients;"
        self.cursor.execute(max_query)
        max_value = float(self.cursor.fetchone()[0])
        return max_value + self.laplaceMechanism(personal_epsilon, self.minmaxSensitivities[attribute])

    def minGeneral(self, attribute, personal_epsilon):
        min_query = f"SELECT MIN({attribute}) FROM patients;"
        self.cursor.execute(min_query)
        min_value = float(self.cursor.fetchone()[0])
        return min_value + self.laplaceMechanism(personal_epsilon, self.minmaxSensitivities[attribute])

    def averageGeneral(self, attribute, personal_epsilon):
        average_query = f"SELECT AVG({attribute}) FROM patients;"
        self.cursor.execute(average_query)
        avg_value = float(self.cursor.fetchone()[0])
        return avg_value + self.laplaceMechanism(personal_epsilon, self.avgSensitivities[attribute])


    """
    def numberOfDiscreteAttribute(self, attribute):
        total_num_query = f"SELECT COUNT({attribute}) FROM patients;"
        self.cursor.execute(total_num_query)
        total_num = self.cursor.fetchone()[0]
        return total_num
    """

    # All discrete attribute total nums.
    def bloodTypeTotalNum(self, blood_type, personal_epsilon, mode):
        query = "SELECT COUNT(*) FROM patients WHERE BloodType = %s;"
        self.cursor.execute(query, (blood_type,))
        total_num = float(self.cursor.fetchone()[0])
        return total_num + self.laplaceMechanism(personal_epsilon, 1) if mode == 0 else total_num

    def diabetesTypeTotalNum(self, diabetes_type, personal_epsilon, mode):
        query = "SELECT COUNT(*) FROM patients WHERE Diabetes = %s;"
        self.cursor.execute(query, (diabetes_type,))
        total_num = float(self.cursor.fetchone()[0])
        return total_num + self.laplaceMechanism(personal_epsilon, 1) if mode == 0 else total_num

    def get_epsilon(self, username):
        epsilon_query = "SELECT epsilon FROM users WHERE username = %s"
        self.cursor.execute(epsilon_query, (username,))
        epsilon_value = float(self.cursor.fetchone()[0])
        return epsilon_value
    
    def update_epsilon(self, username):
        update_epsilon_query = "UPDATE users SET epsilon = %s WHERE username = %s"

        # Get the current epsilon value
        current_epsilon = self.get_epsilon(username)

        # Calculate the new epsilon value (half of the current value)
        new_epsilon = current_epsilon / 2

        # Update the epsilon value in the database
        self.cursor.execute(update_epsilon_query, (new_epsilon, username))
        self.connection.commit()

    def smokeTypeTotalNum(self, smoke_type, personal_epsilon, mode):
        query = "SELECT COUNT(*) FROM patients WHERE Smoking = %s;"
        self.cursor.execute(query, (smoke_type,))
        total_num = float(self.cursor.fetchone()[0])
        return total_num + self.laplaceMechanism(personal_epsilon, 1) if mode == 0 else total_num

    def createHistogram(self, attribute, values, personal_epsilon):
        total_num_list = []
        for value in values:
            query = f"SELECT COUNT(*) FROM patients WHERE {attribute} = %s;"
            self.cursor.execute(query, (value,))
            total_num = float(self.cursor.fetchone()[0])
            total_num_list.append(total_num + self.laplaceMechanism(personal_epsilon, 1))

        # Plotting the bar chart
        plt.bar(values, total_num_list, color='blue')
        plt.xlabel(attribute)
        plt.ylabel('Total Number')
        plt.title(f'{attribute} Numbers')

        fig, ax = plt.subplots()
        ax.bar(values, total_num_list, color='blue')
        ax.set_xlabel(attribute)
        ax.set_ylabel('Total Number')
        ax.set_title(f'{attribute} Numbers')
        return fig

    def mostCommonBloodType(self, personal_epsilon):
        blood_types = ["A", "B", "AB", "O"]
        return self.exponentialMechanism(personal_epsilon, self.exponentialBloodSensitivity, blood_types, "blood")

    # Authentication
    def loginCheck(self, username, password):
        checkQuery = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(checkQuery, (username, password))
        result = self.cursor.fetchone()
        if result:
            print("Login successful")
            return 1
        else:
            print("Invalid username or password")
            return 0

    def register(self, username, password):
        usernameUniqueness = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(usernameUniqueness, (username,))
        notUnique = self.cursor.fetchone()
        if notUnique:
            return 0
        else:
            registerQuery = "INSERT INTO users (username, password, epsilon) VALUES (%s, %s, %s)"
            self.cursor.execute(registerQuery, (username, password, 5.0))
            self.connection.commit()
            return 1
        
    def complexQuery1(self, personal_epsilon):
        query = """
                    SELECT 
                    AgeGroup,
                    -- Calculate the intersection of high counts
                    SUM(HighBMICount * HighBPCount * HighCholesterolCount) AS IntersectionCount
                FROM (
                    SELECT 
                        CASE 
                            WHEN Age BETWEEN 18 AND 30 THEN '18-30'
                            WHEN Age BETWEEN 31 AND 45 THEN '31-45'
                            WHEN Age BETWEEN 46 AND 60 THEN '46-60'
                            ELSE '60+' 
                        END AS AgeGroup,
                        BMI AS AverageBMI,
                        BloodPressure AS AverageBloodPressure,
                        Cholesterol AS AverageCholesterol,
                        CASE WHEN BMI > 25 THEN 1 ELSE 0 END AS HighBMICount,
                        CASE WHEN BloodPressure > 120 THEN 1 ELSE 0 END AS HighBPCount,
                        CASE WHEN Cholesterol > 200 THEN 1 ELSE 0 END AS HighCholesterolCount
                    FROM Patients
                    WHERE Age IS NOT NULL
                ) AS DerivedTable
                GROUP BY AgeGroup;
                """
        
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return self.createHistogram2(result, personal_epsilon)
        

    def createHistogram2(self, result, personal_epsilon):
        values = []
        total_num_list = []
        attribute = "Expected Deaths"
        for tuple in result:
            values.append(tuple[0])
            total_num_list.append(float(tuple[1]) + self.laplaceMechanism(personal_epsilon, 1))

        plt.bar(values, total_num_list, color='blue')
        plt.xlabel(attribute)
        plt.ylabel('Total Number')
        plt.title(f'{attribute} Numbers')

        fig, ax = plt.subplots()
        ax.bar(values, total_num_list, color='blue')
        ax.set_xlabel(attribute)
        ax.set_ylabel('Total Number')
        ax.set_title(f'{attribute} Numbers')
        return fig




    def close_connection(self):
        # Close the database connection
        self.connection.close()


# Example usage:
if __name__ == "__main__":
    medical_db = MedicalDatabase()

    # Retrieve statistics for patients' ages
    # max_age, min_age, avg_age = medical_db.maxMinAverageGeneral("Age", 10)

    # print("Maximum Age:", max_age)
    # print("Minimum Age:", min_age)
    # print("Average Age:", avg_age)
    """
    zeroTypeTotal = medical_db.bloodTypeTotalNum("A", 10, 1)
    print(zeroTypeTotal)
    zeroTypeTotal = medical_db.bloodTypeTotalNum("B", 10, 1)
    print(zeroTypeTotal)
    zeroTypeTotal = medical_db.bloodTypeTotalNum("AB", 10, 1)
    print(zeroTypeTotal)
    zeroTypeTotal = medical_db.bloodTypeTotalNum("O", 10, 1)
    print(zeroTypeTotal)
    """

    # res=medical_db.complexQuery1(10)


    # medical_db.createBloodHistogram(10)
    # medical_db.createDiabetesHistogram(10)
    # medical_db.createSmokeHistogram(10)
    # print(medical_db.mostCommonBloodType(10))

    # Close the database connection
    medical_db.close_connection()
