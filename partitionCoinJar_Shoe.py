import os;
import argparse;
import csv
import time;
import numpy as np;
import matplotlib.pyplot as plt;
from scipy.optimize import curve_fit;

def is_file_valid(filename) -> bool:
  if not os.path.exists(filename):
    print(f"The file {filename} could not be found")
    return False
  return True

def exponential_funct(x, a, b):
  return a * np.exp(b * x)

'''
dumbSolver -- a simple recrusive brute force method to try all pile combos
'''
# Try with itertools?
def dumbSolver(jarOfCoins: list[int], index: int, leftPile: list[int], rightPile: list[int]) \
-> list[list[int], list[int]]:  
  # Base Case: only one coin is left, and we no longer recur
  if (len(jarOfCoins) == index + 1):
    lastCoin = jarOfCoins[index]
    # Compute the value of the left and right piles
    leftSum = sum(leftPile)
    rightSum = sum(rightPile)
    # Try and balance both piles
    if ((leftSum + lastCoin) == rightSum):
      return [leftPile + [lastCoin], rightPile]
    if ((rightSum + lastCoin) == leftSum):
      return [leftPile, rightPile + [lastCoin]]
    # If no pairing works, return empty for failure
    return []
  
  # Otherwise, try putting the coin in the left and right pile
  nextCoin = jarOfCoins[index]

  tryLeftPile = dumbSolver(jarOfCoins, index+1, leftPile + [nextCoin], rightPile)
  if (tryLeftPile): 
    return tryLeftPile
  
  tryRightPile = dumbSolver(jarOfCoins, index+1, leftPile, rightPile + [nextCoin])
  if (tryRightPile): 
    return tryRightPile
    
  # If no combos worked, return empty for failure
  return []

'''
find_coin_coints -- Finds a way to split a coin jar into two even piles.
Returns none if no combination is possible.
Inputs: A numbered index for the test case and a jar of coins
Outputs: A dictionary with the testcase index as the key and data as the value
Data: a list of the left and right piles, the computation time in nanoseconds, and the number of coins in the jajr
'''
def find_coin_counts(testcaseNumber: int, jarOfCoins: list[int]) \
-> dict[int: tuple[list[list[int], list[int]], float, int]]:
  # Get the number of coins to classify the problem
  numCoins = len(jarOfCoins)

  # Start the clock to measure program length
  startTime_ns = time.time_ns()

  # # Sample Unit Case: If the total value of the jar is odd, it cannot be split
  # # Not included as this would cause roughly half the problems to be solved immediately
  # totalValue = sum(jarOfCoins)
  # if (totalValue & 1):
  #   endTime_ns = time.time_ns()
  #   totalTime_ns = endTime_ns - startTime_ns
  #   return {testcaseNumber: ([], totalTime_ns, numCoins)}

  # Use a backtracking algorithm to find the amount of each coin to use
  splitPiles = dumbSolver(jarOfCoins, 0, [], [])

  # Stope the clock
  endTime_ns = time.time_ns()
  totalTime_ns = endTime_ns - startTime_ns

  # Generate testcase result
  return {testcaseNumber: (splitPiles, totalTime_ns/1000, numCoins)}

