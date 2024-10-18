import argparse;
import random;
from datetime import datetime
import textwrap;

def main():
  # Handle arguments
  parser = argparse.ArgumentParser(
    prog='knapsackTestCaseGen',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Creates a given number each of small, medium, and large test cases for the knapsack problem.',
    epilog=textwrap.dedent('''
        The range for total value, number of coins, and coin size can be configured within the code.
        The cases are in format "totalvalue coin1value coin1count coin2value coint2count...'''))
  
  parser.add_argument("--file", "-f", required=True, type=argparse.FileType('w'),
                      help="File to print test cases to (Will overwrite data).")
  parser.add_argument("--size", "-s", required=True, type=int,
                      help="Number of test cases of to generate for each amount of coins.")
  parser.add_argument("--number-coins", "-n", required=True, type=int, dest='maxNumCoins',
                      help="Maximum number of coins (must be 3 or more).")
  
  args = parser.parse_args()

  # If something went wrong and the file cannot be opened, exit with error
  if (not args.file):
    print("Error opening file.")
    return
  
  # Otherwise, print test cases to file
  # Set a total value range
  maxCoinValue = 25
  # Set the maximum number of coin values to generate from input
  maxNumCoins = args.maxNumCoins
  # Set a test case counter
  testcaseNumber = 0

  # Set randomization seed
  random.seed(datetime.now().timestamp())
  # Loop through the given range of coins
  # We start with three coins because this problem is trivial with 2 coins
  for numCoins in range(3, maxNumCoins + 1):
    # Loop through the given number of test cases for each coin quantity
    for test in range(args.size):
      # Write the test case number
      testcaseNumber += 1
      args.file.write(f"{testcaseNumber}")
      # For each coin, generate a random coin value and amount of that coin
      for coin in range(numCoins):
        # Write the coin value
        # We do not include pennies as they somewhat trivialize this problem
        args.file.write(f" {random.randint(2, maxCoinValue)}")
      # Move to the next line
      args.file.write("\n")

  # Close the file once we are done
  args.file.close()

if __name__ == '__main__':
  main()