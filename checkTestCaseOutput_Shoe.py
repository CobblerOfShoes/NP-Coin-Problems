import argparse
import csv
import os

def is_file_valid(filename) -> bool:
  if not os.path.exists(filename):
    print(f"The file {filename} could not be found")
    return False
  return True

def main():
  parser = argparse.ArgumentParser()
  pparser = argparse.ArgumentParser()
  parser.add_argument("-f", dest="infile", required=True,
                      help="Input file with knapsack problem test cases." + "\n" +
                           "Data should be in the format: TestcaseNo., Coin1,  Coin2, Coin3...",
                      metavar="FILE")
  parser.add_argument("-o", dest="outfile", required=True,
                      help="File with coin jar problem test case results." + "\n" +
                           "Data should be in the format: TestcaseNo., leftPile, rightPile, (or neither pile) computationTime, numCoins...",
                      metavar="FILE")
  args = parser.parse_args()
  
  # Check if the file exists
  if (not is_file_valid(args.infile)):
    return
  
  # Keep a bool that is true until a faulty result is read
  allResultsPass: bool = True

  # Keep a list of faulty results:
  faultyResults: list[int] = []

  with open(args.infile, newline='') as csvInfile:
    with open(args.outfile, newline='') as csvOutfile:
      testcases = csv.reader(csvInfile, delimiter=' ')
      outputs = csv.reader(csvOutfile, delimiter=' ')
      # Skip the header
      next(outputs, None)
      for test, output in zip(testcases, outputs):
        # Otherwise, check validity
        test = list(map(int, test))
        output = [list(map(int,output[1].split(','))), list(map(int,(output[2].split(','))))]
        testcaseNumber = test.pop(0)
        # If the test was a failure, skip. No real good way to check if its correct.
        if output[1] == [0]:
          continue
        # Compute the total and do checks
        coinJarTotal = sum(test)
        # If the total is odd, then there is no way it could've been split
        if coinJarTotal & 1:
          print(f"ERROR! Result for testcase {testcaseNumber} was incorrect! Should have been impossible.")
          allResultsPass = False
          faultyResults.append(testcaseNumber)
        # If one of the piles is not half the total, something went wrong
        for halfValuePile in list(map(lambda x: sum(x) == (coinJarTotal/2), output)):
          if not halfValuePile:
            print(f"ERROR! For testcase {testcaseNumber}, a pile does not sum up to half the total jar.")
            allResultsPass = False
            faultyResults.append(testcaseNumber)

  if (allResultsPass):
    print("All results are valid.")
  else:
    print(f"Not all results are valid. Faulty results are: {faultyResults}")




if __name__ == '__main__':
  main()