'''
partitionCoinjar -- takes in testcases from a user given file and plots the computation time.
This reflects the NP-Complete Partition Problem, which centers around finding two subsets of a set with the same sum.
Arguments: -f [infile] -o [outfile] -i [imagefile (optional)]
Outputs: A file containing generated results and a displayed pyplot
'''
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", dest="filename", required=True,
                      help="Input file with coin jar problem test cases." + "\n" +
                           "Data should be in the format: TestcaseNo., Coin1,  Coin2, Coin3...",
                      metavar="FILE")
  parser.add_argument("-o", "--out-file", dest="outfile", required=True,
                      help="File to dump results into", metavar="FILE")
  parser.add_argument("-i", "--image-dest", dest="outimage", required=False,
                      help="Optional: Save generated pyplot to a file.", metavar="FILE")
  args = parser.parse_args()

  # Check if the file exists
  if (not is_file_valid(args.filename)):
    return
  
  # Create a dictionary to store results
  allResults: dict[int: tuple[list[list[int], list[int]], float, int]] = {}
  successfulResults: dict[int: tuple[list[list[int], list[int]], float, int]] = {}
  failureResults: dict[int: tuple[list[list[int], list[int]], float, int]] = {}

  print(f"Computing test cases from {args.filename}...")

  # Parse the input file
  with open(args.filename, newline='') as csvfile:
    testcases = csv.reader(csvfile, delimiter=' ')
    # Loop through the testcases and generate solutions
    for test in testcases:
      # Convert data to a list of ints and grab the test case number
      testCaseInput = list(map(int, test))
      testCaseNumber = testCaseInput.pop(0)
      # Attempt to compute a solution
      testCaseResults = find_coin_counts(testCaseNumber, testCaseInput)
      allResults.update(testCaseResults)
      # Classify as a success or failure
      if (not testCaseResults[testCaseNumber][0] or testCaseResults[testCaseNumber][0] == {}):
        failureResults.update(testCaseResults)
        continue
      successfulResults.update(testCaseResults)

  print(f"Writing results to {args.outfile}")

  with open(args.outfile, 'w') as outputFile:
    # Print column labels
    outputFile.write("Testcase_Number Left_Coin_Pile Right_Coin_Pile Computation_Time Number_of_Coins\n")
    # Print out testcase data
    for testcase in range(1, testCaseNumber + 1):
      outputFile.write(f"{testcase}")
      # Try to plot the left coin pile results
      # We use an exception in case indexing an empty list throws an error
      try:
        # Merge the list into one column, or put a 0 for empty list
        leftPiles = ','.join(list(map(str,allResults[testcase][0][0])))
        if (leftPiles == []):
          outputFile.write(" 0")
          continue
        outputFile.write(f" {leftPiles}")
      except IndexError:
        outputFile.write(" 0")
      # Try to plot the right coin pile results
      try:
        rightPiles = ','.join(list(map(str,allResults[testcase][0][1])))
        if (rightPiles == []):
          outputFile.write(" 0")
          continue
        outputFile.write(f" {rightPiles}")
      except IndexError:
        outputFile.write(" 0")
      # Write the computation time and number of coins to the file
      outputFile.write(f" {allResults[testcase][1]}")
      outputFile.write(f" {allResults[testcase][2]}")
      outputFile.write("\n")

  print("Plotting data...")

  # Get the x and y values for successful results (x = numCoins, y = time elapsed)
  successXPoints = [value[2] for value in successfulResults.values()]
  successYPoints = [value[1] for value in successfulResults.values()]

  # Get x and y for failures
  failureXPoints = [value[2] for value in failureResults.values()]
  failureYPoints = [value[1] for value in failureResults.values()]

  # Generate an exponential curve fit for the worst-case failures
  params, covariance = curve_fit(exponential_funct, failureXPoints, failureYPoints)

  # Generate points for plotting the curve
  x_fit = np.linspace(min(failureXPoints), max(failureXPoints), 100)
  y_fit = exponential_funct(x_fit, *params)

  # Plot the successes and failures
  successData, = plt.plot(successXPoints, successYPoints, 'o', label='Solution Found')
  failureData, = plt.plot(failureXPoints, failureYPoints, 'x', label='No Solution')
  # Plot the curve fit to show time complexity
  line, = plt.plot(x_fit, y_fit, color='red', label='Fitted Exponential Curve')
  plt.title("NP-Complete Coin Jar Partition Problem")
  plt.xlabel("Number of Coins in the Jar")
  plt.ylabel("Computation Time per Testcase (Nanoseconds)")
  # Annotate the graph
  plt.legend()
  # If outimage argument was passed, save the plot
  if (args.outimage):
    plt.savefig(args.outimage)  
  plt.show()

if __name__ == '__main__':
  main()